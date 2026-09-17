# -*- coding: utf-8 -*-
# The resort teacher -- a robot solves Resort Infinity in front of you, the
# way you would, and says what it is doing as it goes.
#
# Ken: "I still find infinity resort very confusing - can you make a meta
# example that solves it." So here is the whole of it done by one robot at
# the table out in the yard, given a thirteen-hole box:
#
#   0 a pad it reads out first
#   1 a little robot: the clerk to be     2 the desk (a box with the post in it)
#   3 a little robot: the mover to be     4 the office desk (a box with the office post)
#   5 a bird to "the guests"              6 a bird to "ring the bell"
#   7 a bird to "five more guests"        8 [set | switch | on], the letter that throws a switch
#   9 a pad, "the front desk"            10 a bird to it
#  11 a pad, "the moving office"         12 a bird to it
#
# It gives "the guests" the switch letter (six letters land on the post),
# teaches the first little robot on the desk -- take the letter off the post,
# copy the number, give the copy to the bird, Dusty takes the empty letter,
# Ruby erases the number in its thought -- and puts the desk and the clerk on
# the front desk pad's panel and switches that on: six guests walk to their
# cottages. Then it rings the bell (every housed guest writes [where I live |
# bird] to the office post), teaches the second little robot on the office
# desk -- the same, with a +5 dropped on the number first -- puts them on the
# moving office pad's panel, switches it on (everybody moves up five), and
# gives "five more guests" the switch letter: the newcomers take 1 to 5.
#
# Nothing here is new. The two lessons are the very robots of
# infinity/make_resort.py, taught step by step; a pad's panel is where a
# robot works when the bench is taken (the teacher is standing there); and a
# switch is thrown by mail. The little robots it taught stay among its
# things, so you can pick them up and look at what they learned.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'infinity'))
from _tt import *                                          # noqa: F403
import make_resort as R

WILDTEXT = {'kind': 'wildText'}
ANYROBOT = {'kind': 'anyRobot'}
FD, MO = 'FD1', 'MO1'

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}
msg = lambda *words: box(*[txt(w) for w in words])        # noqa: E731,F405


def fresh(bot, note):
    """An untrained little robot with the name of the one it will become."""
    return {'kind': 'robot', 'name': bot['name'], 'program': [], 'condition': None,
            'trainedOn': None, 'team': [], 'note': 'Untrained. ' + note}


def sign(text, lid):
    return {'kind': 'text', 'text': text, 'lid': lid, 'evt': 'evt-' + lid,
            'look': {'bg': '#2b3a4a', 'ink': '#e8f0ff', 'font': 'sans', 'h': 0.42},
            'note': 'A pad with a panel: the robot the teacher puts on its panel works there, on the box it puts with it.'}


RQ, LQ, DQ = '’', '“', '”'
FIRST = txt('Watch. I seat the guests, teach a clerk, ring the bell, teach a mover, and welcome five more.')   # noqa: F405

given = box(                                               # noqa: F405
    FIRST,
    fresh(R.address_robot, 'The teacher shows it the clerk' + RQ + 's job on the desk: the letter off the post, a copy of its number to its bird.'),
    R.DESK(),
    fresh(R.move_robot, 'The teacher shows it the mover' + RQ + 's job on the office desk: the letter off the post, five more on its number, the number to its bird.'),
    R.OFFICE(),
    live_bird('M1', 'to the guests'),
    live_bird('BELL1', 'to the bell'),
    live_bird('M2', 'to five more guests'),
    msg('set', 'switch', 'on'),
    sign('the front desk', FD),
    live_bird(FD, 'to the front desk'),
    sign('the moving office', MO),
    live_bird(MO, 'to the moving office'))

speak = {'type': 'speak'}
teach = lambda *p: {'type': 'teach', 'at': at('given', *p)}            # noqa: E731,F405
taught = lambda step: {'type': 'taught', 'step': step}                 # noqa: E731
erase = lambda *path: {'type': 'erase', 'path': list(path)}           # noqa: E731
fold = lambda c: {'type': 'fold', 'at': at(c)}                         # noqa: E731,F405
pupil = lambda k: {'type': 'take', 'at': {'c': 't%d' % k, 'path': [], 'bot': True}}   # noqa: E731
switch_on = lambda hole: [copy('given', 8), put('given', hole)]        # noqa: E731,F405
ground = lambda x, z: {'type': 'put', 'at': {'c': 'ground', 'path': [], 'spot': {'x': x, 'z': z}}}   # noqa: E731


def lesson(k, box_hole, bot):
    """Teach the little robot in the hole before box_hole, on the box in
    box_hole, the robot's own steps, then Ruby on the number in its thought
    (the letter on top of the post had ONE number; any will do). k counts
    the pupils THIS robot taught: each of the team teaches its first."""
    return ([take('given', box_hole), teach(box_hole - 1)]             # noqa: F405
            + [taught(st) for st in bot['program']]
            + [taught(erase(0, 0)), {'type': 'endTeach'}])


def to_work(k, sign_hole, bird_hole, x, z):
    """The sign's panel out onto a work spot, the pupil's box and the pupil on
    it, the panel folded away, the sign set down on the grass (a pad in a
    hole is out of play: its panel gets no turn) and switched on by its
    bird."""
    return ([take('given', sign_hole), {'type': 'panel'}, put('given', sign_hole),   # noqa: F405
             take('t%d' % k), put('s0'), pupil(k), put('s0'), fold('s0'),            # noqa: F405
             take('given', sign_hole), ground(x, z)]                                 # noqa: F405
            + switch_on(bird_hole))


# THREE ROBOTS, BECAUSE A ROBOT CANNOT WAIT MID-ROUND. A lesson takes a letter
# off a post, and the letters take a moment to fly: the guests must have
# written before the clerk's lesson, and the bell must have been answered
# before the mover's. A thought about a post is what waits for that -- a robot
# whose thought wants a letter on the post dozes until one lands, and its team
# with it. So the teacher is a team of three, each taking a turn its
# predecessor makes possible and then makes impossible for itself:
#
#   Seat the guests   hole 0 holds the pad: switch "the guests" on, read the
#                     pad, and Dusty takes it (never again)
#   Teach the clerk   hole 1 holds a little robot and a letter lies on the
#                     desk's post: the lesson, the front desk, the bell (the
#                     pupil leaves hole 1: never again)
#   Teach the mover   hole 3 holds a little robot and a letter lies on the
#                     office post: the lesson, the moving office, five more
LETTER_ON = box(box(ANYNUM, ANYBIRD))                      # a post with a [number | bird] letter on top  # noqa: F405


def cond(**at):
    c = [None] * 13                                        # a hole never looked in: anything, or nothing
    for k, v in at.items():
        c[int(k[1:])] = v
    return box(*c)                                         # noqa: F405


seat = robot(                                              # noqa: F405
    'Seat the guests', cond(h0=WILDTEXT),
    switch_on(5)                                           # the guests write to the post
    + [take('given', 0), speak, put('given', 0), vac('given', 0)],   # ...while I say what I am doing  # noqa: F405
    trained_on=given,
    note='First of the teacher' + RQ + 's team: gives "the guests" the switch letter, so six letters land on the post in the desk, reads the pad out and has Dusty take it, so this turn is never taken again.')

clerking = robot(                                          # noqa: F405
    'Teach the clerk', cond(h1=ANYROBOT, h2=LETTER_ON, h9=WILDTEXT),
    lesson(1, 2, R.address_robot)                          # the clerk, taught on the desk
    + to_work(1, 9, 10, -4.3, 3.4)                         # ...and put to work by the desk: six guests housed
    + switch_on(6),                                        # the bell: everybody asks where to move
    trained_on=given,
    note='Second of the team, once a letter lies on the post: teaches the little robot in hole 1 the clerk' + RQ + 's job on the desk, puts the desk and the clerk on the front desk pad' + RQ + 's panel, switches it on, and rings the bell.')

moving = robot(                                            # noqa: F405
    'Teach the mover', cond(h3=ANYROBOT, h4=LETTER_ON, h11=WILDTEXT),
    lesson(1, 4, R.move_robot)                             # the mover, taught on the office desk (ITS first pupil)
    + to_work(1, 11, 12, -2.9, 3.3)                        # ...and put to work: everybody moves up five
    + switch_on(7),                                        # five more guests: 1 to 5
    trained_on=given,
    note='Third of the team, once a housed guest' + RQ + 's letter lies on the office post: teaches the little robot in hole 3 the mover' + RQ + 's job (+5) on the office desk, puts them on the moving office pad' + RQ + 's panel, switches it on, and welcomes five more guests.')

teacher = dict(seat, name='the teacher', team=[clerking, moving],
               note='A team of three that solves Resort Infinity: seats the guests; teaches a little robot the '
                    'clerk' + RQ + 's job on the desk and puts it to work on a pad' + RQ + 's panel; rings the bell, '
                    'teaches another the mover' + RQ + 's job (+5) on the office desk and puts that to work too, '
                    'then welcomes five more. Three robots because a lesson takes a letter off a post, and a '
                    'thought about a post is what waits for the letter to land. Nothing here is new: a teaching, '
                    'Dusty, Ruby, a panel and a switch thrown by mail are steps like any other.')

ABOUT = ('THE RESORT TEACHER\n\n'
         'A robot that solves Resort\n'
         'Infinity in front of you.\n\n'
         'Give it the thirteen-hole\n'
         'box and press Start. Then\n'
         'watch the grass: the guests\n'
         'write, a clerk is taught,\n'
         'six walk to their cottages;\n'
         'the bell rings, a mover is\n'
         'taught, everybody moves up\n'
         'five, and five more take\n'
         '1 to 5.\n\n'
         'Set the Speed to 4x: a\n'
         'resort takes a while at\n'
         'walking pace.')

WHAT = ('WHAT IT DOES\n\n'
        '1. A switch letter to "the\n'
        'guests": six letters land\n'
        'on the post in the desk.\n'
        '2. Teaches the first little\n'
        'robot on the desk: take the\n'
        'letter, copy the number,\n'
        'give the copy to the bird,\n'
        'Dusty, Ruby.\n'
        '3. Desk and clerk onto the\n'
        'front desk pad' + RQ + 's panel, and\n'
        'a switch letter to the pad.\n'
        '4. A switch letter to the\n'
        'bell: everybody asks the\n'
        'office where to move.\n'
        '5. Teaches the second on the\n'
        'office desk: the same, with\n'
        '+5 dropped on the number.\n'
        '6. Onto the moving office\n'
        'pad' + RQ + 's panel; switched on.\n'
        '7. A switch letter to "five\n'
        'more guests".')

WHY = ('WHY A PANEL, AND WHY THREE\n\n'
       'One robot works at the\n'
       'bench, and the teacher is\n'
       'standing there. A pad' + RQ + 's\n'
       'panel is a bench of its own:\n'
       'a box and a robot put on it\n'
       'work there once the pad is\n'
       'switched on, and a switch is\n'
       'thrown by mail, [set |\n'
       'switch | on] given to a bird\n'
       'to the pad.\n\n'
       'Three robots, because a\n'
       'lesson takes a letter off a\n'
       'post and letters take a\n'
       'moment to fly: a thought\n'
       'about a post waits for one.\n\n'
       'The little robots it taught\n'
       'stay among its things: click\n'
       'one with an empty claw to\n'
       'pick it up and read what it\n'
       'learned.')

INSIDE = txt('THE RESORT TEACHER\n\n'                      # noqa: F405
             'Everything is out the back\n'
             'door: the cottages, the\n'
             'guests, the teacher at the\n'
             'table.\n\n'
             'Go outside.')

# the grass: the resort's own things, without the desk, the office and the
# answers -- the teacher brings the desks in its box, and IS the answer
KEEP_OUT = (R.office, R.clerk, R.move_robot)
yard = [e for e in R.bench_yard
        if e['thing'] not in KEEP_OUT and e['thing'].get('kind') != 'box'
        and not (e['thing'].get('kind') == 'text' and not e['thing'].get('gadget')
                 and e['thing']['text'] != R.FENCE)]
yard += [
    {'thing': teacher, 'x': -1.45, 'z': 1.35},
    {'thing': given, 'x': -0.10, 'z': 1.55},
    {'thing': txt(ABOUT), 'x': -1.15, 'z': 2.25},          # noqa: F405
    {'thing': txt(WHAT), 'x': -0.45, 'z': 2.25},           # noqa: F405
    {'thing': txt(WHY), 'x': 0.25, 'z': 2.25},             # noqa: F405
]

world = {'kind': 'world', 'v': 3, 'bench': [{'thing': INSIDE, 'x': -0.2, 'z': 1.6}],
         'stations': {}, 'active': None, 'yard': {'bench': yard}}
out = os.path.join(HERE, '\U0001f393 resort-teacher.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1, ensure_ascii=False))   # noqa: F405
print('wrote', os.path.basename(out))
