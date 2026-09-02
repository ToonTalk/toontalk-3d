# The first puzzles, after the originals: fix the ship's computer.
#
#   p1  a box with 1 and 2 in it, from a 1, a 2 and an empty box
#   p2  a 4, from two 2s (a number dropped on a number adds)
#   p3  a box with 8, 16 and 32 in it -- boxes join by dropping one on the
#       side of another
#   p4  a zero -- a number wearing a minus badge takes away when dropped
#   p5  a box with two zeros, made by a ROBOT you train, with Mimi to copy
#
# Each is its own world file, and every later one also rides inside p1's
# library, so a robot can open the next by name where nothing can be fetched.
#
# THE LAYOUT, the same on every table: what you work with at the FRONT (near
# you), the bird in the middle, the reply nest beside her, the goal and the
# judge at the back where they are seen and not in the way.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _pz import *                                           # noqa: F403

FRONT = 2.05          # near the camera
MID = 1.55
BACK = 1.2


def table(materials, goal, post, reply, judge_, extra=()):
    """materials: things left to right across the front; the rest fixed."""
    n = len(materials)
    xs = [(-0.45 * (n - 1) / 2) + 0.45 * i for i in range(n)] if n > 1 else [0.0]
    bench = [{'thing': m, 'x': round(x, 2), 'z': FRONT} for m, x in zip(materials, xs)]
    bench += [{'thing': post, 'x': 0.0, 'z': MID},
              {'thing': reply, 'x': 0.55, 'z': MID},
              {'thing': goal, 'x': 1.15, 'z': BACK},
              {'thing': judge_, 'x': -1.25, 'z': BACK}]
    bench += list(extra)
    return bench


def next_note(text):
    return [take('given', 2), put('given', 1)]              # noqa: F405


# --- p5: a robot makes a box with two zeros ----------------------------------
P5 = puzzle(
    'p5',
    'Sometimes to get things done I have to train robots to do work for me. '
    'See if you can train a robot to make a box with two zeros in it. Mimi the '
    'copier is here to help. Give the box to the bird when you have it.',
    'a box with two zeros in it',
    ['You can train the robot if you give it the box with the zero in it. '
     'You’ll end up in its imagination, and it remembers whatever you do.',
     'Set the box on Mimi’s platform: a copy drops into the tray.',
     'Drop the copy on the side of the box and they join into one box.',
     'Here’s what I’d do. I’d drop the box on the robot. Then I’d have it '
     'set the box on Mimi, take the copy, and drop the copy on the side of '
     'the box. When I leave its thought bubble, I’d give it the box and let '
     'it work — then give the bird the box it made.'],
    rules(tools=['mimi'], max_steps=6),
    table([box(num(0)), {'kind': 'robot', 'name': None, 'program': [], 'team': []}],   # noqa: F405
          fixed(box(num(0), num(0)), 'we need this'),      # noqa: F405
          bird(9951, 'p5-post', 'give me your answer'),    # noqa: F405
          nest(9952, 'p5-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 9951, 'p5-post', 9952, 'p5-reply',
                right=box(num(0), num(0)),                  # noqa: F405
                on_right=next_note(''),
                notes=['You trained a robot! The computer has its zeros. '
                       '(More puzzles are on the way.)'])))

# --- p4: a zero --------------------------------------------------------------
P4 = puzzle(
    'p4',
    'The computer’s going to need a zero to work. Notice the badge on one of '
    'these numbers: a number wearing a minus takes away when you drop it on '
    'another. Give the bird a zero.',
    'a zero',
    ['Look at the badge on the 3 that says minus.',
     'Drop the minus 3 on the other 3.',
     'Here’s what I’d do: pick up the 3 wearing the minus badge and drop it on '
     'the plain 3. That leaves a 0. Give the 0 to the bird.'],
    rules(),
    table([num(3), num(3, op='-')],                          # noqa: F405
          fixed(num(0), 'we need this'),                     # noqa: F405
          bird(9941, 'p4-post', 'give me your answer'),      # noqa: F405
          nest(9942, 'p4-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9941, 'p4-post', 9942, 'p4-reply',
                right=num(0),                                # noqa: F405
                on_right=next_note('') + [load('p5')],
                notes=['A zero — just what the computer needed. Next: robots.'])),
    library={'p5': P5})

# --- p3: a box with 8, 16 and 32 ----------------------------------------------
P3 = puzzle(
    'p3',
    'Thanks. Now see if you can make a box with 8, 16 and 32 inside, and give '
    'it to the bird.',
    'a box with 8, 16 and 32 in it',
    ['Did you know that boxes click together when you drop one on the side '
     'of another?',
     'A 16 dropped on a 16 makes a 32 — right there in its box.',
     'OK, here’s what I’d do. I’d drop the loose 16 on the 16 in the box on '
     'the right, which turns it into 32. Then I’d drop the box with 8 on the '
     'LEFT side of the box with 16, and the box with 32 on the RIGHT side of '
     'that. Then I’d give the whole box to the bird.'],
    rules(),
    table([box(num(8)), box(num(16)), box(num(16)), num(16)],   # noqa: F405
          fixed(box(num(8), num(16), num(32)), 'we need this'),  # noqa: F405
          bird(9931, 'p3-post', 'give me your answer'),      # noqa: F405
          nest(9932, 'p3-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9931, 'p3-post', 9932, 'p3-reply',
                right=box(num(8), num(16), num(32)),         # noqa: F405
                on_right=next_note('') + [load('p4')],
                notes=['Three numbers in a row — the computer is filling up. '
                       'Next: a zero.'])),
    library={'p4': P4, 'p5': P5})

# --- p2: we need a 4 ---------------------------------------------------------
P2 = puzzle(
    'p2',
    'Did you notice that things wiggle when they are ready to be picked up? '
    'OK, now we’ll need a 4. Give it to the bird when you have one.',
    'a 4',
    ['Try putting the twos together.',
     'Drop a 2 on a 2 and wait until it turns into a 4.',
     'OK, here’s all you have to do: drop one 2 on the other. When it '
     'turns into a 4, pick up the 4 and give it to the bird.'],
    rules(),
    table([num(2), num(2)],                                  # noqa: F405
          fixed(num(4), 'we need this'),                     # noqa: F405
          bird(9911, 'p2-post', 'give me your answer'),      # noqa: F405
          nest(9912, 'p2-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9911, 'p2-post', 9912, 'p2-reply',
                right=num(4),                                # noqa: F405
                on_right=next_note('') + [load('p3')],
                notes=['That’s it! The computer has its 4. Next: a box of three.'])),
    library={'p3': P3, 'p4': P4, 'p5': P5})

# --- p1: we need a box with 1 and 2 in it -----------------------------------
puzzle(
    'p1',
    'Thanks for coming to help me fix the ship. First we’ll need to fix '
    'the ship’s computer, and it needs numbers to work. Can you make a '
    'box with 1 and 2 in it, and give it to the bird? If you get stuck, ask '
    'me for a hint.',
    'a box with 1 and 2 in it',
    ['Did you notice that you can pick up numbers and let go of them over '
     'holes in the box?',
     'Put the 1 in the first hole and the 2 in the second. Then pick up the '
     'whole box and give it to the bird.',
     'OK, here’s what I’d do if I could. I’d pick up the 1 and '
     'drop it in the first hole. Then I’d pick up the 2 and drop it in '
     'the second hole. Then I’d grab the whole box and give it to the '
     'bird.'],
    rules(),
    table([num(1), num(2), empty_box(2)],                    # noqa: F405
          fixed(box(num(1), num(2)), 'we need this'),        # noqa: F405
          bird(9901, 'p1-post', 'give me your answer'),      # noqa: F405
          nest(9902, 'p1-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9901, 'p1-post', 9902, 'p1-reply',
                right=box(num(1), num(2)),                   # noqa: F405
                on_right=next_note('') + [load('p2')],
                notes=['Well done — the computer has its first numbers. '
                       'Press Next when you are ready.'])),
    library={'p2': P2, 'p3': P3, 'p4': P4, 'p5': P5})
