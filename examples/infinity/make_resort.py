# Resort Infinity -- Hilbert's hotel, in the yard.
#
# The original is a ToonTalk CITY: you are the clerk, guests arrive for ever,
# and you train a robot that says where each new guest's cottage is built --
# and, from problem 2, a second robot that tells the guests already housed
# where to move to. The city was an addressing scheme. This workshop has no
# cities; it has the yard, which suits the story better: a cottage is a house
# standing on the grass, an address is a place along the row, and the whole
# row shuffling up is something you watch happen.
#
# ONE NEST EACH, WHICH IS THE WHOLE DESIGN. A robot team stops at the first
# member whose thought is waiting on an empty nest -- that is what dozing IS
# -- so nobody here may doze on two nests. Everything a guest hears arrives on
# one nest of its own (under its own name, and the bell's, by ALIAS), and
# everything the clerk hears arrives on one nest on the desk. What lands says
# who runs:
#
#   a guest's nest   a NUMBER is an address to stand at
#                    a PAD is the bell: ask where to move to
#   the desk's nest  [number | bird]         -- a new guest asking
#                    [pad | number | bird]   -- a guest asking to move
#
# WHAT IS GIVEN AND WHAT IS YOURS. Every cottage carries its own robots (in
# the macro pad "the guests", one behaviour per cottage): that is the resort's
# machinery and you never need to touch it. Each one asks the desk once, and
# stands wherever it is told -- x = n * 0.6 - 4.5 along the row.
#
# What is YOURS is the arithmetic, three steps of it: take the [number, bird]
# box off the post and give the bird the address. Problem 2's robot does the
# same to a [pad | number | bird] with five added, and joins the first as a
# TEAM -- which is what a team is for: the first member whose thought fits the
# post on top takes the turn. Both answers lie on the grass if you would
# rather read one than write one.
#
#   Problem 1  the first infinite group. Address = the guest's own number.
#   Problem 2  five more guests, and no empty cottages. Everyone already
#              housed moves up five; the newcomers take 1 to 5.
#
# Six and five are what fits on the grass. The fence pad says what the row
# does after that.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

WILDTEXT = {'kind': 'wildText'}
DESK_G = 'resort-desk'
BELL = 'resort-bell'
DESK_ID = 9790

# where cottage n stands: x = n * 0.6 - 4.5, along the row at z = 4.5; a
# guest housed there stands in front of it, at z = 5.2
STEP_N, STEP_D = 6, 10
OFF_N, OFF_D = 45, 10
ROW_N, ROW_D = 52, 10
COTTAGE_Z = 4.5

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,
                                'liveId': lid, 'label': label}
msg = lambda verb, what: box(txt(verb), txt(what), None)   # noqa: F405
dropf = lambda n, d, op, *where: [newnum, setv(n, op, d), put(*where)]   # noqa: F405

DESK = lambda: box(nest(DESK_ID, DESK_G, label='the post'))   # noqa: F405,E731


# --- one guest's behaviour ---------------------------------------------------
# 0 the desk | 1 my nest | 2 my own bird | 3 my number
# 4 my place | 5 [set | position | _]
# (my thing -- the guest -- is the bird on the perch: the panel's own)
def guest_gadget(k, number, lid, gid):
    mail = (9700 + k, 'resort-guest-%d' % k)
    mine = nest(*mail, label='my post')                    # noqa: F405
    mine['aliases'] = [BELL]                               # ...and the bell reaches it too
    work = box(bird(DESK_ID, DESK_G, label='the desk'),    # noqa: F405
               mine,
               bird(*mail, label='my own bird'),           # noqa: F405
               num(number),                                # noqa: F405
               None,                                       # my place: empty until I am housed
               msg('set', 'position'))
    any_ = [ANYBIRD, None, ANYBIRD, None, None, ANYBOX]   # noqa: F405

    def cond(**at):
        c = list(any_)
        for i, v in at.items():
            c[int(i[1:])] = v
        return box(*c)                                     # noqa: F405

    ask = robot(                                           # noqa: F405
        'Ask for a place', cond(h3=ANYNUM),                # noqa: F405
        [newbox, holes(2), put('s0'),                      # noqa: F405
         take('given', 3), put('s0', 0),                   # my number -- taken, so I ask once  # noqa: F405
         copy('given', 2), put('s0', 1),                   # ...and a bird of my own to answer  # noqa: F405
         take('s0'), put('given', 0)],                     # off to the desk  # noqa: F405
        trained_on=work,
        note='Leads. My number is still in the box, so I have nowhere to live: sends [my number, my own bird] to the desk and takes my number out as it goes, so I never ask twice.')

    stand = robot(                                         # noqa: F405
        'Stand at my address', cond(h1=ANYNUM),            # noqa: F405
        [copy('given', 5), put('s0'),                      # the [set | position | _] message  # noqa: F405
         newbox, holes(2), put('s0', 2),                   # an empty [across | away]  # noqa: F405
         takeTop('given', 1), put('s0', 2, 0),             # the address they gave me  # noqa: F405
         copy('s0', 2, 0), put('given', 4),                # ...which is my place from now on  # noqa: F405
         ] + dropf(STEP_N, STEP_D, '*', 's0', 2, 0)        # x = n * 0.6 ...
        + dropf(OFF_N, OFF_D, '-', 's0', 2, 0)             # ... - 4.5
        + [newnum, setv(ROW_N, '+', ROW_D), put('s0', 2, 1),   # the row  # noqa: F405
           take('s0'), put('perch')],                      # and I walk there: to the bird on the perch  # noqa: F405
        note='A number has landed on my nest: that is my address. Works out where that cottage stands along the row, remembers it as my place, and walks there.')

    move = robot(                                          # noqa: F405
        'Move when told to', cond(h1=WILDTEXT, h4=ANYNUM),   # noqa: F405
        [newbox, holes(3), put('s0'),                      # noqa: F405
         takeTop('given', 1), put('s0', 0),                # the ding itself says "a move, please"  # noqa: F405
         take('given', 4), put('s0', 1),                   # where I live now -- taken  # noqa: F405
         copy('given', 2), put('s0', 2),                   # ...and my own bird  # noqa: F405
         take('s0'), put('given', 0)],                     # off to the desk  # noqa: F405
        note='A pad has landed on my nest -- an announcement from the desk, to every guest. Sends [the announcement, where I live, my own bird] to the desk and takes my place out of the box, so that the answer puts a new one in.')

    return {'kind': 'text', 'text': 'guest %d' % number, 'gadget': True,
            'lid': gid, 'evt': 'evt-' + gid, 'boundTo': lid,
            'note': ('Guest %d\u2019s own three robots: ask the desk where to live, walk to '
                     'the cottage it is given, and ask again when the bell rings. They work on '
                     'guest %d, and on nothing else.' % (number, number)),
            'look': {'bg': '#2b2238', 'ink': '#ecd9ff', 'font': 'sans', 'h': 0.34},
            'panel': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {'stand': work},
                      'active': dict(ask, team=[stand, move])}}


def cottage(n):
    return {'kind': 'room', 'label': 'cottage %d' % n, 'opaque': True, 'dirty': False,
            'world': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {}, 'active': None}}


# a guest is a pad with a name: the thing that walks
def guest(name, lid, bg):
    return {'kind': 'text', 'text': name, 'lid': lid, 'evt': 'evt-' + lid,
            'look': {'bg': bg, 'ink': '#fff5e6', 'font': 'sans', 'h': 0.34}}


def macro(name, lid, gadgets, look, note=None):
    return {'kind': 'text', 'text': name, 'gadget': True, 'lid': lid, 'evt': 'evt-' + lid,
            'look': look, 'note': note,
            'panel': {'kind': 'world', 'v': 3, 'stations': {}, 'active': None,
                      'bench': [{'thing': g, 'x': -0.6 + 0.3 * (i % 4), 'z': 1.3 + 0.3 * (i // 4)}
                                for i, g in enumerate(gadgets)]}}


# --- the answers, for the clerk who would rather read one --------------------
address_robot = robot(                                     # noqa: F405
    'Next address', box(box(ANYNUM, ANYBIRD)),             # noqa: F405
    [takeTop('given', 0), put('s0'),                       # a [number, bird] letter: a new guest  # noqa: F405
     copy('s0', 0), put('s0', 1),                          # their own number, to their bird  # noqa: F405
     vac('s0')],                                           # the empty letter away  # noqa: F405
    trained_on=DESK(),
    note='Problem 1, answered: guest i lives at cottage i. Takes the [number, bird] letter off the post and gives the bird a copy of the number.')

move_robot = robot(                                        # noqa: F405
    'Move up five', box(box(WILDTEXT, ANYNUM, ANYBIRD)),   # noqa: F405
    [takeTop('given', 0), put('s0'),                       # a [ding, address, bird] letter: a move  # noqa: F405
     ] + dropf(5, 1, '+', 's0', 1)                         # five further along the row
    + [take('s0', 1), put('s0', 2),                        # the new address, to their bird  # noqa: F405
       vac('s0')],                                         # noqa: F405
    trained_on=DESK(),
    note='Problem 2, answered: everybody moves up five, which empties cottages 1 to 5 for the newcomers. Takes the [the announcement, where I live, bird] letter off the post, adds 5, and gives the answer to the bird.')

# THE CLERK IS A TEAM FROM THE START: whichever letter lies on the post, the
# member that fits it runs -- a newcomer's [number | bird] or a housed guest's
# [announcement | where I live | bird]. Ken switched on the five newcomers
# with only "Move up five" at the desk, and nothing recognised their letters.
clerk = dict(address_robot, team=[move_robot])

ABOUT = ('RESORT INFINITY\n'
      '\n'
      'You are the clerk. Eleven\n'
      'cottages stand in a row,\n'
      'numbered from the left. Guests\n'
      'arrive at the gate; every\n'
      'guest needs a cottage, and no\n'
      'two may share one.\n'
      '\n'
      'Each guest has robots of its\n'
      'own (inside the pad "the\n'
      'guests"): it asks the desk\n'
      'where to live and walks to\n'
      'that cottage. You never need\n'
      'to touch those.\n'
      '\n'
      'What is yours is the\n'
      'arithmetic: a robot at the\n'
      'desk that says WHICH cottage,\n'
      'and later one that says WHERE\n'
      'TO MOVE.\n'
      '\n'
      'Set the Speed to 4x or 8x: a\n'
      'resort takes a while at\n'
      'walking pace.')


P1 = ('PROBLEM 1\n'
      'The first infinite group\n'
      '\n'
      'Six guests wait at the gate,\n'
      'numbered 1 to 6, and more are\n'
      'behind them for ever.\n'
      '\n'
      'The box on the grass with a\n'
      'nest in it is the DESK. Every\n'
      'guest writes to that nest, the\n'
      'post. A clerk answers each\n'
      'letter with a cottage number:\n'
      'train one (see HOW TO TRAIN\n'
      'THE CLERK), or drop the desk\n'
      'on the clerk already trained\n'
      'and press Start.\n'
      '\n'
      'Then point at the pad "the\n'
      'guests", with nothing in your\n'
      'hand, and press SPACE. Letters\n'
      'land on the post, the clerk\n'
      'answers them, and each guest\n'
      'walks to its cottage.\n'
      '\n'
      'Which cottage should guest 1\n'
      'have?')



P2 = ('PROBLEM 2\n'
      'Five more, and no room\n'
      '\n'
      'Five more guests arrive and\n'
      'every cottage is taken. Nobody\n'
      'is turned away: everybody\n'
      'housed moves FIVE cottages\n'
      'along, and the newcomers take\n'
      '1 to 5.\n'
      '\n'
      'The clerk ANNOUNCES it: give\n'
      'the pad "everybody move up\n'
      'five" to the bird "to every\n'
      'guest". It lands on every\n'
      'guest\u2019s nest, and each asks\n'
      'the desk where to go. "Move\n'
      'up five", on the clerk team\n'
      'already, answers: +5.\n'
      '\n'
      'Watch the guests walk along.\n'
      'When cottages 1 to 5 stand\n'
      'empty, SPACE on "five more\n'
      'guests".\n'
      '\n'
      'Why does this work here, and\n'
      'not at a hotel with a hundred\n'
      'rooms?')


TRAIN = ('HOW TO TRAIN THE CLERK\n'
      '\n'
      'Take a little robot from its\n'
      'stack and set it on the grass.\n'
      'Pick up the desk, the box with\n'
      'the nest, and drop it ON the\n'
      'robot: its thought bubble\n'
      'opens and you are teaching it.\n'
      '\n'
      'Three moves: take the [number\n'
      '| bird] letter off the post,\n'
      'copy the number, give the copy\n'
      'to the bird.\n'
      '\n'
      'Leave the bubble and press\n'
      'Start. With the post empty the\n'
      'clerk dozes, which is what a\n'
      'clerk does.')


FENCE = ('THE ROW GOES ON\n'
      '\n'
      'Eleven cottages stand in a\n'
      'row, counted from the left,\n'
      'and a guest given a number\n'
      'walks to that cottage.\n'
      '\n'
      'The row does not stop at the\n'
      'fence: guest 12 would walk\n'
      'past it, and guest a thousand\n'
      'a long way past.\n'
      '\n'
      'Nothing in these robots knows\n'
      'how many guests there are.\n'
      'That is the whole of it.')


INSIDE = ('RESORT INFINITY\n\n'
          'Everything is out the back\n'
          'door: the cottages, the desk,\n'
          'the bell.\n\n'
          'Go outside.')

# the row: eleven cottages, fixed, numbered from the left
row = [{'thing': cottage(n), 'x': n * 0.6 - 4.5, 'z': COTTAGE_Z} for n in range(1, 12)]

g1, g2, gates = [], [], []
for k in range(1, 7):                                      # the first six, at the gate
    lid = 'GST1%d' % k
    g1.append(guest_gadget(k, k, lid, 'G1%d' % k))
    gates.append({'thing': guest('guest %d' % k, lid, '#7a3b2e'), 'x': -4.2 + 0.5 * (k - 1), 'z': 6.6})
for k in range(1, 6):                                      # ...and five more behind them
    lid = 'GST2%d' % k
    g2.append(guest_gadget(10 + k, k, lid, 'G2%d' % k))
    gates.append({'thing': guest('new guest %d' % k, lid, '#2e5a7a'), 'x': -4.2 + 0.5 * (k - 1), 'z': 7.4})

bench_yard = row + gates + [
    {'thing': macro('the guests', 'M1', g1,
                    {'bg': '#1f3b2c', 'ink': '#d9ffe8', 'font': 'sans', 'h': 0.42},
                    note=('The resort\u2019s own machinery, which you never need to touch: '
                          'six behaviours, one per guest, three robots each. SPACE here is the '
                          'six guests arriving at once \u2014 they write to the post and walk to '
                          'their cottages as soon as a clerk answers. Nothing in them knows how '
                          'many guests there are.')),
     'x': 3.3, 'z': 6.6},
    {'thing': macro('five more guests', 'M2', g2,
                    {'bg': '#3b2c1f', 'ink': '#ffe8d9', 'font': 'sans', 'h': 0.42},
                    note=('The same machinery for problem 2\u2019s five newcomers. Switch it '
                          'on only once the bell has moved everybody up and cottages 1 to 5 '
                          'stand empty.')),
     'x': 3.3, 'z': 7.4},

    {'thing': DESK(), 'x': -4.3, 'z': 3.4},
    {'thing': clerk, 'x': -3.4, 'z': 2.8},

    {'thing': bird(9792, BELL, label='to every guest'), 'x': -1.2, 'z': 3.0},    # noqa: F405
    {'thing': txt('everybody move up five'), 'x': -0.55, 'z': 3.0},              # noqa: F405
    {'thing': txt('everybody move up five'), 'x': 0.05, 'z': 3.0},               # noqa: F405

    {'thing': txt(ABOUT), 'x': 1.4, 'z': 3.2},                                   # noqa: F405
    {'thing': txt(P1), 'x': 2.6, 'z': 3.2},                                      # noqa: F405
    {'thing': txt(TRAIN), 'x': 2.0, 'z': 3.9},                                   # noqa: F405
    {'thing': txt(P2), 'x': 3.8, 'z': 3.2},                                      # noqa: F405
    {'thing': txt(FENCE), 'x': -4.4, 'z': 2.5},                                  # noqa: F405
]

bench = [{'thing': txt(INSIDE), 'x': -0.2, 'z': 1.6}]      # noqa: F405

if __name__ == '__main__':
    import json, io
    world = {'kind': 'world', 'v': 3, 'bench': bench, 'stations': {}, 'active': None,
             'yard': {'bench': bench_yard}}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '\U0001f3e8 resort-infinity.world.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1, ensure_ascii=False))
    print('wrote', os.path.basename(out))
