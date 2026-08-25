# The bank account, rebuilt on panels -- Stage 2's canary.
#
# The old account is a robot serving [amount, reply-bird] messages off a
# nest: a message interface built by hand, with the robot as the teller.
# Here the balance IS a live number, and the interface came with it:
#
#   deposit            a +badged number to its bird
#   read the balance   [query | your-bird]
#   watch it move      [listen | your-bird] for its event nest
#
# The teller robot is GONE -- that is the "cleaner, not different" the plan
# demanded. And two depositor rooms hammer the balance at once to show the
# atomicity that came free: each badge is applied whole, so no interleaving
# can tear a deposit, and 100 + 5x10 + 4x25 is 250 however the rounds land.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'infinity'))
from _tt import *                                          # noqa: F403

BAL_LID, BAL_EVT = 'L910', 'evt-L910-account'

liveNum = lambda v, lid, evt: dict(num(v), lid=lid, evt=evt,
                                   panel={'kind': 'world', 'v': 3, 'bench': [],
                                          'stations': {}, 'active': None})
liveBird = lambda lid, label=None: dict(bird(0, None, label), liveId=lid, nestGuid=None)

# each depositor: hand the bird a +N (a fresh number badged and valued), then
# tick its tally up. The condition is a SCALE -- the tally against the stop --
# so the robot halts by the beam coming level, exactly as All Fractions does.
def depositor(name, amount, stop):
    return robot(
        name, box(tilt('R'), ANYBIRD),
        [newnum, setv(amount, '+'), put('given', 1)] +     # the deposit, whole
        drop(1, '+', 'given', 0, 0),                       # tally up one
        trained_on=box(scale(num(1), num(stop)), bird(0, None)))


dep10 = depositor('Tenner', 10, 6)      # runs while 1..5 < 6: five deposits
dep25 = depositor('Quarter', 25, 5)     # runs while 1..4 < 5: four deposits

ABOUT = ('THE ACCOUNT, ON A PANEL\n\n'
         'The balance is a LIVE\n'
         'number. The old teller\n'
         'robot is gone: depositing\n'
         'is a +badge to its bird,\n'
         'reading is [query | bird],\n'
         'watching is [listen | bird].\n\n'
         'Two rooms deposit at once.\n'
         'Each badge is applied whole\n'
         '-- no interleaving can tear\n'
         'a deposit -- so 100, plus\n'
         'five 10s, plus four 25s, is\n'
         '250 however the rounds\n'
         'happen to land.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 5 and pull\n'
       'both levers.\n\n'
       'Tenner banks +10 five\n'
       'times; Quarter banks +25\n'
       'four times (its tally makes\n'
       'the fifth round mismatch).\n\n'
       'The statement nest keeps\n'
       'the history: every balance\n'
       'the account has passed\n'
       'through, newest underneath.')

bench = [
    {'thing': liveNum(100, BAL_LID, BAL_EVT), 'x': 0.0, 'z': 2.6},
    {'thing': nest(9310, BAL_EVT, 'statement'), 'x': 0.75, 'z': 2.6},

    {'thing': room('Tenner', box(scale(num(1), num(6)), liveBird(BAL_LID, 'deposit')),
                   dep10, dirty=False), 'x': -0.75, 'z': 1.6},
    {'thing': room('Quarter', box(scale(num(1), num(5)), liveBird(BAL_LID, 'deposit')),
                   dep25, dirty=False), 'x': 0.75, 'z': 1.6},

    {'thing': txt(ABOUT), 'x': -1.6, 'z': 1.8},
    {'thing': txt(RUN), 'x': 1.7, 'z': 1.9},
]

write('live-account', bench, folder=os.path.dirname(os.path.abspath(__file__)))
