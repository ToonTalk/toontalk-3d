# wandering -- a behaviour that goes nowhere in particular.
#
# The Wanderer is handed [a bird to my thing, an across step, an away step,
# a die of three, a -2, a x1/25]. Each round, for each step:
#
#     a copy of the die lands on the step's number   -> 1, 2 or 3
#     a copy of the -2 lands on it                    -> -1, 0 or 1
#     a copy of the x1/25 lands on it                 -> a small step, or none
#     a copy of the step goes to the bird             -> [move | across | dx]
#
# and the same again for away. Nothing here is about wandering: a die
# re-rolls a number, a -2 is added, a x1/25 is multiplied, a message is
# sent -- the same four gestures a child makes by hand. Drop it on an animal
# in the yard and press SPACE, and the animal wanders.
from _beh import *                                          # noqa: F403

WANDER = 'G913'


def wandering(lid=WANDER):
    across = msg('move', 'across', num(1, 30))               # noqa: F405
    away = msg('move', 'away', num(1, 30))                   # noqa: F405
    die = {'kind': 'die', 'faces': 3}
    minus2 = num(-2)                                         # noqa: F405
    small = num(1, 25, '*')                                  # noqa: F405
    work = box(to(lid, 'my thing'), across, away, die, minus2, small)   # noqa: F405
    trained = box(to(lid), across, away, die, minus2, small)            # noqa: F405

    def roll(hole):
        # the die, the -2 and the x1/25 land on the step's number in turn,
        # then a copy of the step goes to the bird
        return [copy('given', 3), put('given', hole, 2),     # noqa: F405
                copy('given', 4), put('given', hole, 2),     # noqa: F405
                copy('given', 5), put('given', hole, 2),     # noqa: F405
                copy('given', hole), put('given', 0)]        # noqa: F405

    bot = robot('Wanderer',                                  # noqa: F405
                box(ANYBIRD, ANYBOX, ANYBOX, {'kind': 'wildDie'}, ANYNUM, ANYNUM),   # noqa: F405
                roll(1) + roll(2), trained_on=trained)
    return gadget('wandering', lid, bot, work)


if __name__ == '__main__':
    STAR = 'L9513'
    star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), STAR)
    g = wandering()
    # laid out in the open, like the other behaviour worlds: the robot and
    # its work box on the table, the bird pointed at the star
    bot = g['panel']['active']
    work = g['panel']['stations']['stand']
    work['holes'][0] = to(STAR, 'my thing')
    bot['trainedOn']['holes'][0] = to(STAR)

    ABOUT = ('WANDERING\n\n'
             '[my thing, across, away,\n'
             ' a die of 3, a -2, a x1/25]\n\n'
             'Each round, on each step:\n'
             '  the die lands on it: 1..3\n'
             '  the -2 lands on it: -1..1\n'
             '  the x1/25 lands on it\n'
             '  a copy goes to the bird\n\n'
             'That is all wandering is.')

    RUN = ('TO RUN IT\n\n'
           'Set Speed to Instant and\n'
           'give the work box to the\n'
           'Wanderer.\n\n'
           'The star drifts about the\n'
           'table, nowhere in\n'
           'particular.\n\n'
           'Hold the die and type 5:\n'
           'it wanders further to the\n'
           'right and down than left\n'
           'and up. Why?')

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

    bench = [
        {'thing': star, 'x': -1.30, 'z': 1.20},
        {'thing': bot, 'x': -1.45, 'z': 1.62},
        {'thing': work, 'x': -0.45, 'z': 1.62},

        {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},        # noqa: F405
        {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},          # noqa: F405
        {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},          # noqa: F405
    ]
    write_beh('wandering', bench)
