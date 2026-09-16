# -*- coding: utf-8 -*-
# A TIMER, BUILT THE WAY A PLAYER WOULD BUILD IT. Ken: "a user enters a panel
# with an untrained robot then the user begins to train that robot on the box
# that was dropped on the panel earlier... When that robot is run the
# response will arrive and a new robot can be trained to process it. After
# training that robot can be added to the first robot. As a team on a panel
# they can implement a composable transferable behavior."
#
# So: no separate timer pad. The NUMBER's own panel holds a box and a team of
# two, and SPACE on the number starts them; "." rests them.
#   0 a bird to my thing (the panel's own bird)   1 a bird to the computer
#   2 my nest (readings)   3 a bird to my nest    4 [query | time | _]
#   5 [set | value | _]    6 "go"                 7 (asked)
# "Ask the time" runs while the go pad lies in hole 7's neighbour, hole 6:
# it sends the question and moves the pad to hole 7, so it will not ask again
# until the answer is dealt with. "Tell my number" runs when a reading is on
# the nest AND the pad is in hole 7: it tells the number the reading, and
# moves the pad back to hole 6. A pad crossing between two holes is how two
# robots take turns here -- there is no thought that says "an empty nest".
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'behaviours'))
from _dev import *                                         # noqa: F403
from _beh import *                                         # noqa: F403

NUM = 'TIMER1'
MAIL = (9821, 'timer-readings')

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}

work = box(live_bird(NUM, 'my thing'),                      # noqa: F405
           live_bird('COMPUTER', 'the computer'),
           nest(*MAIL, label='readings'),                   # noqa: F405
           bird(*MAIL, label='to my readings'),             # noqa: F405
           box(txt('query'), txt('time'), None),            # noqa: F405
           box(txt('set'), txt('value'), None),             # noqa: F405
           txt('go'), None)                                 # noqa: F405

ask = robot(                                                # noqa: F405
    'Ask the time', box(ANYBIRD, ANYBIRD, None, ANYBIRD, ANYBOX, ANYBOX, WILDTEXT, None),   # noqa: F405
    [copy('given', 4), put('s0'),                           # [query | time | _]  # noqa: F405
     copy('given', 3), put('s0', 2),                        # ...answered to my readings  # noqa: F405
     take('s0'), put('given', 1),                           # asked of the computer  # noqa: F405
     take('given', 6), put('given', 7)],                    # and the go pad crosses over: asked  # noqa: F405
    trained_on=work,
    note='The go pad is in hole 7: asks the computer the time, answered to my readings nest, and moves the pad to hole 8 so it does not ask again until the answer is dealt with.')

tell = robot(                                               # noqa: F405
    'Tell my number', box(ANYBIRD, ANYBIRD, ANYNUM, ANYBIRD, ANYBOX, ANYBOX, None, WILDTEXT),   # noqa: F405
    [copy('given', 5), put('s0'),                           # [set | value | _]  # noqa: F405
     takeTop('given', 2), put('s0', 2),                     # ...with the reading in it  # noqa: F405
     take('s0'), put('given', 0),                           # told to my thing  # noqa: F405
     take('given', 7), put('given', 6)],                    # the go pad comes back: ask again  # noqa: F405
    note='A reading is on my nest and the go pad is in hole 8: tells my thing the reading with [set | value | n], and moves the pad back to hole 7, so the asking robot goes again.')

number = {'kind': 'number', 'value': {'n': '0', 'd': '1'}, 'lid': NUM, 'evt': 'evt-' + NUM,
          'label': 'milliseconds',
          'note': ('A timer: two robots on my own panel. One asks the computer the time, the other '
                   'tells me the answer, and a pad crossing between two holes lets them take turns. '
                   'SPACE on me starts them; "." rests them.'),
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
            'the computer the time, the\n'
            'other tells the number the\n'
            'answer. A pad crossing\n'
            'between two holes lets them\n'
            'take turns.')

HOW = txt('BUILT BY HAND\n\n'                                # noqa: F405
          'Open the number’s panel,\n'
          'drop a box on it, take a\n'
          'bird from the panel’s perch\n'
          'into the box, and a bird to\n'
          'the computer from the\n'
          'devices notebook.\n\n'
          'Drop a robot on the panel\n'
          'and train it: give the\n'
          'computer the question.\n'
          'Start it: the answer lands\n'
          'on the nest. Train a second\n'
          'robot on that, and drop it\n'
          'on the first: a team.')

bench = [
    {'thing': number, 'x': 0.0, 'z': 1.55},
    {'thing': about, 'x': -0.9, 'z': 1.75},
    {'thing': HOW, 'x': 0.9, 'z': 1.75},
]

if __name__ == '__main__':
    write_devices('⏱️ timer', bench)
