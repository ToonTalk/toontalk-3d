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
SEQS = (9284, 'inf8-seqs')       # where the boxes of sequences arrive
CUR = (9285, 'inf8-cur')         # the sequence being read (replaced each round)
DIAG = (9286, 'inf8-diag')       # the diagonal, as the Add 1 room sees it
DIAG_W = (9287, 'inf8-diag')     # the same nest, out on the table to watch
CHANGED = (9288, 'inf8-changed')  # the diagonal with 1 added to every term

# --- three sequences, each making its own terms and needing nobody ----------
source = lambda name, start, step, op, to, why: robot(
    name, box(ANYNUM, ANYBIRD),
    [copy('given', 0), put('given', 1)] + drop(step, op, 'given', 0),
    trained_on=box(num(start), bird(*to)),
    note=why)

numbers = source('Numbers', 1, 1, '+', S1,
                 'Gives the bird a copy of its number and adds 1: 1, 2, 3, 4, ... for ever.')
odds = source('Odd Numbers', 1, 2, '+', S2,
              'Gives the bird a copy of its number and adds 2: 1, 3, 5, 7, ... for ever.')
doubling = source('Doubling', 1, 2, '*', S3,
                  'Gives the bird a copy of its number and doubles it: 1, 2, 4, 8, ... for ever.')

# --- the diagonal -----------------------------------------------------------
skip = robot(
    'Skip a term', box(None, ANYNUM, tilt('R'), ANYBIRD),
    [takeTop('given', 1), put('s0'), vac('s0')] + drop(1, '+', 'given', 2, 0),
    trained_on=box(nest(*SEQS), nest(*CUR), scale(num(1), num(0)), bird(*DIAG)),
    note='Leads the team. The scale tips towards "to skip", so this sequence still has terms to walk past: takes one off it, throws it away, and counts one more skipped.')

handon = robot(
    'Hand one on', box(None, ANYNUM, tilt('='), ANYBIRD),
    [takeTop('given', 1), put('s0'),               # the term we walked to
     take('s0'), put('given', 3),                  # ...off to the bird
     ] + drop(1, '+', 'given', 2, 1)               # next time, skip one more
    + [copy('given', 2, 1), setop('set'), put('given', 2, 0)]   # skipped := to skip
    + drop(1, '+', 'given', 2, 0),                 # ...+1, which tips it the other way
    note='The scale balances: the term under the claw is the one on the diagonal. Hands it to the bird, takes "to skip" up one, and sets "skipped" higher still -- which tips the scale over and asks for the next sequence.')

nextseq = robot(
    'Next sequence', box(box(ANYNEST), None, tilt('L'), ANYBIRD),
    [vac('given', 1),                              # the sequence just finished with
     takeTop('given', 0), put('s0'),               # the box that arrived
     take('s0', 0), put('given', 1),               # its nest becomes Current
     vac('s0'),                                    # the empty box away
     ] + drop(0, 'set', 'given', 2, 0),            # nothing skipped on this one yet
    note='The scale tips towards "skipped": this sequence is done with. Drops it, takes the next box off the Sequences nest, puts the nest inside it in the Current hole, and sets "skipped" back to nothing. Dozes until a sequence arrives.')

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

RUN = ('TO RUN IT\n\n'
       'Give the "Sequence 1" box to\n'
       'the All Sequences bird FIRST,\n'
       'and then pull the lever on the\n'
       'Numbers room. The first term\n'
       'appears on the diagonal nest.\n\n'
       'Hand the box over before you\n'
       'start its room: the team takes\n'
       'the sequence in as it arrives\n'
       'and counts from its first term.\n\n'
       'Now Sequence 2 and the Odd\n'
       'Numbers room; then Sequence 3\n'
       'and Doubling. Pull a lever\n'
       'again when you have seen\n'
       'enough.\n\n'
       'Watch through the glass: the\n'
       'team walks past one term of\n'
       'the second sequence, two of\n'
       'the third, and hands on what\n'
       'it lands on. The diagonal\n'
       'reads 1, 3, 4, ...\n\n'
       'Train a robot of your own,\n'
       'put it in a room with a nest\n'
       'and a bird, and give the bird\n'
       'a box with its nest: any\n'
       'sequence you can make is a\n'
       'row of the table.')

THINK = ('THE ARGUMENT\n\n'
         'The "Add 1 to it" room turns\n'
         'the diagonal into another\n'
         'sequence. Ask yourself:\n\n'
         'Could THAT sequence be one of\n'
         'the rows? It differs from row\n'
         '1 in its 1st term, from row 2\n'
         'in its 2nd, from row n in its\n'
         'nth — so it is none of them.\n\n'
         'Whatever list of sequences you\n'
         'make, this builds a sequence\n'
         'the list left out. The\n'
         'sequences are NOT countable.\n\n'
         'Would Doubling instead of Add\n'
         '1 change that? (Careful: what\n'
         'if a term is 0?)\n\n'
         'Now suppose every row were\n'
         'digits, 0 to 9, and the\n'
         'changer sent 4 for a 5 and 5\n'
         'for anything else. A sequence\n'
         'of digits is the decimal\n'
         '0.d1 d2 d3 ... — a number\n'
         'between 0 and 1. So there are\n'
         'more numbers between 0 and 1\n'
         'than there are counting\n'
         'numbers, and Activity 6\n'
         'counted every fraction.')

bench = [
    {'thing': room('Numbers', box(num(1), bird(*S1, label='Sequence 1')),
                   numbers, dirty=False), 'x': -1.30, 'z': 1.60},
    {'thing': room('Odd Numbers', box(num(1), bird(*S2, label='Sequence 2')),
                   odds, dirty=False), 'x': -0.45, 'z': 1.60},
    {'thing': room('Doubling', box(num(1), bird(*S3, label='Sequence 3')),
                   doubling, dirty=False), 'x': 0.40, 'z': 1.60},

    {'thing': room('Diagonal',
                   box(nest(*SEQS, label='Sequences'), nest(*CUR, label='Current'),
                       scale(num(1), num(0), label='skipped | to skip'),
                       bird(*DIAG, label='Diagonal')),
                   diagonal), 'x': 1.30, 'z': 1.60},

    # the three sequences, ready to hand over, and the bird that takes them in
    {'thing': box(nest(*S1G, label='Sequence 1')), 'x': -1.45, 'z': 2.25},
    {'thing': box(nest(*S2G, label='Sequence 2')), 'x': -1.00, 'z': 2.25},
    {'thing': box(nest(*S3G, label='Sequence 3')), 'x': -0.55, 'z': 2.25},
    {'thing': bird(*SEQS, label='All Sequences'), 'x': -0.10, 'z': 2.25},

    {'thing': nest(*DIAG_W, label='the diagonal'), 'x': 0.40, 'z': 2.25},
    {'thing': room('Add 1 to it',
                   box(nest(*DIAG, label='In'), bird(*CHANGED, label='Out')),
                   add1), 'x': 1.05, 'z': 2.25},
    {'thing': nest(*CHANGED, label='changed'), 'x': 1.60, 'z': 2.25},

    {'thing': txt(ABOUT), 'x': -1.30, 'z': 2.85},
    {'thing': txt(RUN), 'x': -0.35, 'z': 2.85},
    {'thing': txt(THINK), 'x': 0.60, 'z': 2.85},
]

if __name__ == '__main__':
    write('♾️ activity8-counting-sequences', bench)
