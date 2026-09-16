# -*- coding: utf-8 -*-
# THE COMPUTER NOTEBOOK. Ken: "a bird to the computer... found in the default
# notebook... the first example is to query a timer or the time." A notebook
# whose pages alternate a page of words with a thing to take: the bird to the
# computer, then each letter it answers, ready to copy.
#
# The computer is the workshop's own machine, a thing with a fixed name
# (COMPUTER). It answers three letters, with numbers and boxes:
#   [query | time | bird]   the clock, in milliseconds since the workshop opened
#   [query | date | bird]   a box [year | month | day]
#   [query | clock | bird]  a box [hours | minutes | seconds]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _dev import *                                         # noqa: F403

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}
letter = lambda what: box(txt('query'), txt(what), None)   # noqa: E731,F405

pages = [
    txt('BIRD TO THE COMPUTER\n\n'                          # noqa: F405
        'The next page holds a bird\n'
        'to the workshop’s own\n'
        'machine. Take her off the\n'
        'page and give her one of\n'
        'the letters that follow;\n'
        'the answer comes back to\n'
        'her nest as a number or a\n'
        'box.\n\n'
        'Every letter needs a bird\n'
        'in its last hole to answer\n'
        'to: put one of yours there.'),
    live_bird('COMPUTER', 'to the computer'),
    txt('THE TIME\n\n'                                      # noqa: F405
        '[query | time | bird]\n\n'
        'answers with the clock: the\n'
        'milliseconds since the\n'
        'workshop opened, as one\n'
        'number. A thousand a second.\n\n'
        'Ask twice and take the\n'
        'difference: that is how long\n'
        'something took.'),
    letter('time'),
    txt('THE DATE\n\n'                                      # noqa: F405
        '[query | date | bird]\n\n'
        'answers with a box of three\n'
        'numbers: [year | month | day].\n\n'
        'Take the year out of the\n'
        'first hole and it is a\n'
        'number like any other.'),
    letter('date'),
    txt('THE CLOCK\n\n'                                     # noqa: F405
        '[query | clock | bird]\n\n'
        'answers with a box of three\n'
        'numbers:\n'
        '[hours | minutes | seconds].'),
    letter('clock'),
    txt('A TIMER, FROM ROBOTS\n\n'                          # noqa: F405
        'A number can be TOLD its\n'
        'value: give its bird\n'
        '[set | value | n].\n\n'
        'So a timer is a robot that\n'
        'asks the computer the time,\n'
        'tells its number the answer,\n'
        'and asks again. The world\n'
        'timer.world.json in this\n'
        'folder is that robot, bound\n'
        'to a number on the table.'),
    box(txt('set'), txt('value'), None),                    # noqa: F405
]

notebook = {'kind': 'notebook', 'page': 0, 'pages': pages}

about = txt('THE COMPUTER\n\n'                               # noqa: F405
            'This notebook holds a bird\n'
            'to the workshop’s own\n'
            'machine, and the letters it\n'
            'answers. Point at the\n'
            'notebook and press the left\n'
            'and right arrows to turn\n'
            'its pages; click a page to\n'
            'take a copy of what is on\n'
            'it.')

bench = [
    {'thing': notebook, 'x': 0.0, 'z': 1.75},
    {'thing': about, 'x': -0.9, 'z': 1.75},
    {'thing': nest(9811, 'computer-answers', label='answers'), 'x': 0.9, 'z': 1.75},   # noqa: F405
    {'thing': bird(9811, 'computer-answers', label='to answers'), 'x': 1.3, 'z': 1.75},   # noqa: F405
]

if __name__ == '__main__':
    write_devices('\U0001f5a5️ computer', bench)
