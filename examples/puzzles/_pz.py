# Puzzles are WORLD FILES with a few more fields. Nothing here is a new kind of
# thing: a puzzle is a constrained world, a goal in plain sight that cannot be
# picked up, a bird to give your answer to, and a judge -- a robot team in an
# opaque house -- that decides with its own thought bubble and answers by bird.
#
#   intro   what Marty says when the puzzle opens
#   goal    what is wanted, for the card and for Marty
#   hints   in order; the last is the whole answer, for the desperate
#   rules   which stacks and tools exist, what the keyboard may reach, Undo,
#           and how many steps a robot may be taught
#   library other worlds bundled by name, so a robot can open the next one
#           even where nothing can be fetched (a published artifact)
#   wipe    false means "add these things to the table" rather than replace it
#
# This mirrors the original ToonTalk .pzl file, which was Marty's intro, a
# saved room, a goal object, four permission switches, and escalating hints.
import sys, os, json, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'behaviours'))
from _beh import *                                          # noqa: F403,F401

HERE = os.path.dirname(os.path.abspath(__file__))

NO_KEYBOARD = {'numbers': False, 'pads': False}


def fixed(thing, label=None):
    """A thing shown as the goal: it cannot be taken, dropped into, vacuumed
    or erased -- only looked at and copied by hand."""
    t = dict(thing, fixed=True)
    if label:
        t['label'] = label
    return t


def empty_box(n):
    """A box with n empty holes (the sparse form the reader understands)."""
    return {'kind': 'box', 'n': n, 'at': {}}


def load(name):
    """A robot step: open the world called `name`."""
    return {'type': 'load', 'name': name}


def rules(stacks=(), tools=(), typing=NO_KEYBOARD, undo=True, max_steps=None):
    r = {'stacks': list(stacks), 'tools': list(tools), 'typing': dict(typing),
         'undo': undo}
    if max_steps is not None:
        r['maxSteps'] = max_steps
    return r


def judge(name, post_id, post_guid, reply_id, reply_guid, right, on_right,
          notes=(), others=()):
    """The judge: an opaque house whose robot team dozes on the post nest.

    The given box is [the post nest | the reply bird | note pads...].
    `right` is the condition for hole 0 -- what a correct answer looks like on
    the nest -- and `on_right` the steps after the answer has been taken off
    the nest and set down on a work spot. `others` are (condition, program)
    pairs for answers that are wrong but recognisable, so they can be sent
    back; the default sends any box and any number back to the player."""
    holes = [nest(post_id, post_guid, 'the post'),                  # noqa: F405
             bird(reply_id, reply_guid, 'to the player')]           # noqa: F405
    holes += [pad(n) for n in notes]
    work = box(*holes)                                              # noqa: F405
    wild_rest = [WILD] * (len(holes) - 1)                           # noqa: F405
    yes = robot(name, box(right, *wild_rest),                       # noqa: F405
                [takeTop('given', 0), put('s0')] + list(on_right))  # noqa: F405
    send_back = [takeTop('given', 0), put('given', 1)]              # noqa: F405
    team = [robot(name + ' (not a box like that)', box(ANYBOX, *wild_rest), send_back),   # noqa: F405
            robot(name + ' (not a number)', box(ANYNUM, *wild_rest), send_back),          # noqa: F405
            robot(name + ' (not a pad)', box(WILDTEXT, *wild_rest), send_back)]           # noqa: F405
    for cond, prog in others:
        team.insert(0, robot(name + ' (other)', box(cond, *wild_rest), prog))  # noqa: F405
    yes['team'] = team
    return dict(room(name, work, yes, opaque=True, dirty=True), judge=True)     # noqa: F405


def puzzle(name, intro, goal, hints, rules_, bench, library=None):
    world = {'kind': 'world', 'v': 3, 'name': name, 'intro': intro,
             'goal': goal, 'hints': list(hints), 'rules': rules_,
             'bench': bench, 'stations': {}, 'active': None}
    if library:
        world['library'] = library
    out = os.path.join(HERE, name + '.world.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
    print('wrote', os.path.basename(out))
    return world
