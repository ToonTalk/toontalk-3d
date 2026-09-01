# Shared vocabulary for the behaviour worlds (anima-gadgets).
#
# A BEHAVIOUR is an ordinary pad whose PANEL carries robots. The robots speak
# about "my thing" through a live bird, and binding a behaviour to something
# is nothing more than re-pointing that bird. Unattached, the bird points at
# the behaviour itself -- which is why a gadget set down on the table
# demonstrates itself, at no cost and with no demo mode.
#
# Everything a behaviour does, it does by sending its thing a message:
#
#   [set   | across   | n]   [set  | away | n]   [set  | position | [x|z]]
#   [move  | across   | n]   [move | away | n]   [move | position | [dx|dz]]
#   [query | across   | bird]                    [query| position | bird]
#   [listen| position | bird]  [listen | edge | bird]  [listen | touch | bird]
#   [set   | background | grey]  [set | colour | white]  [set | font | sans]
#   [set   | width | 2]          [set | height | 1/3]
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403,F401

HERE = os.path.dirname(os.path.abspath(__file__))

DEV_KEYS = 'dev-keyboard'
DEV_POINT = 'dev-pointer'

WILDTEXT = {'kind': 'wildText'}


def device(nid, guid, label):
    return {'kind': 'nest', 'id': nid, 'guid': guid, 'hasEgg': False,
            'dev': True, 'label': label, 'pile': []}


def live(thing, lid, evt=None):
    """A thing with an identity, so a bird can be addressed to it."""
    return dict(thing, lid=lid, evt=evt or ('evt-' + lid))


def to(lid, label=None):
    """A bird addressed to a THING rather than a nest."""
    b = {'kind': 'bird', 'nestId': 0, 'nestGuid': None, 'liveId': lid}
    if label:
        b['label'] = label
    return b


def msg(*words):
    """A message box: words are pads, numbers are numbers, boxes are boxes."""
    holes = []
    for w in words:
        holes.append(txt(w) if isinstance(w, str) else w)     # noqa: F405
    return box(*holes)                                        # noqa: F405


def look(**kw):
    return kw


def pad(text, **look_kw):
    p = {'kind': 'text', 'text': text}
    if look_kw:
        p['look'] = look_kw
    return p


LOOK = dict(bg='#2a2135', ink='#e8d7ff', font='sans', h=0.42)


def gadget(name, lid, bot, work, look=None, bench=None):
    """A pad whose panel holds a robot team and the box it works on -- and,
    when it needs company (a bell, a score), things on the panel's bench."""
    return {'kind': 'text', 'text': name, 'gadget': True,
            'lid': lid, 'evt': 'evt-' + lid,
            'look': dict(look or LOOK),
            'panel': {'kind': 'world', 'v': 3, 'bench': bench or [],
                      'stations': {'stand': work}, 'active': bot}}


def write_beh(name, bench):
    return write(name, bench, HERE)                           # noqa: F405
