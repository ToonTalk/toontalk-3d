# Activity 2 -- Combining infinite sequences, part 1.
#
#   "Pat says there are more negative and positive whole numbers than just
#    positive whole numbers. Is Pat right?"
#
#   Negator  [in-nest, out-bird]    multiplies by -1.
#   Merge    [in-1, in-2, out-bird] gives away the number on the first nest,
#                                   then SWAPS the two nests over, so the next
#                                   round reads the other one.
#
# Merge alternating strictly is the whole lesson. It cannot run ahead on one
# input while the other is empty -- it will doze instead -- so the interleave
# is fair and every integer arrives after finitely many steps. That is what
# countable means, built out of two nests and a swap.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

NAT_N = (9211, 'inf2-nat')       # the naturals, as Negator sees them
NAT_M = (9214, 'inf2-nat')       # the same nest, as Merge sees them
NEG = (9212, 'inf2-neg')         # -1, -2, -3, ...
ALL = (9213, 'inf2-all')         # both, interleaved

add1 = robot(
    'Add 1', box(ANYNUM, ANYBIRD),
    [copy('given', 0), put('given', 1)] + drop(1, '+', 'given', 0),
    trained_on=box(num(1), bird(*NAT_N)))

negator = robot(
    'Negator', box(ANYNUM, ANYBIRD),
    [takeTop('given', 0), put('s0')] +
    drop(-1, '*', 's0') +
    [take('s0'), put('given', 1)],
    trained_on=box(nest(*NAT_N), bird(*NEG)))

merge = robot(
    'Merge', box(ANYNUM, WILD, ANYBIRD),
    [takeTop('given', 0), put('given', 2),        # this one goes out
     take('given', 0), put('s0'),                 # and the nests trade places
     take('given', 1), put('given', 0),
     take('s0'), put('given', 1)],
    trained_on=box(nest(*NAT_M), nest(*NEG), bird(*ALL)))

ABOUT = ('ACTIVITY 2\nCombining sequences, part 1\n\n'
         'Add 1 makes 1, 2, 3, ... and\n'
         'feeds both rooms at once.\n\n'
         'Negator turns each into its\n'
         'negative. Merge takes one from\n'
         'each nest in turn and hands\n'
         'the result out.\n\n'
         'Merge keeps no count. It gives\n'
         'away what is on the first nest\n'
         'and then swaps the two nests\n'
         'over -- so next round it reads\n'
         'the other. The swap IS the\n'
         'alternation.\n\n'
         'Neither side can run ahead, so\n'
         'every integer arrives after a\n'
         'finite wait. Countable.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 12 and pull the\n'
       'lever on the Add 1 room.\n\n'
       'All three rooms run together.\n\n'
       'Merge lags one behind Negator:\n'
       'it will not hand out a positive\n'
       'until the matching negative has\n'
       'arrived. That is it being fair.\n\n'
       'Then ask: is there an integer\n'
       'that never reaches the last\n'
       'nest, however long it runs?')

bench = [
    {'thing': room('Add 1', box(num(1), bird(*NAT_N, label='Numbers')),
                   add1, dirty=False), 'x': -1.25, 'z': 1.50},

    {'thing': room('Negator',
                   box(nest(*NAT_N, label='In'), bird(*NEG, label='Out')),
                   negator), 'x': -0.35, 'z': 1.50},
    {'thing': room('Merge',
                   box(nest(*NAT_M, label='positives'),
                       nest(*NEG, label='negatives'), bird(*ALL, label='Out')),
                   merge), 'x': 0.60, 'z': 1.50},

    {'thing': nest(*ALL, label='all integers'), 'x': 1.25, 'z': 2.20},

    {'thing': txt(ABOUT), 'x': -1.20, 'z': 2.40},
    {'thing': txt(RUN), 'x': 0.25, 'z': 2.85},
]

if __name__ == '__main__':
    write('activity2-all-integers', bench)
