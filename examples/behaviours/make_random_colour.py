# -*- coding: utf-8 -*-
# 🎨 RANDOM COLOUR (Ken, 19 September 2026): a pad with a robot on its back
# that rolls a die each round and picks a colour from a LIST of colour names
# -- the seven of the rainbow to begin with -- then paints its own paper
# that colour, writes the colour's name on itself, and takes an ink that
# reads against it (white on red and blue, black on yellow and orange).
#
# The list is a box of seven pairs, [name | ink]. Picking the Nth is the
# workshop's own idiom: drop the box on a number and it splits there; the
# rest begins with the one wanted. A die dropped on a number lands as its
# roll, and a -1 makes the roll 0..6, the split point. Add a colour: put
# another pair in the box and give the die a face (hold it and type 8).
#
# Everything the robot does is a letter to its bird -- [set | background |
# name], [set | text | name] (a pad's words are data since 18 Sep), [set |
# colour | ink] -- so the same robot on any pad's back colours THAT pad.
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beh import *                                          # noqa: F403,F401

LID = 'G920'
RAINBOW = [('red', 'white'), ('orange', 'black'), ('yellow', 'black'), ('green', 'white'),
           ('blue', 'white'), ('indigo', 'white'), ('violet', 'white')]


def labelled(holes, labels):
    b = box(*holes)                                          # noqa: F405
    b['holeLabels'] = list(labels)
    return b


def random_colour(lid=LID):
    colours = labelled([labelled([txt(n), txt(i)], ['colour', 'ink']) for n, i in RAINBOW],   # noqa: F405
                       [n for n, _ in RAINBOW])
    die = {'kind': 'die', 'faces': len(RAINBOW)}
    paper = labelled([txt('set'), txt('background'), None], ['action', 'what', 'colour'])       # noqa: F405
    words = labelled([txt('set'), txt('text'), None], ['action', 'what', 'colour'])            # noqa: F405
    ink = labelled([txt('set'), txt('colour'), None], ['action', 'what', 'ink'])               # noqa: F405
    work = labelled([num(0), colours, die, num(-1), paper, words, ink],                        # noqa: F405
                    ['pick', 'colours', 'die', 'one less', 'paper', 'words', 'ink'])
    trained = labelled([num(0), colours, die, num(-1), paper, words, ink],                     # noqa: F405
                       ['pick', 'colours', 'die', 'one less', 'paper', 'words', 'ink'])
    program = [
        # the roll, 0..6: the die lands on pick, then the -1
        copy('given', 2), put('given', 0),                   # noqa: F405
        copy('given', 3), put('given', 0),                   # noqa: F405
        # the Nth pair: a copy of pick on spot 1, a copy of the list dropped on it splits
        # there -- the first N pairs stay on spot 1, the rest go to spot 2
        copy('given', 0), put('s0'),                         # noqa: F405
        copy('given', 1), put('s0'),                         # noqa: F405
        take('s1', 0), put('s2'),                            # noqa: F405   the pair wanted, on spot 3
        # the name into the paper letter and the words letter, the ink into the ink letter
        take('s2', 0), put('given', 4, 2),                   # noqa: F405
        copy('given', 4, 2), put('given', 5, 2),             # noqa: F405
        take('s2', 1), put('given', 6, 2),                   # noqa: F405
        # three letters to the bird on the perch: the pad itself
        copy('given', 4), put('perch'),                      # noqa: F405
        copy('given', 5), put('perch'),                      # noqa: F405
        copy('given', 6), put('perch'),                      # noqa: F405
        # tidy: the split halves, the emptied pair, and the letters' last holes
        vac('s0'), vac('s1'), vac('s2'),                     # noqa: F405
        vac('given', 4, 2), vac('given', 5, 2), vac('given', 6, 2),   # noqa: F405
    ]
    bot = robot('Painter',                                    # noqa: F405
                box(ANYNUM, ANYBOX, {'kind': 'wildDie'}, ANYNUM, ANYBOX, ANYBOX, ANYBOX),   # noqa: F405
                program, trained_on=trained,
                note='Each round: the die lands on pick and a -1 makes it 0 to 6. A copy of pick '
                     'goes on spot 1 and a copy of the colour list is dropped on it, which splits the '
                     'list there; the rest starts with the colour wanted, a [name | ink] pair. The name '
                     'fills the paper and words letters, the ink the ink letter, and all three go to '
                     'the bird on the perch: this pad. Then it tidies up for the next round.')
    return gadget('random colour', lid, bot, work,
                  look=dict(bg='#ffffff', ink='#111111', font='sans', h=0.42))


if __name__ == '__main__':
    ABOUT = ('RANDOM COLOUR\n\n'
             'A pad with a robot on its\n'
             'back. Each round it rolls a\n'
             'die and picks a colour from\n'
             'a LIST -- a box of seven\n'
             '[name | ink] pairs -- then\n'
             'sends itself three letters:\n'
             '  [set | background | name]\n'
             '  [set | text | name]\n'
             '  [set | colour | ink]\n\n'
             'Press SPACE on it. "." stops.')
    HOW = ('PICKING THE Nth\n\n'
           'The die lands on a number\n'
           'as its roll; a -1 makes it\n'
           '0 to 6. A copy of the list\n'
           'dropped on that number\n'
           'SPLITS there, and the rest\n'
           'begins with the colour\n'
           'wanted.\n\n'
           'Hold the pad and press\n'
           'Ctrl+P to watch the robot\n'
           'do it.')
    MORE = ('MORE COLOURS\n\n'
            'Open the panel, take the\n'
            'colour list off the desk,\n'
            'and join another [name |\n'
            'ink] pair on its right edge.\n'
            'Then hold the die and type\n'
            'the new number of faces.\n\n'
            'Any colour the browser\n'
            'knows by name works --\n'
            'try "hotpink", "gold" and\n'
            '"teal".')
    bench = [
        {'thing': random_colour(), 'x': 0.0, 'z': 1.55},
        {'thing': txt(ABOUT), 'x': -1.30, 'z': 2.10},        # noqa: F405
        {'thing': txt(HOW), 'x': -0.55, 'z': 2.10},          # noqa: F405
        {'thing': txt(MORE), 'x': 0.20, 'z': 2.10},          # noqa: F405
    ]
    write_beh('🎨 random-colour', bench)
