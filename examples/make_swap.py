# Generates swap.world.json -- Ken's swap.tt, the smallest program in the set.
#
# One robot, one scale, three steps: if the bigger number is on the left, the
# robot puts the two the other way round. Then the scale tips the other way,
# its thought no longer matches, and it stops. Nothing counts, nothing is
# tested twice -- the scale IS the test, and it is doing the comparing all by
# itself while the robot works.
#
# The original's scale sits in a three-hole box, [a, scale, b], and weighs the
# holes on either side of it. Ours is a balance with two pans and the numbers
# sit in the pans, which is the one deliberate difference (see DIVERGENCE.md);
# the program is otherwise move for move the original:
#
#     Grasp(MyBox.1) Drop(1) Grasp(MyBox.3) DropOn(MyBox.1)
#     Grasp(1)       DropOn(MyBox.3)
import json, io, os

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
scale = lambda a, b: {'kind': 'scale', 'holes': [a, b]}

at = lambda c, *p: {'c': c, 'path': list(p)}
take = lambda c, *p: {'type': 'take', 'at': at(c, *p)}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}

swap = {
    'kind': 'robot', 'name': 'Swap',
    # a scale leaning left: the heavier number is the one on the left
    'condition': {'kind': 'scaleTilt', 'tilt': 'L'},
    'program': [
        take('given', 0), put('s0'),        # the left one, set aside
        take('given', 1), put('given', 0),  # the right one moves over
        take('s0'), put('given', 1),        # and the one set aside comes back
    ],
    'trainedOn': scale(num(7), num(3)),
    'team': [],
}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': scale(num(7), num(3)), 'x': -0.30, 'z': 1.55},
    {'thing': swap, 'x': -1.20, 'z': 1.30},
    {'thing': scale(num(2), num(9)), 'x': 0.55, 'z': 1.55},
    {'thing': txt('SWAP\n\nA scale is a balance: put\na number in each pan and\n'
                  'it leans towards the\nheavier one.\n\n'
                  'The robot\'s thought is "a\nscale leaning left" -- the\n'
                  'numbers themselves are not\nin the thought at all, only\n'
                  'which way it leans.'),
     'x': -0.95, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nGive the leaning scale to\nthe Swap robot. It puts the\n'
                  'two numbers the other way\nround, the scale leans the\n'
                  'other way, and the robot\nstops -- because its thought\n'
                  'no longer matches.\n\n'
                  'Give it the other scale and\nnothing happens: that one is\n'
                  'already in order.'),
     'x': -0.25, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'swap.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
