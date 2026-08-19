# Generates fibonacci.world.json -- doubly-recursive Fibonacci in ToonTalk 3D.
#
# fib(n) is computed as the NUMBER OF LEAVES of the call tree (fib(1) and
# fib(2) each count 1), so no reply channels are needed: every leaf mails a 1
# to one shared nest, and their sum is the answer.
#
# The work box has five holes:
#   0 n     1 bird (to the root nest)     2 a spare copy of the worker team
#   3, 4    parking for the two child rooms it builds
#
# The worker team "Fib" (first member that recognises the box runs):
#   leaf-1  [1,...]: mails a 1 to the bird, vacuums hole 0, stops.
#   leaf-2  [2,...]: the same.
#   branch  [any number,...]:
#     - drops a "-1" number on hole 0                      (n-1)
#     - takes a fresh room, parks it on spot 1
#     - carries its own box to the copier, takes the copy
#     - wand-copies the spare robot out of the copy into the room,
#       then drops the copied box into the room             (child launched)
#     - stows the room in hole 3
#     - repeats with another -1 (n-2) and hole 4, then vacuums hole 0.
#   The emptied hole matches nobody, so the box returns to the table with
#   two smoking rooms aboard; each runs the same team one level deeper.
#
# "Sum" drains the nest: given [total, nest] it moves the top of the pile
# onto the total, one a round, and dozes when the nest is bare.
import json, io, os

N = 8                      # fib(8) = 21 leaves; call-tree rooms nest 6 deep
NEST_GUID = 'fib-nest-1'
NEST_ID = 9101

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
at = lambda c, *p: {'c': c, 'path': list(p)}
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
take = lambda c, *p: {'type': 'take', 'at': at(c, *p)}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}
newnum = lambda: {'type': 'newNumber'}
newroom = lambda: {'type': 'newRoom'}
setv = lambda v, op='+': {'type': 'setValue', 'value': {'n': str(v), 'd': '1'}, 'op': op}

def cond5(first):
    return {'kind': 'box', 'holes': [first, None, None, None, None]}

leaf = lambda k: {'kind': 'robot', 'name': f'leaf-{k}',
    'condition': cond5(num(k)),
    'program': [newnum(), put('given', 1), vac('given', 0)],
    'trainedOn': None, 'team': []}

# Both copies are taken BEFORE either room is stowed aboard: a copy made
# after hole 3 is filled would carry the first child along into the second.
def dec():
    return [newnum(), setv(1, '-'), put('given', 0)]

def copy_box(park):
    return [take('given'), put('in'),                    # box to the copier
            take('in'), put('given'),                    # original back
            take('out'), put(park)]                      # the copy, parked

def build_room(src, hole):
    return [newroom(), put('s2'),                        # fresh room
            copy(src, 2), put('s2'),                     # spare robot -> room
            take(src), put('s2'),                        # copied box -> room
            take('s2'), put('given', hole)]              # room stowed aboard

# work spots are used in order -- spot 1 and 2 hold the two box copies, spot 3
# is where each room is furnished, so no spot is skipped
branch = {'kind': 'robot', 'name': 'branch',
    'condition': cond5({'kind': 'wildNumber'}),
    'program': (dec() + copy_box('s0')                   # box copy with n-1
              + dec() + copy_box('s1')                   # box copy with n-2
              + build_room('s0', 3) + build_room('s1', 4)
              + [vac('given', 0)]),
    'trainedOn': None, 'team': []}

fib_team = {'kind': 'robot', 'name': 'Fib',
    'condition': leaf(1)['condition'], 'program': leaf(1)['program'],
    'trainedOn': None, 'team': [leaf(2), branch]}

summer = {'kind': 'robot', 'name': 'Sum',
    'condition': {'kind': 'box', 'holes': [{'kind': 'wildNumber'}, {'kind': 'wildNumber'}]},
    'program': [dict(take('given', 1), **{'type': 'take'}), put('given', 0)],
    'trainedOn': None, 'team': []}
# the take must read the TOP OF THE PILE on the nest in hole 1
summer['program'][0] = {'type': 'take', 'at': {'c': 'given', 'path': [1], 'nest': True}}

work_box = {'kind': 'box', 'holes': [
    num(N),
    {'kind': 'bird', 'nestId': NEST_ID, 'nestGuid': NEST_GUID},
    fib_team,
    None, None,
]}

sum_box = {'kind': 'box', 'holes': [
    num(0),
    {'kind': 'nest', 'id': NEST_ID, 'guid': NEST_GUID, 'hasEgg': False, 'pile': []},
]}

txt = lambda t: {'kind': 'text', 'text': t}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': work_box, 'x': -0.15, 'z': 1.50},
    {'thing': sum_box, 'x': 1.10, 'z': 1.60},
    {'thing': fib_team, 'x': -1.15, 'z': 1.35},
    {'thing': summer, 'x': 0.60, 'z': 1.30},
    {'thing': txt('FIBONACCI\n\nThe robot marked Fib copies\n'
                  'ITSELF: it takes one off the\nnumber, copies its own box\n'
                  'through Mimi twice, builds\ntwo houses, and puts a copy\n'
                  'of itself in each. Robots\nthat reach 1 or 2 mail a\n'
                  'single 1 to the nest.'),
     'x': -1.05, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\n1. Give the five-hole box to\n   the Fib robot.\n'
                  '2. Watch the houses appear\n   and smoke. fib(8) makes\n'
                  '   forty of them, six deep.\n'
                  '3. When the smoke stops, the\n   nest holds 21 ones.\n'
                  '4. Give the [0, nest] box to\n   the Sum robot: it adds\n'
                  '   them up to 21.'),
     'x': -0.05, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'fibonacci.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
