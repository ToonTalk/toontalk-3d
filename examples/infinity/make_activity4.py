# Activity 4 -- All the fractions between 0 and 1.
#
#   "Can we generate ALL the proper fractions?"
#
# The trick the activity teaches is that you cannot walk the fractions in
# order of size -- between any two there is another, so you would never take a
# first step. You walk them by DENOMINATOR instead, and that is a walk that
# reaches everything:
#
#   1/2 | 1/3 2/3 | 1/4 2/4 3/4 | 1/5 2/5 3/5 4/5 | ...
#
# A team of two robots does it, and the branch is a SCALE. The box is
#
#        [ scale weighing numerator against denominator , bird ]
#
# and the scale's two pans are addressed exactly like box holes.
#
#   Next Numerator    runs while the scale tips towards the denominator
#                     (numerator still the smaller): hand out [n, d], n = n+1.
#   Next Denominator  runs when the scale BALANCES (n has caught d up):
#                     set n back to 1 and take d up one.
#
# The team tries its leader first, so a balanced scale falls through to the
# second robot. Nobody counts anything; the scale is the whole conditional.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

FRAC_B = (9231, 'inf4-frac')     # the [n, d] boxes, as Box to Number sees them
FRAC_W = (9234, 'inf4-frac')     # the same nest, out on the table to watch
NUMS = (9232, 'inf4-nums')       # and as actual fractions

nextnum = robot(
    'Next Numerator', box(tilt('R'), ANYBIRD),
    [newbox, holes(2), put('s0'),
     copy('given', 0, 0), put('s0', 0),            # the numerator
     copy('given', 0, 1), put('s0', 1),            # the denominator
     take('s0'), put('given', 1),                  # the pair, off to the bird
     ] + drop(1, '+', 'given', 0, 0),              # numerator up one
    trained_on=box(scale(num(1), num(2)), bird(*FRAC_B)))

nextden = robot(
    'Next Denominator', box(tilt('='), ANYBIRD),
    drop(1, 'set', 'given', 0, 0) +                # numerator back to 1
    drop(1, '+', 'given', 0, 1))                   # denominator up one

allfractions = dict(nextnum, name='All Fractions', team=[nextden])

# a/b as one number, so the nest reads 1/2, 1/3, 2/3 rather than a row of boxes
boxtonum = robot(
    'Box to Number', box(box(ANYNUM, ANYNUM), ANYBIRD),
    [takeTop('given', 0), put('s0'),               # the [a, b] box
     take('s0', 1), setop('/'), put('s0', 0),      # b divides a, in place
     take('s0', 0), put('given', 1),               # the fraction, out
     vac('s0')],                                   # the emptied box away
    trained_on=box(nest(*FRAC_B), bird(*NUMS)))

ABOUT = ('ACTIVITY 4\nAll fractions between 0 and 1\n\n'
         'You cannot list the fractions\n'
         'in order of size: between any\n'
         'two there is another, so there\n'
         'is no first step to take.\n\n'
         'So walk them by DENOMINATOR:\n\n'
         '  1/2 | 1/3 2/3 | 1/4 2/4 3/4\n'
         '  | 1/5 2/5 3/5 4/5 | ...\n\n'
         'Each group is finite, so the\n'
         'walk reaches every fraction\n'
         'after finitely many steps.\n\n'
         'The branch is the SCALE. While\n'
         'it tips towards the bottom\n'
         'number, Next Numerator runs.\n'
         'When it BALANCES, that robot\n'
         'no longer matches and Next\n'
         'Denominator takes the turn.')

RUN = ('TO RUN IT\n\n'
       'Pull the lever on the All\n'
       'Fractions room — and pull it\n'
       'again when you have seen\n'
       'enough.\n\n'
       'The scale pans are holes: walk\n'
       'in through the door and watch\n'
       'the numbers in them climb.\n\n'
       'Then ask: does 2/4 appear? And\n'
       '1/2 as well? They are the same\n'
       'number written twice -- which\n'
       'is what the No Copies robot in\n'
       'the original set exists to fix.\n\n'
       'Does every proper fraction turn\n'
       'up eventually? Which step\n'
       'reaches 7/8?')

bench = [
    {'thing': room('All Fractions',
                   box(scale(num(1), num(2), label='n over d'),
                       bird(*FRAC_B, label='Fractions')),
                   allfractions, dirty=False), 'x': -1.15, 'z': 1.50},

    {'thing': room('Box to Number',
                   box(nest(*FRAC_B, label='In'), bird(*NUMS, label='Out')),
                   boxtonum), 'x': 0.25, 'z': 1.50},

    {'thing': nest(*FRAC_W, label='as [n, d] boxes'), 'x': -0.35, 'z': 2.20},
    {'thing': nest(*NUMS, label='as fractions'), 'x': 1.15, 'z': 2.20},

    {'thing': txt(ABOUT), 'x': -1.20, 'z': 2.40},
    {'thing': txt(RUN), 'x': 0.25, 'z': 2.90},
]

if __name__ == '__main__':
    write('activity4-all-fractions', bench)
