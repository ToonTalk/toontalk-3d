# Activity 6 -- Combining infinite sequences, part 2: ALL the positive
# rationals, in one sequence.
#
#   "Are all the rational numbers countable?"
#
# This is the capstone, and it is made entirely of parts already built:
#
#   All Fractions   (Activity 4)  the proper fractions, by denominator
#   Box to Number   (Activity 4)  [a, b] as the single number a/b
#   Divides 1       (Activity 5)  each fraction turned over: the rationals > 1
#   Merge           (Activity 2)  one from each, in strict alternation
#
# Five rooms, one Run. Out of the last nest comes a single sequence in which
# every positive rational appears after a finite number of steps -- which is
# the whole of the answer. The rationals are dense: between any two there are
# infinitely many more, and no one of them has a next. And yet here they are,
# in a queue, being counted.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

BOXES = (9251, 'inf6-boxes')
FRAC_D = (9252, 'inf6-frac')     # fractions -> Divides 1
FRAC_M = (9256, 'inf6-frac')     # the same nest -> Merge
BIG_M = (9253, 'inf6-big')       # reciprocals -> Merge
BIG_W = (9257, 'inf6-big')       # the same nest, on the table
ALL = (9254, 'inf6-all')         # every positive rational

nextnum = robot(
    'Next Numerator', box(tilt('R'), ANYBIRD),
    [newbox, holes(2), put('s0'),
     copy('given', 0, 0), put('s0', 0),
     copy('given', 0, 1), put('s0', 1),
     take('s0'), put('given', 1),
     ] + drop(1, '+', 'given', 0, 0),
    trained_on=box(scale(num(1), num(2)), bird(*BOXES)))

nextden = robot(
    'Next Denominator', box(tilt('='), ANYBIRD),
    drop(1, 'set', 'given', 0, 0) + drop(1, '+', 'given', 0, 1))

allfractions = dict(nextnum, name='All Fractions', team=[nextden])

boxtonum = robot(
    'Box to Number', box(box(ANYNUM, ANYNUM), ANYBIRD),
    [takeTop('given', 0), put('s0'),
     take('s0', 1), setop('/'), put('s0', 0),
     take('s0', 0), put('given', 1),
     vac('s0')],
    trained_on=box(nest(*BOXES), bird(*FRAC_D)))

divides1 = robot(
    'Divides 1', box(ANYNUM, ANYBIRD),
    [newnum, put('s0'),
     takeTop('given', 0), setop('/'), put('s0'),
     take('s0'), put('given', 1)],
    trained_on=box(nest(*FRAC_D), bird(*BIG_M)))

merge = robot(
    'Merge', box(ANYNUM, WILD, ANYBIRD),
    [takeTop('given', 0), put('given', 2),
     take('given', 0), put('s0'),
     take('given', 1), put('given', 0),
     take('s0'), put('given', 1)],
    trained_on=box(nest(*FRAC_M), nest(*BIG_M), bird(*ALL)))

ABOUT = ('ACTIVITY 6\nAll the positive rationals\n\n'
         'Nothing new is built here. The\n'
         'rooms hold, in order:\n\n'
         '  All Fractions   (activity 4)\n'
         '  Box to Number   (activity 4)\n'
         '  Divides 1       (activity 5)\n'
         '  Merge           (activity 2)\n\n'
         'Below-1 goes one way and is\n'
         'turned over to make above-1;\n'
         'Merge then takes one from each\n'
         'in strict alternation.\n\n'
         'What comes out is a QUEUE of\n'
         'all the positive rationals.\n\n'
         'Between any two rationals lie\n'
         'infinitely many more. Not one\n'
         'of them has a next. And still\n'
         'they can be stood in a line\n'
         'and counted off.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 24 and pull the\n'
       'lever on the All Fractions\n'
       'room.\n\n'
       'Five rooms wake in turn as the\n'
       'first fraction reaches them.\n\n'
       'Merge lags: it will not hand\n'
       'out a fraction until the\n'
       'matching reciprocal has\n'
       'arrived. That is fairness, and\n'
       'fairness is what makes the\n'
       'count work.\n\n'
       'Does 1 itself ever appear? Does\n'
       'any number appear twice? What\n'
       'would you have to add to stop\n'
       'that -- and does it matter to\n'
       'the argument?')

bench = [
    {'thing': room('All Fractions',
                   box(scale(num(1), num(2), label='n over d'),
                       bird(*BOXES, label='Fractions')),
                   allfractions, dirty=False), 'x': -1.20, 'z': 1.45},

    {'thing': room('Box to Number',
                   box(nest(*BOXES, label='In'), bird(*FRAC_D, label='Out')),
                   boxtonum), 'x': -0.45, 'z': 1.45},
    {'thing': room('Divides 1',
                   box(nest(*FRAC_D, label='In'), bird(*BIG_M, label='Out')),
                   divides1), 'x': 0.30, 'z': 1.45},
    {'thing': room('Merge',
                   box(nest(*FRAC_M, label='below 1'),
                       nest(*BIG_W, label='above 1'), bird(*ALL, label='Out')),
                   merge), 'x': 1.05, 'z': 1.45},

    {'thing': nest(*ALL, label='every positive rational'), 'x': 0.75, 'z': 2.20},

    {'thing': txt(ABOUT), 'x': -1.25, 'z': 2.35},
    {'thing': txt(RUN), 'x': 0.05, 'z': 2.90},
]

if __name__ == '__main__':
    write('activity6-all-rationals', bench)
