# Generates fibonacci.world.json -- recursive Fibonacci, written the way the
# definition reads:
#
#   to fib n:
#     n is 1        -> answer 1
#     n is 2        -> answer 1
#     otherwise     -> ask fib(n-1) and fib(n-2), then answer their sum
#
# "Answer" means: give the number to the bird you were handed. Each call gets
# its own box, its own house, and its own bird to reply on. A caller makes a
# fresh nest for each child and waits until BOTH nests hold a number -- a
# robot facing a bare nest simply dozes, so waiting needs no machinery at all.
#
# The work box has seven holes:
#   0 n          1 the bird to answer on     2 a spare copy of the team
#   3, 4 the two nests the children answer on
#   5, 6 the two houses, kept so they are not lost (and swept up at the end)
import json, io, os

N = 6                       # fib(6) = 8 -- larger trees get slow and flaky
NEST_ID = 9101              # the top-level nest the answer arrives on
NEST_GUID = 'fib-answer'

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
at = lambda c, *p: {'c': c, 'path': list(p)}
top = lambda c, *p: {'c': c, 'path': list(p), 'nest': True}   # the top of a pile
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
take = lambda c, *p: {'type': 'take', 'at': at(c, *p)}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}
setv = lambda v, op='+': {'type': 'setValue', 'value': {'n': str(v), 'd': '1'}, 'op': op}
holes = lambda n: {'type': 'setHoles', 'n': n}

WILD = {'kind': 'wildNumber'}

def cond(n=None, three=None, four=None):
    """The work box as a robot's thought: [n, bird, robot, nestA, nestB, _, _]."""
    return {'kind': 'box', 'holes': [
        n, {'kind': 'anyBird'}, {'kind': 'anyRobot'}, three, four, None, None]}

# --- the two base cases: fib(1) and fib(2) are both 1 -----------------------
def leaf(k):
    return {'kind': 'robot', 'name': f'fib {k} is 1', 'condition': cond(num(k)),
            'program': [
                {'type': 'newNumber'},          # a fresh 1
                put('given', 1),                # into the bird's wings: she flies home
                vac('given', 0),                # the number goes: nothing matches now
            ],
            'trainedOn': None, 'team': []}

# --- the recursive case ----------------------------------------------------
def ask(minus, nest_hole, house_hole):
    """Make a nest, build [n-minus, its bird, a copy of me] and send it into a
    house of its own. The nest stays here; the bird goes with the child."""
    return [
        {'type': 'newNest'}, put('given', nest_hole),   # the egg hatches at once
        {'type': 'newBox'}, holes(7), put('s1'),        # the child's own work box
        copy('given', 0), put('s1', 0),
        {'type': 'newNumber'}, setv(minus, '-'), put('s1', 0),   # n - minus
        take('s0'), put('s1', 1),                       # the newly hatched bird
        copy('given', 2), put('s1', 2),                 # a copy of the whole team
        {'type': 'newRoom'}, put('s2'),
        copy('given', 2), put('s2'),                    # a robot moves in
        take('s1'), put('s2'),                          # its box lands on the desk
        take('s2'), put('given', house_hole),           # keep the house aboard
    ]

branch = {'kind': 'robot', 'name': 'ask both', 'condition': cond(WILD),
          'program': ask(1, 3, 5) + ask(2, 4, 6) + [vac('given', 0)],
          'trainedOn': None, 'team': []}

# --- the answer: both nests have a number, so add them and reply ------------
adder = {'kind': 'robot', 'name': 'add the answers',
         'condition': cond(None, WILD, WILD),
         'program': [
             {'type': 'take', 'at': top('given', 3)},   # what fib(n-1) sent
             put('s0'),
             {'type': 'take', 'at': top('given', 4)},   # what fib(n-2) sent
             put('s0'),                                 # dropped on it: they add
             copy('s0'), put('given', 1),               # the sum goes to the bird
             vac('given', 3), vac('given', 4),          # done: nothing matches now
         ],
         'trainedOn': None, 'team': []}

fib = {'kind': 'robot', 'name': 'fib', 'condition': leaf(1)['condition'],
       'program': leaf(1)['program'], 'trainedOn': None,
       'team': [leaf(2), adder, branch]}
# the adder is asked before the branch: once n has gone, only it can match

work_box = {'kind': 'box', 'holes': [
    num(N),
    {'kind': 'bird', 'nestId': NEST_ID, 'nestGuid': NEST_GUID},
    fib,
    None, None, None, None,
]}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': work_box, 'x': -0.20, 'z': 1.50},
    {'thing': {'kind': 'nest', 'id': NEST_ID, 'guid': NEST_GUID,
               'hasEgg': False, 'pile': [], 'label': 'the answer'},
     'x': 1.15, 'z': 1.60},
    {'thing': fib, 'x': -1.15, 'z': 1.30},
    {'thing': txt('FIBONACCI\n\nto fib n:\n  n is 1 → answer 1\n  n is 2 → answer 1\n'
                  '  else → ask fib(n-1)\n     and fib(n-2), then\n     answer their sum\n\n'
                  '"Answer" means give the\nnumber to the bird you\nwere handed.'),
     'x': -1.05, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nGive the seven-hole box to\nthe fib robot.\n\n'
                  'Each call makes two nests,\nsends a copy of itself into\n'
                  'two houses, and dozes\nuntil both nests answer.\n\n'
                  f'fib({N}) arrives on the nest\nmarked "the answer".'),
     'x': -0.05, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'fibonacci-recursive.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
