# -*- coding: utf-8 -*-
# A TIMER, BUILT THE WAY A PLAYER WOULD BUILD IT. Ken: "a user enters a panel
# with an untrained robot then the user begins to train that robot on the box
# that was dropped on the panel earlier... the bird on the panel can be
# accessed during the training of the robot... When that robot is run the
# response will arrive and a new robot can be trained to process it. After
# training that robot can be added to the first robot. As a team on a panel
# they can implement a composable transferable behavior."
#
# So: no separate timer pad, and no bird to the number in the box. The
# NUMBER's own panel holds a box and a team of two, and the second robot
# writes to THE PERCH -- the pedestal beside the desk, where a panel keeps a
# bird to its own thing. SPACE on the number starts them; "." rests them.
#   0 a bird to the computer   1 my nest (readings)   2 a bird to my nest
#   3 [query | time | _]       4 [set | value | _]     5 "go"    6 (asked)
# "Ask the time" runs while the go pad lies in hole 6: it sends the question
# and moves the pad to hole 7, so it will not ask again until the answer is
# dealt with. "Tell my number" runs when a reading is on the nest AND the
# pad is in hole 7: it puts the reading in a [set | value | _] letter, gives
# the letter to the bird on the perch, and moves the pad back to hole 6. A
# pad crossing between two holes is how two robots take turns here -- there
# is no thought that says "an empty nest".
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'behaviours'))
from _dev import *                                         # noqa: F403
from _beh import *                                         # noqa: F403

NUM = 'TIMER1'
MAIL = (9821, 'timer-readings')

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}

work = box(live_bird('COMPUTER', 'the computer'),           # noqa: F405
           nest(*MAIL, label='readings'),                   # noqa: F405
           bird(*MAIL, label='to my readings'),             # noqa: F405
           box(txt('query'), txt('time'), None),            # noqa: F405
           box(txt('set'), txt('value'), None),             # noqa: F405
           txt('go'), None)                                 # noqa: F405

ask = robot(                                                # noqa: F405
    'Ask the time', box(ANYBIRD, None, ANYBIRD, ANYBOX, ANYBOX, WILDTEXT, None),   # noqa: F405
    [copy('given', 3), put('s0'),                           # [query | time | _]  # noqa: F405
     copy('given', 2), put('s0', 2),                        # ...answered to my readings  # noqa: F405
     take('s0'), put('given', 0),                           # asked of the computer  # noqa: F405
     take('given', 5), put('given', 6)],                    # and the go pad crosses over: asked  # noqa: F405
    trained_on=work,
    note='The go pad is in hole 6: asks the computer the time, answered to my readings nest, and moves the pad to hole 7 so it does not ask again until the answer is dealt with.')

tell = robot(                                               # noqa: F405
    'Tell my number', box(ANYBIRD, ANYNUM, ANYBIRD, ANYBOX, ANYBOX, None, WILDTEXT),   # noqa: F405
    [copy('given', 4), put('s0'),                           # [set | value | _]  # noqa: F405
     takeTop('given', 1), put('s0', 2),                     # ...with the reading in it  # noqa: F405
     take('s0'), put('perch'),                              # given to the bird on the perch: my thing  # noqa: F405
     take('given', 6), put('given', 5)],                    # the go pad comes back: ask again  # noqa: F405
    note='A reading is on my nest and the go pad is in hole 7: puts the reading in a [set | value | _] letter, gives it to the bird on the perch -- the panel’s own thing -- and moves the pad back to hole 6, so the asking robot goes again.')

number = {'kind': 'number', 'value': {'n': '0', 'd': '1'}, 'lid': NUM, 'evt': 'evt-' + NUM,
          'label': 'milliseconds',
          'note': ('A timer: two robots on my own panel. One asks the computer the time, the other '
                   'gives the answer to the bird on the perch, which is a bird to me, and a pad crossing '
                   'between two holes lets them take turns. SPACE on me starts them; "." rests them.'),
          'panel': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {'stand': work},
                    'active': dict(ask, team=[tell])}}

about = txt('A TIMER\n\n'                                    # noqa: F405
            'Press SPACE on the number:\n'
            'it counts the milliseconds\n'
            'since the workshop opened.\n'
            '"." rests it.\n\n'
            'Robots are doing it, on the\n'
            'number’s own panel: open it\n'
            'with the gear and see two\n'
            'robots and a box. One asks\n'
            'the computer the time; the\n'
            'other gives the answer to\n'
            'the bird on the PERCH, the\n'
            'pedestal beside the desk.\n'
            'On a panel that bird goes\n'
            'to the panel’s own thing.')

HOW = txt('BUILT BY HAND\n\n'                                # noqa: F405
          'Open the number’s panel and\n'
          'drop a box on it, with a\n'
          'bird to the computer from\n'
          'the devices notebook.\n\n'
          'Drop a robot on the panel\n'
          'and train it: give the\n'
          'computer the question.\n'
          'Start it: the answer lands\n'
          'on the nest. Train a second\n'
          'robot on that: put the\n'
          'reading in [set | value | _]\n'
          'and give it to the bird on\n'
          'the perch. Drop it on the\n'
          'first robot: a team.')

TRY = txt('TRY IT ANYWHERE\n\n'                              # noqa: F405
          'A robot that writes to the\n'
          'perch works on whatever the\n'
          'panel it is on belongs to.\n\n'
          'To try one on the bench, set\n'
          'any bird on the perch first:\n'
          'its letters go to her.')

bench = [
    {'thing': number, 'x': 0.0, 'z': 1.55},
    {'thing': about, 'x': -0.9, 'z': 1.75},
    {'thing': HOW, 'x': 0.9, 'z': 1.75},
    {'thing': TRY, 'x': 1.4, 'z': 1.4},
]

if __name__ == '__main__':
    write_devices('⏱️ timer', bench)
