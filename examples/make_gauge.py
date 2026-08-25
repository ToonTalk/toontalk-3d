# The gauge, as an idiom -- BACKS.md's central claim, buildable at the table.
#
#   "A gauge is no new kind at all: an ordinary number, kept current by a
#    sync robot, made writable by a controller dozing on its event nest."
#
# Two live numbers, A and B. The Sync room mirrors A onto B: it dozes on A's
# event nest, and each change flies to B's bird wearing a `set` badge. The
# Control room does the same the other way. That is a feedback ring -- change
# either number, by bird or by dropping a number straight on it, and the
# other follows -- and the ECHO RULE is what keeps it from ringing forever:
# a set that changes nothing is swallowed, so the circle stops after one lap.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'infinity'))
from _tt import *                                          # noqa: F403

# live identities, hand-rolled the way the app writes them
A_LID, A_EVT = 'L901', 'evt-L901-gauge'
B_LID, B_EVT = 'L902', 'evt-L902-gauge'

liveNum = lambda v, lid, evt: dict(num(v), lid=lid, evt=evt,
                                   panel={'kind': 'world', 'v': 3, 'bench': [],
                                          'stations': {}, 'active': None})
liveBird = lambda lid, label=None: dict(bird(0, None, label), liveId=lid, nestGuid=None)
evtNest = lambda nid, evt, label: nest(nid, evt, label)

sync = robot(
    'Sync', box(ANYNUM, ANYBIRD),
    [takeTop('given', 0), setop('set'), put('given', 1)],
    trained_on=box(num(0), liveBird(B_LID)))

control = robot(
    'Control', box(ANYNUM, ANYBIRD),
    [takeTop('given', 0), setop('set'), put('given', 1)],
    trained_on=box(num(0), liveBird(A_LID)))

ABOUT = ('THE GAUGE\n\n'
         'A and B are live numbers.\n\n'
         'Sync dozes on A\'s events;\n'
         'each change flies to B\n'
         'wearing a set badge. Control\n'
         'does the same the other way.\n\n'
         'Change EITHER -- drop a\n'
         'number on it, or send its\n'
         'bird a badge -- and the\n'
         'other follows.\n\n'
         'The echo rule is why this\n'
         'ring does not ring forever:\n'
         'a set that changes nothing\n'
         'is swallowed, so the circle\n'
         'stops after one lap.')

RUN = ('TO RUN IT\n\n'
       'Pull both levers up.\n\n'
       'Drop a +3 on A. Watch B\n'
       'follow. Drop a ×2 on B.\n'
       'Watch A follow.\n\n'
       'The events nests keep the\n'
       'history: every value each\n'
       'number has passed through,\n'
       'newest underneath.')

bench = [
    {'thing': liveNum(5, A_LID, A_EVT), 'x': -0.9, 'z': 2.55},
    {'thing': liveNum(5, B_LID, B_EVT), 'x': 0.9, 'z': 2.55},

    {'thing': room('Sync', box(evtNest(9301, A_EVT, "A's events"), liveBird(B_LID, 'to B')),
                   sync, dirty=True), 'x': -0.45, 'z': 1.6},
    {'thing': room('Control', box(evtNest(9302, B_EVT, "B's events"), liveBird(A_LID, 'to A')),
                   control, dirty=True), 'x': 0.45, 'z': 1.6},

    {'thing': txt(ABOUT), 'x': -1.55, 'z': 1.7},
    {'thing': txt(RUN), 'x': 1.55, 'z': 1.7},
]

write('gauge', bench, folder=os.path.dirname(os.path.abspath(__file__)))
