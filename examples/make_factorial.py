# Generates factorial.world.json -- Ken's factorial.tt, a team of three where
# the loop is decided by a balance rather than by counting rounds.
#
# You hand the team a two-hole box, [N, a bird to answer on]. Nothing else:
# the state it needs is BUILT by the first robot, in front of you.
#
#   Start      sees [any number, a bird]
#              fetches a scale, puts a 1 in its left pan and N in its right,
#              sets the scale where N was, then makes a one-hole box holding
#              another 1 and joins it onto the LEFT of its own box.
#              The box it was given is now [so far, scale, bird].
#   Worker     sees [any number, a scale leaning RIGHT, a bird]
#              -- leaning right means the count has not reached N yet.
#              Drops a 1 on the count, wand-copies the count, types a times
#              sign on the copy, and drops that on "so far".
#   Finish     sees [any number, a BALANCED scale, a bird]
#              -- balanced means the count has reached N. Gives "so far" to
#              the bird, who flies it to the nest on your table.
#
# Nobody counts the rounds and nobody compares anything: the scale is doing
# the comparing continuously, and the two workers simply recognise what it
# says. That is the whole trick of the original, and it survives the one
# difference in our scales -- ToonTalk's sits in the box and weighs the holes
# on either side of it, ours holds the two numbers in its own pans.
#
# The original ends with the Finish robot fetching a bomb and blowing up its
# own house. We have no bombs: it empties the "so far" hole instead, which
# stops the team just as dead, since every thought wants a number there.
import json, io, os

N = 5                       # 5! = 120
NEST_ID, NEST_GUID = 9501, 'factorial-answer'

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *holes: {'kind': 'box', 'holes': list(holes)}
scale = lambda a, b: {'kind': 'scale', 'holes': [a, b]}

at = lambda c, *p: {'c': c, 'path': list(p)}
take = lambda c, *p: {'type': 'take', 'at': at(c, *p)}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}
join = lambda side: {'type': 'put', 'at': at('given'), 'side': side}
holes = lambda n: {'type': 'setHoles', 'n': n}
newnum = {'type': 'newNumber'}
newbox = {'type': 'newBox'}
newscale = {'type': 'newScale'}

WILD, ANYBIRD = {'kind': 'wildNumber'}, {'kind': 'anyBird'}
tilt = lambda t: {'kind': 'scaleTilt', 'tilt': t}

# --- the state the other two need, built in front of you --------------------
start = {
    'kind': 'robot', 'name': 'Factorial', 'condition': box(WILD, ANYBIRD),
    'program': [
        newscale, put('s0'),
        newnum, put('s0', 0),            # the count starts at 1
        take('given', 0), put('s0', 1),  # N goes in the other pan
        take('s0'), put('given', 0),     # the scale takes N's place
        newbox, holes(1), put('s1'),
        newnum, put('s1', 0),            # so far = 1
        take('s1'), join('L'),           # joined on: [so far, scale, bird]
    ],
    'trainedOn': box(num(N), {'kind': 'bird', 'nestId': NEST_ID, 'nestGuid': NEST_GUID}),
    'team': [],
}

# --- not there yet: count one more, and multiply it in ----------------------
worker = {
    'kind': 'robot', 'name': 'multiply', 'condition': box(WILD, tilt('R'), ANYBIRD),
    'program': [
        newnum, put('given', 1, 0),      # one more counted
        copy('given', 1, 0),             # a copy of the count, in hand
        {'type': 'setOp', 'op': '*'},    # "make it multiply"
        put('given', 0),                 # dropped on so far, it multiplies
    ],
    'trainedOn': None, 'team': [],
}

# --- the scale has come level: the count has reached N ----------------------
finish = {
    'kind': 'robot', 'name': 'answer', 'condition': box(WILD, tilt('='), ANYBIRD),
    'program': [
        take('given', 0), put('given', 2),   # so far, into the bird's wings
        vac('given', 1),                     # the scale goes, and with it the team
    ],
    'trainedOn': None, 'team': [],
}

start['team'] = [worker, finish]

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': box(num(N), {'kind': 'bird', 'nestId': NEST_ID, 'nestGuid': NEST_GUID}),
     'x': -0.25, 'z': 1.55},
    {'thing': start, 'x': -1.20, 'z': 1.30},
    {'thing': {'kind': 'nest', 'id': NEST_ID, 'guid': NEST_GUID, 'hasEgg': False,
               'pile': [], 'label': 'N factorial'}, 'x': 1.15, 'z': 1.60},
    {'thing': txt('FACTORIAL\n\nGive the team [N, a bird].\n\n'
                  'The first robot builds the\nrest: a scale with 1 in one\n'
                  'pan and N in the other, and\n"so far" joined on in front.\n\n'
                  'Then two robots take turns\nby reading the scale --\n'
                  'leaning means keep going,\nlevel means answer.'),
     'x': -1.05, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nGive the two-hole box to the\nFactorial robot.\n\n'
                  'Watch the scale come level\nas the count climbs to N.\n\n'
                  f'{N}! = 120 arrives on the\nnest marked "N factorial".\n\n'
                  'Nothing counts rounds: the\nscale is the only test.'),
     'x': -0.35, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'factorial.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
