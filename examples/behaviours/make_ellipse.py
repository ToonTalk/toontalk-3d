# move in an ellipse -- the thirteenth behaviour, and Stage 6's proof.
#
# Nothing here is about ellipses. It is one robot doing what a child would do
# with a calculator and two boxes:
#
#     across = centre-x + radius-x * sin(angle)
#     away   = centre-z + radius-z * cos(angle)
#     angle  = angle + a step
#
# Every one of those is a BADGED NUMBER dropped on a running total, exactly as
# arithmetic has always been done in the workshop. What Stage 6 adds is the
# two badges in the middle: a number wearing "sin" turns the number it lands
# on into its sine. The answers come back INEXACT and marked, and the ellipse
# is drawn out of approximations -- which is the honest thing, because no
# rational is the sine of thirty degrees except by luck.
#
# ANGLES ARE DEGREES. The step is 6, so a lap is sixty rounds.
from _beh import *                                          # noqa: F403

ELL = 'G913'

# the work box, hole by hole:
#  0 my thing        1 the angle          2 sin badge     3 cos badge
#  4 radius across   5 radius away        6 centre across 7 centre away
#  8 [set|across|_]  9 [set|away|_]      10 the step
angle = num(0)                                               # noqa: F405
sin_b = dict(num(1), op='sin')                               # noqa: F405
cos_b = dict(num(1), op='cos')                               # noqa: F405
rx = dict(num(11, 10), op='*')                               # noqa: F405
rz = dict(num(2, 5), op='*')                                 # noqa: F405
cx = dict(num(0), op='+')                                    # noqa: F405
cz = dict(num(17, 10), op='+')                               # noqa: F405
across_msg = msg('set', 'across', num(0))                    # noqa: F405
away_msg = msg('set', 'away', num(0))                        # noqa: F405
step = dict(num(6), op='+')                                  # noqa: F405

work = box(to(ELL, 'my thing'), angle, sin_b, cos_b,         # noqa: F405
           rx, rz, cx, cz, across_msg, away_msg, step)
trained = box(to(ELL), angle, sin_b, cos_b,                  # noqa: F405
              rx, rz, cx, cz, across_msg, away_msg, step)

cond = box(ANYBIRD, ANYNUM, ANYNUM, ANYNUM, ANYNUM,          # noqa: F405
           ANYNUM, ANYNUM, ANYNUM, ANYBOX, ANYBOX, ANYNUM)


def axis(trig_hole, radius_hole, centre_hole, msg_hole):
    """Build one coordinate on the scratch spot and post it.

    A copy of the angle goes down; the trig badge turns it into a sine or a
    cosine; the radius multiplies it; the centre shifts it. Four drops, and
    the running total is the answer -- there is no expression anywhere, only
    numbers landing on a number.
    """
    return [
        copy('given', 1), put('s0'),                         # noqa: F405
        copy('given', trig_hole), put('s0'),                 # noqa: F405
        copy('given', radius_hole), put('s0'),               # noqa: F405
        copy('given', centre_hole), put('s0'),               # noqa: F405
        # swap the answer into the message and send it
        vac('given', msg_hole, 2),                           # noqa: F405
        take('s0'), put('given', msg_hole, 2),               # noqa: F405
        copy('given', msg_hole), put('given', 0),            # noqa: F405
    ]


program = axis(2, 4, 6, 8) + axis(3, 5, 7, 9) + [
    copy('given', 10), put('given', 1),        # the angle takes its step  # noqa: F405
]

bot = robot('Ellipse', cond, program, trained_on=trained)    # noqa: F405
ellipse = gadget('moving in an ellipse', ELL, bot, work)     # noqa: F405

ABOUT = ('MOVING IN AN ELLIPSE\n\n'
         'across = centre + radius x\n'
         '         sin(angle)\n'
         'away   = centre + radius x\n'
         '         cos(angle)\n'
         'angle  = angle + 6\n\n'
         'Each line is badged numbers\n'
         'dropped on a running total.\n'
         'Nothing knows what an\n'
         'ellipse is.')

WHY = ('WHY IT IS APPROXIMATE\n\n'
       'No fraction IS the sine of\n'
       '6 degrees. A number wearing\n'
       'the sin badge answers to\n'
       'twelve decimal places and\n'
       'MARKS ITSELF with a wavy\n'
       'equals: ~0.104528463268\n\n'
       'Touch an approximation and\n'
       'the answer is one too. That\n'
       'is the only way an exact\n'
       'number ever becomes\n'
       'inexact.')

HOW = ('DEGREES, AND TWELVE PLACES\n\n'
       'Angles are in DEGREES: 360\n'
       'is a full turn, so a step of\n'
       '6 makes a lap in 60 rounds.\n\n'
       'The sine is worked out from\n'
       'a series over fractions, not\n'
       'from the machine\'s own sine.\n'
       'That is slower, and it is\n'
       'the SAME on every machine --\n'
       'so a saved world replays\n'
       'digit for digit.')

star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), 'L9598')   # noqa: F405

bench = [
    {'thing': star, 'x': 0.00, 'z': 1.70},
    {'thing': ellipse, 'x': -1.45, 'z': 1.15},
    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.28},           # noqa: F405
    {'thing': txt(WHY), 'x': -0.75, 'z': 2.28},             # noqa: F405
    {'thing': txt(HOW), 'x': -0.05, 'z': 2.28},             # noqa: F405
]

write_beh('ellipse', bench)
