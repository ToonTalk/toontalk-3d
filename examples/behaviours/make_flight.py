# The airplane takes off, flies, and loops -- and draws its own flight path.
#
# The whole trick is that a LOOP needs no counting. A constant pitch and a
# constant move IS a loop: turn the same few degrees every stride and the
# path closes into a circle. So the pilot has no counter, no phases and no
# comparisons -- its round is three orders, always the same three:
#
#     move 10, move 10, pitch 30
#
# Two strides for every thirty degrees, so the arc is wide: the plane runs
# along the table, lifts, climbs away, arcs over the top and comes round --
# a takeoff and then a loop, out of one repeated round. Twelve rounds is
# three hundred and sixty degrees.
#
# TWO behaviours are bound to the same airplane, which is the point worth
# noticing: "a 3D turtle" gives it the vocabulary (move, yaw, pitch, roll),
# and "the pilot" is what speaks that vocabulary. SPACE on the airplane
# starts both, because everything bound to a thing starts as one.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'models'))
from _beh import *                                          # noqa: F403
import make_turtle3d as T3                                  # noqa: E402
from make_models import airplane as PLANE_PARTS             # noqa: E402
import json                                                 # noqa: E402

PLANE = 'A901'
PILOT = 'A903'
TURTLE = 'A902'


def rebound(gadget_spec, own_lid, target_lid, fresh_lid):
    """The same rename a drop performs: every reference to the gadget's own
    name becomes the target's, and the gadget takes a fresh name."""
    j = json.dumps(gadget_spec).replace(own_lid, target_lid)
    g = json.loads(j)
    g['lid'] = fresh_lid
    g['evt'] = 'evt-' + fresh_lid
    g['boundTo'] = target_lid
    return g


# --- the airplane, with its pen already down --------------------------------
plane = {'kind': 'model', 'parts': PLANE_PARTS, 'label': 'the airplane',
         'lid': PLANE, 'evt': 'evt-' + PLANE,
         'pen': True, 'penInk': 0xb8241a, 'penWide': 2}

# --- the vocabulary: the 3D turtle, bound to the airplane --------------------
turtle = rebound(T3.turtle3d, T3.T3, PLANE, TURTLE)

# --- the pilot: one round, three orders, for ever ----------------------------
#  0 the bird to the letterbox   1 [move | 10]   2 [pitch | 30]
pilot_work = box(bird(T3.ORDERS_ID, T3.ORDERS_GUID, 'to the airplane'),   # noqa: F405
                 box(txt('move'), num(10)),                  # noqa: F405
                 box(txt('pitch'), num(30)))                 # noqa: F405
pilot_bot = robot(                                           # noqa: F405
    'the pilot', box(ANYBIRD, ANYBOX, ANYBOX),               # noqa: F405
    [copy('given', 1), put('given', 0),      # a stride              # noqa: F405
     copy('given', 1), put('given', 0),      # and another           # noqa: F405
     copy('given', 2), put('given', 0)],     # then nose up a little # noqa: F405
    trained_on=box(bird(T3.ORDERS_ID, T3.ORDERS_GUID),       # noqa: F405
                   box(txt('move'), num(10)),                # noqa: F405
                   box(txt('pitch'), num(30))))              # noqa: F405
pilot = dict(gadget('the pilot', PILOT, pilot_bot, pilot_work,   # noqa: F405
                    look=dict(bg='#3a2340', ink='#ffd9a0', font='sans', h=0.42)),
             boundTo=PLANE)

# --- what a person can post by hand -----------------------------------------
level = box(txt('pitch'), num(-30))                          # noqa: F405
climb = box(txt('pitch'), num(30))                           # noqa: F405
stride = box(txt('move'), num(10))                           # noqa: F405
roll_it = box(txt('roll'), num(30))                          # noqa: F405
home = txt('home')                                           # noqa: F405
penup = txt('penup')                                         # noqa: F405
post = bird(T3.ORDERS_ID, T3.ORDERS_GUID, 'to the airplane')  # noqa: F405

ABOUT = ('TAKE OFF AND LOOP\n\n'
         'Press SPACE on THE\n'
         'AIRPLANE. Two behaviours\n'
         'are bound to it and both\n'
         'start at once:\n\n'
         '  a 3D turtle -- which\n'
         '    gives it move, yaw,\n'
         '    pitch and roll\n'
         '  the pilot -- which\n'
         '    speaks them\n\n'
         '"." lands it. Its pen is\n'
         'down, so it draws its own\n'
         'flight path as it goes.')

HOW = ('A LOOP NEEDS NO COUNTING\n\n'
       'The pilot\'s whole round is\n'
       'three orders, always the\n'
       'same three:\n\n'
       '  move 10\n'
       '  move 10\n'
       '  pitch 30\n\n'
       'Turn the same few degrees\n'
       'every stride and the path\n'
       'closes into a circle. Two\n'
       'strides per turn makes the\n'
       'arc wide, so it runs, lifts,\n'
       'climbs, and comes over the\n'
       'top. Twelve rounds is a\n'
       'full 360.')

TRY = ('TRY THIS\n\n'
       'Open the pilot\'s panel and\n'
       'change 30 to 45: a tighter\n'
       'loop. Change it to 0 and it\n'
       'flies straight until the\n'
       'table runs out.\n\n'
       'Post [roll | 30] to the bird\n'
       'while it loops and the loop\n'
       'tilts -- roll turns about\n'
       'the line of travel, so it\n'
       'changes the PLANE the loop\n'
       'is drawn in.\n\n'
       '"home" puts it back on the\n'
       'table, level and facing the\n'
       'far edge.')

def scenery(t):
    """Not solid: a loop passes THROUGH the cards rather than bumping them."""
    return dict(t, ghost=True)


bench = [
    # MID-TABLE, because the loop is a circle standing on its start: it
    # spans a radius (0.38) in front of the plane and a radius behind it,
    # and from the near edge the back quarter would be clipped by the wall.
    {'thing': plane, 'x': 0.10, 'z': 1.70},
    {'thing': post, 'x': 0.95, 'z': 1.28},
    {'thing': turtle, 'x': 1.42, 'z': 1.28},
    {'thing': pilot, 'x': 1.42, 'z': 1.62},

    {'thing': stride, 'x': -1.45, 'z': 1.28},
    {'thing': climb, 'x': -1.05, 'z': 1.28},
    {'thing': level, 'x': -0.65, 'z': 1.28},
    {'thing': roll_it, 'x': -1.45, 'z': 1.62},
    {'thing': home, 'x': -1.05, 'z': 1.62},
    {'thing': penup, 'x': -0.65, 'z': 1.62},

    {'thing': scenery(txt(ABOUT)), 'x': -0.75, 'z': 2.30},           # noqa: F405
    {'thing': scenery(txt(HOW)), 'x': -0.05, 'z': 2.30},             # noqa: F405
    {'thing': scenery(txt(TRY)), 'x': 0.65, 'z': 2.30},              # noqa: F405
]

write_beh('airplane-flight', bench)                          # noqa: F405
