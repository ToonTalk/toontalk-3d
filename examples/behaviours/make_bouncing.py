# bouncing -- a team that differs only in which word it expects.
#
# The team is handed [a step, the edge], and writes to the bird on the perch
# -- out here a bird to the star; on a thing's panel, to that thing. The edge is one
# of the workshop's readings: a nest holding exactly one pad, saying which
# edge the thing is against, or "none". A reading rather than an event, so it
# is never empty -- which matters, because a team member facing an empty nest
# DOZES, and a dozing member stops the whole team.
#
# So three robots, in order, and the only difference between them is the word
# they expect in the second hole:
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
        name, box(ANYBOX, txt(word)),                        # noqa: F405
        drop(-1, '*', 'given', 0, 2)                         # noqa: F405
        + [copy('given', 0), put('perch')],
        trained_on=box(step, edge_nest(word)),
        note=('Leads the team. ' if word == 'left' else '')
        + 'The edge reading says “' + word + '”: drops a x-1 on the step’s number '
        'to turn round, then sends the step.')


left = turner('at the left', 'left')
right = turner('at the right', 'right')
mover = robot(
    'moving', box(ANYBOX, WILDTEXT),
    [copy('given', 0), put('perch')],
    trained_on=box(step, edge_nest()),
    note='Any other reading: sends the step. It comes last, so at an edge a turner '
         'gets the turn first.')

team = dict(left)
team['team'] = [right, mover]

work = box(step, edge_nest())

ABOUT = ('BOUNCING\n\n'
         '[a step, the edge]\n\n'
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
       'Press SPACE on the star: it\n'
       'runs to the right edge, turns\n'
       'round, runs back, turns\n'
       'again, and keeps going. "."\n'
       'stops it.\n\n'
       'THE TEAM IS ON ITS BACK. Hold\n'
       'the star and press Ctrl+P (or\n'
       'the gear on the holding card)\n'
       'to go through its door and\n'
       'watch them take turns: the\n'
       'two turners look and step\n'
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
       'here is about bouncing.\n\n'
       'The step goes to the bird on\n'
       'the perch: out here, a bird\n'
       'to the star.')

# PACKAGED (Ken, 19 Sep): the team and its box on the star's own panel.
bench = [
    {'thing': gadget('*', STAR, team, work, look=dict(bg='#1b2233', ink='#ffd23f', font='sans')), 'x': -1.30, 'z': 1.40},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},             # noqa: F405
]

write_beh('🏀 bouncing', bench)
