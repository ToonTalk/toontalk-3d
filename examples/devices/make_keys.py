# keys -- a robot that types what you type.
#
# The smallest possible use of a device, and the one that shows why devices
# needed no new machinery at all. The Scribe is handed [keyboard, a pad]. Its
# thought is "some words on the nest, and anything beside them", so:
#
#   * when the nest is bare, nothing on it matches, and a robot facing a bare
#     nest DOZES. That is the whole of "waiting for a key press".
#   * when you press a key, a pad naming it lands on the nest, the nest wakes
#     whoever is dozing on it, and the Scribe joins the key onto the pad.
#
# No event loop, no callback, no subscribe. The key press is mail.
from _dev import *                                         # noqa: F403

KEYS = 9811

scribe = robot(
    'Scribe', box(WILDTEXT, WILD),
    [
        takeTop('given', 0),          # the key that was pressed, off the nest
        put('given', 1),              # joined onto the right edge of the pad
    ],
    trained_on=box(device(KEYS, DEV_KEYS, 'keyboard'), txt('')))

work = box(device(KEYS, DEV_KEYS, 'keyboard'), txt(''))

ABOUT = ('KEYS\n\n'
         'The Scribe is handed\n'
         '[keyboard, a pad].\n\n'
         'Its thought is "some words\n'
         'on the nest, and anything\n'
         'beside them". A bare nest\n'
         'matches nothing, and a robot\n'
         'facing a bare nest dozes.\n\n'
         'So "waiting for a key" is\n'
         'not a feature. It is what\n'
         'dozing already was.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 500 and give\n'
       'the work box to the Scribe.\n'
       'It shrinks and waits.\n\n'
       'Now type. Each key lands on\n'
       'the keyboard nest, wakes it,\n'
       'and is joined onto the pad --\n'
       'so the pad says what you\n'
       'typed.\n\n'
       'A printable key arrives as\n'
       'itself -- including the\n'
       'space. The rest arrive as\n'
       'words: Enter, ArrowLeft.')

WHY = ('THE DEVICE ITSELF\n\n'
       'The nest in hole 1 is one of\n'
       'the workshop\'s senses. There\n'
       'is nothing to connect: it\n'
       'wears the keyboard\'s name, so\n'
       'the keyboard delivers to it.\n\n'
       'Take another out of the\n'
       'Devices notebook (the menu)\n'
       'and it joins the same flock --\n'
       'two robots can watch the one\n'
       'keyboard.\n\n'
       'It has no egg, so no bird can\n'
       'be had from it: nothing you\n'
       'build can write to a device.')

bench = [
    {'thing': scribe, 'x': -1.45, 'z': 1.30},
    {'thing': work, 'x': -0.70, 'z': 1.32},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},
]

write_devices('keys', bench)
