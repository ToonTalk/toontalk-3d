# pointer -- a gauge that follows your hand.
#
# The pointer nest holds ONE thing: [across | away], where the pointer is on
# the table, in the table's own steps. A position is a reading and not a
# history, so a new one replaces the last rather than piling up.
#
# The Watcher keeps the current reading in a hole where you can see it:
# sweep away what is there, take what is on the nest, put it in. Three steps,
# and it is a live instrument -- the numbers change under your hand.
from _dev import *                                         # noqa: F403

POINT = 9821

watcher = robot(
    'Watcher', box(ANYBOX, WILD),
    [
        vac('given', 1),              # last reading out
        takeTop('given', 0),          # this one off the nest
        put('given', 1),              # and into the hole
    ],
    trained_on=box(device(POINT, DEV_POINT, 'pointer'), box(num(0), num(0))))

# The second hole starts with a reading of its own -- zero, zero. A hole with
# nothing in it is not "anything", it is nothing, and the Watcher's thought
# asks for something there.
work = box(device(POINT, DEV_POINT, 'pointer'), box(num(0), num(0)))

ABOUT = ('POINTER\n\n'
         'The pointer nest holds one\n'
         'thing: [across | away], in\n'
         'the table\'s own steps.\n\n'
         'A position is a reading, not\n'
         'a history, so each new one\n'
         'replaces the last instead of\n'
         'piling up.\n\n'
         'The Watcher keeps the\n'
         'current one in a hole where\n'
         'you can see it.')

RUN = ('TO RUN IT\n\n'
       'Give the work box to the\n'
       'Watcher.\n\n'
       'Now move the pointer over the\n'
       'table. The two numbers in the\n'
       'second hole follow it.\n\n'
       'Its three steps are: sweep\n'
       'the old reading away, take\n'
       'what is on the nest, put it\n'
       'in the hole. Nothing about\n'
       'the pointer is built in -- it\n'
       'is a box arriving as mail.')

WHY = ('WHAT IT IS FOR\n\n'
       'Anything that reads a number\n'
       'can read this one: a scale\n'
       'can weigh it, a robot can\n'
       'compare it, a bird can carry\n'
       'it into a house.\n\n'
       'Zero across is the middle of\n'
       'the table; away grows towards\n'
       'you. So the numbers are worth\n'
       'watching as you move -- they\n'
       'are the table\'s own\n'
       'coordinates, not the screen\'s.')

bench = [
    {'thing': watcher, 'x': -1.45, 'z': 1.30},
    {'thing': work, 'x': -0.70, 'z': 1.32},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},
]

write_devices('pointer', bench)
