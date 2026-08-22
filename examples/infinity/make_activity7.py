# Activity 7 -- An infinite sequence of rationals between ANY two numbers.
#
#   "Pat says there are an infinite number of rationals between any two
#    rationals. Is Pat right?"
#
# Take the sequence of all fractions between 0 and 1 -- Activity 4 -- and do
# one arithmetic step to every term:
#
#   Doubler      x 2      lands them all between 0 and 2
#   Add 10       + 10     lands them all between 10 and 11
#   Halve        x 1/2    lands them all between 0 and 1/2
#
# Each robot is the same three steps with a different number dropped on. And
# each output has exactly as many terms as the input, because every term came
# from precisely one term: multiplying by two does not thin a sequence out,
# and halving does not crowd it. Any interval you like, however short, holds
# a full copy of all the rationals between 0 and 1.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

BOXES = (9261, 'inf7-boxes')
F_A = (9262, 'inf7-frac')        # the fractions, three times over: one nest
F_B = (9263, 'inf7-frac')        # in three places, so each room gets every
F_C = (9264, 'inf7-frac')        # term rather than a third of them
TWO = (9265, 'inf7-two')         # 0 to 2
TEN = (9266, 'inf7-ten')         # 10 to 11
HALF = (9267, 'inf7-half')       # 0 to a half

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
    trained_on=box(nest(*BOXES), bird(*F_A)))


def shifter(name, v, op, src, dst, d=1):
    """One term in, one term out, with a single number dropped on it. Every
    robot in this activity is this robot with a different drop."""
    return robot(name, box(ANYNUM, ANYBIRD),
                 [takeTop('given', 0), put('s0')] +
                 drop(v, op, 's0') + [take('s0'), put('given', 1)],
                 trained_on=box(nest(*src), bird(*dst)))


doubler = shifter('Doubler', 2, '*', F_A, TWO)
add10 = shifter('Add 10', 10, '+', F_B, TEN)
halve = robot('Halve', box(ANYNUM, ANYBIRD),
              [takeTop('given', 0), put('s0'),
               newnum, setv(2, '/'), put('s0'),           # divided by two
               take('s0'), put('given', 1)],
              trained_on=box(nest(*F_C), bird(*HALF)))

ABOUT = ('ACTIVITY 7\nRationals between any two\n\n'
         'All Fractions makes every\n'
         'fraction between 0 and 1. Then\n'
         'one arithmetic step each:\n\n'
         '  Doubler  x 2   -> 0 to 2\n'
         '  Add 10   + 10  -> 10 to 11\n'
         '  Halve    / 2   -> 0 to 1/2\n\n'
         'Same robot three times over,\n'
         'with a different number\n'
         'dropped on the term.\n\n'
         'Every output term came from\n'
         'exactly one input term, so no\n'
         'sequence is longer or shorter\n'
         'than another. Doubling does\n'
         'not thin them out; halving\n'
         'does not crowd them.\n\n'
         'So any interval, however\n'
         'short, holds a full copy of\n'
         'all of them. Pat is right.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 20, give the\n'
       '[scale, Fractions] box to All\n'
       'Fractions and press Run.\n\n'
       'Four rooms run at once. The\n'
       'three nests fill at exactly the\n'
       'same rate -- that is the whole\n'
       'argument, visible.\n\n'
       'Joe says doubling must lose\n'
       'some numbers between 0 and 2,\n'
       'because it spreads them out.\n'
       'Is he right? Which number\n'
       'between 0 and 2 is missing?\n\n'
       'Change the 10 in Add 10 to any\n'
       'number you like: hold the\n'
       'number in its room and type.')

bench = [
    {'thing': allfractions, 'x': -1.40, 'z': 1.25},
    {'thing': box(scale(num(1), num(2), label='n over d'),
                  bird(*BOXES, label='Fractions')), 'x': -1.30, 'z': 1.80},

    {'thing': room('Box to Number',
                   box(nest(*BOXES, label='In'), bird(*F_A, label='Out')),
                   boxtonum), 'x': -0.50, 'z': 1.45},
    {'thing': room('Doubler', box(nest(*F_A, label='In'), bird(*TWO, label='Out')),
                   doubler), 'x': 0.20, 'z': 1.45},
    {'thing': room('Add 10', box(nest(*F_B, label='In'), bird(*TEN, label='Out')),
                   add10), 'x': 0.90, 'z': 1.45},
    {'thing': room('Halve', box(nest(*F_C, label='In'), bird(*HALF, label='Out')),
                   halve), 'x': 1.60, 'z': 1.45},

    {'thing': nest(*TWO, label='0 to 2'), 'x': 0.20, 'z': 2.15},
    {'thing': nest(*TEN, label='10 to 11'), 'x': 0.90, 'z': 2.15},
    {'thing': nest(*HALF, label='0 to a half'), 'x': 1.60, 'z': 2.15},

    {'thing': txt(ABOUT), 'x': -1.25, 'z': 2.35},
    {'thing': txt(RUN), 'x': -0.10, 'z': 2.95},
]

if __name__ == '__main__':
    write('activity7-any-interval', bench)
