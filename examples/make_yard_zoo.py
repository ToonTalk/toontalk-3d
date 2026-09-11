# -*- coding: utf-8 -*-
# A ZOO IN THE YARD: a sample world whose table is bare and whose yard holds
# six animals built from solid shapes, the way Marty builds them, each with
# its name on a sign, and a welcome pad by the door. Open it, step through
# the green back door, and there they are. Run this to regenerate
# yard-zoo.world.json; the app carries no copy of it.
import io, json, os

def part(shape, size, at, color, rot=None):
    d = {'shape': shape, 'size': size, 'at': at, 'color': color}
    if rot: d['rot'] = rot
    return d

def model(name, parts):
    return {'kind': 'model', 'parts': parts, 'label': name}

def legs(color, x, z, h=0.08, r=0.015, y=None):
    y = h / 2 if y is None else y
    return [part('cylinder', [r, r, h], [sx * x, y, sz * z], color) for sx in (-1, 1) for sz in (-1, 1)]

GREY, TAN, YELLOW, WHITE, BLACK, GREEN, PINK, DARK = '#8f8f94', '#c9a063', '#e8c24a', '#f2f2ef', '#242424', '#5f8f3c', '#f0a3b8', '#3a2a1a'

elephant = model('elephant', legs(GREY, 0.07, 0.05, 0.09, 0.02) + [
    part('box', [0.22, 0.14, 0.13], [0, 0.15, 0], GREY),
    part('sphere', [0.07], [0.15, 0.2, 0], GREY),
    part('cylinder', [0.02, 0.015, 0.16], [0.21, 0.13, 0], GREY, [0, 0, 20]),
    part('box', [0.01, 0.08, 0.07], [0.13, 0.2, 0.07], '#a5a5aa'),
    part('box', [0.01, 0.08, 0.07], [0.13, 0.2, -0.07], '#a5a5aa'),
    part('sphere', [0.012], [0.2, 0.22, 0.04], BLACK),
    part('sphere', [0.012], [0.2, 0.22, -0.04], BLACK),
])
giraffe = model('giraffe', legs(YELLOW, 0.05, 0.035, 0.14, 0.013) + [
    part('box', [0.16, 0.09, 0.09], [0, 0.18, 0], YELLOW),
    part('cylinder', [0.022, 0.026, 0.22], [0.07, 0.33, 0], YELLOW, [0, 0, -15]),
    part('box', [0.07, 0.045, 0.045], [0.12, 0.45, 0], YELLOW),
    part('sphere', [0.02], [0.03, 0.21, 0.03], '#a7712b'),
    part('sphere', [0.018], [-0.04, 0.17, -0.03], '#a7712b'),
    part('sphere', [0.016], [0.06, 0.15, 0.04], '#a7712b'),
    part('cylinder', [0.004, 0.004, 0.03], [0.1, 0.48, 0.015], '#a7712b'),
    part('cylinder', [0.004, 0.004, 0.03], [0.1, 0.48, -0.015], '#a7712b'),
])
lion = model('lion', legs(TAN, 0.06, 0.04, 0.07, 0.016) + [
    part('box', [0.18, 0.1, 0.1], [0, 0.12, 0], TAN),
    part('sphere', [0.065], [0.12, 0.17, 0], '#b07a2a'),
    part('sphere', [0.045], [0.15, 0.17, 0], TAN),
    part('sphere', [0.01], [0.185, 0.18, 0.02], BLACK),
    part('sphere', [0.01], [0.185, 0.18, -0.02], BLACK),
    part('cylinder', [0.006, 0.006, 0.12], [-0.13, 0.13, 0], TAN, [0, 0, 70]),
    part('sphere', [0.014], [-0.19, 0.16, 0], '#b07a2a'),
])
zebra = model('zebra', legs(WHITE, 0.06, 0.035, 0.09, 0.013) + [
    part('box', [0.18, 0.1, 0.09], [0, 0.14, 0], WHITE),
    part('box', [0.02, 0.1, 0.092], [-0.05, 0.14, 0], BLACK),
    part('box', [0.02, 0.1, 0.092], [0.0, 0.14, 0], BLACK),
    part('box', [0.02, 0.1, 0.092], [0.05, 0.14, 0], BLACK),
    part('cylinder', [0.02, 0.024, 0.09], [0.1, 0.21, 0], WHITE, [0, 0, -30]),
    part('box', [0.07, 0.04, 0.04], [0.15, 0.25, 0], WHITE),
    part('box', [0.005, 0.045, 0.02], [0.1, 0.22, 0], BLACK),
    part('sphere', [0.008], [0.18, 0.26, 0.015], BLACK),
    part('sphere', [0.008], [0.18, 0.26, -0.015], BLACK),
])
penguin = model('penguin', [
    part('cylinder', [0.05, 0.06, 0.16], [0, 0.08, 0], BLACK),
    part('cylinder', [0.035, 0.045, 0.14], [0.012, 0.075, 0], WHITE),
    part('sphere', [0.045], [0, 0.18, 0], BLACK),
    part('cone', [0.012, 0.03], [0.05, 0.18, 0], '#f0a020', [0, 0, -90]),
    part('sphere', [0.008], [0.035, 0.2, 0.02], WHITE),
    part('sphere', [0.008], [0.035, 0.2, -0.02], WHITE),
    part('box', [0.02, 0.09, 0.03], [-0.005, 0.09, 0.06], BLACK, [15, 0, 0]),
    part('box', [0.02, 0.09, 0.03], [-0.005, 0.09, -0.06], BLACK, [-15, 0, 0]),
    part('box', [0.04, 0.01, 0.03], [0.02, 0.005, 0.025], '#f0a020'),
    part('box', [0.04, 0.01, 0.03], [0.02, 0.005, -0.025], '#f0a020'),
])
crocodile = model('crocodile', [
    part('box', [0.3, 0.05, 0.09], [0, 0.03, 0], GREEN),
    part('box', [0.14, 0.03, 0.06], [0.2, 0.025, 0], GREEN),
    part('box', [0.12, 0.02, 0.05], [-0.2, 0.02, 0], GREEN, [0, 12, 0]),
    part('box', [0.02, 0.02, 0.05], [0.05, 0.065, 0], '#3d6b25'),
    part('box', [0.02, 0.02, 0.05], [-0.02, 0.065, 0], '#3d6b25'),
    part('box', [0.02, 0.02, 0.05], [-0.09, 0.065, 0], '#3d6b25'),
    part('sphere', [0.012], [0.12, 0.06, 0.03], YELLOW),
    part('sphere', [0.012], [0.12, 0.06, -0.03], YELLOW),
    part('box', [0.04, 0.02, 0.02], [0.02, 0.005, 0.06], GREEN),
    part('box', [0.04, 0.02, 0.02], [0.02, 0.005, -0.06], GREEN),
    part('box', [0.04, 0.02, 0.02], [-0.1, 0.005, 0.06], GREEN),
    part('box', [0.04, 0.02, 0.02], [-0.1, 0.005, -0.06], GREEN),
])
flamingo = model('flamingo', [
    part('cylinder', [0.004, 0.004, 0.14], [0.01, 0.07, 0], PINK),
    part('sphere', [0.04], [0, 0.17, 0], PINK),
    part('cylinder', [0.01, 0.014, 0.16], [0.035, 0.28, 0], PINK, [0, 0, -12]),
    part('sphere', [0.022], [0.06, 0.37, 0], PINK),
    part('cone', [0.008, 0.04], [0.085, 0.355, 0], BLACK, [0, 0, -120]),
    part('sphere', [0.005], [0.07, 0.38, 0.015], BLACK),
])

# each animal is shown at twice hand size, so a child can see them from the door
def on_ground(thing, x, z):
    t = dict(thing); t['sz'] = 2
    return {'thing': t, 'x': x, 'z': z + 1.4}      # the ground begins past the helpers

sign = {'kind': 'text', 'text': 'Welcome to the zoo!\n\nAsk Marty for more animals,\nor copy one on Mimi.'}

world = {
    'kind': 'world', 'v': 4, 'stations': {}, 'active': None,
    'name': 'yard-zoo',
    'bench': [],
    'yard': {'bench': [
        {'thing': sign, 'x': -2.6, 'z': 6.0},
        on_ground(elephant, -1.6, 2.4),
        on_ground(giraffe, 0.4, 2.2),
        on_ground(lion, 2.2, 2.6),
        on_ground(zebra, -0.6, 4.2),
        on_ground(penguin, 1.4, 4.4),
        on_ground(crocodile, 3.2, 4.2),
        on_ground(flamingo, -2.8, 2.8),
    ]},
}
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, 'yard-zoo.world.json')
io.open(out, 'w', encoding='utf-8', newline='').write(json.dumps(world, ensure_ascii=False))
print('wrote', out)
