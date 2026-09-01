# moving -- the smallest behaviour there is, laid out in the open.
#
# A gadget's robots live on its panel, out of the way. This world puts the
# same robots on the open table instead, so you can see what a behaviour IS
# before meeting one folded up.
#
# The Mover is handed [a bird to my thing, a step]. Each round it copies the
# step and gives it to the bird:
#
#     [move | across | 1/60]
#
# That is the whole of "start moving right". The thing it moves does not know
# it is being moved, and the robot does not know what it is moving -- only
# that its bird goes somewhere.
from _beh import *                                          # noqa: F403

STAR = 'L9501'

star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), STAR)
step = msg('move', 'across', num(1, 60))                     # noqa: F405

mover = robot(
    'Mover', box(ANYBIRD, ANYBOX),
    [copy('given', 1), put('given', 0)],
    trained_on=box(to(STAR), step))

work = box(to(STAR, 'my thing'), step)

ABOUT = ('MOVING\n\n'
         'The Mover is handed\n'
         '[a bird to my thing, a step].\n\n'
         'Each round it copies the step\n'
         'and gives it to the bird:\n\n'
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
       'it is moving. It knows a bird\n'
       'goes somewhere.\n\n'
       'The star does not know it is\n'
       'being moved. It answers a\n'
       'message, as it would answer\n'
       'one from you.\n\n'
       'So the same two steps move\n'
       'anything: point the bird at\n'
       'something else and the same\n'
       'robot moves that instead.\n'
       'THAT is what a behaviour is.')

bench = [
    {'thing': star, 'x': -1.30, 'z': 1.20},
    {'thing': mover, 'x': -1.45, 'z': 1.62},
    {'thing': work, 'x': -0.55, 'z': 1.62},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},             # noqa: F405
]

write_beh('moving', bench)
