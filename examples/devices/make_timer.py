# -*- coding: utf-8 -*-
# A TIMER, BUILT FROM ROBOTS. Ken: "construct something like the timer sensor
# that when turned on updates by sending a message to the computer bird and
# then uses the number API to change its value."
#
# One robot, one thought. Its work box:
#   0 a bird to my number     1 a bird to the computer   2 my nest
#   3 a bird to my nest       4 [query | time | _]        5 [set | value | _]
# The nest starts with a 0 on it. Each round the robot takes the reading off
# the nest, puts it in a [set | value | _] letter and gives that to its number,
# then asks the computer the time again with a bird to its own nest -- so the
# next reading lands, and the next round begins. Switch the pad on and the
# number counts the milliseconds; "." and it stops where it is.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'behaviours'))
from _dev import *                                         # noqa: F403
from _beh import *                                         # noqa: F403

NUM = 'TIMER1'
PAD = 'T901'
MAIL = (9821, 'timer-readings')

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}

work = box(live_bird(NUM, 'my number'),                     # noqa: F405
           live_bird('COMPUTER', 'the computer'),
           nest(*MAIL, label='readings', pile=[num(0)]),    # noqa: F405
           bird(*MAIL, label='to my readings'),             # noqa: F405
           box(txt('query'), txt('time'), None),            # noqa: F405
           box(txt('set'), txt('value'), None))             # noqa: F405

tell = robot(                                               # noqa: F405
    'Tell the time', box(ANYBIRD, ANYBIRD, ANYNUM, ANYBIRD, ANYBOX, ANYBOX),   # noqa: F405
    [copy('given', 5), put('s0'),                           # a [set | value | _] letter  # noqa: F405
     takeTop('given', 2), put('s0', 2),                     # ...with the reading in it  # noqa: F405
     take('s0'), put('given', 0),                           # told to my number  # noqa: F405
     copy('given', 4), put('s1'),                           # [query | time | _]  # noqa: F405
     copy('given', 3), put('s1', 2),                        # ...answered to my readings  # noqa: F405
     take('s1'), put('given', 1)],                          # asked of the computer  # noqa: F405
    trained_on=work,
    note='A reading is on my nest. Puts it in a [set | value | _] letter for my number, then asks the computer the time again, to my own nest -- so there is always a next reading to wait for.')

timer = gadget('timer', PAD, tell, work,                     # noqa: F405
               look=dict(bg='#1f2f3f', ink='#dff3ff', font='sans', h=0.34))
timer['boundTo'] = NUM
timer['note'] = ('A timer built from one robot: it asks the computer the time and tells the number '
                 'it is bound to. SPACE starts it, "." stops it where it is.')

number = {'kind': 'number', 'value': {'n': '0', 'd': '1'}, 'lid': NUM, 'evt': 'evt-' + NUM,
          'label': 'milliseconds'}

about = txt('A TIMER\n\n'                                    # noqa: F405
            'The number counts the\n'
            'milliseconds since the\n'
            'workshop opened, and it is\n'
            'robots doing it: press\n'
            'SPACE on the "timer" pad.\n\n'
            'Open the pad’s panel: one\n'
            'robot asks the computer\n'
            'the time and tells the\n'
            'number the answer, round\n'
            'after round. "." rests it.')

bench = [
    {'thing': number, 'x': 0.0, 'z': 1.55},
    {'thing': timer, 'x': 0.55, 'z': 1.55},
    {'thing': about, 'x': -0.9, 'z': 1.75},
]

if __name__ == '__main__':
    write_devices('⏱️ timer', bench)
