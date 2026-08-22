# Shared vocabulary for the Exploring Infinity worlds.
#
# These activities are all the same shape: a robot with a box of
# [somewhere to read from, somewhere to write to], reading the top of a nest
# and giving a bird the answer. That is a dataflow process, and the workshop
# already has one -- a robot whose condition cannot be met by an EMPTY nest
# does not fail, it dozes until a bird delivers. So a chain of these robots is
# a pipeline, and the pipeline is the whole point of the activities: sequences
# feeding sequences, forever, without anybody holding a whole sequence.
import json, io, os

# --- things -----------------------------------------------------------------
num = lambda n, d=1, op='+': {'kind': 'number', 'value': {'n': str(n), 'd': str(d)},
                              'op': op}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *holes: {'kind': 'box', 'holes': list(holes)}
scale = lambda a, b, label=None: dict(
    {'kind': 'scale', 'holes': [a, b]}, **({'label': label} if label else {}))


def nest(nid, guid, label=None, pile=None):
    n = {'kind': 'nest', 'id': nid, 'guid': guid, 'hasEgg': False,
         'pile': pile or []}
    if label:
        n['label'] = label
    return n


def bird(nid, guid, label=None):
    b = {'kind': 'bird', 'nestId': nid, 'nestGuid': guid}
    if label:
        b['label'] = label
    return b


# --- conditions -------------------------------------------------------------
WILD = {'kind': 'wild'}
ANYNUM = {'kind': 'wildNumber'}
ANYBIRD = {'kind': 'anyBird'}
ANYNEST = {'kind': 'anyNest'}
ANYBOX = {'kind': 'anyBox'}
tilt = lambda t: {'kind': 'scaleTilt', 'tilt': t}      # 'L', 'R' or '='

# --- steps ------------------------------------------------------------------
at = lambda c, *p: {'c': c, 'path': list(p)}
take = lambda c, *p: {'type': 'take', 'at': at(c, *p)}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}
# the TOP OF THE PILE on the nest at that address, not the nest itself
takeTop = lambda c, *p: {'type': 'take', 'at': dict(at(c, *p), nest=True)}

newnum = {'type': 'newNumber'}
newbox = {'type': 'newBox'}
newnest = {'type': 'newNest'}
newscale = {'type': 'newScale'}
holes = lambda n: {'type': 'setHoles', 'n': n}
setop = lambda op: {'type': 'setOp', 'op': op}
setv = lambda v, op='+', d=1: {'type': 'setValue',
                               'value': {'n': str(v), 'd': str(d)}, 'op': op}


def robot(name, condition, program, trained_on=None, team=None):
    return {'kind': 'robot', 'name': name, 'condition': condition,
            'program': program, 'trainedOn': trained_on, 'team': team or []}


def room(label, stand, bot, opaque=False, dirty=True, bench=None):
    """One robot, in a workshop of its own.

    Rooms are how several of these robots run at once. Out on the open bench
    only one robot can stand, and a robot dozing on an empty nest keeps that
    place until somebody picks it up -- so a pipeline built in the open has to
    be run a stage at a time, by hand. A room is a bench of its own: the robot
    inside dozes there, wakes when a bird delivers through the roof, and never
    competes for the one outside. Glass by default, so you can watch."""
    return {'kind': 'room', 'label': label, 'opaque': opaque, 'dirty': dirty,
            'world': {'kind': 'world', 'v': 3, 'bench': bench or [],
                      'stations': {'stand': stand}, 'active': bot}}


def drop(v, op, *where):
    """A fresh number, given an operation, dropped somewhere: how arithmetic
    is done to a thing that stays where it is."""
    return [newnum, setv(v, op), put(*where)]


def write(name, bench, folder=None):
    world = {'kind': 'world', 'v': 3, 'bench': bench, 'stations': {},
             'active': None}
    out = os.path.join(folder or os.path.dirname(os.path.abspath(__file__)),
                       name + '.world.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
    print('wrote', os.path.basename(out))
    return out
