# wandering -- a behaviour that goes nowhere in particular, in the turtle's
# own words.
#
# The Wanderer is handed [a bird to my thing, a forward step, a turn, a die
# of three, a -2, a x30]. Each round:
#
#     a copy of the die lands on the turn's number   -> 1, 2 or 3
#     a copy of the -2 lands on it                    -> -1, 0 or 1
#     a copy of the x30 lands on it                   -> -30, 0 or 30 degrees
#     a copy of the turn goes to the bird             -> [move | yaw | a]
#     a copy of the step goes to the bird             -> [move | forward | 1/25]
#
# yaw and forward are the 3D turtle's orders (make_turtle3d.py): a turn about
# its own upright, and a step along the way it is pointing -- so an animal
# faces where it goes. Nothing here is about wandering: a die re-rolls a
# number, a -2 is added, a x30 is multiplied, two messages are sent -- the
# same gestures a child makes by hand.
from _beh import *                                          # noqa: F403

WANDER = 'G913'


def wandering(lid=WANDER):
    step = msg('move', 'forward', num(1, 25))                # noqa: F405
    turn = msg('move', 'yaw', num(0))                        # noqa: F405
    die = {'kind': 'die', 'faces': 3}
    minus2 = num(-2)                                         # noqa: F405
    times30 = num(30, 1, '*')                                # noqa: F405
    work = box(step, turn, die, minus2, times30)             # noqa: F405
    trained = box(step, turn, die, minus2, times30)          # noqa: F405
    program = [copy('given', 2), put('given', 1, 2),         # noqa: F405
               copy('given', 3), put('given', 1, 2),         # noqa: F405
               copy('given', 4), put('given', 1, 2),         # noqa: F405
               copy('given', 1), put('perch'),               # noqa: F405
               copy('given', 0), put('perch')]               # noqa: F405
    bot = robot('Wanderer',                                  # noqa: F405
                box(ANYBOX, ANYBOX, {'kind': 'wildDie'}, ANYNUM, ANYNUM),   # noqa: F405
                program, trained_on=trained,
                note='Each round, on the turn’s number: a copy of the die lands (1, 2 or '
                     '3), then the -2 (-1, 0 or 1), then the x30 (-30, 0 or 30 degrees). '
                     'A copy of the turn goes to the bird on the perch, then a copy of the forward '
                     'step: a yaw, then a step the way it faces.')
    return gadget('wandering', lid, bot, work)


if __name__ == '__main__':
    STAR = 'L9513'
    star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), STAR)
    g = wandering()
    # laid out in the open, like the other behaviour worlds: the robot and
    # its work box on the table, and a bird to the star on the perch
    bot = g['panel']['active']
    work = g['panel']['stations']['stand']

    ABOUT = ('WANDERING\n\n'
             '[forward, turn,\n'
             ' a die of 3, a -2, a x30]\n\n'
             'Each round, on the turn:\n'
             '  the die lands on it: 1..3\n'
             '  the -2 lands on it: -1..1\n'
             '  the x30 lands on it\n'
             '  a copy goes to the bird\n'
             'then a copy of forward goes\n'
             'to the bird.\n\n'
             'yaw and forward are the\n'
             'turtle\'s own words.')

    RUN = ('TO RUN IT\n\n'
           'Press SPACE on the star: it\n'
           'drifts about the table,\n'
           'nowhere in particular. "."\n'
           'stops it.\n\n'
           'THE ROBOT IS ON ITS BACK.\nHold the star and press\nCtrl+P (or the gear on the\nholding card) to go through\nits door and watch the\nrobot at work. Escape\ncomes back out.\n\n'
           'In there, hold the die and\n'
           'type 5: it turns right more\n'
           'often than left, and\n'
           'circles. Why?')

    WHY = ('IN THE YARD\n\n'
           'Set the zoo out, carry this\n'
           'pad through the back door,\n'
           'drop it on an animal and\n'
           'press SPACE on the pad.\n\n'
           'The animal wanders. Copy the\n'
           'pad on Mimi for the next one.\n\n'
           'Nothing here is about\n'
           'animals: a die re-rolls a\n'
           'number, and a bird carries\n'
           'a message.')

    # PACKAGED (Ken, 19 Sep): the Wanderer and its box on the star's own panel.
    bench = [
        {'thing': gadget('*', STAR, bot, work, look=dict(bg='#1b2233', ink='#ffd23f', font='sans')), 'x': -1.30, 'z': 1.40},

        {'thing': txt(RUN), 'x': -1.45, 'z': 2.15},          # noqa: F405
        {'thing': txt(WHY), 'x': -0.75, 'z': 2.15},          # noqa: F405
        {'thing': txt(ABOUT), 'x': -0.05, 'z': 2.15},        # noqa: F405
    ]
    write_beh('🦋 wandering', bench)
