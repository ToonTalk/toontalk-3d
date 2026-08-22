# Activity 3 -- A variety of infinite sequences, and dancing partners.
#
#   "Do all infinite sequences have the same size? How can you compare the
#    sizes of infinite sequences?"
#
#   Squares      [in-nest, out-bird]   n becomes n x n. A sequence that grows
#                                      much faster than the naturals.
#   Match Maker  [in-nest, count, out] makes the box [count, term] and hands
#                                      it over, then counts up. That box IS
#                                      the pairing: this natural number, with
#                                      this term of the sequence.
#
# The point of Match Maker is that it needs nothing clever. Whatever sequence
# you feed it, it pairs term 1 with 1, term 2 with 2, and so on -- so ANY
# sequence you can produce one term at a time is already in one-to-one
# correspondence with the naturals. It is countable by construction.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

NAT = (9221, 'inf3-nat')         # 1, 2, 3, ...
SQ_M = (9222, 'inf3-sq')         # 1, 4, 9, 16, ... as Match Maker sees them
SQ_W = (9225, 'inf3-sq')         # the same nest, out on the table to watch
PAIRS = (9223, 'inf3-pairs')     # [n, term] boxes

add1 = robot(
    'Add 1', box(ANYNUM, ANYBIRD),
    [copy('given', 0), put('given', 1)] + drop(1, '+', 'given', 0),
    trained_on=box(num(1), bird(*NAT)))

# n x n: take the number, copy it, and drop the copy back on with times.
squares = robot(
    'Squares', box(ANYNUM, ANYBIRD),
    [takeTop('given', 0), put('s0'),
     copy('s0'), setop('*'), put('s0'),
     take('s0'), put('given', 1)],
    trained_on=box(nest(*NAT), bird(*SQ_M)))

matchmaker = robot(
    'Match Maker', box(ANYNUM, ANYNUM, ANYBIRD),
    [newbox, holes(2), put('s0'),
     copy('given', 1), put('s0', 0),               # which one this is
     takeTop('given', 0), put('s0', 1),            # and what it is
     take('s0'), put('given', 2),                  # the pair, off to the bird
     ] + drop(1, '+', 'given', 1),                 # count up for the next
    trained_on=box(nest(*SQ_M), num(1), bird(*PAIRS)))

ABOUT = ('ACTIVITY 3\nA variety of sequences\n\n'
         'Squares makes 1, 4, 9, 16, ...\n'
         '-- a sequence that leaves the\n'
         'naturals far behind.\n\n'
         'Match Maker pairs each term\n'
         'with a natural number and\n'
         'hands out the box\n\n'
         '        [ n , term ]\n\n'
         'That box is the dance: this\n'
         'natural, with this term.\n\n'
         'Notice it does nothing clever.\n'
         'It never looks at the numbers.\n'
         'ANY sequence you can make one\n'
         'term at a time can be paired\n'
         'off this way -- so any such\n'
         'sequence is countable, however\n'
         'fast it grows.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 10 and pull the\n'
       'lever on the Add 1 room.\n\n'
       'The squares appear on their\n'
       'nest, and the pairs nest fills\n'
       'with boxes: [1,1] [2,4] [3,9]\n'
       '[4,16] and so on.\n\n'
       'Try it with another sequence.\n'
       'Train a robot of your own that\n'
       'takes a number and gives back\n'
       'something else -- thirds, or\n'
       'powers of two -- and put it in\n'
       'the Squares room instead.\n'
       'Match Maker will not notice.')

bench = [
    {'thing': room('Add 1', box(num(1), bird(*NAT, label='Numbers')),
                   add1, dirty=False), 'x': -1.25, 'z': 1.50},

    {'thing': room('Squares',
                   box(nest(*NAT, label='In'), bird(*SQ_M, label='Out')),
                   squares), 'x': -0.35, 'z': 1.50},
    {'thing': room('Match Maker',
                   box(nest(*SQ_M, label='Input'), num(1),
                       bird(*PAIRS, label='Dances')),
                   matchmaker), 'x': 0.60, 'z': 1.50},

    {'thing': nest(*SQ_W, label='the squares'), 'x': 0.15, 'z': 2.20},
    {'thing': nest(*PAIRS, label='dancing partners'), 'x': 1.15, 'z': 2.20},

    {'thing': txt(ABOUT), 'x': -1.20, 'z': 2.40},
    {'thing': txt(RUN), 'x': 0.25, 'z': 2.90},
]

if __name__ == '__main__':
    write('activity3-sequences-and-pairs', bench)
