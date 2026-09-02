# The first two puzzles, after the originals: fix the ship's computer.
#
#   p1  a box with 1 and 2 in it, from a 1, a 2 and an empty box
#   p2  a 4, from two 2s (a number dropped on a number adds)
#
# Each is its own world file, and p2 also rides inside p1's library so that a
# robot can open it by name where nothing can be fetched.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _pz import *                                           # noqa: F403

# --- p2: we need a 4 -------------------------------------------------------
P2_JUDGE = judge('the judge', 9911, 'p2-post', 9912, 'p2-reply',
                 right=num(4),                              # noqa: F405
                 on_right=[take('given', 2), put('given', 1)],   # send the note  # noqa: F405
                 notes=['That’s it! The computer has its 4. '
                        '(More puzzles are on the way.)'])

p2 = puzzle(
    'p2',
    'Did you notice that things wiggle when they are ready to be picked up? '
    'OK, now we’ll need a 4. Give it to the bird when you have one.',
    'a 4',
    ['Try putting the twos together.',
     'Drop a 2 on a 2 and wait until it turns into a 4.',
     'OK, here’s all you have to do: drop one 2 on the other. When it '
     'turns into a 4, pick up the 4 and give it to the bird.'],
    rules(),
    [{'thing': num(2), 'x': -0.5, 'z': 1.6},                # noqa: F405
     {'thing': num(2), 'x': -0.1, 'z': 1.6},                # noqa: F405
     {'thing': fixed(num(4), 'we need this'), 'x': 0.9, 'z': 2.05},   # noqa: F405
     {'thing': bird(9911, 'p2-post', 'give me your answer'), 'x': 0.9, 'z': 1.35},   # noqa: F405
     {'thing': nest(9912, 'p2-reply', 'from the judge'), 'x': 1.35, 'z': 1.35},     # noqa: F405
     {'thing': P2_JUDGE, 'x': -1.25, 'z': 2.1}])

# --- p1: we need a box with 1 and 2 in it -----------------------------------
P1_JUDGE = judge('the judge', 9901, 'p1-post', 9902, 'p1-reply',
                 right=box(num(1), num(2)),                 # noqa: F405
                 on_right=[take('given', 2), put('given', 1),   # send the note  # noqa: F405
                           load('p2')],                     # ...and open the next
                 notes=['Well done — the computer has its first numbers. '
                        'Here comes the next puzzle.'])

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
    [{'thing': num(1), 'x': -0.6, 'z': 1.6},                # noqa: F405
     {'thing': num(2), 'x': -0.2, 'z': 1.6},                # noqa: F405
     {'thing': empty_box(2), 'x': 0.3, 'z': 1.6},           # noqa: F405
     {'thing': fixed(box(num(1), num(2)), 'we need this'), 'x': 0.9, 'z': 2.05},   # noqa: F405
     {'thing': bird(9901, 'p1-post', 'give me your answer'), 'x': 0.9, 'z': 1.35},   # noqa: F405
     {'thing': nest(9902, 'p1-reply', 'from the judge'), 'x': 1.35, 'z': 1.35},     # noqa: F405
     {'thing': P1_JUDGE, 'x': -1.25, 'z': 2.1}],
    library={'p2': p2})
