# Activity 5 -- All the rational numbers greater than 1.
#
#   "Pat says there must be more numbers between 1 and infinity than between
#    0 and 1. Is Pat right?"
#
# There is a laborious way -- redo Activity 4 with the inequality the other
# way round -- and a clever way, which is the one the activity wants you to
# find. Every proper fraction a/b has a reciprocal b/a, and b/a is greater
# than 1. Turn the sequence over and you have the other sequence, with the
# pairing already built in: 1/2 with 2, 2/3 with 3/2, 3/4 with 4/3.
#
#   Divides 1  [in-nest, out-bird]  takes a fresh 1, drops the incoming number
#                                   on it with DIVIDE, and hands out 1/n.
#
# So the two sets are the same size, and there was never any work to do: the
# answer to Pat is a single robot three steps long.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

BOXES = (9241, 'inf5-boxes')     # the [n, d] boxes from All Fractions
FRAC_D = (9242, 'inf5-frac')     # fractions, as Divides 1 sees them
FRAC_W = (9245, 'inf5-frac')     # the same nest, out on the table
BIG = (9243, 'inf5-big')         # and their reciprocals

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

# a fresh 1, with the incoming number dropped on it set to divide: 1/n.
divides1 = robot(
    'Divides 1', box(ANYNUM, ANYBIRD),
    [newnum, put('s0'),                            # a 1 off the stack
     takeTop('given', 0), setop('/'), put('s0'),   # n divides it
     take('s0'), put('given', 1)],
    trained_on=box(nest(*FRAC_D), bird(*BIG)))

ABOUT = ('ACTIVITY 5\nRationals greater than 1\n\n'
         'Pat says there must be more\n'
         'numbers above 1 than between\n'
         '0 and 1 -- after all, above 1\n'
         'there is endless room.\n\n'
         'You could redo Activity 4 with\n'
         'the scale the other way round.\n'
         'Or you could notice that every\n'
         'a/b below 1 has a b/a above\n'
         'it, and just turn the sequence\n'
         'over.\n\n'
         'Divides 1 is three steps long:\n'
         'take a 1, drop the incoming\n'
         'number on it set to DIVIDE,\n'
         'hand out the result.\n\n'
         'The pairing comes free. 1/2\n'
         'dances with 2, 2/3 with 3/2.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 20, give the\n'
       '[scale, Fractions] box to All\n'
       'Fractions and press Run.\n\n'
       'Three rooms run at once: the\n'
       'boxes become fractions, and\n'
       'the fractions become their own\n'
       'reciprocals.\n\n'
       'Sally objects: there is a whole\n'
       'copy of 0-to-1 between 1 and 2,\n'
       'another between 2 and 3, and so\n'
       'on forever -- so surely there\n'
       'are infinitely many times more\n'
       'above 1?\n\n'
       'Every number on the right nest\n'
       'came from exactly one on the\n'
       'left. What is wrong with\n'
       "Sally's argument?")

bench = [
    {'thing': allfractions, 'x': -1.40, 'z': 1.30},
    {'thing': box(scale(num(1), num(2), label='n over d'),
                  bird(*BOXES, label='Fractions')), 'x': -1.30, 'z': 1.85},

    {'thing': room('Box to Number',
                   box(nest(*BOXES, label='In'), bird(*FRAC_D, label='Out')),
                   boxtonum), 'x': -0.25, 'z': 1.50},
    {'thing': room('Divides 1',
                   box(nest(*FRAC_D, label='In'), bird(*BIG, label='Out')),
                   divides1), 'x': 0.65, 'z': 1.50},

    {'thing': nest(*FRAC_W, label='below 1'), 'x': 0.20, 'z': 2.20},
    {'thing': nest(*BIG, label='above 1'), 'x': 1.20, 'z': 2.20},

    {'thing': txt(ABOUT), 'x': -1.25, 'z': 2.40},
    {'thing': txt(RUN), 'x': 0.30, 'z': 2.90},
]

if __name__ == '__main__':
    write('activity5-above-one', bench)
