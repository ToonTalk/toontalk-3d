# -*- coding: utf-8 -*-
# Telling -- a robot teaches a robot to tell its thing what it read.
#
# Ken: "add a few examples to meta where a robot demonstrates how to create
# a behavior like this." The behaviour in question is the timer's second
# half: a robot that takes a reading off a nest, puts it in a
# [set | value | _] letter, and gives the letter to THE BIRD ON THE PERCH --
# the pedestal beside the desk, which on a panel holds a bird to the panel's
# own thing. So the robot never learns what it tells: on a number's panel it
# tells the number, on a picture's panel the picture.
#
# The teacher's box has four holes:
#   0 a pad it reads out first          1 a little robot, untrained (Tell)
#   2 a box [readings, with a 5 | [set | value | _]]   3 a pad it reads out at the end
#
# Out here on the bench the perch holds a bird of your own, to the nest
# "what it told" on the table -- Ken: "a user should be able to test such a
# robot without entering a panel by placing any bird on that pedestal." So
# the lesson, done for real in the run, lands [set | value | 5] on that nest.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403

WILDTEXT = {'kind': 'wildText'}
ANYROBOT = {'kind': 'anyRobot'}
TOLD = (9831, 'telling-what-it-told')
READ = (9832, 'telling-readings')

first = txt('I am going to teach this little robot to tell its thing what it read.')   # noqa: F405
last = txt('Now it tells. Put it on any thing’s panel, with its box, and it tells that thing.')   # noqa: F405
pupil = {'kind': 'robot', 'name': 'Tell', 'program': [], 'condition': None,
         'trainedOn': None, 'team': [],
         'note': 'The pupil. The teacher gives it a box -- a nest with a reading on it, and a '
                 '[set | value | _] letter -- and shows it how to tell the bird on the perch.'}
work = box(nest(*READ, label='readings', pile=[num(5)]),   # noqa: F405
           box(txt('set'), txt('value'), None))            # noqa: F405

speak = {'type': 'speak'}
teach = lambda *p: {'type': 'teach', 'at': at('given', *p)}            # noqa: E731,F405
taught = lambda step: {'type': 'taught', 'step': step}                 # noqa: E731
erase = lambda *path: {'type': 'erase', 'path': list(path)}           # noqa: E731

teacher = robot(                                                       # noqa: F405
    'the teacher',
    box(WILDTEXT, ANYROBOT, box(ANYNUM, ANYBOX), WILDTEXT),            # noqa: F405
    [take('given', 0), speak, put('given', 0),                         # noqa: F405
     take('given', 2),                                                 # noqa: F405
     teach(1),                                                         # the box goes to Tell: its lesson begins
     taught(copy('given', 1)), taught(put('s0')),                      # a [set | value | _] letter  # noqa: F405
     taught(takeTop('given', 0)), taught(put('s0', 2)),                # ...with the reading in it  # noqa: F405
     taught(take('s0')), taught(put('perch')),                         # given to the bird on the perch  # noqa: F405
     taught(erase(0)),                                                 # any reading, not just 5
     {'type': 'endTeach'},
     take('given', 3), speak, put('given', 3)],                        # noqa: F405
    trained_on=box(first, pupil, work, last),                          # noqa: F405
    note='A robot that trains a robot to tell its thing. It reads the first pad out, '
         'gives the box to the little robot in its second hole and teaches it: copy the '
         '[set | value | _] letter, put the reading in it, give it to the bird on the '
         'perch; then has Ruby loosen the reading in the pupil’s thought so any reading '
         'will do, and reads the last pad out.')

ABOUT = ('TELLING\n\n'
         'A robot trained to train a\n'
         'robot to TELL ITS THING.\n\n'
         'The pedestal beside the desk\n'
         'is the perch. On a thing’s\n'
         'panel it holds a bird to\n'
         'that thing; out here it\n'
         'holds a bird of your own,\n'
         'to the nest “what it told”.\n\n'
         'A letter put on the perch\n'
         'goes to whichever bird\n'
         'stands there.')

RUN = ('TO RUN IT\n\n'
       'Give the four-hole box to\n'
       'the teacher and press Start.\n\n'
       'Watch the pupil take a desk,\n'
       'copy the [set | value | _]\n'
       'letter, put the reading in\n'
       'it and give it to the bird\n'
       'on the perch: it lands on\n'
       '“what it told” as\n'
       '[set | value | 5].')

THEN = ('THEN, ON A PANEL\n\n'
        'Take a number from the\n'
        'stack. Open its panel with\n'
        'the gear, and drop on the\n'
        'panel a copy of the box and\n'
        'the trained pupil.\n\n'
        'Press SPACE on the number:\n'
        'the pupil runs on the\n'
        'number’s own panel, and the\n'
        'bird on the perch there is\n'
        'a bird to the number. It\n'
        'reads 5 now.')

HOW = ('WHY THE PERCH\n\n'
       'The pupil never learned\n'
       'what it tells. It learned\n'
       '“give the letter to the bird\n'
       'on the perch”, and the perch\n'
       'means the thing whose panel\n'
       'it is on.\n\n'
       'That is what makes a\n'
       'behaviour: the same robot,\n'
       'the same box, on any thing.')

bench = [
    {'thing': teacher, 'x': -1.20, 'z': 1.35},
    {'thing': box(first, pupil, work, last), 'x': -0.10, 'z': 1.55},   # noqa: F405
    {'thing': nest(*TOLD, label='what it told'), 'x': 1.10, 'z': 1.30},   # noqa: F405

    {'thing': txt(ABOUT), 'x': -1.15, 'z': 2.25},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.45, 'z': 2.25},             # noqa: F405
    {'thing': txt(THEN), 'x': 0.25, 'z': 2.25},             # noqa: F405
    {'thing': txt(HOW), 'x': 0.95, 'z': 2.25},              # noqa: F405
]

world = {'kind': 'world', 'v': 3, 'bench': bench,
         'stations': {'perch': bird(*TOLD, label='to what it told')},   # noqa: F405
         'active': None}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '\U0001f393 telling.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))   # noqa: F405
print('wrote', os.path.basename(out))
