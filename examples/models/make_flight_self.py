# The airplane that carries its own pilot.
#
# The first flight (make_flight.py) binds two behaviours to the airplane from
# OUTSIDE -- "a 3D turtle" and "the pilot" lie on the table beside it -- which
# is the right picture for seeing what a behaviour is. This one puts both
# INSIDE the airplane's own panel, so the airplane is a thing that flies: SPACE
# on it starts everything grouped inside it, "." rests them, and you can pick
# it up, copy it, file it on a page or carry it out to the yard with its
# pilot aboard. A copy is a second airplane with a second pilot -- both in one
# copy, since a panel travels with its thing -- and one bird still reaches
# both letterboxes, because a copied nest keeps its name (Ken: "shouldn't the
# copy have kept the bird connection?").
#
# Nothing else changes: the same three orders, the same loop, the same pen.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'behaviours'))
from _beh import *                                          # noqa: F403
import make_flight as F                                     # noqa: E402

PLANE = F.PLANE

# the airplane, with the turtle and the pilot grouped inside its panel: both
# still bound to the airplane, which is what "works on the thing whose panel
# it is in" means
plane = dict(F.plane)
plane['panel'] = {'kind': 'world', 'v': 3, 'stations': {}, 'active': None,
                  'bench': [{'thing': F.turtle, 'x': -0.35, 'z': 1.3},
                            {'thing': F.pilot, 'x': 0.35, 'z': 1.3}]}
plane['note'] = ('An airplane with its pilot aboard: the 3D turtle that gives it move, '
                 'yaw, pitch and roll, and the pilot that speaks them, both inside its '
                 'panel. SPACE on the airplane flies it; "." lands it.')

ABOUT = ('AN AIRPLANE THAT FLIES\n\n'
         'Press SPACE on THE\n'
         'AIRPLANE and it takes off\n'
         'and loops. "." lands it.\n\n'
         'Nothing lies beside it this\n'
         'time: the 3D turtle and the\n'
         'pilot are INSIDE its panel.\n'
         'Hold it and press the gear\n'
         'to see them.\n\n'
         'Its pen is down, so it\n'
         'draws its own flight path.')

COPY = ('COPY IT\n\n'
        'Put the airplane on Mimi:\n'
        'the copy comes with a pilot\n'
        'of its own, because a panel\n'
        'travels with its thing.\n'
        'SPACE on each, and two\n'
        'loops.\n\n'
        'Post [roll | 30] to the bird\n'
        'while both fly and BOTH tilt:\n'
        'a copied letterbox keeps its\n'
        'name, so one bird reaches\n'
        'every airplane that listens.')

def scenery(t):
    return dict(t, ghost=True)


bench = [
    {'thing': plane, 'x': 0.10, 'z': 1.70},
    {'thing': F.post, 'x': 1.30, 'z': 1.28},

    {'thing': F.stride, 'x': -1.44, 'z': 1.28},
    {'thing': F.climb, 'x': -0.94, 'z': 1.28},
    {'thing': F.level, 'x': -0.44, 'z': 1.28},
    {'thing': F.roll_it, 'x': -1.44, 'z': 1.62},
    {'thing': F.home, 'x': -0.94, 'z': 1.62},
    {'thing': F.penup, 'x': -0.44, 'z': 1.62},

    {'thing': scenery(txt(ABOUT)), 'x': -1.45, 'z': 2.30},           # noqa: F405
    {'thing': scenery(txt(COPY)), 'x': -0.75, 'z': 2.30},            # noqa: F405
    {'thing': scenery(txt(F.HOW)), 'x': -0.05, 'z': 2.30},           # noqa: F405
    {'thing': scenery(txt(F.ROUND)), 'x': 0.65, 'z': 2.30},          # noqa: F405
]

write_beh('✈️ airplane-with-pilot', bench, os.path.dirname(os.path.abspath(__file__)))   # noqa: F405
