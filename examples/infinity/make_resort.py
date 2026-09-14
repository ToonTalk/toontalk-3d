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

# where address n stands: x = n * 0.6 - 4.5, along the row at z = 4.5
STEP_N, STEP_D = 6, 10
OFF_N, OFF_D = 45, 10
ROW_N, ROW_D = 45, 10

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,
                                'liveId': lid, 'label': label}
msg = lambda verb, what: box(txt(verb), txt(what), None)   # noqa: F405
dropf = lambda n, d, op, *where: [newnum, setv(n, op, d), put(*where)]   # noqa: F405

DESK = lambda: box(nest(DESK_ID, DESK_G, label='the post'))   # noqa: F405,E731


# --- one guest's behaviour ---------------------------------------------------
# 0 my thing | 1 the desk | 2 my nest | 3 my own bird | 4 my number
# 5 my place | 6 [set | position | _]
def guest_gadget(k, number, lid, gid):
    mail = (9700 + k, 'resort-guest-%d' % k)
    mine = nest(*mail, label='my post')                    # noqa: F405
    mine['aliases'] = [BELL]                               # ...and the bell reaches it too
    work = box(live_bird(lid, 'my thing'),                 # noqa: F405
               bird(DESK_ID, DESK_G, label='the desk'),    # noqa: F405
               mine,
               bird(*mail, label='my own bird'),           # noqa: F405
               num(number),                                # noqa: F405
               None,                                       # my place: empty until I am housed
               msg('set', 'position'))
    any_ = [ANYBIRD, ANYBIRD, None, ANYBIRD, None, None, ANYBOX]   # noqa: F405

    def cond(**at):
        c = list(any_)
        for i, v in at.items():
            c[int(i[1:])] = v
        return box(*c)                                     # noqa: F405

    ask = robot(                                           # noqa: F405
        'Ask for a place', cond(h4=ANYNUM),                # noqa: F405
        [newbox, holes(2), put('s0'),                      # noqa: F405
         take('given', 4), put('s0', 0),                   # my number -- taken, so I ask once  # noqa: F405
         copy('given', 3), put('s0', 1),                   # ...and a bird of my own to answer  # noqa: F405
         take('s0'), put('given', 1)],                     # off to the desk  # noqa: F405
        trained_on=work,
        note='Leads. My number is still in the box, so I have nowhere to live: sends [my number, my own bird] to the desk and takes my number out as it goes, so I never ask twice.')

    stand = robot(                                         # noqa: F405
        'Stand at my address', cond(h2=ANYNUM),            # noqa: F405
        [copy('given', 6), put('s0'),                      # the [set | position | _] message  # noqa: F405
         newbox, holes(2), put('s0', 2),                   # an empty [across | away]  # noqa: F405
         takeTop('given', 2), put('s0', 2, 0),             # the address they gave me  # noqa: F405
         copy('s0', 2, 0), put('given', 5),                # ...which is my place from now on  # noqa: F405
         ] + dropf(STEP_N, STEP_D, '*', 's0', 2, 0)        # x = n * 0.6 ...
        + dropf(OFF_N, OFF_D, '-', 's0', 2, 0)             # ... - 4.5
        + [newnum, setv(ROW_N, '+', ROW_D), put('s0', 2, 1),   # the row  # noqa: F405
           take('s0'), put('given', 0)],                   # and my cottage stands there  # noqa: F405
        note='A number has landed on my nest: that is an address. Works out where it is along the row, remembers it as my place, and tells my cottage to stand there.')

    move = robot(                                          # noqa: F405
        'Move when the bell rings', cond(h2=WILDTEXT, h5=ANYNUM),   # noqa: F405
        [newbox, holes(3), put('s0'),                      # noqa: F405
         takeTop('given', 2), put('s0', 0),                # the ding itself says "a move, please"  # noqa: F405
         take('given', 5), put('s0', 1),                   # where I live now -- taken  # noqa: F405
         copy('given', 3), put('s0', 2),                   # ...and my own bird  # noqa: F405
         take('s0'), put('given', 1)],                     # off to the desk  # noqa: F405
        note='A pad has landed on my nest -- the bell. Sends [the ding, where I live, my own bird] to the desk and takes my place out of the box, so that the answer puts a new one in.')

    return {'kind': 'text', 'text': 'guest %d' % number, 'gadget': True,
            'lid': gid, 'evt': 'evt-' + gid, 'boundTo': lid,
            'look': {'bg': '#2b2238', 'ink': '#ecd9ff', 'font': 'sans', 'h': 0.34},
            'panel': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {'stand': work},
                      'active': dict(ask, team=[stand, move])}}


def cottage(k, number, group):
    lid = 'K%d%d' % (group, k)
    return lid, {'kind': 'room',
                 'label': ('guest %d' % number) if group == 1 else ('new guest %d' % number),
                 'lid': lid, 'evt': 'evt-' + lid, 'opaque': True, 'dirty': False,
                 'world': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {}, 'active': None}}


def macro(name, lid, gadgets, look):
    return {'kind': 'text', 'text': name, 'gadget': True, 'lid': lid, 'evt': 'evt-' + lid,
            'look': look,
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
    note='Problem 2, answered: everybody moves up five, which empties cottages 1 to 5 for the newcomers. Takes the [ding, where I live, bird] letter off the post, adds 5, and gives the answer to the bird.')

ABOUT = ('RESORT INFINITY\n\n'
         'You are the clerk. Guests\n'
         'arrive; every guest needs a\n'
         'cottage, and no two cottages\n'
         'may stand at the same address.\n\n'
         'Each cottage has robots of\n'
         'its own (inside the pad "the\n'
         'guests"): it asks the desk\n'
         'where to live, and stands\n'
         'there. You never need to\n'
         'touch those.\n\n'
         'What is yours is the\n'
         'arithmetic: a robot at the\n'
         'desk that says WHERE, and\n'
         'later one that says WHERE TO\n'
         'MOVE.\n\n'
         'Set the Speed to 4x or 8x: a\n'
         'resort takes a while at\n'
         'walking pace.')

P1 = ('PROBLEM 1\nThe first infinite group\n\n'
      'Six guests are at the gate,\n'
      'numbered 1 to 6, and more are\n'
      'behind them for ever.\n\n'
      'On the grass is the desk: a box\n'
      'holding one nest, THE POST.\n'
      'Every guest writes to it.\n\n'
      'Train a robot on that box to\n'
      'take the [number, bird] letter\n'
      'off the post and give the bird\n'
      'the address. Give the box to\n'
      'your robot and press Start:\n'
      'with the nest empty it dozes,\n'
      'which is what a clerk does.\n\n'
      'Then press SPACE on the pad\n'
      '"the guests": they ask, and\n'
      'they house themselves.\n\n'
      'Where should guest 1 live?\n'
      '("Next address", on the grass,\n'
      'is one answer.)')

P2 = ('PROBLEM 2\nFive more, and no room\n\n'
      'Five more guests arrive, and\n'
      'every cottage is taken. You\n'
      'cannot turn them away: this is\n'
      'Resort Infinity.\n\n'
      'A guest asking to MOVE writes a\n'
      'longer letter: [ding | where I\n'
      'live | my bird]. Train a second\n'
      'robot for that letter — five\n'
      'further along — and drop it on\n'
      'your first robot. They are a\n'
      'team now, and a team runs\n'
      'whichever member fits the\n'
      'letter on top. Start it again.\n\n'
      'Ring the bell: drop a ding on\n'
      'the bell bird, and watch the\n'
      'row shuffle up.\n\n'
      'When cottages 1 to 5 stand\n'
      'empty, press SPACE on "five\n'
      'more guests".\n\n'
      'Everybody moved; nobody was\n'
      'turned out; nobody shares an\n'
      'address. Why does that work\n'
      'here and not at a hotel with a\n'
      'hundred rooms?')

FENCE = ('THE ROW GOES ON\n\n'
         'Eleven cottages is what fits\n'
         'on this grass. The row does\n'
         'not stop at the fence: guest\n'
         '12 stands past it, and guest\n'
         'a thousand a long way past.\n\n'
         'Nothing in these robots knows\n'
         'how many guests there are.\n'
         'That is the whole of it.')

INSIDE = ('RESORT INFINITY\n\n'
          'Everything is out the back\n'
          'door: the cottages, the desk,\n'
          'the bell.\n\n'
          'Go outside.')

g1, g2, gates = [], [], []
for k in range(1, 7):                                      # the first six
    lid, house = cottage(k, k, 1)
    g1.append(guest_gadget(k, k, lid, 'G1%d' % k))
    gates.append({'thing': house, 'x': -4.2 + 0.75 * (k - 1), 'z': 6.6})
for k in range(1, 6):                                      # ...and five more
    lid, house = cottage(k, k, 2)
    g2.append(guest_gadget(10 + k, k, lid, 'G2%d' % k))
    gates.append({'thing': house, 'x': -4.2 + 0.75 * (k - 1), 'z': 7.4})

bench_yard = gates + [
    {'thing': macro('the guests', 'M1', g1,
                    {'bg': '#1f3b2c', 'ink': '#d9ffe8', 'font': 'sans', 'h': 0.42}),
     'x': 3.3, 'z': 6.6},
    {'thing': macro('five more guests', 'M2', g2,
                    {'bg': '#3b2c1f', 'ink': '#ffe8d9', 'font': 'sans', 'h': 0.42}),
     'x': 3.3, 'z': 7.4},

    {'thing': DESK(), 'x': -4.3, 'z': 3.4},
    {'thing': address_robot, 'x': -3.4, 'z': 2.8},
    {'thing': move_robot, 'x': -2.4, 'z': 2.8},

    {'thing': bird(9792, BELL, label='the bell'), 'x': -1.2, 'z': 3.0},          # noqa: F405
    {'thing': txt('ding'), 'x': -0.6, 'z': 3.0},                                 # noqa: F405
    {'thing': txt('ding'), 'x': -0.2, 'z': 3.0},                                 # noqa: F405
    {'thing': txt('ding'), 'x': 0.2, 'z': 3.0},                                  # noqa: F405

    {'thing': txt(ABOUT), 'x': 1.4, 'z': 3.2},                                   # noqa: F405
    {'thing': txt(P1), 'x': 2.6, 'z': 3.2},                                      # noqa: F405
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
