# The teacher -- a robot trained to train a robot.
#
# ToonTalk Reborn's first tour had a robot pick up a fresh robot, give it a
# number, start its training, do two gestures, stop, and name it "Add 1".
# This is that, in the workshop: a robot whose lesson includes GIVING a box
# to a little robot among its things and TEACHING it. Nothing new was added
# to what a robot can be given; teaching is a gesture like any other, made
# in a lesson and repeated in a run.
#
# The teacher's box has four holes:
#   0 a pad it reads out first        1 a little robot, untrained (the pupil)
#   2 a box [count 0 | 1] (the pupil's)  3 a pad it reads out at the end
#
# Its lesson, as a person would give it:
#   take the first pad, press Read (the robot learns to read it aloud), put
#   it back; take the box; click the little robot -- the pupil steps up to a
#   desk of its own, and everything next is the PUPIL's lesson: a copy of
#   the 1 it was given dropped on the count (0 + 1 = 1), then Ruby on the
#   count in its thought, so it counts on from any number -- the 1 is the
#   teacher's, not the stack's (Ken); "Stop teaching it"; then the last
#   pad, read out.
#
# Run, the teacher does all of that for real, and the pupil stands trained
# at its own desk with its box reading 1. Click the pupil and press Start:
# 2, 3, 4, ... The teacher itself runs once -- with the pupil gone from its
# box, its thought no longer fits.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403

WILDTEXT = {'kind': 'wildText'}
ANYROBOT = {'kind': 'anyRobot'}

first = txt('I am going to teach this little robot to count.')          # noqa: F405
last = txt('Now it counts: click it, and press Start.')                # noqa: F405
pupil = {'kind': 'robot', 'name': 'the pupil', 'program': [], 'condition': None,
         'trainedOn': None, 'team': [],
         'note': 'The pupil. The teacher gives it a box -- a count, and a 1 -- and '
                 'shows it how to count with them.'}
counting = box(num(0), num(1))                                         # noqa: F405

work = box(first, pupil, counting, last)                               # noqa: F405

speak = {'type': 'speak'}
teach = lambda *p: {'type': 'teach', 'at': at('given', *p)}            # noqa: E731,F405
taught = lambda step: {'type': 'taught', 'step': step}                 # noqa: E731
erase = lambda *path: {'type': 'erase', 'path': list(path)}           # noqa: E731

teacher = robot(                                                       # noqa: F405
    'the teacher',
    box(WILDTEXT, ANYROBOT, box(ANYNUM, ANYNUM), WILDTEXT),            # noqa: F405
    [take('given', 0), speak, put('given', 0),                         # noqa: F405
     take('given', 2),                                                 # noqa: F405
     teach(1),                                                         # the box goes to the pupil: its lesson begins
     taught(copy('given', 1)),                                         # the 1 it was given  # noqa: F405
     taught(put('given', 0)),                                          # ...dropped on the count  # noqa: F405
     taught(erase(0)),                                                 # any count, not just 0
     {'type': 'endTeach'},
     take('given', 3), speak, put('given', 3)],                        # noqa: F405
    trained_on=work,
    note='A robot that trains a robot. It reads the first pad out, gives the '
         'box [0 | 1] to the little robot in its second hole and teaches it to '
         'drop a copy of the 1 it was given on the count, has Ruby loosen the '
         'count in the pupil’s thought so it counts on from any number, and '
         'reads the last pad out. It runs once: with the pupil gone from its '
         'box, its thought no longer fits.')

ABOUT = ('THE TEACHER\n\n'
         'A robot trained to train a\n'
         'robot. Its box holds a pad,\n'
         'a little robot, a box with\n'
         'a count and a 1, and\n'
         'another pad.\n\n'
         'Run, it reads the pad out,\n'
         'gives the box to the little\n'
         'robot, and TEACHES it: the\n'
         'pupil steps up to a desk of\n'
         'its own and does each step\n'
         'as the teacher shows it.')

RUN = ('TO RUN IT\n\n'
       'Give the four-hole box to\n'
       'the teacher and press Start.\n\n'
       'Watch the pupil take a desk,\n'
       'drop a copy of its 1 on its\n'
       'count, and have its thought\n'
       'loosened by Ruby.\n\n'
       'Then click the pupil -- it is\n'
       'trained now -- and press\n'
       'Start: 2, 3, 4, ...')

HOW = ('HOW IT WAS TAUGHT\n\n'
       'In the teacher’s lesson, the\n'
       'claw took the box and was\n'
       'dropped on the little robot.\n'
       'That is “teach”: everything\n'
       'done next was the PUPIL’s\n'
       'lesson, and the teacher kept\n'
       'each step as a “taught” step\n'
       'of its own.\n\n'
       'Read on a pad in a lesson is\n'
       'a step too: the robot reads\n'
       'it out when it runs.')

bench = [
    {'thing': teacher, 'x': -1.20, 'z': 1.35},
    {'thing': work, 'x': -0.10, 'z': 1.55},

    {'thing': txt(ABOUT), 'x': -1.15, 'z': 2.25},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.45, 'z': 2.25},             # noqa: F405
    {'thing': txt(HOW), 'x': 0.25, 'z': 2.25},              # noqa: F405
]

write('🎓 teacher', bench, os.path.dirname(os.path.abspath(__file__)))   # noqa: F405
