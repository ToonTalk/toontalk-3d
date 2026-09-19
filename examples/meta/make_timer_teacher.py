# -*- coding: utf-8 -*-
# The timer teacher -- a robot builds the stopwatch's four robots, the way you
# would, and puts them on a number's panel: a stopwatch.
#
# The stopwatch (devices/timer) is four robots on a number's own panel. Two
# take turns by a "go" token crossing between two holes: "Ask the time" sends
# the computer [query | time | _] while the token is in hole 6 and moves it
# to hole 7; "Tell my number" runs when a reading is on the nest and the token
# is in hole 7, gives the reading minus the START to the bird on the perch in
# a [set | value | _] letter, and moves the token back. Two more make it a
# stopwatch rather than a clock: "Started" hears "on" on the number's own
# switch nest and asks the number what it shows; "Zero" sets the start from
# the next reading and that value, so the count goes on from whatever the
# number showed. This teacher trains all four, one after the other, each on
# the box in the state that robot works in -- the very robots of
# devices/make_timer.py, taught step by step:
#
#   0 a pad it reads out first
#   1 Started   2 its box: "on" on the switch
#   3 Ask       4 its box: nothing asked yet, the token in hole 6
#   5 Zero      6 its box: a reading, the fresh mark and my value have arrived
#   7 Tell      8 its box: a reading, a start, the token in hole 7
#   9 a number  10 a pad it reads out at the end
#
# Run, it does it all for real: Ask's lesson really asks the computer (the
# answer lands on the nest in Ask's box); Started's, Zero's and Tell's
# letters really go to the bird on the perch -- out here, a bird of your own
# to the nest "what it told". Then it takes the number's panel out onto a
# work spot, puts three boxes back in their holes, sets Started's box on the
# panel, then Started, Ask, Zero and Tell (a team, in that order), folds the
# panel away, and reads the last pad. The little robots it taught stay among
# its things -- the first, the second... little robot it taught -- so it can
# pick them up again. Take the number out of the box and press SPACE.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'infinity'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'devices'))
from _tt import *                                          # noqa: F403
import make_timer as T

WILDTEXT = {'kind': 'wildText'}
ANYROBOT = {'kind': 'anyRobot'}
TOLD = (9841, 'timer-teacher-what-it-told')
NUM = 'SW1'


def fresh(bot, note):
    """An untrained little robot with the name of the one it will become."""
    return {'kind': 'robot', 'name': bot['name'], 'program': [], 'condition': None,
            'trainedOn': None, 'team': [], 'note': 'A pupil. ' + note}


pupils = [
    (fresh(T.started, 'The teacher shows it what to do when the switch says "on".'),
     T.started, T.work(lid=NUM, switch='on')),
    (fresh(T.ask, 'The teacher shows it how to ask the computer the time and move the go token across.'),
     T.ask, T.work(lid=NUM)),
    (fresh(T.zero, 'The teacher shows it how to set the start from a fresh reading and what the number showed.'),
     T.zero, T.work(lid=NUM, reading=5000, asked=True, my_value=3, fresh=True)),
    (fresh(T.tell, 'The teacher shows it how to tell the number the reading minus the start, and move the token back.'),
     T.tell, T.work(lid=NUM, reading=5000, asked=True, start=4000)),
]

first = txt('I am going to teach four little robots to be a stopwatch.')   # noqa: F405
last = txt('The number is a stopwatch now. Take it out of the box and press SPACE on it.')   # noqa: F405
number = {'kind': 'number', 'value': {'n': '0', 'd': '1'}, 'label': 'stopwatch',
          'lid': NUM, 'evt': 'evt-' + NUM}

speak = {'type': 'speak'}
teach = lambda *p: {'type': 'teach', 'at': at('given', *p)}            # noqa: E731,F405
taught = lambda step: {'type': 'taught', 'step': step}                 # noqa: E731
erase = lambda *path: {'type': 'erase', 'path': list(path)}           # noqa: E731
fold = lambda c: {'type': 'fold', 'at': at(c)}                         # noqa: E731,F405
pupil = lambda k: {'type': 'take', 'at': {'c': 't%d' % k, 'path': [], 'bot': True}}   # noqa: E731

holes = [first]
for p, _, bx in pupils:
    holes += [p, bx]
holes += [number, last]
given = box(*holes)                                                    # noqa: F405

# the lessons, one per pupil: the robot's own steps, taught -- then Ruby on
# the holes that must fit any reading, value, start or token (not just
# these), and Dusty on the holes a robot must not look in at all (the token
# may be in either of two holes, or a mark may be there or not)
forget = lambda *path: {'type': 'forget', 'path': list(path)}          # noqa: E731
# (a hole empty at the lesson already takes anything or nothing; a nest empty
# at the lesson already takes any nest -- only what was THERE needs loosening)
LOOSEN = {'Started': ([], [5]),                  # the token: whichever hole, or none
          'Ask the time': ([5], [9]),            # any token; the switch nest, whatever it holds
          'Zero': ([1, 6, 8, 10], [9]),          # any reading, token, mark and value
          'Tell my number': ([1, 6, 7], [9])}    # any reading, token and start
program = [take('given', 0), speak, put('given', 0)]                   # noqa: F405
for i, (p, bot, bx) in enumerate(pupils):
    program += [take('given', 2 + 2 * i), teach(1 + 2 * i)]            # noqa: F405
    program += [taught(st) for st in bot['program']]
    ruby, dusty = LOOSEN[bot['name']]
    program += [taught(erase(h)) for h in ruby]
    program += [taught(forget(h)) for h in dusty]
    program += [{'type': 'endTeach'}]
program += [
    # THE STOPWATCH: the number's panel out onto a work spot, three boxes back in their
    # holes (a desk left aside holds the panels still), Started's box on the panel, then
    # the four pupils in order -- a team -- and the panel folded away
    take('given', 9), {'type': 'panel'}, put('given', 9),              # noqa: F405
    take('t2'), put('given', 4),                                       # noqa: F405
    take('t3'), put('given', 6),                                       # noqa: F405
    take('t4'), put('given', 8),                                       # noqa: F405
    take('t1'), put('s0'),                                             # Started's box, on the panel  # noqa: F405
    pupil(1), put('s0'), pupil(2), put('s0'), pupil(3), put('s0'), pupil(4), put('s0'),   # noqa: F405
    fold('s0'),
    take('given', 10), speak, put('given', 10)]                        # noqa: F405

teacher = robot(                                                       # noqa: F405
    'the teacher',
    box(WILDTEXT, ANYROBOT, ANYBOX, ANYROBOT, ANYBOX, ANYROBOT, ANYBOX, ANYROBOT, ANYBOX, ANYNUM, WILDTEXT),   # noqa: F405
    program, trained_on=given,
    note='A robot that trains the stopwatch’s four robots -- Started, Ask, Zero and Tell, '
         'each on the box in the state that robot works in -- then takes the number’s panel out, '
         'sets Started’s box and the four pupils on it, and folds the panel away: the number is a '
         'stopwatch. Nothing here is new: put on the perch, Dusty, Ruby and a teaching are steps like '
         'any other.')

RQ, LQ, DQ = '’', '“', '”'
ABOUT = ('THE TIMER TEACHER\n\n'
         'A robot that trains the four\n'
         'robots of the stopwatch, one\n'
         'after the other, each on the\n'
         'box in the state it works\n'
         'in -- then puts them on a\n'
         'number' + RQ + 's panel.\n\n'
         'Started: "on" on my switch.\n'
         'Ask: the token in hole 6.\n'
         'Zero: a fresh reading, and\n'
         'what the number showed.\n'
         'Tell: a reading and a start.')

RUN = ('TO RUN IT\n\n'
       'Give the eleven-hole box to\n'
       'the teacher and press Start.\n\n'
       'Ask really asks: the\n'
       'computer' + RQ + 's answer lands on\n'
       'the nest in its box. The\n'
       'others really tell: their\n'
       'letters go to the bird on\n'
       'the perch, and out here she\n'
       'takes them to ' + LQ + 'what it told' + DQ + '.\n\n'
       'Then the number' + RQ + 's panel\n'
       'comes out, a box and the\n'
       'four robots go on it, and\n'
       'it folds away.')

THEN = ('THE STOPWATCH\n\n'
        'Take the number out of the\n'
        'teacher' + RQ + 's box and press\n'
        'SPACE on it: it counts the\n'
        'milliseconds from 0. ' + LQ + '.' + DQ + '\n'
        'rests it; SPACE goes on from\n'
        'there. Set it to 0 and start\n'
        'it, and it starts from 0.\n\n'
        'Open its panel with the\n'
        'gear: the box and the team\n'
        'are there, and the bird on\n'
        'the perch is a bird to the\n'
        'number.')

HOW = ('HOW IT REACHES THEM\n\n'
       'A little robot the teacher\n'
       'taught stays among its\n'
       'things: ' + LQ + 'the first little\n'
       'robot it taught' + DQ + ', at its own\n'
       'desk, with its box. Click\n'
       'the pupil with an empty\n'
       'claw to pick it up; click\n'
       'the box on its desk to take\n'
       'that.\n\n'
       'Four robots, because a robot\n'
       'cannot wait mid-round for\n'
       'an answer, and a stopwatch\n'
       'must know when it started.')

bench = [
    {'thing': teacher, 'x': -1.45, 'z': 1.35},
    {'thing': given, 'x': -0.10, 'z': 1.55},
    {'thing': nest(*TOLD, label='what it told'), 'x': 1.35, 'z': 1.30},   # noqa: F405

    {'thing': txt(ABOUT), 'x': -1.15, 'z': 2.25},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.45, 'z': 2.25},             # noqa: F405
    {'thing': txt(THEN), 'x': 0.25, 'z': 2.25},             # noqa: F405
    {'thing': txt(HOW), 'x': 0.95, 'z': 2.25},              # noqa: F405
]

world = {'kind': 'world', 'v': 3, 'bench': bench,
         'stations': {'perch': bird(*TOLD, label='to what it told')},   # noqa: F405
         'active': None}
out = os.path.join(HERE, '\U0001f393 timer-teacher.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))   # noqa: F405
print('wrote', os.path.basename(out))
