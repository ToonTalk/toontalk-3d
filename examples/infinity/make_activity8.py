# Activity 8 -- Counting sequences: Cantor's diagonal, built out of robots.
#
#   "Can we make a sequence of ALL sequences?"
#
# The Diagonal team is given a box of
#
#   [ Sequences (a nest) , Current (a nest) , scale(skipped | to skip) , bird ]
#
# The Sequences nest receives BOXES, each holding a nest that some other robot
# is filling with terms. The team hands the bird the 1st term of the 1st
# sequence, the 2nd term of the 2nd, the 3rd of the 3rd, for ever: the
# diagonal of the table of sequences.
#
# WHY IT NEEDS A SCALE. A robot here says "hole 1 of what I was given", never
# "the nth one", so the nth term of a sequence cannot be addressed -- it has
# to be COUNTED to. The team walks up to it and throws away what it passes:
#
#   Skip a term     the scale tips to "to skip": take a term off Current and
#                   vacuum it; one more skipped.
#   Hand one on     the scale BALANCES: this is the term. Give it to the bird,
#                   take "to skip" up one, and set "skipped" one higher still,
#                   which tips the scale the other way.
#   Next sequence   the scale tips to "skipped": drop the old sequence, take
#                   the next box off Sequences, put its nest in Current, and
#                   set "skipped" back to 0.
#
# Three tilts, three robots, no counter anywhere but the scale. And each robot
# dozes on exactly what it needs: Skip and Hand one on look THROUGH Current
# for a number, Next sequence looks through Sequences for a box -- so the
# diagonal waits politely when a sequence has not arrived yet.
#
# Round 1: skipped 1, to skip 0 -- tips to "skipped", so the team asks for a
# sequence before it does anything else.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

S1 = (9281, 'inf8-s1')           # 1, 2, 3, 4, ...
S2 = (9282, 'inf8-s2')           # 1, 3, 5, 7, ...
S3 = (9283, 'inf8-s3')           # 1, 2, 4, 8, ...
S1G = (9291, 'inf8-s1')          # the same three, in the boxes you hand over
S2G = (9292, 'inf8-s2')
S3G = (9293, 'inf8-s3')
REQ1 = (9295, 'inf8-req1')       # "more, please": one nest per sequence room
REQ2 = (9296, 'inf8-req2')
REQ3 = (9297, 'inf8-req3')
SEQS = (9284, 'inf8-seqs')       # where the boxes of sequences arrive
CUR = (9285, 'inf8-cur')         # the sequence being read (replaced each round)
DIAG = (9286, 'inf8-diag')       # the diagonal, as the Add 1 room sees it
DIAG_W = (9287, 'inf8-diag')     # the same nest, out on the table to watch
CHANGED = (9288, 'inf8-changed')  # the diagonal with 1 added to every term

# --- three sequences, each making its terms ON DEMAND -----------------------
# A sequence room dozes on its "asked" nest. A number landing there is a request:
# the robot spends it, gives the bird a copy of its number, and moves on to the
# next. Nothing is made that nobody asked for, so nothing piles up -- the rooms
# used to run for ever and stacked terms two metres high on the boxes still
# waiting to be handed over.
source = lambda name, start, step, op, to, req, why: robot(
    name, box(ANYNUM, ANYBIRD, ANYNUM),                  # a request (a number) on the nest
    [takeTop('given', 2), put('s0'), vac('s0'),          # the request, spent
     copy('given', 0), put('given', 1)] + drop(step, op, 'given', 0),
    trained_on=box(num(start), bird(*to), nest(*req, label='asked')),
    note=why)

numbers = source('Numbers', 1, 1, '+', S1, REQ1,
                 'Dozes until a number lands on "asked" -- a request. Then spends it, gives the bird a copy of its number and adds 1: 1, 2, 3, 4, ... one term per request.')
odds = source('Odd Numbers', 1, 2, '+', S2, REQ2,
              'Dozes until a number lands on "asked" -- a request. Then spends it, gives the bird a copy of its number and adds 2: 1, 3, 5, 7, ... one term per request.')
doubling = source('Doubling', 1, 2, '*', S3, REQ3,
                  'Dozes until a number lands on "asked" -- a request. Then spends it, gives the bird a copy of its number and doubles it: 1, 2, 4, 8, ... one term per request.')

# --- the diagonal -----------------------------------------------------------
# A sequence arrives as a box: [its nest | a bird that asks its room for more].
# Current holds that whole box. Every term the team takes, it asks for the
# next by dropping a copy of its "more" pad on that bird; so a room is always
# exactly one term ahead of the team, and never a tower.
#   0 Sequences   1 Current [nest | bird]   2 scale   3 bird   4 "more" (a 1)
ASK = [copy('given', 4), put('given', 1, 1)]           # more, please
skip = robot(
    'Skip a term', box(None, box(ANYNUM, ANYBIRD), tilt('R'), ANYBIRD, None),
    [takeTop('given', 1, 0), put('s0'), vac('s0')] + ASK + drop(1, '+', 'given', 2, 0),
    trained_on=box(nest(*SEQS), nest(*CUR), scale(num(1), num(0)), bird(*DIAG), num(1, 1)),
    note='Leads the team. The scale tips towards "to skip", so this sequence still has terms to walk past: takes one off its nest, throws it away, asks the room for the next, and counts one more skipped.')

handon = robot(
    'Hand one on', box(None, box(ANYNUM, ANYBIRD), tilt('='), ANYBIRD, None),
    [takeTop('given', 1, 0), put('s0'),            # the term we walked to
     take('s0'), put('given', 3),                  # ...off to the bird
     ] + ASK                                       # and the next one, please
    + drop(1, '+', 'given', 2, 1)                  # next time, skip one more
    + [copy('given', 2, 1), setop('set'), put('given', 2, 0)]   # skipped := to skip
    + drop(1, '+', 'given', 2, 0),                 # ...+1, which tips it the other way
    note='The scale balances: the term under the claw is the one on the diagonal. Hands it to the bird, asks the room for the next, takes "to skip" up one, and sets "skipped" higher still -- which tips the scale over and asks for the next sequence.')

nextseq = robot(
    'Next sequence', box(box(ANYNEST, ANYBIRD), None, tilt('L'), ANYBIRD, None),
    [vac('given', 1),                              # the sequence just finished with
     takeTop('given', 0), put('given', 1),         # the box that arrived becomes Current
     ] + ASK                                       # its first term, please
    + drop(0, 'set', 'given', 2, 0),               # nothing skipped on this one yet
    note='The scale tips towards "skipped": this sequence is done with. Drops it, takes the next box off the Sequences nest -- a nest and a bird to its room -- puts it in the Current hole, asks for its first term, and sets "skipped" back to nothing. Dozes until a sequence arrives.')

diagonal = dict(skip, name='Diagonal', team=[handon, nextseq])

# --- Task B: the diagonal, changed ------------------------------------------
add1 = robot(
    'Add 1 to it', box(ANYNUM, ANYBIRD),
    [takeTop('given', 0), put('s0')] + drop(1, '+', 's0')
    + [take('s0'), put('given', 1)],
    trained_on=box(nest(*DIAG), bird(*CHANGED)),
    note='Takes each term of the diagonal off the nest, adds 1 to it and sends it on: a sequence that differs from every sequence the diagonal was made from.')

ABOUT = ('ACTIVITY 8\nCounting sequences\n\n'
         'Can we make a sequence of ALL\n'
         'sequences? Write them in a\n'
         'table, one sequence a row:\n\n'
         '  1  2  3  4 ...\n'
         '  1  3  5  7 ...\n'
         '  1  2  4  8 ...\n\n'
         'The DIAGONAL of that table is\n'
         'a sequence too: the 1st term\n'
         'of the 1st, the 2nd of the\n'
         '2nd, the 3rd of the 3rd.\n\n'
         'A robot cannot say "the nth\n'
         'one", so the team COUNTS to\n'
         'it and throws away what it\n'
         'passes. The scale says which\n'
         'of the three robots runs:\n'
         'tipped one way it skips a\n'
         'term, balanced it hands one\n'
         'on, tipped the other it asks\n'
         'for the next sequence.')

RUN = ('TO RUN IT\n'
      '\n'
      'Give the three "Sequence"\n'
      'boxes to the All Sequences\n'
      'bird, and pull the lever on\n'
      'each of the three rooms. Any\n'
      'order: a room sends a term\n'
      'only when the team asks for\n'
      'one, so nothing piles up.\n'
      '\n'
      'Watch through the glass: the\n'
      'team takes the 1st term of the\n'
      '1st sequence, walks past one\n'
      'term of the 2nd and takes its\n'
      '2nd, walks past two of the\n'
      '3rd. The diagonal reads 1, 3,\n'
      '4.\n'
      '\n'
      'Then it waits for a fourth\n'
      'row. The list is yours to go\n'
      'on adding to: every row you\n'
      'add gives the diagonal one\n'
      'more term.')

OWN = ('A ROW OF YOUR OWN\n'
      '\n'
      'Any sequence you can make is a\n'
      'row of the table. Train a\n'
      'robot that answers a number on\n'
      'its nest with the next term to\n'
      'a bird, put it in a room, and\n'
      'give the All Sequences bird a\n'
      'box holding [a nest its bird\n'
      'writes to | a bird to that\n'
      "room's nest].\n"
      '\n'
      'Open a room here and copy how\n'
      '"Numbers" does it: it dozes on\n'
      '"asked", spends the number,\n'
      'sends its term, and adds 1.')

THINK = ('THE ARGUMENT\n'
      '\n'
      'The "Add 1 to it" room turns\n'
      'the diagonal into another\n'
      'sequence. Ask yourself:\n'
      '\n'
      'Could THAT sequence be one of\n'
      'the rows? It differs from row\n'
      '1 in its 1st term, from row 2\n'
      'in its 2nd, from row n in its\n'
      'nth -- so it is none of them.\n'
      '\n'
      'Whatever list of sequences you\n'
      'make, this builds a sequence\n'
      'the list left out. The\n'
      'sequences are NOT countable.')

MORE = ('GOING FURTHER\n'
      '\n'
      'Would Doubling instead of Add\n'
      '1 change that? (Careful: what\n'
      'if a term is 0?)\n'
      '\n'
      'Now suppose every row were\n'
      'digits, 0 to 9, and the\n'
      'changer sent 4 for a 5 and 5\n'
      'for anything else. A sequence\n'
      'of digits is the decimal 0.d1\n'
      'd2 d3 ... -- a number between\n'
      '0 and 1. So there are more\n'
      'numbers between 0 and 1 than\n'
      'there are counting numbers,\n'
      'and Activity 6 counted every\n'
      'fraction.')

# A NEST'S PILE GROWS UPWARD, so a nest in the middle of the table hides
# whatever stands behind it. The two you watch sit at the front corners, where
# the only thing behind them is the edge of the table; the pads lie flat and
# take the middle.
bench = [
    {'thing': room('Numbers', box(num(1), bird(*S1, label='Sequence 1'), nest(*REQ1, label='asked')),
                   numbers, dirty=False), 'x': -1.15, 'z': 1.42},
    {'thing': room('Odd Numbers', box(num(1), bird(*S2, label='Sequence 2'), nest(*REQ2, label='asked')),
                   odds, dirty=False), 'x': -0.35, 'z': 1.42},
    {'thing': room('Doubling', box(num(1), bird(*S3, label='Sequence 3'), nest(*REQ3, label='asked')),
                   doubling, dirty=False), 'x': 0.45, 'z': 1.42},

    {'thing': room('Diagonal',
                   box(nest(*SEQS, label='Sequences'), nest(*CUR, label='Current'),
                       scale(num(1), num(0), label='skipped | to skip'),
                       bird(*DIAG, label='Diagonal'), num(1, 1)),
                   diagonal), 'x': 1.25, 'z': 1.42},

    # the three sequences, ready to hand over, and the bird that takes them in
    # each: its nest, and a bird that asks its room for the next term
    {'thing': box(nest(*S1G, label='Sequence 1'), bird(*REQ1, label='more')), 'x': -1.00, 'z': 1.80},
    {'thing': box(nest(*S2G, label='Sequence 2'), bird(*REQ2, label='more')), 'x': -0.50, 'z': 1.80},
    {'thing': box(nest(*S3G, label='Sequence 3'), bird(*REQ3, label='more')), 'x': 0.00, 'z': 1.80},
    {'thing': bird(*SEQS, label='All Sequences'), 'x': 0.36, 'z': 1.80},
    {'thing': room('Add 1 to it',
                   box(nest(*DIAG, label='In'), bird(*CHANGED, label='Out')),
                   add1), 'x': 0.75, 'z': 1.95},

    {'thing': nest(*DIAG_W, label='the diagonal'), 'x': -1.52, 'z': 2.80},
    {'thing': nest(*CHANGED, label='changed'), 'x': 1.52, 'z': 2.80},

    {'thing': txt(ABOUT), 'x': -1.10, 'z': 2.85},
    {'thing': txt(RUN), 'x': -0.45, 'z': 2.85},
    {'thing': txt(THINK), 'x': 0.20, 'z': 2.85},
    {'thing': txt(OWN), 'x': -1.50, 'z': 1.80},     # the front-left corner, beside Sequence 1
    {'thing': txt(MORE), 'x': 1.40, 'z': 1.80},     # beside the Add 1 room
]

if __name__ == '__main__':
    write('♾️ activity8-counting-sequences', bench)
