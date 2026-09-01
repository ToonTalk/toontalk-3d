# The second half of the shelf -- the six that wanted a sayable SIZE or
# arithmetic on what the touch channel hands over. Both exist now, so these
# are ordinary robots sending ordinary messages, like everything else here.
#
# Two idioms are new to this file and worth naming:
#
# DOZING ON TOUCH. The touch nest of these gadgets starts EMPTY, and the
# robots' conditions read its top -- so the whole team DOZES until something
# actually touches the thing. The workshop announces a touch only when the
# contact CHANGES, and the robot eats the announcement it acted on; so "grow
# when touched" grows once per touch, not sixty times a second, and a gadget
# nobody is touching costs nothing at all. (The gadgets that must MOVE every
# round -- bouncing, reversing -- keep a seeded reading instead: a dozing
# member stops its whole team, mover included.)
#
# COMPARISON IS A SCALE. The speed limit weighs the across-speed against the
# limit on an ordinary scale and dispatches on the lean. There is no "if"
# anywhere -- the scale is the if.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beh import *                                          # noqa: F403

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'sounds'))
from _snd import seg, sound                                 # noqa: F401


def touch_nest(lid, nid, side=None, empty=False):
    """The thing's touch channel. empty=True is the dozing idiom: the team
    sleeps until a real announcement arrives."""
    pile = [] if empty else [box(txt('nothing'), txt(side or 'none'))]   # noqa: F405
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#touch',
            'hasEgg': False, 'label': 'touching', 'pile': pile}


# a touch announcement: [what I ran into | which side of me]. The first hole
# holds a bird when it is a real thing, and the pad "nothing" as contact ends.
hit_box = lambda side=None: box(WILD, txt(side) if side else WILDTEXT)   # noqa: E731,F405

# ---------------------------------------------------------------- 7 & 8
def sized(title, lid, n, d):
    step = msg('move', 'size', num(n, d))                    # noqa: F405
    t_on = lambda side: box(to(lid), touch_nest(lid, 0, side), step)   # noqa: E731,F405
    quiet = robot('contact ends', box(ANYBIRD, hit_box('none'), ANYBOX),   # noqa: F405
                  [takeTop('given', 1), put('s0'), vac('s0')],             # noqa: F405
                  trained_on=t_on('none'))
    act = robot(title, box(ANYBIRD, hit_box(), ANYBOX),      # noqa: F405
                [takeTop('given', 1), put('s0'), vac('s0'),  # noqa: F405
                 copy('given', 2), put('given', 0)],         # noqa: F405
                trained_on=t_on('left'))
    team = dict(quiet)
    team['team'] = [act]
    work = box(to(lid, 'my thing'), touch_nest(lid, 0, empty=True), step)   # noqa: F405
    return gadget(title, lid, team, work)                    # noqa: F405


# BUMPED, not touched: being touched is what a click does, and a click picks
# a thing up. This is one thing running into another.
growing = sized('grow when bumped', 'G907', 1, 4)
shrinking = sized('shrink when bumped', 'G908', -1, 4)

# ---------------------------------------------------------------- 9 sound
SND = 'G909'
BELL = 'G909S'
bell = live(dict(sound(seg(880, 0.14, 'triangle'), seg(1318, 0.22, 'triangle'),
                       label='ding')), BELL)
s_play = txt('play')                                          # noqa: F405
s_on = lambda side: box(touch_nest(SND, 0, side),             # noqa: E731,F405
                        to(BELL), s_play, bell)
s_quiet = robot('contact ends', box(hit_box('none'), ANYBIRD, WILDTEXT, WILD),   # noqa: F405
                [takeTop('given', 0), put('s0'), vac('s0')],               # noqa: F405
                trained_on=s_on('none'))
s_act = robot('ding on a hit', box(hit_box(), ANYBIRD, WILDTEXT, WILD),          # noqa: F405
              [takeTop('given', 0), put('s0'), vac('s0'),                  # noqa: F405
               copy('given', 2), put('given', 1)],                         # noqa: F405
              trained_on=s_on('left'))
s_team = dict(s_quiet)
s_team['team'] = [s_act]
s_work = box(touch_nest(SND, 0, empty=True), to(BELL, 'the bell'),          # noqa: F405
             s_play, bell)
sounding = gadget('make a sound on hit', SND, s_team, s_work)               # noqa: F405

# ---------------------------------------------------------------- 10 reverse
# This one MOVES every round, so its touch nest is a seeded READING like the
# ball's: a dozing member would stop the mover. Against a contact, flipping
# is not safe (half the time it turns you INTO the thing) -- so each side
# SETS the step away from what was hit, exactly as Pong's ball does.
REV = 'G910'
r_across = msg('move', 'across', num(1, 50))                  # noqa: F405
r_away = msg('move', 'away', num(1, 80))                      # noqa: F405
r_on = lambda side: box(to(REV), r_across, r_away,            # noqa: E731,F405
                        touch_nest(REV, 0, side))
r_cond = lambda side: box(ANYBIRD, ANYBOX, ANYBOX,            # noqa: E731,F405
                          hit_box(side))


def r_head(hole, n, d):
    return [vac('given', hole, 2), newnum,                    # noqa: F405
            setv(n, '+', d), put('given', hole, 2)]           # noqa: F405


r_fly = [copy('given', 1), put('given', 0),                   # noqa: F405
         copy('given', 2), put('given', 0)]                   # noqa: F405
r_lead = robot('thing on my left', r_cond('left'), r_head(1, 1, 50) + r_fly,
               trained_on=r_on('left'))
r_lead['team'] = [
    robot('thing on my right', r_cond('right'), r_head(1, -1, 50) + r_fly,
          trained_on=r_on('right')),
    robot('thing on my near side', r_cond('near'), r_head(2, -1, 80) + r_fly,
          trained_on=r_on('near')),
    robot('thing on my far side', r_cond('far'), r_head(2, 1, 80) + r_fly,
          trained_on=r_on('far')),
    robot('moving', r_cond(None), r_fly, trained_on=r_on('none')),
]
r_work = box(to(REV, 'my thing'), r_across, r_away, touch_nest(REV, 0))   # noqa: F405
reversing = gadget('reverse on collision', REV, r_lead, r_work)           # noqa: F405

# ---------------------------------------------------------------- 11 limit
# [my thing | its #speed channel | a scale | the limit | the cap message].
# The team dozes on the channel. A speed arrives: the WEIGHER puts its
# across-number on one pan and the limit on the other. Next round the lean
# decides: leaning to the speed, the CAPPER sends [set | speed | [1/2 | ]]
# (the empty hole leaves away alone) and clears the pans; any other lean,
# the CLEARER just clears.
LIM = 'G911'
l_nest = lambda: {'kind': 'nest', 'id': 0,                    # noqa: E731
                  'guid': 'evt-' + LIM + '#speed', 'hasEgg': False,
                  'label': 'speed', 'pile': [box(num(9, 10), num(0))]}   # noqa: F405
l_limit = num(1, 2)                                           # noqa: F405
l_cap = msg('set', 'speed', box(num(1, 2), None))             # noqa: F405
l_on = box(to(LIM), l_nest(), scale(None, None), l_limit, l_cap)   # noqa: F405
capper = robot('over the limit',
               box(ANYBIRD, ANYNEST, tilt('L'), ANYNUM, ANYBOX),   # noqa: F405
               [copy('given', 4), put('given', 0),            # noqa: F405
                vac('given', 2, 0), vac('given', 2, 1)],      # noqa: F405
               trained_on=l_on)
clearer = robot('weighed and fine',
                box(ANYBIRD, ANYNEST, scale(ANYNUM, ANYNUM), ANYNUM, ANYBOX),  # noqa: F405
                [vac('given', 2, 0), vac('given', 2, 1)],     # noqa: F405
                trained_on=l_on)
weigher = robot('a speed arrives',
                box(ANYBIRD, box(ANYNUM, ANYNUM), scale(None, None), ANYNUM, ANYBOX),  # noqa: F405
                [takeTop('given', 1), put('s0'),              # noqa: F405
                 take('s0', 0), put('given', 2, 0),           # noqa: F405
                 copy('given', 3), put('given', 2, 1),        # noqa: F405
                 vac('s0')],                                  # noqa: F405
                trained_on=l_on)
l_team = dict(capper)
l_team['team'] = [clearer, weigher]
l_work = box(to(LIM, 'my thing'), l_nest(), scale(None, None), l_limit, l_cap)  # noqa: F405
limiting = dict(gadget('speed limit', LIM, l_team, l_work),   # noqa: F405
                speed={'x': 0.9, 'z': 0})       # born too fast, on purpose

# ---------------------------------------------------------------- 12 score
SCR = 'G912'
TALLY = 'G912S'
tally = live(dict(num(0), label='the score'), TALLY)          # noqa: F405
one = num(1)                                                  # noqa: F405
c_on = lambda side: box(touch_nest(SCR, 0, side),             # noqa: E731,F405
                        to(TALLY), one, tally)
c_quiet = robot('contact ends', box(hit_box('none'), ANYBIRD, ANYNUM, ANYNUM),    # noqa: F405
                [takeTop('given', 0), put('s0'), vac('s0')],              # noqa: F405
                trained_on=c_on('none'))
c_act = robot('one for a hit', box(hit_box(), ANYBIRD, ANYNUM, ANYNUM),           # noqa: F405
              [takeTop('given', 0), put('s0'), vac('s0'),                 # noqa: F405
               copy('given', 2), put('given', 1)],                        # noqa: F405
              trained_on=c_on('left'))
c_team = dict(c_quiet)
c_team['team'] = [c_act]
c_work = box(touch_nest(SCR, 0, empty=True), to(TALLY, 'the score'),       # noqa: F405
             one, tally)
scoring = gadget('send 1 to the score when hit', SCR, c_team, c_work)      # noqa: F405

# ------------------------------------------------- 15 reverse AT A SPEED
# The same four sides, one box deeper, and no mover: hole 1 is the whole
# message [set | speed | [across | away]] and each robot fills in ONE of the
# two, leaving the other hole EMPTY so the axis it says nothing about is left
# alone. No mover means the touch nest can be the dozing kind: between
# contacts this gadget costs nothing at all.
RSP = 'G917'
rs_msg = lambda a, b: msg('set', 'speed', box(a, b))         # noqa: E731,F405
rs_work = lambda side=None, empty=True: box(                 # noqa: E731,F405
    to(RSP, 'my thing'), rs_msg(None, None),                 # noqa: F405
    touch_nest(RSP, 9171, side, empty=empty))
rs_on = lambda side: box(to(RSP), rs_msg(None, None),        # noqa: E731,F405
                         touch_nest(RSP, 9171, side, empty=False))
rs_cond = lambda side: box(ANYBIRD, ANYBOX, hit_box(side))   # noqa: E731,F405


def rs_set(hole, n, d):
    """Put a fresh number in ONE hole of the speed box and clear the other,
    so the message speaks about a single axis."""
    other = 1 - hole
    return [vac('given', 1, 2, hole), vac('given', 1, 2, other),   # noqa: F405
            newnum, setv(n, '+', d), put('given', 1, 2, hole)]     # noqa: F405


# hand the speed over, then eat the announcement and go back to sleep
rs_fly = [copy('given', 1), put('given', 0),                 # noqa: F405
          takeTop('given', 2), put('s0'), vac('s0')]         # noqa: F405
rs_lead = robot('thing on my left', rs_cond('left'),         # noqa: F405
                rs_set(0, 9, 20) + rs_fly, trained_on=rs_on('left'))
rs_lead['team'] = [
    robot('thing on my right', rs_cond('right'),             # noqa: F405
          rs_set(0, -9, 20) + rs_fly, trained_on=rs_on('right')),
    robot('thing on my near side', rs_cond('near'),          # noqa: F405
          rs_set(1, -11, 40) + rs_fly, trained_on=rs_on('near')),
    robot('thing on my far side', rs_cond('far'),            # noqa: F405
          rs_set(1, 11, 40) + rs_fly, trained_on=rs_on('far')),
    # contact ending is an announcement too: eat it and sleep again
    robot('contact ends', box(ANYBIRD, ANYBOX, hit_box('none')),   # noqa: F405
          [takeTop('given', 2), put('s0'), vac('s0')],             # noqa: F405
          trained_on=rs_on('none')),
]
reversing_speed = gadget('reverse a speed on collision', RSP,   # noqa: F405
                         rs_lead, rs_work())

SIX = {'growing': growing, 'shrinking': shrinking, 'sounding': sounding,
       'reversing': reversing, 'limiting': limiting, 'scoring': scoring,
       'reversing_speed': reversing_speed}
