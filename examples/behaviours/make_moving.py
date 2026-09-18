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
       'Press SPACE on the star: it\n'
       'slides right and stops at\n'
       'the table\'s edge. "." stops.\n\n'
       'THE ROBOT IS ON ITS BACK.\nHold the star and press\nCtrl+P (or the gear on the\nholding card) to go through\nits door and watch the\nrobot at work. Escape\ncomes back out.\n\n'
       'In there, pick up the step,\n'
       'type a minus, and it goes\n'
       'the other way.')

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

# PACKAGED (Ken, 19 Sep): the Mover and its box are on the star's own panel,
# and the star is the thing -- press SPACE on it; go through its door to
# watch. The open layout it replaced is what the panel holds.
bench = [
    {'thing': gadget('*', STAR, mover, work, look=dict(bg='#1b2233', ink='#ffd23f', font='sans')), 'x': -1.30, 'z': 1.40},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},             # noqa: F405
]

write_beh('🏃 moving', bench)
