# bouncing -- a team that differs only in which word it expects.
#
# The star is handed [a bird to my thing, a step, the edge]. The edge is one
# of the workshop's readings: a nest holding exactly one pad, saying which
# edge the thing is against, or "none". A reading rather than an event, so it
# is never empty -- which matters, because a team member facing an empty nest
# DOZES, and a dozing member stops the whole team.
#
# So three robots, in order, and the only difference between them is the word
# they expect in the third hole:
#
#     at the left   flip the step, then move
#     at the right  flip the step, then move
#     anywhere      move
#
# Flipping is not a special operation: it is a x-1 dropped on the number in
# the step box, exactly as you would drop one by hand.
from _beh import *                                          # noqa: F403

STAR = 'L9511'
EDGE = 9512

star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), STAR)
step = msg('move', 'across', num(1, 40))                     # noqa: F405


def edge_nest(reading='none'):
    return {'kind': 'nest', 'id': EDGE, 'guid': 'evt-' + STAR + '#edge',
            'hasEgg': False, 'label': 'edge',
            'pile': [txt(reading)]}                          # noqa: F405


def turner(name, word):
    """Flip the step, then move: the step's number takes a x-1."""
    return robot(
        name, box(ANYBIRD, ANYBOX, txt(word)),               # noqa: F405
        drop(-1, '*', 'given', 1, 2)                         # noqa: F405
        + [copy('given', 1), put('given', 0)],
        trained_on=box(to(STAR), step, edge_nest(word)))


left = turner('at the left', 'left')
right = turner('at the right', 'right')
mover = robot(
    'moving', box(ANYBIRD, ANYBOX, WILDTEXT),
    [copy('given', 1), put('given', 0)],
    trained_on=box(to(STAR), step, edge_nest()))

team = dict(left)
team['team'] = [right, mover]

work = box(to(STAR, 'my thing'), step, edge_nest())

ABOUT = ('BOUNCING\n\n'
         '[my thing, a step, the edge]\n\n'
         'The edge is a READING: one\n'
         'pad saying which edge the\n'
         'star is against, or "none".\n\n'
         'Three robots, in order,\n'
         'differing only in the word\n'
         'they expect:\n\n'
         '  left    flip, then move\n'
         '  right   flip, then move\n'
         '  any     move')

RUN = ('TO RUN IT\n\n'
       'Set Speed to 8x and give the\n'
       'work box to the team leader.\n'
       'It runs until you take the\n'
       'box back or press Pause.\n\n'
       'The star runs to the right\n'
       'edge, turns round, runs back,\n'
       'turns again, and keeps going.\n\n'
       'Watch the team take turns:\n'
       'the two turners look and step\n'
       'aside all the way across, and\n'
       'take the floor at the edge.')

WHY = ('WHY A READING\n\n'
       'An event would leave the nest\n'
       'empty most of the time -- and\n'
       'a team member facing a bare\n'
       'nest dozes, which stops the\n'
       'whole team, including the one\n'
       'doing the moving.\n\n'
       'A reading is never empty, so\n'
       'every member can be decided\n'
       'every round.\n\n'
       'Flipping the step is a x-1\n'
       'dropped on a number. Nothing\n'
       'here is about bouncing.')

bench = [
    {'thing': star, 'x': -1.30, 'z': 1.20},
    {'thing': team, 'x': -1.45, 'z': 1.62},
    {'thing': work, 'x': -0.45, 'z': 1.62},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},             # noqa: F405
]

write_beh('bouncing', bench)
