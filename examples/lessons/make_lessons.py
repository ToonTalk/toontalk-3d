# -*- coding: utf-8 -*-
# Three small drawing lessons, written by ChatGPT (18 September 2026) as
# "kid-friendly versions" of three programs it had generated before -- and
# kept here as it wrote them, moved into the examples' own vocabulary. Each
# is one small team at the main desk sharing a labelled work box: a number
# counts the work left, a bird delivers letters to the thing, a smaller box
# keeps the letters together, and the finisher -- the robot that recognises
# ZERO -- goes first so it is tried before "any number". Sending a letter is
# two actions: copy it, give the copy to the bird; the original stays for the
# next turn. The finisher uses Dusty to put the work box away, which ends the
# program for good.
#
#   🪐 step-and-turn-planet   repeated motion: walk a little, turn a little,
#                             thirty-six times, and a ring appears
#   🌸 easy-flower            nested repetition: four sides make a square
#                             petal, six petals round a centre make a flower
#   ✨ jumping-spark          a movement amount that changes over time: the
#                             upward step shrinks by gravity each jump
#
# What changed in the move: numbers are written as fractions in lowest terms
# (the originals carried 36000000/1000000); and the flower's petals stand
# off the centre on SPOKES drawn in INVISIBLE INK -- [set | pen | invisible]
# keeps the pen drawing, unseen, so the six petals and the stalk are one
# trail for Dusty and one thing to save (Ken's idea; before that a lifted
# pen ended the trail, and a flower came apart into petals).
#
# The same teams are also written as behaviour cards (the *-helper.thing.json
# files): their birds address "my thing", so a card dropped on any sphere
# draws with that sphere.
import io, json, os, sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403,F401

HERE = os.path.dirname(os.path.abspath(__file__))


# --- the vocabulary ---------------------------------------------------------
def n(v, op='+'):
    """A number in lowest terms: 0.09 is 9/100, not 90000/1000000."""
    f = Fraction(str(v))
    return num(f.numerator, f.denominator, op)                # noqa: F405


def labelled(holes, labels):
    b = box(*holes)                                           # noqa: F405
    b['holeLabels'] = list(labels)
    return b


def letter(verb, what, amount):
    """[action | what | amount] -- a letter to a thing, kept in the letters box."""
    return labelled([txt(verb), txt(what),                    # noqa: F405
                     n(amount) if isinstance(amount, (int, float)) else txt(amount)],   # noqa: F405
                    ['action', 'what', 'amount'])


def my_thing():
    """A bird to whatever the robots are working for: the thing on the table
    in a lesson world, the thing a helper card is dropped on."""
    return {'kind': 'bird', 'nestId': None, 'nestGuid': None, 'liveId': 'MYTHING',
            'label': 'my thing'}


def send(letter_path, bird_path):
    """Copy a letter and give the copy to the bird: the original stays."""
    return [copy('given', *letter_path), put('given', *bird_path)]   # noqa: F405


change = send            # a spare number copied onto a counter is the same two actions
finish = vac('given')    # Dusty puts the work box away: the program is over   # noqa: F405


def worker(work, name, matches, program, note):
    """A robot for this work box: it wants the box, with the holes in
    `matches` as given and the rest anything."""
    holes = [None] * len(work['holes'])
    for i, v in matches:
        holes[i] = v
    cond = labelled(holes, work['holeLabels'])
    return robot(name, cond, program, trained_on=json.loads(json.dumps(work)), note=note)   # noqa: F405


def team(work, robots):
    """The first robot leads; the panel is a world with the box on the stand."""
    lead = robots[0]
    lead['team'] = robots[1:]
    return {'kind': 'world', 'v': 4, 'bench': [], 'stations': {'stand': work}, 'active': lead}


# --- the three teams --------------------------------------------------------
def flower():
    letters = labelled([
        letter('set', 'pen', 'down'), letter('move', 'forward', 0.09), letter('move', 'yaw', 90),
        letter('set', 'pen', 'invisible'), letter('move', 'forward', 0.06), letter('set', 'pen', 'hotpink'),
        letter('move', 'yaw', 180), letter('move', 'yaw', 240),
        letter('move', 'up', -0.35), letter('set', 'pen', 'up'), letter('move', 'up', 0.35),
    ], ['pen down', 'one side', 'square corner',
        'invisible ink', 'one spoke', 'pink ink',
        'about turn', 'next spoke',
        'stalk down', 'pen up', 'back to centre'])
    spare = labelled([n(5, 'set'), n(-1)], ['five again', 'one less'])
    work = labelled([n(6), n(5), my_thing(), letters, spare],
                    ['petals left', 'sides left', 'my flower bird', 'letters', 'spare numbers'])
    return team(work, [
        worker(work, 'Draw the stalk and rest', [(0, n(0))],
               send([3, 5], [2]) + send([3, 0], [2]) + send([3, 8], [2]) + send([3, 9], [2]) + send([3, 10], [2]) + [finish],
               'When no petals remain: pink ink and pen down again (the spoke back was in invisible ink), draw down to the table, lift the pen and return to the centre. Put away the work box.'),
        worker(work, 'Go out to the petal', [(0, ANYNUM), (1, n(5))],                    # noqa: F405
               send([3, 3], [2]) + send([3, 4], [2]) + send([3, 5], [2]) + change([4, 1], [1]),
               'A petal begins. Walk out along a spoke in invisible ink, so the petals stand apart but the whole flower stays one drawing; then pink again, and count the spoke as a side.'),
        worker(work, 'Back to the centre', [(0, ANYNUM), (1, n(0))],                     # noqa: F405
               send([3, 3], [2]) + send([3, 6], [2]) + send([3, 4], [2]) + send([3, 7], [2])
               + change([4, 1], [0]) + change([4, 0], [1]),
               'A square is finished. In invisible ink, turn about and walk the spoke back to the centre; turn to the next spoke, count one petal, and put five back into sides left.'),
        worker(work, 'Draw one side', [(0, ANYNUM), (1, ANYNUM)],                       # noqa: F405
               send([3, 0], [2]) + send([3, 1], [2]) + send([3, 2], [2]) + change([4, 1], [1]),
               'Put the pen down, walk one side, turn a square corner, and count one side.'),
    ])


def orbit(turn):
    letters = labelled([letter('set', 'pen', 'down'), letter('move', 'forward', 0.06),
                        letter('move', 'yaw', turn), letter('set', 'pen', 'up')],
                       ['pen down', 'one step', 'one turn', 'pen up'])
    work = labelled([n(36), my_thing(), letters, n(-1)],
                    ['steps left', 'my planet bird', 'letters', 'one less'])
    return team(work, [
        worker(work, 'Rest at zero', [(0, n(0))], send([2, 3], [1]) + [finish],
               'Lift the pen and put away the work box after 36 steps.'),
        worker(work, 'Step and turn', [(0, ANYNUM)],                                      # noqa: F405
               send([2, 0], [1]) + send([2, 1], [1]) + send([2, 2], [1]) + change([3], [0]),
               'Draw one short step, turn, and count one step. Repeating makes a ring.'),
    ])


def spark():
    letters = labelled([letter('move', 'up', 0.1), letter('move', 'forward', 0.02),
                        letter('drop', 'sphere', 0.02), letter('set', 'shown', 'no')],
                       ['upward step', 'forward step', 'leave a dot', 'hide'])
    work = labelled([n(20), my_thing(), letters, n(-0.01), n(-1)],
                    ['jumps left', 'my spark bird', 'letters', 'gravity', 'one less'])
    return team(work, [
        worker(work, 'Hide and rest', [(0, n(0))], send([2, 3], [1]) + [finish],
               'After 20 jumps, hide the spark and put away the work box. Its dots remain.'),
        worker(work, 'Fly one step', [(0, ANYNUM)],                                       # noqa: F405
               send([2, 0], [1]) + send([2, 1], [1]) + send([2, 2], [1])
               + change([3], [2, 0, 2]) + change([4], [0]),
               'Move up and forward. Leave a dot. Subtract a little from the number in the upward-step letter, then count one jump.'),
    ])


# --- the things they draw with ---------------------------------------------
def actor(lid, colour, up, r=0.025, facing=0):
    """A small sphere with an identity, standing `up` above the table, whose
    pen draws in its own colour."""
    return {'kind': 'model', 'parts': [{'shape': 'sphere', 'size': [r], 'color': colour, 'at': [0, 0, 0]}],
            'ghost': True, 'lid': lid, 'evt': 'evt-' + lid, 'up': up, 'facing': facing,
            'penInk': int(colour[1:], 16), 'penWide': 2}


def card(lid, name, panel):
    """The same team as a behaviour card: drop it on a thing and its bird is
    a bird to that thing."""
    return {'kind': 'text', 'text': name, 'gadget': True, 'lid': lid, 'evt': 'evt-' + lid,
            'look': {'bg': '#fff1ba', 'ink': '#24334d', 'font': 'sans', 'h': 0.2},
            'note': 'Pick me up and press Ctrl+P to look inside. My bird talks to the thing I am attached to.',
            'panel': json.loads(json.dumps(panel))}


def lesson(name, intro, actors, panel, thing_lid):
    """A lesson world: the team at the main desk, its bird addressed to the
    thing on the table."""
    p = json.loads(json.dumps(panel).replace('MYTHING', thing_lid))
    return {'kind': 'world', 'v': 4, 'name': name, 'intro': intro,
            'bench': [{'thing': a, 'x': x, 'z': z} for x, z, a in actors],
            'stations': p['stations'], 'active': p['active']}


def write_json(name, rec):
    out = os.path.join(HERE, name)
    io.open(out, 'w', encoding='utf-8', newline='\n').write(json.dumps(rec, indent=2, ensure_ascii=False) + '\n')
    print('wrote', name)


HOTPINK = '#ff69b4'
WORLDS = [
    ('🪐 step-and-turn-planet.world.json', lesson(
        'A step-and-turn planet',
        'Start the team. The planet walks a little and turns 20 degrees, again and again. After 36 steps it has '
        'gone around twice. Two robots share the jobs: step and turn, and rest at zero. The README in '
        'examples/lessons has experiments to try.',
        [(0, 1.65, actor('sun', '#ffd45e', 0.25, 0.07)),
         (-0.03 / __import__('math').tan(__import__('math').pi / 18), 1.62, actor('blue-planet', '#55afff', 0.3, 0.02))],
        orbit(20), 'blue-planet')),
    ('🌸 easy-flower.world.json', lesson(
        'An easy flower',
        'Start the team to draw six square petals on spokes, and a stalk. Four robots share the jobs: go out to '
        'the petal, draw one side, come back to the centre, and draw the stalk. The spokes are drawn in '
        'invisible ink, so the whole flower is one drawing. Click the condition above Trained actions to see '
        'the next team member. The README in examples/lessons has the whole recipe.',
        [(0, 1.55, actor('pink-flower', HOTPINK, 0.35))],
        flower(), 'pink-flower')),
    ('✨ jumping-spark.world.json', lesson(
        'A jumping spark',
        'Start the team. The spark moves up and forward, leaves a dot, and makes its next upward step a little '
        'smaller. Twenty jumps draw an arch. Two robots share the jobs: fly one step, and hide and rest. The '
        'README in examples/lessons has experiments to try.',
        [(0, 1.5, actor('spark-1', '#ffca55', 0.05, 0.025, 0))],
        spark(), 'spark-1')),
]
CARDS = [
    ('🌸 flower-helper.thing.json', card('flower-helper', 'Draw a flower', flower())),
    ('🪐 orbit-helper.thing.json', card('orbit-helper', 'Step and turn', orbit(20))),
    ('✨ spark-helper.thing.json', card('spark-helper', 'Fly a spark', spark())),
]

if __name__ == '__main__':
    for name, rec in WORLDS:
        write_json(name, rec)
    for name, thing in CARDS:
        write_json(name, {'kind': 'thing', 'v': 3, 'thing': thing})
