# Generates sentence-generator.world.json -- a ToonTalk 3D program.
#
# One glass room ("Scriptorium") holds a robot team and its state box; a nest
# outside receives the sentences. The state box:
#   0 phase   1 die roll   2 sentence-under-construction   3 nouns (box of 6)
#   4 verbs (box of 6)     5 bird                          6 "the"   7 "."
#
# Each round one team member fires, keyed on [phase, roll]:
#   Scribe (phase 0): starts a sentence with "the", rolls the die, phase 1
#   noun1-k (1,k):    appends noun k, rolls again, phase 2
#   verb-k  (2,k):    appends verb k (each ends with "the"), rolls, phase 3
#   noun2-k (3,k):    appends noun k, phase 4
#   post    (4):      appends ".", hands the sentence to the bird, phase 0
#
# The die is thrown by dropping it on the number in hole 1 (dice re-roll the
# number they land on, 1..faces); the branching is ordinary team matching on
# the rolled number. Five rounds per sentence.
import json, io, os

NOUNS = [' cat', ' dog', ' frog', ' witch', ' robot', ' bird']
VERBS = [' sees the', ' chases the', ' likes the', ' fears the',
         ' paints the', ' dreams of the']
NEST_GUID = 'sentence-gen-nest-1'
NEST_ID = 9001

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
at = lambda *p: {'c': 'given', 'path': list(p)}
copy = lambda *p: {'type': 'copy', 'at': at(*p)}
take = lambda *p: {'type': 'take', 'at': at(*p)}
put = lambda *p: {'type': 'put', 'at': at(*p)}
die = lambda: {'type': 'newDie'}
setv = lambda v: {'type': 'setValue', 'value': {'n': str(v), 'd': '1'}, 'op': '+'}

def cond(phase, roll=None):
    holes = [num(phase), None if roll is None else num(roll)] + [None] * 6
    return {'kind': 'box', 'holes': holes}

def bot(name, condition, program, team=()):
    return {'kind': 'robot', 'name': name, 'program': program,
            'condition': condition, 'trainedOn': None, 'team': list(team)}

team = []
for k in range(1, 7):
    team.append(bot(f'noun1-{k}', cond(1, k),
        [copy(3, k - 1), put(2), die(), put(1), take(0), setv(2), put(0)]))
for k in range(1, 7):
    team.append(bot(f'verb-{k}', cond(2, k),
        [copy(4, k - 1), put(2), die(), put(1), take(0), setv(3), put(0)]))
for k in range(1, 7):
    team.append(bot(f'noun2-{k}', cond(3, k),
        [copy(3, k - 1), put(2), take(0), setv(4), put(0)]))
team.append(bot('post', cond(4),
    [copy(7), put(2), take(2), put(5), take(0), setv(0), put(0)]))

scribe = bot('Scribe', cond(0),
    [copy(6), put(2), die(), put(1), take(0), setv(1), put(0)], team)

gbox = {'kind': 'box', 'holes': [
    num(0), num(1), None,
    {'kind': 'box', 'holes': [txt(w) for w in NOUNS]},
    {'kind': 'box', 'holes': [txt(w) for w in VERBS]},
    {'kind': 'bird', 'nestId': NEST_ID, 'nestGuid': NEST_GUID},
    txt('the'), txt('.'),
]}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': {'kind': 'nest', 'id': NEST_ID, 'guid': NEST_GUID,
               'hasEgg': False, 'pile': []}, 'x': 1.35, 'z': 2.05},
    {'thing': {'kind': 'room', 'label': 'Scriptorium', 'opaque': False,
               'dirty': False,
               'world': {'kind': 'world', 'v': 1, 'bench': [],
                         'stations': {'stand': gbox}, 'active': scribe}},
     'x': -0.4, 'z': 1.7},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'sentence-generator.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
