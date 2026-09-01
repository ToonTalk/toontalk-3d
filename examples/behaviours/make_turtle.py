# a turtle -- and it is NOT built in.
#
# Logo's turtle takes two orders: go FORWARD so far, and turn RIGHT so many
# degrees. Here it is a behaviour like any other, and the whole of it is:
#
#     forward n   ->  across = across + n x sin(heading)
#                     away   = away   + n x cos(heading)
#     right a     ->  heading = heading + a
#
# Every one of those is badged numbers dropped on a running total. What makes
# it possible at all is Stage 6: a number wearing the "sin" badge turns the
# heading it lands on into its sine. Before inexact numbers there was no way
# to face a direction that was not a right angle.
#
# HOW IT HEARS. The turtle keeps a NEST -- its letterbox -- in its work box,
# and its two robots read the top of it. A nest with nothing on it puts a
# robot to sleep, so an idle turtle costs nothing at all; post an order and
# the team wakes, the member whose condition names that word takes the floor,
# and it eats the order it acted on. Dispatching on a word in a box is the
# same thing the arrow-key gadget does with key names and Pong's ball does
# with edges.
#
# Heading 0 points AWAY from you; right turns toward across-positive. So a
# square is: forward, right 90, four times.
from _beh import *                                          # noqa: F403

TURTLE = 'G914'
ORDERS_GUID = 'turtle-orders'
ORDERS_ID = 9701


def orders_nest(top=None):
    """The turtle's letterbox. Empty, it puts the whole team to sleep."""
    return {'kind': 'nest', 'id': ORDERS_ID, 'guid': ORDERS_GUID,
            'hasEgg': False, 'label': 'orders',
            'pile': ([top] if top else [])}


# the work box, hole by hole:
#  0 my thing   1 heading   2 the letterbox   3 sin badge   4 cos badge
#  5 [move|position|[across|away]] -- ONE message, so a step is one straight
#                                     line and not an across-then-away
#                                     staircase
#  6 [set|pen|down]         7 [set|pen|up]        8 step size
#  9 [set|facing|_]  -- the turn made visible: heading 0 points at the far
#                      edge of the table (or of the pad it is riding on)
# Every hole is LABELLED on the box, so opening the panel tells you what each
# one is for without having to work it out from the robots.
heading = num(0)                                             # noqa: F405
sin_b = dict(num(1), op='sin')                               # noqa: F405
cos_b = dict(num(1), op='cos')                               # noqa: F405
step_msg = msg('move', 'position', box(num(0), num(0)))      # noqa: F405
pen_down = msg('set', 'pen', 'down')                         # noqa: F405
pen_up = msg('set', 'pen', 'up')                             # noqa: F405

# ONE HUNDREDTH: the turtle speaks Logo's units, where forward 100 is a good
# stride rather than a hundred table-widths. It lives in the box, in plain
# sight, so the scale is a thing you can pick up and change.
step_size = num(1, 100)                                      # noqa: F405
facing_msg = msg('set', 'facing', num(0))                    # noqa: F405
HOLE_NAMES = ['my thing', 'heading', 'letterbox', 'sine', 'cosine',
              'the step', 'pen down', 'pen up', 'step size', 'facing']

work = dict(box(to(TURTLE, 'my thing'), heading, orders_nest(),   # noqa: F405
                sin_b, cos_b, step_msg,
                pen_down, pen_up, step_size, facing_msg),
            holeLabels=HOLE_NAMES)


def trained(top):
    return dict(box(to(TURTLE), heading, orders_nest(top),   # noqa: F405
                    sin_b, cos_b, step_msg,
                    pen_down, pen_up, step_size, facing_msg),
                holeLabels=HOLE_NAMES)


def cond(word):
    return box(ANYBIRD, ANYNUM,                              # noqa: F405
               box(txt(word), ANYNUM),                       # noqa: F405
               ANYNUM, ANYNUM, ANYBOX,                       # noqa: F405
               ANYBOX, ANYBOX, ANYNUM, ANYBOX)               # noqa: F405


def word_cond(word):
    """An order that is just a WORD on the letterbox: pendown, penup."""
    return box(ANYBIRD, ANYNUM, txt(word),                   # noqa: F405
               ANYNUM, ANYNUM, ANYBOX,                       # noqa: F405
               ANYBOX, ANYBOX, ANYNUM, ANYBOX)               # noqa: F405


def leg(trig_hole, axis):
    """One axis of a step forward: a copy of the heading goes down on the
    scratch spot, the trig badge turns it into a sine or a cosine, and the
    distance -- taken out of the order and told to MULTIPLY -- scales it.
    The answer goes INTO the step message rather than being sent: both axes
    are filled in first, so the thing takes one diagonal step instead of an
    across one and then an away one, which is a staircase and not a line."""
    return [
        copy('given', 1), put('s0'),                         # noqa: F405
        copy('given', trig_hole), put('s0'),                 # noqa: F405
        copy('s1', 1), setop('*'), put('s0'),                # noqa: F405
        copy('given', 8), setop('*'), put('s0'),             # ...times the step size  # noqa: F405
        vac('given', 5, 2, axis),                            # noqa: F405
        take('s0'), put('given', 5, 2, axis),                # noqa: F405
    ]


forward_bot = robot(                                          # noqa: F405
    'forward', cond('forward'),
    [takeTop('given', 2), put('s1')]                          # noqa: F405
    + leg(3, 0) + leg(4, 1)
    + [copy('given', 5), put('given', 0),                     # ONE move  # noqa: F405
       vac('s1')],                                            # noqa: F405
    trained_on=trained(box(txt('forward'), num(30))))      # noqa: F405

right_bot = robot(                                            # noqa: F405
    'right', cond('right'),
    [takeTop('given', 2), put('s1'),                           # the order   # noqa: F405
     copy('s1', 1), setop('+'), put('given', 1),               # heading += n  # noqa: F405
     vac('s1'),                                                # noqa: F405
     # ...and TURN THE THING, so it points where it will walk
     vac('given', 9, 2),                                       # noqa: F405
     copy('given', 1), put('given', 9, 2),                     # noqa: F405
     copy('given', 9), put('given', 0)],                       # noqa: F405
    trained_on=trained(box(txt('right'), num(90))))           # noqa: F405

def pen_bot(word, hole):
    """Eat the word off the letterbox and send the pen message."""
    return robot(word, word_cond(word),                       # noqa: F405
                 [takeTop('given', 2), put('s1'), vac('s1'),  # noqa: F405
                  copy('given', hole), put('given', 0)],      # noqa: F405
                 trained_on=trained(txt(word)))               # noqa: F405


team = dict(forward_bot)
team['team'] = [right_bot, pen_bot('pendown', 6), pen_bot('penup', 7)]

turtle = gadget('a turtle', TURTLE, team, work,               # noqa: F405
                look=dict(bg='#14352a', ink='#8ff0b5', font='sans', h=0.42))

# --- what you post to it ----------------------------------------------------
post = bird(ORDERS_ID, ORDERS_GUID, 'to the turtle')          # noqa: F405
fwd = box(txt('forward'), num(30))                         # noqa: F405
turn = box(txt('right'), num(90))                             # noqa: F405
turn30 = box(txt('right'), num(30))                           # noqa: F405
back = box(txt('forward'), num(-30))                       # noqa: F405
pendown = txt('pendown')                                      # noqa: F405
penup = txt('penup')                                          # noqa: F405
# The pen has a colour and a width, and both are said the ordinary way: give
# one of these to the same bird. They are messages to the TURTLE'S THING, not
# orders on the letterbox, which is worth noticing -- the letterbox takes the
# words the turtle's own robots know, and everything else a thing can answer
# is said straight to it.
pen_red = msg('set', 'pen', 'red')                            # noqa: F405
pen_blue = msg('set', 'pen', 'blue')                          # noqa: F405
pen_thick = msg('set', 'pen', num(4))                         # noqa: F405
pen_thin = msg('set', 'pen', num(1))                          # noqa: F405

shell = live(pad('\U0001f422', bg='none', font='sans'), 'L9597')   # noqa: F405

ABOUT = ('A TURTLE\n\n'
         'It takes two orders:\n\n'
         '  [forward | 30]\n'
         '  [right | 90]\n\n'
         'Give one to the bird and\n'
         'she posts it to the\n'
         'turtle\'s letterbox. The\n'
         'robot whose thought names\n'
         'that word wakes up and\n'
         'does it.')

HOW = ('WHAT FORWARD MEANS\n\n'
       'across = across +\n'
       '         n x sin(heading)\n'
       'away   = away   +\n'
       '         n x cos(heading)\n\n'
       'Heading 0 points AWAY from\n'
       'you. Right turns toward\n'
       'across.\n\n'
       'Nothing here is built in.\n'
       'There is no forward and no\n'
       'right -- only a nest, two\n'
       'robots, and messages the\n'
       'turtle already answered.')

WHY = ('WHY IT NEEDED STAGE 6\n\n'
       'To face a direction that is\n'
       'not a right angle you need\n'
       'a sine. Before inexact\n'
       'numbers there was none, so\n'
       'a turtle could only have\n'
       'turned in quarters.\n\n'
       'A SLEEPING TURTLE COSTS\n'
       'NOTHING: an empty nest puts\n'
       'a robot to sleep, so the\n'
       'team waits for the post\n'
       'rather than spinning.')

PENS = ('THE PEN\n\n'
        'The four boxes on the left\n'
        'of the turtle are the pen\n'
        'itself:\n\n'
        '  [set | pen | red]\n'
        '  [set | pen | blue]\n'
        '  [set | pen | 4]\n'
        '  [set | pen | 1]\n\n'
        'Give one to the bird like\n'
        'anything else. A colour\n'
        'starts a new line; a\n'
        'number is how many\n'
        'ordinary widths wide.\n\n'
        'Wake Dusty and point him\n'
        'at a line to sweep up the\n'
        'whole trail it belongs to.')

TRY = ('TO DRAW A SQUARE\n\n'
       '1. drop the turtle on the\n'
       '   shell and press SPACE\n'
       '2. give the bird "pendown"\n'
       '3. give [forward], then\n'
       '   [right 90] -- four times\n'
       '4. "penup" lifts the chalk\n\n'
       'Copy the orders at Mimi so\n'
       'you do not run out. A robot\n'
       'trained to do all four is a\n'
       'Logo program.')

bench = [
    # the bird stands in FRONT with nothing behind her; the shell has the
    # middle; the orders make one spaced row on the left
    {'thing': post, 'x': 0.85, 'z': 1.30},
    {'thing': shell, 'x': 0.25, 'z': 1.60},
    # beside the bird, not off in the far corner: the working set --
    # behaviour, bird, shell -- reads as one group
    {'thing': turtle, 'x': 1.30, 'z': 1.30},

    {'thing': fwd, 'x': -1.48, 'z': 1.62},
    {'thing': back, 'x': -1.08, 'z': 1.62},
    {'thing': turn, 'x': -1.48, 'z': 1.98},
    {'thing': turn30, 'x': -1.08, 'z': 1.98},
    {'thing': pendown, 'x': -0.65, 'z': 1.62},
    {'thing': penup, 'x': -0.65, 'z': 1.98},

    # ...and what the pen is like, in a row of its own
    {'thing': pen_red, 'x': -1.48, 'z': 1.38},
    {'thing': pen_blue, 'x': -1.08, 'z': 1.38},
    {'thing': pen_thick, 'x': -0.65, 'z': 1.38},
    {'thing': pen_thin, 'x': -0.22, 'z': 1.38},

    {'thing': txt(ABOUT), 'x': -0.10, 'z': 2.32},           # noqa: F405
    {'thing': txt(HOW), 'x': 0.60, 'z': 2.32},              # noqa: F405
    {'thing': txt(WHY), 'x': 1.30, 'z': 2.32},              # noqa: F405
    {'thing': txt(TRY), 'x': 1.30, 'z': 1.75},              # noqa: F405
    {'thing': txt(PENS), 'x': -0.80, 'z': 2.32},            # noqa: F405
]

write_beh('turtle', bench)
