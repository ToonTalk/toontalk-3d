# Shared vocabulary for the picture worlds -- and a PNG writer, because a
# saved world can only carry a picture as a data URL and there is no reason to
# make anyone install a drawing library to regenerate three examples.
#
# A picture in the workshop is not a new kind of thing. It is a PAD: the same
# tablet you write words on, with an image on its face. So a picture copies,
# files into a notebook, goes in a box, is vacuumed by Dusty and is recognised
# by a robot's thought exactly as a word is -- and a robot's thought compares
# the picture itself, which is what makes `naming` possible.
import sys, os, zlib, struct, base64, math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403,F401

HERE = os.path.dirname(os.path.abspath(__file__))
N = 128                                     # every picture here is 128 square


def _png(rows):
    """RGB rows -> a data: URL. Filter 0 on every scanline; zlib does the rest,
    and for flat shapes that is a couple of kilobytes."""
    h = len(rows)
    w = len(rows[0])
    raw = b''.join(b'\x00' + bytes(v for px in r for v in px) for r in rows)

    def chunk(tag, data):
        body = tag + data
        return (struct.pack('>I', len(data)) + body
                + struct.pack('>I', zlib.crc32(body) & 0xffffffff))

    out = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    return 'data:image/png;base64,' + base64.b64encode(out).decode('ascii')


def draw(shape, ink, ground=(0xf7, 0xf1, 0xdf)):
    """One flat shape, centred, on a paper-coloured ground.

    Sampled 3x3 per pixel so the edges are not a staircase -- at this size an
    aliased circle reads as a cog."""
    rows = []
    for y in range(N):
        row = []
        for x in range(N):
            hits = 0
            for sy in range(3):
                for sx in range(3):
                    u = (x + (sx + 0.5) / 3) / N * 2 - 1
                    v = (y + (sy + 0.5) / 3) / N * 2 - 1
                    if shape(u, v):
                        hits += 1
            a = hits / 9.0
            row.append(tuple(int(round(g + (i - g) * a))
                             for g, i in zip(ground, ink)))
        rows.append(row)
    return _png(rows)


# --- the shapes -------------------------------------------------------------
circle = lambda u, v: u * u + v * v <= 0.62 ** 2
square = lambda u, v: abs(u) <= 0.55 and abs(v) <= 0.55


def triangle(u, v):
    v = -v                                   # point upwards on screen
    return v <= 0.62 and v >= -0.52 and abs(u) <= (0.62 - v) * 0.62


def star(u, v, points=5):
    a = math.atan2(v, u) + math.pi / 2
    r = math.hypot(u, v)
    k = math.cos(points * a / 2) ** 2
    return r <= 0.20 + 0.46 * k ** 2.6


def heart(u, v):
    v = -v * 1.12 + 0.18
    x, y = u * 1.25, v * 1.25
    q = x * x + y * y - 0.42
    return q * q * q - x * x * y * y * y <= 0


def ring(u, v):
    r = u * u + v * v
    return 0.28 ** 2 <= r <= 0.62 ** 2


# --- the pictures the worlds share ------------------------------------------
# Names and colours are ordinary data; the robots in `naming` recognise the
# PICTURE and answer with the name, so these two lists are the whole dictionary.
PICTURES = [
    ('circle', draw(circle, (0xd8, 0x4a, 0x3c))),
    ('square', draw(square, (0x2f, 0x6f, 0xb5))),
    ('triangle', draw(triangle, (0x3f, 0x9a, 0x5c))),
    ('star', draw(star, (0xd8, 0xa5, 0x1c))),
    ('heart', draw(heart, (0xc4, 0x3f, 0x74))),
    ('ring', draw(ring, (0x6b, 0x46, 0x30))),
]
BY_NAME = dict(PICTURES)


# A LABEL is an ordinary pad that has been told what to look like: grey paper,
# white writing, wide and short. Nothing here is a caption feature -- it is the
# appearance API, which is exactly what a robot would send:
#
#   [set | background | #3a3f47]   [set | colour | white]
#   [set | font       | sans]      [set | height | 0.26]
LABEL_LOOK = {'bg': '#3a3f47', 'ink': 'white', 'font': 'sans', 'h': 0.26}


def label(text, **over):
    look = dict(LABEL_LOOK)
    look.update(over)
    return {'kind': 'text', 'text': text, 'look': look}


def pic(name, caption='', sz=None, at=(0, 0.38)):
    """A picture pad, with its caption RIDING on it as a label.

    The caption used to be the pad's own writing, drawn on a band the app put
    there. Ken was right that that is too special-purpose: a label is a pad
    with a look, and riding on a picture is what any pad does in the middle of
    another. So the album's labels are now the same thing anybody can build --
    and Dusty takes the label off without taking the picture."""
    p = {'kind': 'text', 'text': '', 'img': BY_NAME[name]}
    if sz:
        p['sz'] = sz
    if caption:
        p['subs'] = [{'at': {'u': at[0], 'v': at[1]},
                      'thing': label(caption)}]
    return p


def write_images(name, bench):
    return write(name, bench, HERE)                        # noqa: F405
