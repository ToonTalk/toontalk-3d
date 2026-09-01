# Generates n-to-1.world.json -- Ken's n-to-1.tt: a team of two that answers
# with the list [n, n-1, ... 1] without ever holding the whole list.
#
# A list here is the pair [first, the rest], and "the rest" is usually a NEST:
# an answer that has not arrived yet. So the list is handed over one link at a
# time, each link carrying a promise of the next -- a lazy stream, built out
# of nothing but boxes, nests and birds.
#
#   FinishList  sees [the number 0, a bird]
#               makes a box with NO holes -- the empty list -- and gives it to
#               the bird. That is the end of the list.
#   ListWorker  sees [any number, a bird]
#               makes a two-hole box, copies the number into the front of it,
#               drops a fresh nest in the back, and gives that pair to the
#               bird. Then it keeps the new nest's bird for itself and types
#               a minus sign on a 1 to count down.
#
# The leader is checked first, which is why the finisher leads: 0 is a number
# too, and the worker would happily grab it.
#
# Move for move the original, except that the original's finisher fetches a
# bomb and blows up its own house; ours vacuums the box it was working on,
# which ends the team for good and, in a house, folds the house away.
import json, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _listbox import list_to_box_room

N = 5
NEST_ID, NEST_GUID = 9601, 'n-to-1-answer'
# a twin of the answer nest, so the converter reads its own copy of every link
TWIN_ID = 9611
BOXOUT_ID, BOXOUT_GUID = 9612, 'n-to-1-as-box'

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *holes: {'kind': 'box', 'holes': list(holes)}
bird = lambda: {'kind': 'bird', 'nestId': NEST_ID, 'nestGuid': NEST_GUID}

at = lambda c, *p: {'c': c, 'path': list(p)}
take = lambda c, *p: {'type': 'take', 'at': at(c, *p)}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}
holes = lambda n: {'type': 'setHoles', 'n': n}
newnum, newbox, newnest = ({'type': 'newNumber'}, {'type': 'newBox'},
                           {'type': 'newNest'})

WILD, ANYBIRD = {'kind': 'wildNumber'}, {'kind': 'anyBird'}

# --- 0: the list ends ------------------------------------------------------
finish = {
    'kind': 'robot', 'name': 'FinishList',
    'condition': box(num(0), ANYBIRD),
    'program': [
        newbox, holes(0),        # a box with no holes at all: the empty list
        put('given', 1),         # to the bird, who takes it home
        vac('given'),            # then its own box: finished, for good
    ],
    'trainedOn': box(num(N), bird()),
    'team': [],
}

# --- any other number: hand over one link and count down -------------------
worker = {
    'kind': 'robot', 'name': 'ListWorker',
    'condition': box(WILD, ANYBIRD),
    'program': [
        newbox, holes(2), put('s1'),     # the link: [this one, the rest]
        copy('given', 0), put('s1', 0),
        newnest, put('s1', 1),           # the rest is a promise; its bird hatches
        take('s1'), put('given', 1),     # the link flies off to whoever asked
        vac('given', 1),                 # that bird has done her job
        take('s0'), put('given', 1),     # the new nest's bird takes over
        newnum, {'type': 'setOp', 'op': '-'},
        put('given', 0),                 # one less to go
    ],
    'trainedOn': None, 'team': [],
}

finish['team'] = [worker]

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': box(num(N), bird()), 'x': -0.30, 'z': 1.55},
    {'thing': finish, 'x': -1.20, 'z': 1.30},
    {'thing': {'kind': 'nest', 'id': NEST_ID, 'guid': NEST_GUID, 'hasEgg': False,
               'pile': [], 'label': 'the list'}, 'x': 1.15, 'z': 1.60},
    {'thing': list_to_box_room(TWIN_ID, NEST_GUID, BOXOUT_ID, BOXOUT_GUID),
     'x': 0.35, 'z': 1.35},
    {'thing': {'kind': 'nest', 'id': BOXOUT_ID, 'guid': BOXOUT_GUID,
               'hasEgg': False, 'pile': [], 'label': 'the same, as a box'},
     'x': 1.15, 'z': 2.15},
    {'thing': txt('COUNTING DOWN\n\nA list is a pair:\n\n  [ first, the rest ]\n\n'
                  'and "the rest" is a nest --\nan answer that has not\n'
                  'arrived yet. The team hands\nthe list over one link at a\n'
                  'time and never holds all of\nit at once.'),
     'x': -1.05, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nGive the two-hole box to the\nFinishList robot.\n\n'
                  'Each round one link lands on\nthe nest marked "the list":\n'
                  f'{N}, then {N - 1}, and so on down to\n1, and last a box with no\n'
                  'holes, which means the end.\n\n'
                  'It stops by itself at the\nend: an empty box fits no\nthought.'),
     'x': -0.35, 'z': 2.15},
    {'thing': txt('BOTH FORMS AT ONCE\n\nThe house reads the list as it\n'
                  'arrives and builds the same\nthing as a flat box.\n\n'
                  'A list is easy to BUILD one\nlink at a time and hard to\n'
                  'READ: [1,[2,[3,[]]]] is a box\nholding a nest holding a box,\n'
                  'three deep. A box with three\nholes you can take in at a\nglance.\n\n'
                  'It never touches the original.\nIts nest is a twin of the\n'
                  'answer nest -- one nest in\ntwo places -- so both fill\n'
                  'link by link, side by side.'),
     'x': 0.55, 'z': 2.55},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'n-to-1.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
