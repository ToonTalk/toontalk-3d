# -*- coding: utf-8 -*-
# Toy models -- things built of PARTS, importable with Import file.
#
# A part is a primitive (box, sphere, cylinder, cone) with a size, a place, a
# turn in degrees, and a colour. That is deliberately all: a model this small
# is a JSON file a person can read, and the workshop rebuilds it from
# primitives with no loader and no download.
#
# Both models face +z -- heading zero, the far edge -- so the 3D turtle's
# frame agrees with their noses from the moment the behaviour is bound.
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def part(shape, size, at, color, rot=None):
    p = {'shape': shape, 'size': size, 'at': at, 'color': color}
    if rot:
        p['rot'] = rot
    return p


RED = '#b8241a'
CREAM = '#efe2c6'
DARK = '#1c2330'

airplane = [
    # fuselage lies along z (a cylinder stands along y; rot x=90 lays it forward)
    part('cylinder', [0.035, 0.035, 0.30], [0, 0.075, 0.0], RED, rot=[90, 0, 0]),
    part('cone', [0.035, 0.07], [0, 0.075, 0.185], RED, rot=[90, 0, 0]),
    # wings and tail
    part('box', [0.42, 0.012, 0.10], [0, 0.082, 0.03], CREAM),
    part('box', [0.17, 0.010, 0.06], [0, 0.085, -0.125], CREAM),
    part('box', [0.010, 0.075, 0.065], [0, 0.115, -0.125], RED),
    # wheels
    part('sphere', [0.018], [0.06, 0.018, 0.04], DARK),
    part('sphere', [0.018], [-0.06, 0.018, 0.04], DARK),
    part('sphere', [0.014], [0, 0.014, -0.12], DARK),
]

GREEN = '#2e7d5b'
PALE = '#cfe2f5'
EYE = '#141821'

dragonfly = [
    part('cylinder', [0.020, 0.014, 0.20], [0, 0.070, -0.01], GREEN, rot=[90, 0, 0]),
    part('cylinder', [0.008, 0.005, 0.18], [0, 0.070, -0.19], GREEN, rot=[90, 0, 0]),
    part('sphere', [0.026], [0, 0.072, 0.10], GREEN),
    part('sphere', [0.012], [0.017, 0.085, 0.115], EYE),
    part('sphere', [0.012], [-0.017, 0.085, 0.115], EYE),
    # two pairs of wings, swept slightly
    part('box', [0.17, 0.004, 0.05], [0.105, 0.088, 0.03], PALE, rot=[0, 8, 4]),
    part('box', [0.17, 0.004, 0.05], [-0.105, 0.088, 0.03], PALE, rot=[0, -8, -4]),
    part('box', [0.15, 0.004, 0.045], [0.095, 0.085, -0.045], PALE, rot=[0, -10, 3]),
    part('box', [0.15, 0.004, 0.045], [-0.095, 0.085, -0.045], PALE, rot=[0, 10, -3]),
]


def write(name, label, lid, parts):
    rec = {'v': 4, 'kind': 'thing',
           'thing': {'kind': 'model', 'label': label,
                     'lid': lid, 'evt': 'evt-' + lid, 'parts': parts}}
    out = os.path.join(HERE, name + '.thing.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(rec, indent=1))
    print('wrote', out)


write('airplane', 'a toy airplane', 'L9560', airplane)
write('dragonfly', 'a dragonfly', 'L9561', dragonfly)
