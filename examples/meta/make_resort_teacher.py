# -*- coding: utf-8 -*-
# The resort teacher -- a robot solves Resort Infinity in front of you, the
# way you would, and says what it is doing as it goes.
#
# Ken: "I still find infinity resort very confusing - can you make a meta
# example that solves it." And, on the first version: "I have the feeling
# you've made it more complex than it needs to be" -- it was; the resort has
# the original's shape now, and so has this. One robot at the table out in
# the yard, given a ten-hole box:
#
#   0 a pad it reads out first
#   1 a little robot: the clerk to be     2 a practice letter, [7 | bird to the practice nest]
#   3 a little robot: the mover to be     4 another practice letter
#   5 a bird to "the guests"              6 the bird "to the front desk"
#   7 the bird "to the moving office"     8 a bird to "five more guests"
#   9 [set | switch | on], the letter that throws a switch
#
# It gives "the guests" the switch letter (six letters land on the front
# desk's post), teaches the first little robot on a practice letter -- take
# the number, give it to the bird, Ruby erases the number in its thought --
# and gives that robot to the bird "to the front desk": the desk runs it on
# every letter, and six guests walk to their cottages. Then it teaches the
# second on the other letter -- a +5 dropped on the number first -- gives it
# to the bird "to the moving office" (the office rings the bell, every housed
# guest writes where it lives, and the office runs the robot on each: everyone
# moves up five), and gives "five more guests" the switch letter: the
# newcomers take 1 to 5. Nothing waits on anything: the desks do the waiting.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'infinity'))
from _tt import *                                          # noqa: F403
import make_resort as R

WILDTEXT = {'kind': 'wildText'}
ANYROBOT = {'kind': 'anyRobot'}

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}
msg = lambda *words: box(*[txt(w) for w in words])        # noqa: E731,F405


def fresh(bot, note):
    """An untrained little robot with the name of the one it will become."""
    return {'kind': 'robot', 'name': bot['name'], 'program': [], 'condition': None,
            'trainedOn': None, 'team': [], 'note': 'Untrained. ' + note}


RQ, LQ, DQ = '’', '“', '”'
FIRST = txt('Watch. I seat the guests, teach a clerk and give it to the front desk, teach a mover and give it to the moving office, and welcome five more.')   # noqa: F405

given = box(                                               # noqa: F405
    FIRST,
    fresh(R.address_robot, 'The teacher shows it the clerk' + RQ + 's job on a practice letter: the number to the bird.'),
    R.LETTER(7, 'a practice letter'),
    fresh(R.move_robot, 'The teacher shows it the mover' + RQ + 's job on a practice letter: five more on the number, then the number to the bird.'),
    R.LETTER(3, 'a practice letter'),
    live_bird('M1', 'to the guests'),
    bird(*R.ROBOT_NESTS[R.DESK_G], label='to the front desk'),          # noqa: F405
    bird(*R.ROBOT_NESTS[R.OFFICE_G], label='to the moving office'),     # noqa: F405
    live_bird('M2', 'to five more guests'),
    msg('set', 'switch', 'on'))

speak = {'type': 'speak'}
teach = lambda *p: {'type': 'teach', 'at': at('given', *p)}            # noqa: E731,F405
taught = lambda step: {'type': 'taught', 'step': step}                 # noqa: E731
erase = lambda *path: {'type': 'erase', 'path': list(path)}           # noqa: E731
pupil = lambda k: {'type': 'take', 'at': {'c': 't%d' % k, 'path': [], 'bot': True}}   # noqa: E731
switch_on = lambda hole: [copy('given', 9), put('given', hole)]        # noqa: E731,F405


def lesson(k, letter_hole, bot):
    """Teach the little robot in the hole before letter_hole, on that letter,
    the robot's own steps, then Ruby on the number in its thought (the letter
    had ONE number; any will do)."""
    return ([take('given', letter_hole), teach(letter_hole - 1)]       # noqa: F405
            + [taught(st) for st in bot['program']]
            + [taught(erase(0)), {'type': 'endTeach'}])


program = (switch_on(5)                                    # the guests write to the front desk
           + [take('given', 0), speak, put('given', 0)]    # ...while I say what I am doing  # noqa: F405
           + lesson(1, 2, R.address_robot)                 # the clerk, taught on a practice letter
           + [take('t1'), put('given', 2),                 # the letter back in its hole (a desk left aside with a box on it holds the houses still)  # noqa: F405
              pupil(1), put('given', 6)]                   # ...and the clerk given to the front desk: six guests housed  # noqa: F405
           + lesson(2, 4, R.move_robot)                    # the mover, taught on the other letter
           + [take('t2'), put('given', 4),                 # noqa: F405
              pupil(2), put('given', 7)]                   # ...and given to the moving office: everybody moves up five  # noqa: F405
           + switch_on(8))                                 # five more guests: 1 to 5

teacher = robot(                                           # noqa: F405
    'the teacher',
    box(WILDTEXT, ANYROBOT, ANYBOX, ANYROBOT, ANYBOX, ANYBIRD, ANYBIRD, ANYBIRD, ANYBIRD, ANYBOX),   # noqa: F405
    program, trained_on=given,
    note='A robot that solves Resort Infinity: seats the guests, teaches a little robot the '
         'clerk' + RQ + 's job on a practice letter and gives it to the bird to the front desk, teaches '
         'another the mover' + RQ + 's job (+5) and gives it to the bird to the moving office, then '
         'welcomes five more. Nothing here is new: a teaching, Ruby, a robot given to a bird and a '
         'switch thrown by mail are steps like any other.')

ABOUT = ('THE RESORT TEACHER\n\n'
         'A robot that solves Resort\n'
         'Infinity in front of you.\n\n'
         'Give it the ten-hole box:\n'
         'the drop sets it to work.\n'
         'Then watch the grass: the\n'
         'guests write, a clerk is\n'
         'taught and given to the\n'
         'front desk, six walk to\n'
         'their cottages; a mover is\n'
         'taught and given to the\n'
         'moving office, everybody\n'
         'moves up five, and five\n'
         'more take 1 to 5.\n\n'
         'Set the Speed to 4x: a\n'
         'resort takes a while at\n'
         'walking pace.')

WHAT = ('WHAT IT DOES\n\n'
        '1. A switch letter to "the\n'
        'guests": six letters land\n'
        'on the front desk' + RQ + 's post.\n'
        '2. Teaches the first little\n'
        'robot on a practice letter:\n'
        'take the number, give it to\n'
        'the bird. Ruby erases the\n'
        'number in its thought.\n'
        '3. Picks the robot up and\n'
        'gives it to the bird "to the\n'
        'front desk". The desk runs it\n'
        'on every letter.\n'
        '4. Teaches the second on the\n'
        'other letter: a +5 dropped\n'
        'on the number first.\n'
        '5. Gives it to the bird "to\n'
        'the moving office". The\n'
        'office rings the bell, and\n'
        'runs it on every reply.\n'
        '6. A switch letter to "five\n'
        'more guests".')

HOW = ('HOW THE DESKS WORK\n\n'
       'The front desk and the moving\n'
       'office are houses, closed.\n'
       'Inside, a robot waits for a\n'
       'letter on the post and a\n'
       'robot of yours in its box;\n'
       'for each letter it takes a\n'
       'fresh little house, puts the\n'
       'letter and a copy of your\n'
       'robot in it, and sets it\n'
       'down: the house works on its\n'
       'own, like the trucks of the\n'
       'original. Your robot is never\n'
       'used up.\n\n'
       'The little robots the teacher\n'
       'taught stay among its things:\n'
       'click one with an empty claw\n'
       'to pick it up and read what\n'
       'it learned.')

INSIDE = txt('THE RESORT TEACHER\n\n'                      # noqa: F405
             'Everything is out the back\n'
             'door: the cottages, the\n'
             'guests, the teacher at the\n'
             'table.\n\n'
             'Go outside.')

# the grass: the resort's own things, without the practice letters, the
# answers and the pads -- the teacher brings its letters in its box, and IS
# the answer
KEEP_OUT = (R.clerk, R.move_robot)
yard = [e for e in R.bench_yard
        if e['thing'] not in KEEP_OUT
        and not (e['thing'].get('kind') == 'box' and e['thing'].get('label') == 'a practice letter')
        and not (e['thing'].get('kind') == 'text' and not e['thing'].get('gadget')
                 and e['thing']['text'] != R.FENCE)]
yard += [
    {'thing': teacher, 'x': -1.45, 'z': 1.35},
    {'thing': given, 'x': -0.10, 'z': 1.55},
    {'thing': txt(ABOUT), 'x': -1.15, 'z': 2.25},          # noqa: F405
    {'thing': txt(WHAT), 'x': -0.45, 'z': 2.25},           # noqa: F405
    {'thing': txt(HOW), 'x': 0.25, 'z': 2.25},             # noqa: F405
]

world = {'kind': 'world', 'v': 3, 'bench': [{'thing': INSIDE, 'x': -0.2, 'z': 1.6}],
         'stations': {}, 'active': None, 'yard': {'bench': yard}}
out = os.path.join(HERE, '\U0001f393 resort-teacher.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1, ensure_ascii=False))   # noqa: F405
print('wrote', os.path.basename(out))
