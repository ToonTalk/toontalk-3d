# moving -- the smallest behaviour there is, laid out in the open.
#
# A gadget's robots live on its panel, out of the way. This world puts the
# same robot on the open table instead, so you can see what a behaviour IS
# before meeting one folded up.
#
# The Mover is handed [a step]. Each round it copies the step and gives it to
# THE BIRD ON THE PERCH -- the pedestal beside its desk:
#
#     [move | across | 1/60]
#
# That is the whole of "start moving right". On a thing's panel the perch
# holds a bird to that thing; out here it holds a bird to the star. The
# thing it moves does not know it is being moved, and the robot does not
# know what it is moving -- only that the bird on the perch goes somewhere.
from _beh import *                                          # noqa: F403

STAR = 'L9501'

star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), STAR)
step = msg('move', 'across', num(1, 60))                     # noqa: F405

mover = robot(
    'Mover', box(ANYBOX),
    [copy('given', 0), put('perch')],
    trained_on=box(step),
    note='Each round it copies the step and gives it to the bird on the perch: '
         '[move | across | 1/60]. That is the whole of “start moving right”. It '
         'does not know what it is moving, only that the bird on the perch goes somewhere.')

work = box(step)

ABOUT = ('MOVING\n\n'
         'The Mover is handed [a step].\n\n'
         'Each round it copies the step\n'
         'and gives it to the bird on\n'
         'the PERCH, the pedestal\n'
         'beside its desk:\n\n'
         '  [move | across | 1/60]\n\n'
         'That is the whole of "start\n'
         'moving right".')

RUN = ('TO RUN IT\n\n'
       'Set Speed to 8x and give the\n'
       'work box to the Mover.\n\n'
       'The star slides right and\n'
       'stops at the table\'s edge.\n\n'
       'Pick up the step, type a\n'
       'minus, and it goes the other\n'
       'way. Type a bigger number and\n'
       'it goes faster.')

WHY = ('WHAT IS NOT HERE\n\n'
       'The robot does not know what\n'
       'it is moving. It knows the\n'
       'bird on the perch goes\n'
       'somewhere.\n\n'
       'Out here she is a bird to the\n'
       'star. On a thing\'s panel the\n'
       'perch holds a bird to THAT\n'
       'thing -- so the same two\n'
       'steps move anything: put the\n'
       'robot on a panel and it moves\n'
       'whatever the panel belongs to.\n'
       'THAT is what a behaviour is.')

bench = [
    {'thing': star, 'x': -1.30, 'z': 1.20},
    {'thing': mover, 'x': -1.45, 'z': 1.62},
    {'thing': work, 'x': -0.55, 'z': 1.62},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},             # noqa: F405
]

write_beh('🏃 moving', bench, perch=to(STAR, 'to the star'))
