# a turtle in THREE dimensions -- move, yaw, pitch, roll.
#
# The 2D turtle works out its own trigonometry: a heading number, a sin badge,
# a cos badge, and two running totals. That is the whole point of it -- nothing
# built in, and a child can take the lid off and see the sine.
#
# In three dimensions that stops being possible and pretending otherwise would
# be a lie. A turn in space is not an angle you can keep in a hole; it is an
# orientation, and composing two of them is quaternion multiplication, which is
# not something to build out of number badges on a table. So the FRAME is built
# in -- as speed is, as the table's edges are -- and this turtle's robots do
# what robots are good at: hear a word, fill in a number, hand over a message.
#
# The vocabulary is the one every 3D turtle has converged on, borrowed whole
# from aeroplanes, and the reason it is worth borrowing is that half the world
# already half-knows it:
#
#     move n     go n along the way you are pointing
#     yaw a      turn a degrees about your own upright   (2D's "right")
#     pitch a    tilt your nose a degrees up
#     roll a     roll a degrees about your line of travel
#     home       level, facing the far edge, back on the table
#
# All three turns are in the TURTLE'S OWN frame, which is what makes them
# turtle-ish rather than world-ish, and they are one quaternion multiplied and
# renormalised -- not three angles kept side by side. Ninety one-degree yaws
# land on exactly the quaternion of one ninety-degree yaw, so a staircase built
# out of many small turns closes.
from _beh import *                                          # noqa: F403

T3 = 'G918'
ORDERS_GUID = 'turtle3d-orders'
ORDERS_ID = 9801


def orders_nest(top=None):
    """The letterbox. Empty, it puts the whole team to sleep."""
    return {'kind': 'nest', 'id': ORDERS_ID, 'guid': ORDERS_GUID,
            'hasEgg': False, 'label': 'orders',
            'pile': ([top] if top else [])}


# the work box, hole by hole:
#  0 my thing        1 the letterbox
#  2 [move|forward|_]  3 [move|yaw|_]  4 [move|pitch|_]  5 [move|roll|_]
#  6 [set|pen|down]    7 [set|pen|up]  8 step size       9 [set|home|yes]
fwd_msg = msg('move', 'forward', num(0))                     # noqa: F405
yaw_msg = msg('move', 'yaw', num(0))                         # noqa: F405
pitch_msg = msg('move', 'pitch', num(0))                     # noqa: F405
roll_msg = msg('move', 'roll', num(0))                       # noqa: F405
pen_down = msg('set', 'pen', 'down')                         # noqa: F405
pen_up = msg('set', 'pen', 'up')                             # noqa: F405
home_msg = msg('set', 'home', 'yes')                         # noqa: F405
step_size = num(1, 100)                                      # noqa: F405

HOLE_NAMES = ['my thing', 'letterbox', 'the step', 'yaw', 'pitch', 'roll',
              'pen down', 'pen up', 'step size', 'home']

MSG_HOLE = {'forward': 2, 'yaw': 3, 'pitch': 4, 'roll': 5}


def work_box(top=None, mine=True):
    return dict(box(to(T3, 'my thing') if mine else to(T3),   # noqa: F405
                    orders_nest(top), fwd_msg, yaw_msg, pitch_msg, roll_msg,
                    pen_down, pen_up, step_size, home_msg),
                holeLabels=HOLE_NAMES)


work = work_box()
trained = lambda top: work_box(top, mine=False)               # noqa: E731


def cond(word):
    """An order that is a WORD and a NUMBER, lying on the letterbox."""
    return box(ANYBIRD, box(txt(word), ANYNUM),               # noqa: F405
               ANYBOX, ANYBOX, ANYBOX, ANYBOX,                # noqa: F405
               ANYBOX, ANYBOX, ANYNUM, ANYBOX)                # noqa: F405


def word_cond(word):
    """An order that is just a word: pendown, penup, home."""
    return box(ANYBIRD, txt(word),                            # noqa: F405
               ANYBOX, ANYBOX, ANYBOX, ANYBOX,                # noqa: F405
               ANYBOX, ANYBOX, ANYNUM, ANYBOX)                # noqa: F405


def turn_bot(word):
    """Hear a turn, fill its degrees into the message, hand it over. Degrees
    are degrees: nothing scales them, unlike a distance."""
    hole = MSG_HOLE[word]
    return robot(word, cond(word),                            # noqa: F405
                 [takeTop('given', 1), put('s1'),             # noqa: F405
                  copy('s1', 1), put('s0'),                   # noqa: F405
                  vac('given', hole, 2),                      # noqa: F405
                  take('s0'), put('given', hole, 2),          # noqa: F405
                  copy('given', hole), put('given', 0),       # noqa: F405
                  vac('s1')],                                 # noqa: F405
                 trained_on=trained(box(txt(word), num(30))))  # noqa: F405


move_bot = robot(                                             # noqa: F405
    'move', cond('move'),
    [takeTop('given', 1), put('s1'),                          # the order  # noqa: F405
     copy('s1', 1), put('s0'),                                # how far    # noqa: F405
     copy('given', 8), setop('*'), put('s0'),                 # x step size  # noqa: F405
     vac('given', 2, 2),                                      # noqa: F405
     take('s0'), put('given', 2, 2),                          # noqa: F405
     copy('given', 2), put('given', 0),                       # noqa: F405
     vac('s1')],                                              # noqa: F405
    trained_on=trained(box(txt('move'), num(30))))            # noqa: F405


def plain_bot(word, hole):
    """A word with nothing else to it: eat it and send the message."""
    return robot(word, word_cond(word),                       # noqa: F405
                 [takeTop('given', 1), put('s1'), vac('s1'),  # noqa: F405
                  copy('given', hole), put('given', 0)],      # noqa: F405
                 trained_on=trained(txt(word)))               # noqa: F405


team = dict(move_bot)
team['team'] = [turn_bot('yaw'), turn_bot('pitch'), turn_bot('roll'),
                plain_bot('pendown', 6), plain_bot('penup', 7),
                plain_bot('home', 9)]

turtle3d = gadget('a 3D turtle', T3, team, work,              # noqa: F405
                  look=dict(bg='#1b2f42', ink='#9fd8ff', font='sans', h=0.42))

# --- what you post to it ----------------------------------------------------
post = bird(ORDERS_ID, ORDERS_GUID, 'to the turtle')          # noqa: F405
shell = live(pad('\U0001f422', bg='none', font='sans'), 'L9596')   # noqa: F405

mv30 = box(txt('move'), num(30))                              # noqa: F405
mv_back = box(txt('move'), num(-30))                          # noqa: F405
yaw90 = box(txt('yaw'), num(90))                              # noqa: F405
yaw30 = box(txt('yaw'), num(30))                              # noqa: F405
pitch30 = box(txt('pitch'), num(30))                          # noqa: F405
pitch_dn = box(txt('pitch'), num(-30))                        # noqa: F405
roll45 = box(txt('roll'), num(45))                            # noqa: F405
pendown = txt('pendown')                                      # noqa: F405
penup = txt('penup')                                          # noqa: F405
home = txt('home')                                            # noqa: F405
pen_red = msg('set', 'pen', 'red')                            # noqa: F405
pen_thick = msg('set', 'pen', num(3))                         # noqa: F405

ABOUT = ('A TURTLE IN THE AIR\n\n'
         'Five orders:\n\n'
         '  [move  | 30]\n'
         '  [yaw   | 90]\n'
         '  [pitch | 30]\n'
         '  [roll  | 45]\n'
         '  home\n\n'
         'Give one to the bird and\n'
         'she posts it to the\n'
         'letterbox, exactly as the\n'
         'flat turtle works.')

FRAME = ('ITS OWN FRAME\n\n'
         'The three turns are about\n'
         'the TURTLE\'S axes, not the\n'
         'table\'s:\n\n'
         '  yaw   -- its upright\n'
         '  pitch -- nose up\n'
         '  roll  -- its line of\n'
         '           travel\n\n'
         'So pitch 90 then yaw 90 is\n'
         'not yaw 90 then pitch 90 --\n'
         'try both and watch.')

WHY = ('WHY THIS ONE IS BUILT IN\n\n'
       'The flat turtle works out\n'
       'its own sines: a heading, a\n'
       'sin badge, a cos badge.\n'
       'You can lift the lid and\n'
       'see the whole sum.\n\n'
       'A turn in space is not an\n'
       'angle you can keep in a\n'
       'hole -- it is an\n'
       'orientation, and two of\n'
       'them compose by quaternion\n'
       'multiplication. Pretending\n'
       'that could be built from\n'
       'badges would be a lie, so\n'
       'the FRAME is built in and\n'
       'the robots do the rest.')

TRY = ('TRY THIS\n\n'
       'A SPIRAL STAIRCASE:\n'
       '  pendown, then\n'
       '  move 30, yaw 30,\n'
       '  pitch 10 -- over and\n'
       '  over.\n\n'
       'A CUBE\'S CORNER:\n'
       '  move 30, yaw 90,\n'
       '  move 30, pitch 90,\n'
       '  move 30.\n\n'
       'Ninety one-degree yaws\n'
       'land exactly where one\n'
       'ninety-degree yaw does, so\n'
       'a shape made of small\n'
       'turns still closes.')

bench = [
    {'thing': post, 'x': 0.85, 'z': 1.30},
    {'thing': shell, 'x': 0.25, 'z': 1.60},
    # beside the bird, not off in the far corner
    {'thing': turtle3d, 'x': 1.30, 'z': 1.30},

    {'thing': mv30, 'x': -1.48, 'z': 1.62},
    {'thing': mv_back, 'x': -1.08, 'z': 1.62},
    {'thing': yaw90, 'x': -1.48, 'z': 1.98},
    {'thing': yaw30, 'x': -1.08, 'z': 1.98},
    {'thing': pitch30, 'x': -0.68, 'z': 1.62},
    {'thing': pitch_dn, 'x': -0.28, 'z': 1.62},
    {'thing': roll45, 'x': -0.68, 'z': 1.98},
    {'thing': home, 'x': -0.28, 'z': 1.98},

    {'thing': pendown, 'x': -1.48, 'z': 1.38},
    {'thing': penup, 'x': -1.08, 'z': 1.38},
    {'thing': pen_red, 'x': -0.68, 'z': 1.38},
    {'thing': pen_thick, 'x': -0.28, 'z': 1.38},

    {'thing': txt(ABOUT), 'x': -0.10, 'z': 2.32},           # noqa: F405
    {'thing': txt(FRAME), 'x': 0.60, 'z': 2.32},            # noqa: F405
    {'thing': txt(WHY), 'x': 1.30, 'z': 2.32},              # noqa: F405
    {'thing': txt(TRY), 'x': 1.30, 'z': 1.75},              # noqa: F405
]

write_beh('turtle3d', bench)                                  # noqa: F405
