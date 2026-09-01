# melody -- a robot that sings what it is handed.
#
# The first two worlds are things on a table. This one is a program, and it is
# the smallest program that says something true about sounds: a robot that
# turns a QUEUE OF NUMBERS into a tune, one note a round.
#
# The trick worth noticing is that the robot never knows a note. Its thought is
# [any number, anything, anything, anything] -- the pitch comes off the nest,
# and the recipe box it fills in has an EMPTY frequency hole, so filling that
# hole is an ordinary put and nothing has to be typed. Change the numbers on
# the nest and it sings a different tune; change the seconds or the shape in
# the recipe and the same tune comes out on a different instrument. No robot is
# retrained, because none of them ever knew the tune.
from _snd import *                                         # noqa: F403

PITCH = 9601                                    # the queue of pitches

# The recipe, with its frequency hole left EMPTY: that is what lets the pitch
# arrive by a plain put. A hole that already held a number would ADD.
recipe = {'kind': 'box',
          'holeLabels': ['frequency', 'seconds', 'shape'],
          'holes': [None, num(1, 4), txt('sine')]}

singer = robot(
    'Singer', box(ANYNUM, WILD, WILD, WILD),
    [
        copy('given', 2), put('s0'),        # a silent sound to sing into
        copy('given', 3), put('s1'),        # and a recipe to fill in
        takeTop('given', 0), put('s1', 0),  # the pitch, into the empty hole
        take('s1'), put('s0'),              # the recipe makes the sound sing
        take('s0'), put('given', 1),        # and it joins the tune's right edge
    ],
    trained_on=box(nest(PITCH, 'snd-melody'), sound(), sound(), recipe))

SCALE = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

work = box(
    # a nest is a pile, and the TOP of a pile is its last entry -- so the
    # scale is written down last note first, and comes off in order
    nest(PITCH, 'snd-melody', 'pitches',
         pile=[num(NOTES[n]) for n in reversed(SCALE)]),
    sound(label='the tune'),
    sound(label='blank'),
    recipe)

ABOUT = ('MELODY\n\n'
         'The Singer is handed\n'
         '[pitches, the tune, a blank\n'
         'sound, a recipe].\n\n'
         'Each round it copies the\n'
         'blank and the recipe, takes\n'
         'the next pitch off the nest,\n'
         'drops it into the recipe\'s\n'
         'EMPTY frequency hole, drops\n'
         'the recipe on the copy to\n'
         'make it sing, and joins the\n'
         'result onto the right edge\n'
         'of the tune.\n\n'
         'It knows no notes. Its\n'
         'thought is "any number".')

RUN = ('TO RUN IT\n\n'
       'Give the work box to the\n'
       'Singer. Eight pitches wait\n'
       'on the nest, so eight rounds\n'
       'later it dozes, done.\n\n'
       'The tune plays as it grows,\n'
       'a note longer each round --\n'
       'that is not a demonstration\n'
       'mode, it is the same "listen\n'
       'to what you just made" that\n'
       'happens when you drop a\n'
       'sound on a sound by hand.\n\n'
       'Press SPACE over the tune\n'
       'afterwards to hear it whole,\n'
       '"." to stop it.')

WHY = ('THEN CHANGE IT\n\n'
       'Write "square" over "sine"\n'
       'in the recipe and run it\n'
       'again: same tune, new\n'
       'instrument.\n\n'
       'Type other numbers onto the\n'
       'pitches, or drop more on the\n'
       'nest: a different tune, same\n'
       'robot.\n\n'
       'And drop a x-1 on the\n'
       'finished tune to hear the\n'
       'whole scale run backwards.')

bench = [
    {'thing': work, 'x': -0.70, 'z': 1.35},
    {'thing': singer, 'x': -1.50, 'z': 1.30},
    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},
]

write_sounds('melody', bench)
