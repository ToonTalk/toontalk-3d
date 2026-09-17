# -*- coding: utf-8 -*-
# A STOPWATCH, BUILT THE WAY A PLAYER WOULD BUILD IT. Ken: "a user enters a
# panel with an untrained robot then the user begins to train that robot on
# the box that was dropped on the panel earlier... the bird on the panel can
# be accessed during the training of the robot... As a team on a panel they
# can implement a composable transferable behavior." And, once it ran: "You
# can turn off the stop watch and edit its value (e.g. to zero) but then
# starting it again resumes its old value. I wonder if an event an object
# can listen for is when it is started."
#
# So: no separate pad, and no bird to the number in the box. The NUMBER's
# own panel holds a box and a team of four, and whoever tells the number
# writes to THE PERCH -- the pedestal beside the desk, where a panel keeps a
# bird to its own thing. SPACE on the number starts it; "." rests it; start
# it again and it goes on from whatever it shows -- set it to 0 first and it
# starts from 0. The box, hole by hole (thirteen: a box of more is drawn
# with its middle elided, and a nest in an elided hole is out of reach):
#   0 a bird to the computer   1 readings (my nest)     2 a bird to my readings
#   3 [query | time | _]       4 [set | value | _]      5 "go"    6 (asked)
#   7 start                    8 (fresh)                9 my switch (a nest)
#   10 my value (a nest)      11 a bird to my value    12 a bird to my switch
# The team, in order:
#   Started    "on" on my switch: takes the word off and puts it in hole 9 as
#              the FRESH mark; sends a copy of the "time" pad to the switch
#              nest by its bird (a thought about an empty nest WAITS, and a
#              waiting leader stops the whole team, so the nest is never left
#              bare -- the next "on" replaces it, a channel keeps only its
#              newest); has Dusty take any stale reading off the nest; puts a
#              "time" pad in hole 6 as the go token, whichever hole the old
#              one was in; forgets the start; and asks the number, by the
#              perch, what it shows -- [query | time | _] with a bird to my
#              value in it, and a number answers any query with its value.
#   Ask        the go token is in hole 6: asks the computer the time, answered
#              to my readings, and moves the token to hole 7.
#   Zero       a reading, the fresh mark and my value have all arrived: the
#              start is reading minus value, so that from now on reading
#              minus start is what the number showed; tells it that, spends
#              the fresh mark, and moves the token back.
#   Tell       a reading is on the nest, the start is known and the token is
#              in hole 7: tells the number reading minus start, token back.
# A pad crossing between two holes is how two robots take turns here -- there
# is no thought that says "an empty nest". The computer's clock is the
# milliseconds since the workshop opened; the start turns it into a stopwatch.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'behaviours'))
from _dev import *                                         # noqa: F403
from _beh import *                                         # noqa: F403

NUM = 'TIMER1'
MAIL = (9821, 'timer-readings')
VALUE = (9822, 'timer-my-value')

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}
switch_nest = lambda lid, nid: {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#switch',   # noqa: E731
                                'hasEgg': False, 'label': 'my switch', 'pile': []}

HOLES = ['the computer', 'readings', 'to my readings', 'ask the time', 'tell a value',
         'go', 'asked', 'start', 'fresh', 'my switch', 'my value', 'to my value', 'to my switch']


def work(lid=NUM, mail=MAIL, value=VALUE, reading=None, asked=False, start=None,
         fresh=False, switch='idle', my_value=None):
    """The box, in the state one of the robots works in."""
    return dict(box(live_bird('COMPUTER', 'the computer'),          # noqa: F405
                    nest(*mail, label='readings', pile=[num(reading)] if reading is not None else []),   # noqa: F405
                    bird(*mail, label='to my readings'),            # noqa: F405
                    box(txt('query'), txt('time'), None),           # noqa: F405
                    box(txt('set'), txt('value'), None),            # noqa: F405
                    None if asked else txt('go'),                   # noqa: F405
                    txt('go') if asked else None,                   # noqa: F405
                    num(start) if start is not None else None,      # noqa: F405
                    txt('on') if fresh else None,                   # noqa: F405
                    dict(switch_nest(lid, 9823), pile=[txt(switch)] if switch else []),   # noqa: F405
                    nest(*value, label='my value', pile=[num(my_value)] if my_value is not None else []),   # noqa: F405
                    bird(*value, label='to my value'),              # noqa: F405
                    bird(9823, 'evt-' + lid + '#switch', label='to my switch')),   # noqa: F405
                holeLabels=HOLES)


ANY = [ANYBIRD, None, ANYBIRD, ANYBOX, ANYBOX, None, None, None, None, None, None, ANYBIRD, ANYBIRD]   # noqa: F405


def cond(**at):
    c = list(ANY)
    for k, v in at.items():
        c[int(k[1:])] = v
    return box(*c)                                             # noqa: F405


vac_top = lambda c, *p: {'type': 'vacuum', 'at': dict(at(c, *p), nest=True)}   # noqa: E731,F405

started = robot(                                               # noqa: F405
    'Started', cond(h9=txt('on')),                             # noqa: F405
    [takeTop('given', 9), put('s0'),                           # "on", off my switch  # noqa: F405
     vac('given', 8), take('s0'), put('given', 8),             # ...is the fresh mark  # noqa: F405
     copy('given', 3, 1), put('given', 12),                    # a "time" pad to my switch: never bare  # noqa: F405
     vac_top('given', 1),                                      # a stale reading, if one landed after the stop
     vac('given', 5), vac('given', 6),                         # the go token, wherever it was  # noqa: F405
     copy('given', 3, 1), put('given', 5),                     # ...is a "time" pad in hole 6 again  # noqa: F405
     vac('given', 7),                                          # the old start goes  # noqa: F405
     copy('given', 3), put('s0'),                              # [query | time | _]  # noqa: F405
     copy('given', 11), put('s0', 2),                          # ...answered to my value  # noqa: F405
     take('s0'), put('perch')],                                # asked of my thing: what does it show?  # noqa: F405
    trained_on=work(switch='on'),
    note='Leads the team. My switch says "on": takes the word off and puts it in hole 9 as the fresh mark, sends a "time" pad to the switch nest so it is never bare (a thought about an empty nest waits, and a waiting leader stops the team), has Dusty take a stale reading if one landed after the stop, puts a fresh go token in hole 6, forgets the old start, and asks the number -- by the bird on the perch -- what it shows now.')

ask = robot(                                                   # noqa: F405
    'Ask the time', cond(h5=WILDTEXT),                         # noqa: F405
    [copy('given', 3), put('s0'),                              # [query | time | _]  # noqa: F405
     copy('given', 2), put('s0', 2),                           # ...answered to my readings  # noqa: F405
     take('s0'), put('given', 0),                              # asked of the computer  # noqa: F405
     take('given', 5), put('given', 6)],                       # the go token crosses over: asked  # noqa: F405
    trained_on=work(),
    note='The go token is in hole 6: asks the computer the time, answered to my readings, and moves the token to hole 7 so it does not ask again until the answer is dealt with.')

zero = robot(                                                  # noqa: F405
    'Zero', cond(h1=ANYNUM, h6=WILDTEXT, h8=WILDTEXT, h10=ANYNUM),   # noqa: F405
    [takeTop('given', 1), put('s0'),                           # the reading  # noqa: F405
     copy('s0'), put('s1'),                                    # ...twice  # noqa: F405
     takeTop('given', 10), setop('-'), put('s1'),              # minus what the number showed: the start  # noqa: F405
     take('s1'), put('given', 7),                              # noqa: F405
     copy('given', 7), setop('-'), put('s0'),                  # reading minus start: what it showed  # noqa: F405
     copy('given', 4), put('s1'),                              # [set | value | _]  # noqa: F405
     take('s0'), put('s1', 2),                                 # noqa: F405
     take('s1'), put('perch'),                                 # told to my thing  # noqa: F405
     vac('given', 8),                                          # the fresh mark is spent  # noqa: F405
     take('given', 6), put('given', 5)],                       # the go token comes back  # noqa: F405
    trained_on=work(reading=5000, asked=True, my_value=3, fresh=True),
    note='A reading, the fresh mark and my value have all arrived: the start is the reading minus the value, so that from now on reading minus start is what the number showed; tells it that, spends the fresh mark, and moves the go token back.')

tell = robot(                                                  # noqa: F405
    'Tell my number', cond(h1=ANYNUM, h6=WILDTEXT, h7=ANYNUM),   # noqa: F405
    [copy('given', 4), put('s0'),                              # [set | value | _]  # noqa: F405
     takeTop('given', 1), put('s0', 2),                        # ...with the reading in it  # noqa: F405
     copy('given', 7), setop('-'), put('s0', 2),               # ...minus the start  # noqa: F405
     take('s0'), put('perch'),                                 # given to the bird on the perch: my thing  # noqa: F405
     take('given', 6), put('given', 5)],                       # the go token comes back: ask again  # noqa: F405
    trained_on=work(reading=5000, asked=True, start=4000),
    note='A reading is on my nest, the start is known and the go token is in hole 7: puts the reading minus the start in a [set | value | _] letter, gives it to the bird on the perch -- the panel\u2019s own thing -- and moves the token back to hole 6, so the asking robot goes again.')

number = {'kind': 'number', 'value': {'n': '0', 'd': '1'}, 'lid': NUM, 'evt': 'evt-' + NUM,
          'label': 'stopwatch',
          'note': ('A stopwatch: four robots on my own panel. One asks the computer the time, one tells '
                   'me the time since the start, and two -- when my switch says "on" -- set the start so I '
                   'go on from whatever I show. SPACE on me starts; "." rests; set me to 0 and start again.'),
          'panel': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {'stand': work()},
                    'active': dict(started, team=[ask, zero, tell])}}

about = txt('A STOPWATCH\n\n'                                # noqa: F405
            'Press SPACE on the number:\n'
            'it counts milliseconds. "."\n'
            'rests it; SPACE again goes\n'
            'on from where it stopped.\n'
            'Set it to 0 (drop a 0 with\n'
            'a set badge) and start it,\n'
            'and it starts from 0.\n\n'
            'Robots are doing it, on the\n'
            'number’s own panel: open it\n'
            'with the gear and see four\n'
            'robots and a box.')

HOW = txt('HOW IT WORKS\n\n'                                 # noqa: F405
          'The computer’s clock is the\n'
          'milliseconds since the\n'
          'workshop opened. Tell shows\n'
          'reading minus a START.\n\n'
          'The number announces its\n'
          'switch: [listen | switch |\n'
          'bird] gives a nest that gets\n'
          '"on" or "off". Started hears\n'
          '"on", forgets the start and\n'
          'asks the number what it\n'
          'shows; Zero sets the start\n'
          'so the count goes on from\n'
          'there. Ask and Tell take\n'
          'turns by the go pad.')

BUILT = txt('BUILT BY HAND\n\n'                              # noqa: F405
            'Open the number’s panel,\n'
            'drop the box on it, then a\n'
            'robot, and go in: the\n'
            'lesson begins. Train it;\n'
            'leave the thought; drop the\n'
            'next robot on the panel for\n'
            'the next lesson. Each joins\n'
            'the team.\n\n'
            'The bird on the perch is a\n'
            'bird to the number, and a\n'
            'letter given to her in a\n'
            'lesson really arrives.')

bench = [
    {'thing': number, 'x': 0.0, 'z': 1.55},
    {'thing': about, 'x': -0.9, 'z': 1.75},
    {'thing': HOW, 'x': 0.9, 'z': 1.75},
    {'thing': BUILT, 'x': 1.5, 'z': 1.35},
]

if __name__ == '__main__':
    write_devices('⏱️ timer', bench)
