# -*- coding: utf-8 -*-
# The timer teacher -- a robot builds the timer's two robots, the way you
# would, and puts them on a number's panel: a stopwatch.
#
# The timer (devices/timer) is two robots on a number's own panel, taking
# turns by a "go" pad crossing between two holes: "Ask the time" sends the
# computer [query | time | _] while the pad is in hole 6 and moves it to
# hole 7; "Tell my number" runs when a reading is on the nest and the pad is
# in hole 7, gives the reading to the bird on the perch in a
# [set | value | _] letter, and moves the pad back. This teacher trains both,
# one after the other, each on a box in the state that robot works in:
#
#   0 a pad it reads out first
#   1 a little robot (Ask)   2 the box as Ask finds it: nest empty, "go" in hole 6
#   3 a little robot (Tell)  4 the box as Tell finds it: a reading on the nest, "go" in hole 7
#   5 a number               6 a pad it reads out at the end
#
# Run, it does it all for real: Ask's lesson really asks the computer (the
# answer lands on the nest in Ask's box), and Tell's lesson really gives its
# letter to the bird on the perch -- out here, a bird of your own to the
# nest "what it told". Then it takes the number's panel out onto a work
# spot, puts Ask's box back in its hole, sets Tell's box on the panel, then
# Ask, then Tell (a team), folds the panel away, and reads the last pad. The little robots it taught stay among its
# things -- the first, the second little robot it taught -- so it can pick
# them up again. Take the number out of the box and press SPACE: it counts
# the milliseconds. "." rests it.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403

WILDTEXT = {'kind': 'wildText'}
ANYROBOT = {'kind': 'anyRobot'}
TOLD = (9841, 'timer-teacher-what-it-told')
ASK_MAIL = (9842, 'timer-teacher-readings')
TELL_MAIL = (9843, 'timer-teacher-readings-2')

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}
query = box(txt('query'), txt('time'), None)               # noqa: F405
setter = box(txt('set'), txt('value'), None)               # noqa: F405


def work(mail, reading, asked):
    """The timer's box, in the state one of its robots works in."""
    return box(live_bird('COMPUTER', 'the computer'),        # noqa: F405
               nest(*mail, label='readings', pile=[num(reading)] if reading is not None else []),   # noqa: F405
               bird(*mail, label='to my readings'),          # noqa: F405
               query, setter,
               None if asked else txt('go'),                 # noqa: F405
               txt('go') if asked else None)                 # noqa: F405


ask_box = work(ASK_MAIL, None, False)       # nothing asked yet: go in hole 6
tell_box = work(TELL_MAIL, 5, True)         # a reading waiting, go in hole 7

first = txt('I am going to teach two little robots to be a timer.')    # noqa: F405
last = txt('The number is a stopwatch now. Take it out of the box and press SPACE on it.')   # noqa: F405
ask = {'kind': 'robot', 'name': 'Ask', 'program': [], 'condition': None,
       'trainedOn': None, 'team': [],
       'note': 'Untrained. The teacher shows it how to ask the computer the time and move the go pad across.'}
tell = {'kind': 'robot', 'name': 'Tell', 'program': [], 'condition': None,
        'trainedOn': None, 'team': [],
        'note': 'Untrained. The teacher shows it how to give a reading to the bird on the perch and move the go pad back.'}

speak = {'type': 'speak'}
teach = lambda *p: {'type': 'teach', 'at': at('given', *p)}            # noqa: E731,F405
taught = lambda step: {'type': 'taught', 'step': step}                 # noqa: E731
erase = lambda *path: {'type': 'erase', 'path': list(path)}           # noqa: E731

number = {'kind': 'number', 'value': {'n': '0', 'd': '1'}, 'label': 'stopwatch'}
given = box(first, ask, ask_box, tell, tell_box, number, last)         # noqa: F405
fold = lambda c: {'type': 'fold', 'at': at(c)}                         # noqa: E731,F405
pupil = lambda k: {'type': 'take', 'at': {'c': 't%d' % k, 'path': [], 'bot': True}}   # noqa: E731

teacher = robot(                                                       # noqa: F405
    'the teacher',
    box(WILDTEXT, ANYROBOT, ANYBOX, ANYROBOT, ANYBOX, ANYNUM, WILDTEXT),   # noqa: F405
    [take('given', 0), speak, put('given', 0),                         # noqa: F405
     # ASK: the pad is in hole 6 -- ask the computer, answered to my readings, and cross the pad over
     take('given', 2), teach(1),                                       # noqa: F405
     taught(copy('given', 3)), taught(put('s0')),                      # [query | time | _]  # noqa: F405
     taught(copy('given', 2)), taught(put('s0', 2)),                   # ...answered to my readings  # noqa: F405
     taught(take('s0')), taught(put('given', 0)),                      # asked of the computer  # noqa: F405
     taught(take('given', 5)), taught(put('given', 6)),                # the go pad crosses over  # noqa: F405
     {'type': 'endTeach'},
     # TELL: a reading is on the nest and the pad is in hole 7 -- tell the perch, and bring the pad back
     take('given', 4), teach(3),                                       # noqa: F405
     taught(copy('given', 4)), taught(put('s0')),                      # [set | value | _]  # noqa: F405
     taught(takeTop('given', 1)), taught(put('s0', 2)),                # ...with the reading in it  # noqa: F405
     taught(take('s0')), taught(put('perch')),                         # given to the bird on the perch  # noqa: F405
     taught(take('given', 6)), taught(put('given', 5)),                # the go pad comes back  # noqa: F405
     taught(erase(1)),                                                 # any reading, not just 5
     {'type': 'endTeach'},
     # THE STOPWATCH: the number's panel out onto a work spot, Tell's box on it, Ask, then Tell -- a team
     take('given', 5), {'type': 'panel'}, put('given', 5),             # noqa: F405
     take('t1'), put('given', 2),                                      # Ask's box back in its hole: its desk goes  # noqa: F405
     take('t2'), put('s0'),                                            # the box on the second pupil's desk  # noqa: F405
     pupil(1), put('s0'),                                              # Ask, behind the panel's desk  # noqa: F405
     pupil(2), put('s0'),                                              # Tell joins: a team  # noqa: F405
     fold('s0'),                                                       # the panel goes home into the number
     take('given', 6), speak, put('given', 6)],                        # noqa: F405
    trained_on=given,
    note='A robot that trains the timer’s two robots. It teaches Ask on a box with the go '
         'pad in hole 6: ask the computer the time, answered to my readings, and move the pad '
         'to hole 7. Then it teaches Tell on a box with a reading and the pad in hole 7: put the '
         'reading in a [set | value | _] letter, give it to the bird on the perch, move the pad '
         'back, and have Ruby loosen the reading. Then it takes the number’s panel out, sets '
         'Tell’s box, Ask and Tell on it, and folds the panel away: the number is a stopwatch.')

ABOUT = ('THE TIMER TEACHER\n\n'
         'A robot that trains the two\n'
         'robots of the timer, one\n'
         'after the other, each on a\n'
         'box in the state it works\n'
         'in -- then puts them on a\n'
         'number’s panel.\n\n'
         'Ask: the go pad is in hole 6.\n'
         'Ask the computer the time,\n'
         'move the pad to hole 7.\n\n'
         'Tell: a reading, pad in 7.\n'
         'Give it to the bird on the\n'
         'perch, move the pad back.')

RUN = ('TO RUN IT\n\n'
       'Give the seven-hole box to\n'
       'the teacher and press Start.\n\n'
       'Ask really asks: the\n'
       'computer’s answer lands on\n'
       'the nest in its box. Tell\n'
       'really tells: its letter\n'
       'goes to the bird on the\n'
       'perch, and out here she\n'
       'takes it to “what it told”.\n\n'
       'Then the number’s panel\n'
       'comes out, the box and the\n'
       'two robots go on it, and\n'
       'it folds away.')

THEN = ('THE STOPWATCH\n\n'
        'Take the number out of the\n'
        'teacher’s box and press\n'
        'SPACE on it: it counts the\n'
        'milliseconds. “.” rests it.\n\n'
        'Open its panel with the\n'
        'gear: the box and the team\n'
        'are there, and the bird on\n'
        'the perch is a bird to the\n'
        'number.')

HOW = ('HOW IT REACHES THEM\n\n'
       'A little robot the teacher\n'
       'taught stays among its\n'
       'things: “the first little\n'
       'robot it taught”, at its own\n'
       'desk, with its box. Click\n'
       'the pupil with an empty\n'
       'claw to pick it up; click\n'
       'the box on its desk to take\n'
       'that.\n\n'
       'One asks and one tells\n'
       'because a robot cannot wait\n'
       'mid-round for an answer.')

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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '\U0001f393 timer-teacher.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))   # noqa: F405
print('wrote', os.path.basename(out))
