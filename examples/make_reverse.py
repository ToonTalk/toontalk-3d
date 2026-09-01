# Generates reverse.world.json -- Ken's reverse.tt: reversing a list by
# sending the work out to a crowd of houses.
#
#   to reverse [first, rest]:  reverse(rest) with [first] appended to it
#   to reverse []:             []
#
# The trick is that nothing waits. For each link the robot builds a box
#
#     [ a nest, [first, []], the bird that asked ]
#
# and sends it into a house of its own along with a copy of the APPEND team
# from append.world.json. That house cannot start yet -- its first list is a
# bare nest, and a robot facing a bare nest simply dozes -- so it stands there
# smoking gently until the answer it needs turns up. Meanwhile the reverse
# robot carries on down the list with the nest's own bird, so the LAST link is
# the first to be settled, and the answer unwinds from the end of the list
# back to the front.
#
# The work box is [List, a bird to answer on, a spare append team, houses].
# The last hole is only a place to keep the houses so they are not lost; the
# original leaves them standing about in the world instead.
#
# Move for move the original, but for two things: the original fetches its
# append team from the notebook by writing its name on a pad (we carry a spare
# in a hole, as fibonacci-recursive does), and the finisher blows up its own
# house (ours vacuums the bird it has just answered, which stops it dead).
import json, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _listbox import list_to_box_room

REP_ID, REP_GUID = 9801, 'reverse-answer'
# a twin of the answer nest, so the converter reads its own copy of every link
TWIN_ID = 9811
BOXOUT_ID, BOXOUT_GUID = 9812, 'reverse-as-box'

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *holes: {'kind': 'box', 'holes': list(holes)}
bird = lambda: {'kind': 'bird', 'nestId': REP_ID, 'nestGuid': REP_GUID}

at = lambda c, *p: {'c': c, 'path': list(p)}
top = lambda c, *p: {'c': c, 'path': list(p), 'nest': True}
take = lambda a: {'type': 'take', 'at': a}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}
holes = lambda n: {'type': 'setHoles', 'n': n}
newbox, newnest, newroom = ({'type': 'newBox'}, {'type': 'newNest'},
                            {'type': 'newRoom'})

ANYBOX, ANYBIRD = {'kind': 'anyBox'}, {'kind': 'anyBird'}
ANYROBOT = {'kind': 'anyRobot'}
CELL = box(None, None)
EMPTY = box()

# --- the append team, exactly as in make_append.py --------------------------
append_worker = {
    'kind': 'robot', 'name': 'AppendWorker',
    'condition': box(CELL, ANYBOX, ANYBIRD),
    'program': [
        take(top('given', 0)), put('s1'),
        vac('given', 0),
        take(at('s1', 1)), put('given', 0),
        newnest, put('s1', 1),
        take(at('s1')), put('given', 2),
        vac('given', 2),
        take(at('s0')), put('given', 2),
    ],
    'trainedOn': None, 'team': [],
}
append = {
    'kind': 'robot', 'name': 'FinishAppend',
    'condition': box(EMPTY, ANYBOX, ANYBIRD),
    'program': [
        take(at('given', 1)), put('given', 2),
        vac('given'),          # its own box: the house folds away with it
    ],
    'trainedOn': None, 'team': [append_worker],
}

# --- one link: send [promise, [first], the bird] out to a house of its own --
worker = {
    'kind': 'robot', 'name': 'ReverseWorker',
    'condition': box(CELL, ANYBIRD, ANYROBOT, ANYBOX),
    'program': [
        newbox, holes(3), put('s2'),           # the box that house will work on
        take(at('given', 1)), put('s2', 2),    # the bird that asked me
        take(top('given', 0)), put('s2', 1),   # the first link
        vac('given', 0),                       # sweep away the nest it came on
        take(at('s2', 1, 1)), put('given', 0),  # its tail is the rest to reverse
        newbox, holes(0), put('s2', 1, 1),     # so the link becomes a list of one
        newnest, put('s2', 0),                 # the reversed rest, when it comes
        take(at('s0')), put('given', 1),       # that nest's bird answers to me now
        newroom, put('s1'),
        copy('given', 2), put('s1'),           # the append team moves in
        take(at('s2')), put('s1'),             # and its box lands on the desk
        newbox, holes(1), put('s2'),
        take(at('s1')), put('s2', 0),
        take(at('s2')), {'type': 'put', 'at': at('given', 3), 'side': 'R'},
    ],
    'trainedOn': None, 'team': [],
}

# --- nothing left: the empty list is its own reverse ------------------------
finish = {
    'kind': 'robot', 'name': 'Reverse',
    'condition': box(EMPTY, ANYBIRD, ANYROBOT, ANYBOX),
    'program': [
        take(top('given', 0)), put('given', 1),   # [] goes to whoever asked
        vac('given', 1),                          # and with the bird gone, it stops
    ],
    'trainedOn': None, 'team': [worker],
}

the_list = box(num(1), box(num(2), box(num(3), EMPTY)))
work = box(the_list, bird(), append, EMPTY)
finish['trainedOn'] = box(the_list, bird(), None, EMPTY)

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': work, 'x': -0.35, 'z': 1.50},
    {'thing': finish, 'x': -1.25, 'z': 1.30},
    {'thing': {'kind': 'nest', 'id': REP_ID, 'guid': REP_GUID, 'hasEgg': False,
               'pile': [], 'label': 'reversed'}, 'x': 1.15, 'z': 1.60},
    {'thing': list_to_box_room(TWIN_ID, REP_GUID, BOXOUT_ID, BOXOUT_GUID),
     'x': 0.35, 'z': 1.30},
    {'thing': {'kind': 'nest', 'id': BOXOUT_ID, 'guid': BOXOUT_GUID,
               'hasEgg': False, 'pile': [], 'label': 'the same, as a box'},
     'x': 1.15, 'z': 2.20},
    {'thing': txt('REVERSE\n\n  reverse [first, rest] =\n    reverse rest\n'
                  '      with [first] appended\n\nFor each link the robot\n'
                  'builds a box holding a nest,\na one-link list and the bird\n'
                  'that asked -- and sends it\ninto a house with a copy of\n'
                  'the APPEND team.\n\nEach house dozes until the\nnest it is watching fills.'),
     'x': -1.05, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nGive the four-hole box to\nthe Reverse robot.\n\n'
                  'Houses pile up in the last\nhole, all smoking, all\n'
                  'waiting on one another.\n\n[1,[2,[3,[]]]] goes in and\n'
                  '[3,[2,[1,[]]]] comes back on\nthe nest marked "reversed"\n'
                  '-- last link settled first.'),
     'x': -0.35, 'z': 2.15},
    {'thing': txt('BOTH FORMS AT ONCE\n\nThe house reads the answer as\nit arrives and builds the same\nthing as a flat box.\n\nA list is easy to BUILD one\nlink at a time and hard to\nREAD: [1,[2,[3,[]]]] is a box\nholding a nest holding a box,\nthree deep. A box with three\nholes you can take in at a\nglance.\n\nIt never touches the original.\nIts nest is a twin of the\nanswer nest -- one nest in two\nplaces -- so both fill link by\nlink, side by side.'),
     'x': 0.55, 'z': 2.60},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'reverse.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
