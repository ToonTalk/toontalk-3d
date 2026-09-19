# -*- coding: utf-8 -*-
# Three larger drawing lessons, written by ChatGPT (17 September 2026) as
# programs 3, 5 and 6 of its lesson series (1, 2 and 4 are make_lessons.py's
# planet, flower and spark), moved into the examples' own vocabulary (Ken,
# 19 Sep: "regenerate the 3 lessons ChatGPT made to fit everything else").
#
#   🌷 flower-garden        a repeat inside a repeat inside a repeat: three
#                           flowers, each a stem, two leaves and a ring of
#                           tilted curved petals (8, 10 and 12), 667 rounds
#   🔭 planetary-clockwork  three planets on inclined tracks round a sun,
#                           a moon round the blue one: sin and cos as
#                           badges, angles modulo 360, 120 ticks
#   🎆 firework-fountain    eight sparks under gravity, three bursts of
#                           thirty ticks, a dot stamped every tick
#
# THE SHAPE OF ITS PROGRAMS. The work box holds the stage (a word), the
# counters, the records of the things, and a LIBRARY box of every constant
# and letter the robots use. A robot copies a letter and gives the copy to a
# thing's bird; a letter with a changing amount ("dynamic") has that amount
# put into it first, from a slot of the box. Arithmetic is a copy of a
# number dropped on another, wearing the badge it needs (+, *, mod, sin,
# cos). `set` empties a slot and puts a copy there; `apply` drops one.
#
# What changed in the move: numbers are fractions in lowest terms; a team
# ends by putting its work box away with Dusty -- finished, for good --
# rather than writing "done" and stopping on a mismatch; the garden's pen
# goes invisible between the parts of a flower rather than up, so each
# flower is ONE trail (a stem, two leaves and the petals) for Dusty and for
# saving; and the experiments are on pads by the things.
import io, json, os, sys, math
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403,F401

HERE = os.path.dirname(os.path.abspath(__file__))


def n(v, op='+'):
    f = Fraction(str(v)) if not isinstance(v, Fraction) else v
    return num(f.numerator, f.denominator, op)             # noqa: F405


def labelled(holes, labels):
    b = box(*holes)                                        # noqa: F405
    b['holeLabels'] = list(labels)
    return b


def bird_to(lid):
    return {'kind': 'bird', 'nestId': None, 'nestGuid': None, 'liveId': lid, 'label': 'to ' + lid}


def sphere(r, color, at=(0, 0, 0)):
    return {'shape': 'sphere', 'size': [r], 'color': color, 'at': list(at)}


def model(label, parts, **extra):
    return dict({'kind': 'model', 'label': label, 'parts': parts, 'ghost': True}, **extra)


def live(lid, parts, **extra):
    return model(lid, parts, lid=lid, evt='evt-' + lid, **extra)


NUMCOND = ANYNUM                                           # noqa: F405


class Program:
    """A work box with a library of constants, and the robots that use it."""
    def __init__(self, holes, labels, lib):
        self.work = labelled(holes, labels)
        self.lib = lib
        self.work['holes'][lib] = labelled([], [])
        self.robots = []
        self.cache = {}

    def constant(self, o, label, tag=''):
        k = tag + json.dumps(o, sort_keys=True)
        if k in self.cache:
            return self.cache[k]
        b = self.work['holes'][self.lib]
        p = [self.lib, len(b['holes'])]
        b['holes'].append(o)
        b['holeLabels'].append(label or o.get('text') or o['kind'])
        self.cache[k] = p
        return p

    def N(self, v):
        return self.constant(n(v), str(v))

    def T(self, t):
        return self.constant(txt(t), t)                    # noqa: F405

    def at(self, p):
        o = self.work
        for i in p:
            o = o['holes'][i]
        return o

    def cp(self, p):
        return copy('given', *p)                           # noqa: F405

    def pt(self, p):
        return put('given', *p)                            # noqa: F405

    def vc(self, p):
        return vac('given', *p)                            # noqa: F405

    def set(self, dst, src):
        a, s = self.at(dst), self.at(src)
        if a and s and a['kind'] == 'number' and s['kind'] == 'number':
            return self.apply(dst, src, 'set')
        if a and s and a['kind'] == 'box' and s['kind'] == 'box' and len(a['holes']) == len(s['holes']):
            return [st for i in range(len(a['holes'])) for st in self.set(dst + [i], src + [i])]
        return [self.vc(dst), self.cp(src), self.pt(dst)]

    def apply(self, dst, src, op='+'):
        return [self.cp(src)] + ([] if op == '+' else [setop(op)]) + [self.pt(dst)]   # noqa: F405

    def state(self, s):
        return self.set([0], self.T(s))

    def msg(self, verb, what, arg):
        a = n(arg) if isinstance(arg, (int, float)) else (txt(arg) if isinstance(arg, str) else arg)   # noqa: F405
        return self.constant(labelled([txt(verb), txt(what), a], ['action', 'what', 'amount']), '%s %s' % (verb, what))   # noqa: F405

    def send(self, m, to):
        return [self.cp(m), self.pt(to)]

    def cmd(self, to, verb, what, arg):
        return self.send(self.msg(verb, what, arg), to)

    def dynamic(self, to, verb, what, source):
        sample = self.at(source)
        arg = (n(0) if sample['kind'] == 'number'
               else box(*[n(0) for _ in sample['holes']]) if sample['kind'] == 'box'   # noqa: F405
               else txt(''))                               # noqa: F405
        m = self.constant(labelled([txt(verb), txt(what), arg], ['action', 'what', 'amount']),   # noqa: F405
                          '%s %s (changing)' % (verb, what), 'dynamic:')
        return self.set(m + [2], source) + self.send(m, to)

    def robot(self, name, conditions, steps, note):
        holes = [None] * len(self.work['holes'])
        for p, v in conditions:
            h = holes
            for i in range(len(p) - 1):
                if h[p[i]] is None:
                    h[p[i]] = box(*[None] * len(self.at(p[:i + 1])['holes']))   # noqa: F405
                h = h[p[i]]['holes']
            h[p[-1]] = v
        cond = box(*holes)                                 # noqa: F405
        cond['holeLabels'] = self.work['holeLabels']
        self.robots.append(robot(name, cond, steps, trained_on=json.loads(json.dumps(self.work)), note=note))   # noqa: F405

    def finish(self, name, intro, bench, camera=None):
        lead = self.robots[0]
        lead['team'] = self.robots[1:]
        w = {'kind': 'world', 'v': 4, 'name': name, 'intro': intro, 'bench': bench,
             'stations': {'stand': self.work}, 'active': lead}
        if camera:
            w['camera'] = camera
        return w


FINISH = vac('given')                                      # Dusty puts the work box away: over, for good   # noqa: F405


# --- 3. the flower garden ------------------------------------------------
def garden():
    b = Program([txt('plant'), n(3), n(0), n(0), None,     # noqa: F405
                 labelled([n(0), n(0), n(0), n(0), n(0), box(n(0), n(1.7)), txt('#ec4899')],   # noqa: F405
                          ['height', 'forward step', 'heading', 'petal turn', 'leaf height', 'flower position', 'petal colour']),
                 None],
                ['stage', 'flowers left', 'petals left', 'segments left', 'my pen bird', 'flower settings', 'letters'], 6)
    B = [4]
    C = lambda i: [5, i]                                   # noqa: E731
    b.robot('Garden complete', [([0], txt('plant')), ([1], n(0))], [FINISH],   # noqa: F405
            'No flowers are left to plant: puts the work box away. The three flowers stay.')
    specs = [dict(x=-0.8, h=0.58, k=8, step=0.037, col='#ed5393'),
             dict(x=0, h=0.8, k=10, step=0.034, col='#8f73ed'),
             dict(x=0.8, h=0.64, k=12, step=0.029, col='#ffad37')]
    bench = []
    for i, f in enumerate(specs):
        lid = 'garden-pen-%d' % (i + 1)
        bench.append({'x': f['x'], 'z': 1.7, 'thing': model('flower pot %d' % (i + 1), [
            {'shape': 'cylinder', 'size': [0.105, 0.08, 0.12], 'at': [0, 0.06, 0], 'color': '#ac6648'},
            {'shape': 'cylinder', 'size': [0.11, 0.11, 0.018], 'at': [0, 0.12, 0], 'color': '#d98e60'},
            {'shape': 'cylinder', 'size': [0.09, 0.09, 0.012], 'at': [0, 0.135, 0], 'color': '#453c2b'}])})
        bench.append({'x': f['x'], 'z': 1.7, 'thing': live(lid, [sphere(0.018, '#a7e6b1')], penInk=0x38a867, penWide=2)})
        a = (b.set(B, b.constant(bird_to(lid), lid)) + b.set(C(0), b.N(f['h'])) + b.set(C(1), b.N(f['step']))
             + b.set(C(2), b.N(0)) + b.set(C(3), b.N(Fraction(360, f['k'])))
             + b.set(C(5), b.constant(box(n(f['x']), n(1.7)), 'flower centre %d' % i))   # noqa: F405
             + b.set(C(6), b.T(f['col'])) + b.set([2], b.N(f['k'])))
        # the stem: from the pot, straight up, in green
        a += (b.cmd(B, 'set', 'pen', 'up') + b.cmd(B, 'move', 'home', 0) + b.dynamic(B, 'set', 'position', C(5))
              + b.cmd(B, 'set', 'up', 0.14) + b.cmd(B, 'set', 'pen', '#38965b') + b.cmd(B, 'set', 'pen', 3)
              + b.cmd(B, 'set', 'pen', 'down') + b.dynamic(B, 'set', 'up', C(0)))
        # two leaves: back to the stem in INVISIBLE ink (the pen stays down, so
        # the flower stays one trail), then twenty curved segments each
        for heading, height in ((85, f['h'] * 0.46), (265, f['h'] * 0.7)):
            a += (b.cmd(B, 'set', 'pen', 'invisible') + b.dynamic(B, 'set', 'position', C(5))
                  + b.cmd(B, 'set', 'up', round(height, 4)) + b.cmd(B, 'set', 'facing', heading)
                  + b.cmd(B, 'move', 'pitch', 65) + b.cmd(B, 'set', 'pen', '#38965b'))
            for _ in range(20):
                a += b.cmd(B, 'move', 'forward', 0.017) + b.cmd(B, 'move', 'yaw', 18)
        a += b.state('petal ready')
        b.robot('Plant flower %d' % (i + 1), [([0], txt('plant')), ([1], n(3 - i))], a,   # noqa: F405
                'Flowers left is %d: this pen. Grow a stem and two leaves, then get ready for %d petals in %s.' % (3 - i, f['k'], f['col']))
    b.robot('Finish flower', [([0], txt('petal ready')), ([2], n(0))],   # noqa: F405
            (b.cmd(B, 'set', 'pen', 'invisible') + b.dynamic(B, 'set', 'position', C(5)) + b.dynamic(B, 'set', 'up', C(0))
             + b.cmd(B, 'set', 'pen', '#ffd96b') + b.cmd(B, 'drop', 'sphere', 0.105) + b.cmd(B, 'set', 'pen', 'up')
             + b.cmd(B, 'set', 'shown', 'no') + b.apply([1], b.N(-1)) + b.state('plant')),
            'No petals left: back to the top of the stem, a golden centre dropped there, the pen hidden, and one flower fewer to plant.')
    b.robot('Begin petal', [([0], txt('petal ready')), ([2], NUMCOND)],   # noqa: F405
            (b.cmd(B, 'set', 'pen', 'invisible') + b.dynamic(B, 'set', 'position', C(5)) + b.dynamic(B, 'set', 'up', C(0))
             + b.dynamic(B, 'set', 'facing', C(2)) + b.cmd(B, 'move', 'pitch', 55) + b.dynamic(B, 'set', 'pen', C(6))
             + b.cmd(B, 'set', 'pen', 3) + b.set([3], b.N(20)) + b.state('drawing petal')),
            'Petals are left: back to the top of the stem in invisible ink, face the next spoke, tilt up 55 degrees, and the petal colour. Twenty segments to draw.')
    b.robot('Next petal', [([0], txt('drawing petal')), ([3], n(0))],   # noqa: F405
            b.apply([2], b.N(-1)) + b.apply(C(2), C(3)) + b.state('petal ready'),
            'Twenty segments have closed the petal: one petal fewer, and the heading turns on by the petal turn.')
    b.robot('Draw petal segment', [([0], txt('drawing petal')), ([3], NUMCOND)],   # noqa: F405
            b.dynamic(B, 'move', 'forward', C(1)) + b.cmd(B, 'move', 'yaw', 18) + b.apply([3], b.N(-1)),
            'The innermost repeat: forward a little, turn 18 degrees, one segment fewer. Twenty of these make a petal, 8, 10 or 12 petals a flower, three flowers a garden.')
    bench.append({'x': -1.3, 'z': 2.2, 'thing': txt(TRY['garden'])})   # noqa: F405
    return b.finish('A flower garden',
                    'Start the team to grow three flowers, with 8, 10 and 12 petals. A stem, two leaves and a ring of '
                    'tilted petals each, drawn by a repeat inside a repeat inside a repeat: twenty segments make a '
                    'petal, petals make a flower, flowers make the garden. Instant shows it at once. Click next member '
                    'above Trained actions to see each of the seven robots. The pad on the table has things to try.',
                    bench, camera={'at': [0.0, 2.0, 3.6], 'look': [0.0, 1.3, 1.7]})   # all three pots in view


# --- 5. the planetary clockwork ------------------------------------------
def clockwork():
    specs = [dict(id='amber-planet', r=0.18, step=12, h=0.55, tilt=0.03, color='#ffb95d', size=0.032),
             dict(id='blue-planet', r=0.31, step=6, h=0.55, tilt=0.075, color='#4eafff', size=0.045),
             dict(id='red-planet', r=0.44, step=3, h=0.55, tilt=-0.11, color='#ef6d80', size=0.037),
             dict(id='blue-moon', r=0.075, step=24, h=0.045, tilt=0.025, color='#e6e8ff', size=0.016)]
    bodies = box(*[labelled([bird_to(s['id']), n(0), n(s['step']), n(s['r']), n(s['h']), n(s['tilt']), box(n(0), n(0)), n(0), n(0)],   # noqa: F405
                            ['bird', 'angle', 'degrees per tick', 'radius', 'base height', 'vertical amplitude', 'current x-z', 'current height', 'sine scratch'])
                   for s in specs])
    b = Program([txt('orbit'), n(120), bodies, None], ['stage', 'ticks left', 'four orbit records', 'letters'], 3)   # noqa: F405
    stand = model('the sun and its stand', [
        {'shape': 'cylinder', 'size': [0.12, 0.14, 0.04], 'at': [0, 0.02, 0], 'color': '#3a465f'},
        {'shape': 'cylinder', 'size': [0.014, 0.014, 0.48], 'at': [0, 0.28, 0], 'color': '#8793b1'},
        sphere(0.073, '#ffd46c', (0, 0.55, 0))])
    # the three tracks, as thin boxes on the stand itself, so loading cannot part them
    for s in specs[:3]:
        for i in range(120):
            a0, a1 = i * math.pi / 60, (i + 1) * math.pi / 60
            x0, y0, z0 = s['r'] * math.cos(a0), s['h'] + s['tilt'] * math.sin(a0), s['r'] * math.sin(a0)
            x1, y1, z1 = s['r'] * math.cos(a1), s['h'] + s['tilt'] * math.sin(a1), s['r'] * math.sin(a1)
            dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
            stand['parts'].append({'shape': 'box', 'size': [round(math.hypot(dx, dy, dz), 5), 0.004, 0.004],
                                   'at': [round((x0 + x1) / 2, 5), round((y0 + y1) / 2, 5), round((z0 + z1) / 2, 5)],
                                   'rot': [0, round(-math.atan2(dz, dx) * 180 / math.pi, 3), round(math.atan2(dy, math.hypot(dx, dz)) * 180 / math.pi, 3)],
                                   'color': '#42546e'})
    bench = [{'x': 0, 'z': 1.7, 'thing': stand}]
    for i, s in enumerate(specs):
        bench.append({'x': (0.31 + s['r']) if i == 3 else s['r'], 'z': 1.7,
                      'thing': live(s['id'], [sphere(s['size'], s['color'])], up=(0.595 if i == 3 else s['h']))})
    b.robot('Clockwork complete', [([0], txt('orbit')), ([1], n(0))], [FINISH],   # noqa: F405
            '120 ticks are done -- four amber orbits, two blue, one red, eight of the moon: puts the work box away.')
    a = []
    for i, s in enumerate(specs):
        p = lambda j, i=i: [2, i, j]                       # noqa: E731
        x, z, y, sn, B = [2, i, 6, 0], [2, i, 6, 1], p(7), p(8), p(0)
        a += b.apply(p(1), p(2)) + b.apply(p(1), b.N(360), 'mod')                     # the angle takes its step, modulo 360
        a += b.set(x, p(1)) + b.apply(x, b.N(0), 'cos') + b.apply(x, p(3), '*')     # x = r cos
        a += (b.set(sn, p(1)) + b.apply(sn, b.N(0), 'sin') + b.set(z, sn) + b.apply(z, p(3), '*')   # z = r sin
              + b.set(y, sn) + b.apply(y, p(5), '*') + b.apply(y, p(4)))              # height = base + amplitude sin
        if i == 3:
            a += b.apply(x, [2, 1, 6, 0]) + b.apply(z, [2, 1, 6, 1]) + b.apply(y, [2, 1, 7])   # the moon: round the blue planet
        else:
            a += b.apply(z, b.N(1.7))
        a += b.dynamic(B, 'set', 'position', p(6)) + b.dynamic(B, 'set', 'up', y)
    a += b.apply([1], b.N(-1))
    b.robot('Advance all four orbits', [([0], txt('orbit')), ([1], NUMCOND)], a,   # noqa: F405
            'Each angle takes its step, modulo 360. A cos badge and a sin badge turn a copy of the angle into the position, the radius scales it, the tilt lifts it. The moon adds the blue planet’s new position to its own. One tick fewer.')
    bench.append({'x': -1.3, 'z': 2.2, 'thing': txt(TRY['clockwork'])})   # noqa: F405
    return b.finish('A planetary clockwork',
                    'Start the team. Three planets travel round the sun on tilted tracks and a moon follows the blue one. '
                    'Every tick each angle grows by its own step and sin and cos badges turn it into a position; the '
                    'periods are 30, 60, 120 and 15 ticks. Slow it down to watch the arithmetic; Instant plays it. The '
                    'pad on the table has things to try.',
                    bench, camera={'at': [0.9, 1.75, 2.9], 'look': [0.0, 1.35, 1.7]})


# --- 6. the firework fountain --------------------------------------------
def fountain():
    colors = ['#ff687c', '#ffc25b', '#eeef7c', '#72e0ad', '#57c8fa', '#9290ff', '#d189fa', '#ff9bcf']
    parts = box(*[labelled([bird_to('spark-%d' % i), n(i * 45), n(0), n(0), n(Fraction(118 + 2 * i, 1000)), n(Fraction(118 + 2 * i, 1000))],   # noqa: F405
                           ['bird', 'launch angle', 'across velocity', 'away velocity', 'upward velocity', 'launch velocity'])
                  for i in range(8)])
    b = Program([txt('launch'), n(3), n(0), n(30), n(-0.008), n(0.012), parts, None],   # noqa: F405
                ['stage', 'bursts left', 'ticks left', 'lifetime per burst', 'gravity per tick', 'sideways speed', 'eight spark records', 'letters'], 7)
    bench = [{'x': 0, 'z': 1.7, 'thing': model('the fountain nozzle', [
        {'shape': 'cylinder', 'size': [0.08, 0.12, 0.09], 'at': [0, 0.045, 0], 'color': '#314156'},
        {'shape': 'cylinder', 'size': [0.045, 0.045, 0.035], 'at': [0, 0.095, 0], 'color': '#a8bdd1'}])}]
    for i, color in enumerate(colors):
        bench.append({'x': 0, 'z': 1.7, 'thing': live('spark-%d' % i, [sphere(0.024, color)], up=0.06, penInk=int(color[1:], 16))})
    b.robot('Fountain complete', [([0], txt('launch')), ([1], n(0))], [FINISH],   # noqa: F405
            'Three bursts are done: puts the work box away. The last burst’s dots remain; the sparks are hidden.')
    start = []
    for i, color in enumerate(colors):
        p = lambda j, i=i: [6, i, j]                       # noqa: E731
        B = p(0)
        start += (b.cmd(B, 'set', 'pen', 'up') + b.cmd(B, 'set', 'pen', 'clear')
                  + b.cmd(B, 'set', 'position', box(n(0), n(1.7))) + b.cmd(B, 'set', 'up', 0.06)   # noqa: F405
                  + b.cmd(B, 'set', 'shown', 'yes') + b.cmd(B, 'set', 'pen', color)
                  + b.set(p(4), p(5))                                                    # upward velocity = launch velocity
                  + b.set(p(2), p(1)) + b.apply(p(2), b.N(0), 'cos') + b.apply(p(2), [5], '*')   # across = cos(angle) * speed
                  + b.set(p(3), p(1)) + b.apply(p(3), b.N(0), 'sin') + b.apply(p(3), [5], '*')   # away = sin(angle) * speed
                  + b.apply(p(1), b.N(15)) + b.apply(p(1), b.N(360), 'mod'))                     # the next burst turns 15 degrees
    start += b.set([2], [3]) + b.state('flying')
    b.robot('Launch eight sparks', [([0], txt('launch')), ([1], NUMCOND)], start,   # noqa: F405
            'Bursts are left: every spark back at the nozzle, shown, its old dots cleared, its upward velocity set to its launch velocity, its sideways velocities from its angle with cos and sin -- and its angle turned 15 degrees for the next burst. Ticks left set to the lifetime.')
    end = []
    for i in range(8):
        end += b.cmd([6, i, 0], 'set', 'shown', 'no')
    end += b.apply([1], b.N(-1)) + b.state('launch')
    b.robot('Retire this burst', [([0], txt('flying')), ([2], n(0))], end,   # noqa: F405
            'No ticks left: every spark hidden, one burst fewer, and back to launching.')
    tick = []
    for i in range(8):
        p = lambda j, i=i: [6, i, j]                       # noqa: E731
        B = p(0)
        tick += (b.dynamic(B, 'move', 'across', p(2)) + b.dynamic(B, 'move', 'away', p(3))
                 + b.dynamic(B, 'move', 'up', p(4)) + b.cmd(B, 'drop', 'sphere', 0.018) + b.apply(p(4), [4]))
    tick += b.apply([2], b.N(-1))
    b.robot('Fly one tick', [([0], txt('flying')), ([2], NUMCOND)], tick,   # noqa: F405
            'Ticks are left: each spark moves by its three velocities, stamps a dot, and gravity comes off its upward velocity. Rising sparks slow, turn and fall. One tick fewer.')
    bench.append({'x': -1.3, 'z': 2.2, 'thing': txt(TRY['fountain'])})   # noqa: F405
    return b.finish('A firework fountain',
                    'Start the team for three bursts of eight coloured sparks. Every tick each spark moves by its '
                    'velocities and stamps a dot, and gravity takes a little off its upward velocity, so it slows, '
                    'turns and falls. After thirty ticks the sparks hide and the next burst turns 15 degrees. Instant '
                    'plays it; the dots remain. The pad on the table has things to try.',
                    bench, camera={'at': [1.1, 1.7, 3.0], 'look': [0.0, 1.3, 1.7]})


TRY = {
    'garden': ('TRY\n\nSet "flowers left" to 1 and\nwatch one flower closely.\n\n'
               'Each petal is twenty turns\nof 18 degrees -- a full\nturn. In the letters box,\nwhat if "move yaw" said 20?\n\n'
               'Sweep a flower up with\nDusty: one thing -- stem,\nleaves and petals (the pen\nwent invisible between\nthem).'),
    'clockwork': ('TRY\n\nSet "ticks left" to 30:\nwhich planet gets all the\nway round? Then 60.\n\n'
                  'Open the blue planet\'s\nrecord and change "degrees\nper tick" from 6 to 12.\nPredict the moon.\n\n'
                  'The tracks are drawn for\nthe presets; the planets\nfollow the numbers.'),
    'fountain': ('TRY\n\nSet "gravity per tick" to\n-1/250 (half). Predict the\nheight of the arches.\n\n'
                 'Set "lifetime per burst" to\n15: do the sparks come\ndown before they hide?\n\n'
                 'Set "sideways speed" to 0.\nWhat shape is a burst then?'),
}


def write_json(name, rec):
    out = os.path.join(HERE, name)
    io.open(out, 'w', encoding='utf-8', newline='\n').write(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
    print('wrote', name)


if __name__ == '__main__':
    write_json('\U0001f337 flower-garden.world.json', garden())
    write_json('\U0001f52d planetary-clockwork.world.json', clockwork())
    write_json('\U0001f386 firework-fountain.world.json', fountain())
