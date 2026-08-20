# Generates append.world.json -- Ken's append.tt: two robots that join one
# list onto the end of another, a link at a time.
#
# A list is the pair [first, the rest], and the empty list is a box with no
# holes at all. The work box is [List1, List2, a bird to answer on].
#
#   AppendWorker  sees [a two-hole box, any box, a bird]
#                 takes the first link off List1, keeps its head, replaces its
#                 tail with a fresh NEST, and gives that link to the bird. The
#                 caller now has [head, a promise]. The robot keeps the new
#                 nest's bird, so the next link it makes will land inside that
#                 promise, and carries on with the tail.
#   FinishAppend  sees [a box with NO holes, any box, a bird]
#                 List1 is used up, so List2 itself is the rest of the answer:
#                 hand it to the bird and stop.
#
# Nothing is ever copied and nothing waits for the whole of List1 to be known:
# each link is passed on as soon as it exists. That is why the same two robots
# work when List1 is still being computed somewhere else -- which is exactly
# what reverse.world.json does with them.
import json, io, os

REP_ID, REP_GUID = 9701, 'append-answer'

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *holes: {'kind': 'box', 'holes': list(holes)}
bird = lambda: {'kind': 'bird', 'nestId': REP_ID, 'nestGuid': REP_GUID}

at = lambda c, *p: {'c': c, 'path': list(p)}
top = lambda c, *p: {'c': c, 'path': list(p), 'nest': True}
take = lambda a: {'type': 'take', 'at': a}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}
newnest = {'type': 'newNest'}

ANYBOX, ANYBIRD = {'kind': 'anyBox'}, {'kind': 'anyBird'}
CELL = box(None, None)        # a box of two holes, whatever is in them
EMPTY = box()                 # a box of no holes: the end of a list

# --- a link to pass on ------------------------------------------------------
worker = {
    'kind': 'robot', 'name': 'AppendWorker',
    'condition': box(CELL, ANYBOX, ANYBIRD),
    'program': [
        take(top('given', 0)), put('s1'),   # the first link, set aside
        vac('given', 0),                     # sweep away the nest it came on
        take(at('s1', 1)), put('given', 0),  # its tail is the rest to do
        newnest, put('s1', 1),               # and a promise takes the tail's place
        take(at('s1')), put('given', 2),     # the link flies to whoever asked
        vac('given', 2),                     # that bird has done her job
        take(at('s0')), put('given', 2),     # the promise's own bird takes over
    ],
    'trainedOn': None, 'team': [],
}

# --- List1 is used up: List2 is the rest ------------------------------------
finish = {
    'kind': 'robot', 'name': 'FinishAppend',
    'condition': box(EMPTY, ANYBOX, ANYBIRD),
    'program': [
        take(at('given', 1)), put('given', 2),   # List2 itself, to the bird
        vac('given', 0),                         # nothing matches now: it stops
    ],
    'trainedOn': box(box(num(1), box(num(2), EMPTY)),
                     box(num(3), box(num(4), EMPTY)), bird()),
    'team': [],
}

finish['team'] = [worker]

list1 = box(num(1), box(num(2), EMPTY))
list2 = box(num(3), box(num(4), EMPTY))

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': box(list1, list2, bird()), 'x': -0.30, 'z': 1.50},
    {'thing': finish, 'x': -1.20, 'z': 1.30},
    {'thing': {'kind': 'nest', 'id': REP_ID, 'guid': REP_GUID, 'hasEgg': False,
               'pile': [], 'label': 'both lists'}, 'x': 1.15, 'z': 1.60},
    {'thing': txt('APPEND\n\nA list is a pair:\n\n  [ first, the rest ]\n\n'
                  'and a box with NO holes is\nthe empty list. Here\n\n'
                  '  [1,[2,[]]]  and  [3,[4,[]]]\n\n'
                  'go in, and 1,2,3,4 comes\nback -- one link at a time,\n'
                  'each carrying a promise of\nthe next.'),
     'x': -1.05, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nGive the three-hole box to\nthe FinishAppend robot.\n\n'
                  'Set Rounds to 5 or more.\n\n'
                  'Each link lands inside the\npromise the last one carried,\n'
                  'so the answer grows on the\nnest marked "both lists"\n'
                  'from the outside in.'),
     'x': -0.35, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'append.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
