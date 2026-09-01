# Zeno's postman -- one robot halves, one robot totals, a bird between them.
#
# The halver's whole program is two ordinary moves: copy the fraction and give
# the copy to the bird; then drop a x1/2 badge on the fraction, so what it
# gives next time is half of what it gave this time. 1/2, 1/4, 1/8, ...
#
# The totaller's program is ONE move: take the delivery off the nest and drop
# it on the running total -- a number dropped on a number adds itself, so the
# total IS the arithmetic, with no adding machine anywhere.
#
# The point of doing this here rather than in a spreadsheet: the workshop's
# numbers are exact. After twenty deliveries the total is not 0.99999-ish, it
# is 1048575/1048576 -- you can read the whole fraction off the block, watch
# the denominator double, and see exactly why the total creeps toward 1 and
# never arrives. An empty nest puts the totaller to sleep, so it works only
# when the post comes.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beh import *                                          # noqa: F403

ZENO_ID = 9901
ZENO_GUID = 'zeno-post'


def post_nest(pile=None):
    return {'kind': 'nest', 'id': ZENO_ID, 'guid': ZENO_GUID,
            'label': 'the post', 'hasEgg': False, 'pile': pile or []}


# --- the halver: [bird | the fraction] --------------------------------------
halver_work = box(bird(ZENO_ID, ZENO_GUID, 'to the total'),  # noqa: F405
                  dict(num(1, 2), label='the fraction'))     # noqa: F405
halver_bot = robot(                                          # noqa: F405
    'the halver', box(ANYBIRD, ANYNUM),                      # noqa: F405
    [copy('given', 1), put('given', 0),      # give the bird a copy  # noqa: F405
     newnum, setv(1, '*', 2), put('given', 1)],   # ...and halve what is left  # noqa: F405
    trained_on=box(bird(ZENO_ID, ZENO_GUID), num(1, 2)))     # noqa: F405

halver = room('the halver', halver_work, halver_bot, dirty=False)   # noqa: F405

# --- the totaller: [nest | running total] -----------------------------------
total_work = box(post_nest(),                                # noqa: F405
                 dict(num(0), label='the total so far'))     # noqa: F405
total_bot = robot(                                           # noqa: F405
    'the totaller', box(ANYNUM, ANYNUM),                     # noqa: F405
    [takeTop('given', 0), put('given', 1)],   # a number dropped on a number ADDS  # noqa: F405
    trained_on=box(post_nest([num(1, 2)]), num(0)))          # noqa: F405

totaller = room('the totaller', total_work, total_bot, dirty=False)   # noqa: F405

ABOUT = ('ZENO\'S POSTMAN\n\n'
         'The left house halves: its\n'
         'robot copies the fraction,\n'
         'gives the copy to the bird,\n'
         'and drops a x1/2 badge on\n'
         'what is left. 1/2, 1/4,\n'
         '1/8, ...\n\n'
         'The right house totals: its\n'
         'robot takes each delivery\n'
         'off the nest and drops it\n'
         'on the running total. A\n'
         'number dropped on a number\n'
         'ADDS -- the total IS the\n'
         'arithmetic.')

WHY = ('WHY IT NEVER GETS TO 1\n\n'
       'These numbers are EXACT.\n'
       'After 20 deliveries the\n'
       'total is not 0.99999-ish,\n'
       'it is\n\n'
       '   1048575\n'
       '   -------\n'
       '   1048576\n\n'
       'Read it off the block: the\n'
       'bottom doubles each time\n'
       'and the top stays one\n'
       'behind it. That missing\n'
       'ONE PART is why the total\n'
       'creeps toward 1 for ever\n'
       'and never arrives.')

RUN = ('TO RUN IT\n\n'
       'Pull the lever on each\n'
       'house (the halver\'s and\n'
       'the totaller\'s), and\n'
       'watch the bird carry the\n'
       'post between them.\n\n'
       'The totaller SLEEPS when\n'
       'the nest is empty -- it\n'
       'works only when the post\n'
       'comes. "." on a house\n'
       'stops it.')

bench = [
    {'thing': halver, 'x': -0.85, 'z': 1.45},
    {'thing': totaller, 'x': 0.55, 'z': 1.45},

    {'thing': txt(ABOUT), 'x': -0.75, 'z': 2.25},           # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.25},             # noqa: F405
    {'thing': txt(RUN), 'x': 0.65, 'z': 2.25},              # noqa: F405
]

write_beh('zeno', bench)                                     # noqa: F405
