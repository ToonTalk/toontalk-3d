# -*- coding: utf-8 -*-
# A compact reading of an ORIGINAL ToonTalk city or object: every robot's
# label, the shape of its thought bubble, and its actions in order. The .cty
# and .tt files at toontalk.github.io/tt-wasm are zips of XML; unzip one and
# point this at its data.xml. Written to read Resort Infinity's machinery
# before rebuilding the resort in its shape.
import re, io, sys
import xml.etree.ElementTree as ET
NS = '{http://www.toontalk.com}'
src = sys.argv[1] if len(sys.argv) > 1 else 'resort_infinity.xml.cty.data.xml'
s = io.open(src, encoding='utf-8', errors='replace').read()
root = ET.fromstring(s)

def tag(e): return e.tag.replace(NS, '')

def shape(e, depth=0):
    t = tag(e)
    lab = e.find(NS + 'Label')
    lt = ('"' + lab.text.strip().replace('\n', ' ') + '"') if lab is not None and lab.text else ''
    erased = e.find(NS + 'Erased') is not None
    if t == 'Box':
        holes = e.findall(NS + 'Hole')
        parts = []
        for h in holes:
            inner = [c for c in h if tag(c) not in ('Label',)]
            hl = h.find(NS + 'Label')
            hlt = (hl.text.strip() + ':') if hl is not None and hl.text else ''
            parts.append(hlt + (shape(inner[0], depth + 1) if inner else '_'))
        return ('[' + ' | '.join(parts) + ']' + (lt if depth == 0 else '') + ('~' if erased else ''))
    if t == 'Integer':
        return ('int' if erased else (e.text or '?').strip()) + lt
    if t == 'TextPad':
        tv = e.find(NS + 'TextValue')
        return ('text' if erased else '"' + ((tv.text or '') if tv is not None else '').strip()[:30] + '"') + lt
    if t == 'Bird': return 'bird' + lt + ('~' if erased else '')
    if t == 'Nest': return 'nest' + lt + ('~' if erased else '')
    if t == 'Robot':
        l = e.find(NS + 'Label'); return 'robot' + (('"' + l.text.strip().replace('\n',' ') + '"') if l is not None and l.text else '')
    if t == 'Picture' or t == 'PictureOf': return 'picture' + lt
    if t == 'RemoteControl': return 'sensor' + lt
    return t + lt

def actions(a):
    out = []
    for c in a:
        t = tag(c)
        txt = (c.text or '').strip()
        extra = ''
        if t == 'TypeTo': extra = ' ' + c.get('KeyDescription', '')
        if t == 'MadeOrMoved': extra = ' type' + c.get('TypeCode', '')
        out.append(t + extra + ('>' + txt if txt else ''))
    return out

for r in root.iter(NS + 'Robot'):
    l = r.find(NS + 'Label'); name = l.text.strip().replace('\n', ' ') if l is not None and l.text else '?'
    tb = r.find(NS + 'ThoughtBubble')
    inner = [c for c in tb if tag(c) not in ('GeometricRelationToContainer', 'Active', 'SeeAll', 'VolatileAttributes', 'Erased')] if tb is not None else []
    th = shape(inner[0]) if inner else '?'
    a = r.find(NS + 'Actions')
    nxt = r.find(NS + 'Next')
    print('ROBOT', name)
    print('  thought:', th)
    if a is not None: print('  actions:', ' ; '.join(actions(a)))
    if nxt is not None: print('  has team member')
