# Shared vocabulary for the sound worlds.
#
# A sound in the workshop is a little speaker lying face-up on the table, and
# what it holds is a list of SEGMENTS played one after another. A segment is
# either a made tone -- a frequency in hertz, a duration in seconds, and one of
# four waveshapes -- or a recording, which carries the sound file itself. These
# worlds only build made tones, because those are the ones a file can carry
# without carrying a megabyte with it.
#
#   space plays whatever is in your hand or under the pointer; "." stops it.
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403,F401

HERE = os.path.dirname(os.path.abspath(__file__))

SHAPES = ('sine', 'square', 'sawtooth', 'triangle')


def seg(f, d=0.5, shape='sine'):
    """One tone. Frequencies are hertz; the app clamps durations to 0.05..6s."""
    return {'f': f, 'd': d, 'shape': shape}


def sound(*segs, rate=1, reversed_=False, label=None):
    s = {'segs': list(segs), 'rate': rate}
    if reversed_:
        s['reversed'] = True
    out = {'kind': 'sound', 'sound': s}
    if label:
        out['label'] = label
    return out


silent = lambda label=None: sound(label=label)


def tone_box(f=440, d=(1, 2), shape='sine', label=None):
    """The [frequency, seconds, shape] box: drop it on a sound and it sings.

    The holes are LABELLED, so the box explains itself on the table -- the same
    plaques the built-in message boxes wear in a thing's info notebook."""
    b = {'kind': 'box',
         'holeLabels': ['frequency', 'seconds', 'shape'],
         'holes': [num(f), num(d[0], d[1]), txt(shape)]}
    if label:
        b['label'] = label
    return b


# Equal temperament from A440, rounded to whole hertz: enough for a tune, and
# whole numbers are what you would type on a number yourself.
NOTES = {}
for _i, _n in enumerate(('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A',
                         'A#', 'B')):
    for _oct in (3, 4, 5):
        _semis = (_oct - 4) * 12 + _i - 9          # from A4
        NOTES[_n + str(_oct)] = int(round(440 * (2 ** (_semis / 12))))


def note(name, d=0.4, shape='sine'):
    return seg(NOTES[name], d, shape)


def write_sounds(name, bench):
    return write(name, bench, HERE)                        # noqa: F405
