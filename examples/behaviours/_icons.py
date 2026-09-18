# -*- coding: utf-8 -*-
# ICONS FOR THE ANIMA-GADGETS (Ken, 19 Sep 2026: "generate iconic images
# conveying what it does, e.g. bouncing"). Each is a small SVG, drawn here in
# code so it regenerates with the world: the star the shelf's gadgets are
# tried on, and the one thing the behaviour does to it. The pad keeps its
# name on the band under the picture.
import base64

BG = '#2a2135'
INK = '#e8d7ff'
GOLD = '#ffd23f'
W, H = 200, 120


def star(cx, cy, r=13, fill=GOLD):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append('%.1f,%.1f' % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return '<polygon points="%s" fill="%s"/>' % (' '.join(pts), fill)


def arrow(x1, y1, x2, y2, w=3, colour=INK):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2, y2
    l = 9
    p1 = (hx - l * math.cos(a - 0.5), hy - l * math.sin(a - 0.5))
    p2 = (hx - l * math.cos(a + 0.5), hy - l * math.sin(a + 0.5))
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d" stroke-linecap="round"/>'
            % (x1, y1, x2, y2, colour, w)
            + '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (hx, hy, p1[0], p1[1], p2[0], p2[1], colour))


def wall(x, colour=INK):
    return '<rect x="%d" y="20" width="6" height="80" rx="2" fill="%s" opacity="0.8"/>' % (x, colour)


def text(x, y, t, size=22, colour=INK, anchor='middle', weight='700'):
    return ('<text x="%s" y="%s" font-family="system-ui, sans-serif" font-size="%d" font-weight="%s" '
            'fill="%s" text-anchor="%s">%s</text>' % (x, y, size, weight, colour, anchor, t))


def spark(x, y, colour=GOLD):
    return ('<g stroke="%s" stroke-width="3" stroke-linecap="round">'
            '<line x1="%d" y1="%d" x2="%d" y2="%d"/><line x1="%d" y1="%d" x2="%d" y2="%d"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d"/><line x1="%d" y1="%d" x2="%d" y2="%d"/></g>'
            % (colour, x - 10, y, x - 4, y, x + 4, y, x + 10, y, x, y - 10, x, y - 4, x, y + 4, x, y + 10))


def cursor(x, y):
    return ('<polygon points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" fill="#fff" stroke="#000" stroke-width="1.5"/>'
            % (x, y, x, y + 26, x + 7, y + 20, x + 12, y + 30, x + 17, y + 27, x + 12, y + 18, x + 21, y + 18))


ICONS = {
    'moving right': lambda: star(80, 60) + arrow(100, 60, 160, 60),
    'moving left': lambda: star(120, 60) + arrow(100, 60, 40, 60),
    'bouncing': lambda: wall(14) + wall(180) + star(100, 60)
        + arrow(118, 52, 168, 52) + arrow(168, 68, 118, 68),
    'wrapping at the edges': lambda: wall(14) + wall(180)
        + star(160, 60) + arrow(172, 60, 196, 60)
        + star(40, 60, fill='#a58e2a') + arrow(4, 60, 26, 60),
    'following the pointer': lambda: cursor(120, 22) + star(60, 80)
        + '<line x1="74" y1="76" x2="118" y2="46" stroke="%s" stroke-width="3" stroke-dasharray="5 6"/>' % INK,
    'following up and down': lambda: cursor(120, 22) + star(60, 88)
        + '<line x1="60" y1="70" x2="60" y2="30" stroke="%s" stroke-width="3" stroke-dasharray="5 6"/>' % INK
        + arrow(60, 40, 60, 24, 2),
    'bouncing at a speed': lambda: wall(14) + wall(180) + star(100, 60)
        + '<g stroke="%s" stroke-width="3" stroke-linecap="round" opacity="0.7"><line x1="40" y1="50" x2="70" y2="50"/><line x1="34" y1="60" x2="70" y2="60"/><line x1="40" y1="70" x2="70" y2="70"/></g>' % INK
        + arrow(122, 60, 166, 60),
    'moving with the arrow keys': lambda: star(100, 60)
        + ''.join('<rect x="%d" y="%d" width="28" height="24" rx="5" fill="none" stroke="%s" stroke-width="2.5"/>' % (x, y, INK)
                  + text(x + 14, y + 17, t, 15) for x, y, t in [(86, 8, '&#8593;'), (86, 88, '&#8595;'), (30, 48, '&#8592;'), (142, 48, '&#8594;')]),
    'grow when bumped': lambda: star(50, 70, 9) + spark(80, 70) + arrow(92, 70, 118, 70) + star(150, 62, 22),
    'shrink when bumped': lambda: star(52, 62, 22) + spark(92, 66) + arrow(104, 66, 128, 66) + star(156, 70, 9),
    'make a sound on hit': lambda: star(70, 70) + spark(100, 66)
        + text(140, 82, '&#9835;', 52, INK),
    'reverse on collision': lambda: star(70, 60) + star(130, 60, fill='#7fd7ff') + spark(100, 60)
        + arrow(60, 88, 24, 88) + arrow(140, 88, 176, 88),
    'speed limit': lambda: star(60, 66)
        + '<g stroke="%s" stroke-width="3" stroke-linecap="round" opacity="0.7"><line x1="14" y1="58" x2="40" y2="58"/><line x1="10" y1="66" x2="40" y2="66"/><line x1="14" y1="74" x2="40" y2="74"/></g>' % INK
        + '<circle cx="140" cy="60" r="30" fill="none" stroke="#ff6b6b" stroke-width="5"/>' + text(140, 68, '30', 24, INK),
    'send 1 to the score when hit': lambda: star(60, 70) + spark(92, 66)
        + '<rect x="112" y="40" width="70" height="44" rx="6" fill="none" stroke="%s" stroke-width="2.5"/>' % INK
        + text(147, 72, '+1', 28, GOLD),
    'reverse a speed on collision': lambda: star(70, 60) + star(130, 60, fill='#7fd7ff') + spark(100, 60)
        + '<g stroke="%s" stroke-width="3" stroke-linecap="round" opacity="0.7"><line x1="20" y1="54" x2="44" y2="54"/><line x1="16" y1="66" x2="44" y2="66"/><line x1="156" y1="54" x2="180" y2="54"/><line x1="156" y1="66" x2="184" y2="66"/></g>' % INK
        + arrow(60, 92, 24, 92) + arrow(140, 92, 176, 92),
    'wandering': lambda: '<path d="M20,90 C40,30 70,110 95,60 S140,20 160,70 S185,100 190,40" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="6 5"/>' % INK
        + star(160, 70) + '<rect x="24" y="22" width="30" height="30" rx="6" fill="#fff"/>'
        + ''.join('<circle cx="%d" cy="%d" r="3" fill="#222"/>' % (x, y) for x, y in [(32, 30), (46, 30), (39, 37), (32, 44), (46, 44)]),
    'random colour': lambda: ''.join('<rect x="%d" y="30" width="22" height="22" rx="4" fill="%s"/>' % (20 + i * 26, c)
                                     for i, c in enumerate(['#e33', '#f80', '#fd0', '#3a3', '#36f', '#529', '#a4c'][:6]))
        + '<rect x="70" y="66" width="40" height="40" rx="8" fill="#fff"/>'
        + ''.join('<circle cx="%d" cy="%d" r="4" fill="#222"/>' % (x, y) for x, y in [(80, 76), (100, 76), (90, 86), (80, 96), (100, 96)])
        + arrow(120, 86, 156, 86) + '<rect x="160" y="70" width="30" height="30" rx="4" fill="#36f"/>',
}


def icon(name):
    """The gadget's picture as a data URL, or None for a gadget without one."""
    draw = ICONS.get(name)
    if not draw:
        return None
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
           '<rect width="%d" height="%d" fill="%s"/>%s</svg>' % (W, H, W * 2, H * 2, W, H, BG, draw()))
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode('utf-8')).decode('ascii')


if __name__ == '__main__':
    import io, os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_icons_preview.html')
    cells = ''.join('<figure><img src="%s" width="200"><figcaption>%s</figcaption></figure>' % (icon(n), n) for n in ICONS)
    io.open(out, 'w', encoding='utf-8').write('<body style="background:#111;color:#ddd;font:13px system-ui;display:flex;flex-wrap:wrap;gap:12px">' + cells)
    print('preview', out)
