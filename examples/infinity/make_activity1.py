# Activity 1 -- Computing the even numbers in two ways.
#
#   "Can the same thing be made using ALL the numbers once, and also using
#    every other number once?"
#
#   Add 1     [n, bird]                 gives the bird n, then adds 1 to n.
#                                       That is the natural numbers, forever.
#   Doubler   [in-nest, out-bird]       every number handed to it, doubled.
#   Split     [in-nest, A, B]           alternates: one to A, the next to B,
#                                       by SWAPPING the two birds each round.
#
# Feed the naturals to Doubler and the evens come out, one for every natural.
# Feed the same naturals to Split and B's nest fills with the evens too --
# out of every OTHER natural. Same sequence, two ways, and one of the two
# looks as though it ought to be half the size. Galileo said so in 1638.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

# Two nests written with the SAME guid and different ids are one nest in two
# places: a bird delivers to every nest that answers to her name, so Add 1
# feeds Doubler and Split at once without either taking from the other.
NAT_D = (9201, 'inf1-nat')       # the naturals, as Doubler sees them
NAT_S = (9205, 'inf1-nat')       # the same nest, as Split sees them
EVEN = (9202, 'inf1-even')       # Doubler's answers
A = (9203, 'inf1-a')             # Split's first bird
B = (9204, 'inf1-b')             # Split's second

add1 = robot(
    'Add 1', box(ANYNUM, ANYBIRD),
    [copy('given', 0), put('given', 1)] +          # the bird takes it home
    drop(1, '+', 'given', 0),                      # and the count goes up
    trained_on=box(num(1), bird(*NAT_D)))

doubler = robot(
    'Doubler', box(ANYNUM, ANYBIRD),
    [takeTop('given', 0), put('s0')] +             # the number off the nest
    drop(2, '*', 's0') +                           # doubled where it stands
    [take('s0'), put('given', 1)],                 # and away to the bird
    trained_on=box(nest(*NAT_D), bird(*EVEN)))

# No counter and no memory: it hands the number to whichever bird is in hole 1
# and then swaps the two birds over, so next round the other one gets it.
split = robot(
    'Split', box(ANYNUM, ANYBIRD, ANYBIRD),
    [takeTop('given', 0), put('given', 1),         # this one to the near bird
     take('given', 1), put('s0'),                  # now swap the birds over
     take('given', 2), put('given', 1),
     take('s0'), put('given', 2)],
    trained_on=box(nest(*NAT_S), bird(*A), bird(*B)))

ABOUT = ('ACTIVITY 1\nThe even numbers, two ways\n\n'
         'Add 1 makes 1, 2, 3, ... for\n'
         'ever. Both rooms are fed from\n'
         'that one sequence.\n\n'
         'Doubler doubles each: the\n'
         'evens, out of EVERY natural.\n\n'
         'Split deals them out left,\n'
         'right, left: A gets the odds\n'
         'and B the evens -- out of\n'
         'every OTHER natural.\n\n'
         'Watch B and doubled fill at\n'
         'the same rate. Same sequence,\n'
         'two ways. One of them looks\n'
         'as if it should be half the\n'
         'size of the other.')

RUN = ('TO RUN IT\n\n'
       'Pull the lever on the Add 1\n'
       'room.\n\n'
       'That is all. Every robot is\n'
       'already in place; the three\n'
       'rooms work at the same time,\n'
       'each waking as the first\n'
       'number reaches it.\n\n'
       'Watch B and doubled fill at\n'
       'the same rate.\n\n'
       'Then ask: is there an even\n'
       'number on B that is not on\n'
       'doubled? Will there ever be?')

bench = [
    {'thing': room('Add 1', box(num(1), bird(*NAT_D, label='Numbers')),
                   add1, dirty=False), 'x': -1.20, 'z': 1.50},

    {'thing': room('Doubler',
                   box(nest(*NAT_D, label='In'), bird(*EVEN, label='Out')),
                   doubler), 'x': -0.30, 'z': 1.50},
    {'thing': room('Split',
                   box(nest(*NAT_S, label='Input'), bird(*A, label='A'),
                       bird(*B, label='B')),
                   split), 'x': 0.60, 'z': 1.50},

    {'thing': nest(*EVEN, label='doubled'), 'x': -0.30, 'z': 2.20},
    {'thing': nest(*A, label='A: odds'), 'x': 0.45, 'z': 2.20},
    {'thing': nest(*B, label='B: evens'), 'x': 1.05, 'z': 2.20},

    {'thing': txt(ABOUT), 'x': -1.20, 'z': 2.40},
    {'thing': txt(RUN), 'x': 0.20, 'z': 2.80},
]

if __name__ == '__main__':
    write('activity1-even-numbers', bench)
