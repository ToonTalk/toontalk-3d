# Shared vocabulary for the behaviour worlds (anima-gadgets).
#
# A BEHAVIOUR is an ordinary pad whose PANEL carries robots. The robots speak
# about "my thing" through THE BIRD ON THE PERCH -- the pedestal beside every
# robot's desk, which on a panel holds a bird to whatever the panel is the
# back of -- and binding a behaviour to something is nothing more than
# deciding what that is. Unattached, the panel is the back of the pad itself
# -- which is why a gadget set down on the table demonstrates itself, at no
# cost and with no demo mode. The robots' boxes hold no bird to my thing at
# all (since 16 Sep 2026); a robot's letter put on the perch goes to her.
#
# Everything a behaviour does, it does by sending its thing a message:
#
#   [set   | across   | n]   [set  | away | n]   [set  | position | [x|z]]
#   [move  | across   | n]   [move | away | n]   [move | position | [dx|dz]]
#   [query | across   | bird]                    [query| position | bird]
#   [listen| position | bird]  [listen | edge | bird]  [listen | touch | bird]
#   [listen| touches  | bird]  (a scene: every pair of riders that meets)
#   [set   | shown | no]   [vanish]   [drop | thing | [across | away]]
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


# --- the touch reading, four holes since 12 Sep 2026 -------------------------
#   [what I ran into | which side of me | its name | which way, [across|away]]
def touch_reading(thing=None, side='none', name='nothing', normal=(0, 0)):
    return box(thing or txt('nothing'), txt(side), txt(name),   # noqa: F405
               box(num(normal[0]), num(normal[1])))              # noqa: F405


def touch_nest(lid, nid, thing=None, side='none', name='nothing', empty=False):
    """A thing's touch channel. empty=True is the dozing idiom: the team
    sleeps until a real announcement arrives."""
    pile = [] if empty else [touch_reading(thing, side, name)]
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#touch',
            'hasEgg': False, 'label': 'touching', 'pile': pile}


def touch_cond(side=None, name=None):
    """A thought about the reading: any bird (or anything), this side, this
    name -- each None for never-mind."""
    return box(WILD, txt(side) if side else WILDTEXT,            # noqa: F405
               txt(name) if name else WILDTEXT, WILD)            # noqa: F405


def touches_nest(lid, nid):
    """A scene's own channel: every pair of riders that starts touching, as
    [bird | name | bird | name | normal]. Starts empty -- a referee dozes."""
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#touches',
            'hasEgg': False, 'label': 'touches', 'pile': []}


def touches_cond(name_a=None, name_b=None):
    return box(WILD, txt(name_a) if name_a else WILDTEXT,        # noqa: F405
               WILD, txt(name_b) if name_b else WILDTEXT, WILD)  # noqa: F405


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


def write_beh(name, bench, folder=None, perch=None):
    """A behaviour world -- and, when its robots stand in the open rather
    than on a panel, the bird on the PERCH: the pedestal beside the desk that
    a robot's letters to "my thing" go to. On a panel it holds the panel's
    own bird; out here, a bird to the star."""
    return write(name, bench, folder or HERE,                           # noqa: F405
                 stations={'perch': perch} if perch else None)
