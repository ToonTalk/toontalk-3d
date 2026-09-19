# Resort Infinity, problems 3 to 5 -- the original's other three, each a
# world of its own that opens where the last one ended (Ken, 19 Sep 2026:
# "We never did problems 3 to 5 for Infinity Resort";
# toontalk.com/Tools/Infinity/Doc/resort_infinity_guide.htm).
#
#   Problem 3  a new infinite group arrives. Everybody housed moves from i
#              to 2i; the newcomers take the odd cottages, 2i - 1.
#   Problem 4  three infinite groups arrive. Everybody moves from i to 4i;
#              a newcomer i of group j takes 4i - j.
#   Problem 5  an infinite number of infinite groups. Everybody moves from
#              i to 2i, and a newcomer (i, j) takes the odd cottage 2n - 1
#              where n counts the grid by growing squares (Barrow):
#                 n = j^2 - (i - 1)   if i <= j
#                 n = (i - 1)^2 + j   if i >= j
#
# THE LETTER CARRIES THE GROUP NOW, as the original's did: a newcomer writes
# [my number | my group | bird] to the front desk. The moving office's letter
# is [where I live | bird], as before. The guests' machinery, the desk, the
# office, the mist and the row are make_resort.py's; what changes is who
# stands where when the world opens, and the arithmetic that is yours.
#
# EVERYBODY HOUSED IS LISTENING: the macro pad of the housed guests is saved
# `running`, so their behaviours are switched on when the world opens and the
# bell reaches them (a behaviour saved running opens running, 19 Sep).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403
import make_resort as R

WILDTEXT = R.WILDTEXT
DESK_ID, DESK_G, BELL = R.DESK_ID, R.DESK_G, R.BELL
OFFICE_ID, OFFICE_G = R.OFFICE_ID, R.OFFICE_G
STEP_N, STEP_D, OFF_N, OFF_D, ROW_N, ROW_D = R.STEP_N, R.STEP_D, R.OFF_N, R.OFF_D, R.ROW_N, R.ROW_D
COTTAGE_Z = R.COTTAGE_Z
msg, dropf, live_bird = R.msg, R.dropf, R.live_bird
cottage_x = lambda n: n * 0.6 - 4.5                        # noqa: E731


# --- one guest's behaviour, with a group ------------------------------------
# 0 the desk | 1 my nest | 2 my own bird | 3 my number | 4 my place
# 5 [set | position | _] | 6 the moving office | 7 a bell kept for later | 8 my group
# A guest already housed opens with its number taken (it asked once) and its
# place in hole 4, standing at that cottage; a newcomer at the gate has its
# number and no place.
def guest_gadget(k, number, group, lid, gid, housed_at=None):
    mail = (9700 + k, 'resort-guest-%d' % k)
    mine = nest(*mail, label='my post')                    # noqa: F405
    mine['aliases'] = [BELL]
    work = box(bird(DESK_ID, DESK_G, label='the desk'),    # noqa: F405
               mine,
               bird(*mail, label='my own bird'),           # noqa: F405
               None if housed_at else num(number),         # noqa: F405
               num(housed_at) if housed_at else None,      # noqa: F405
               msg('set', 'position'),
               bird(OFFICE_ID, OFFICE_G, label='the moving office'),   # noqa: F405
               None,
               num(group))                                 # noqa: F405
    any_ = [ANYBIRD, None, ANYBIRD, None, None, ANYBOX, ANYBIRD, None, WILD]   # noqa: F405

    def cond(**at):
        c = list(any_)
        for i, v in at.items():
            c[int(i[1:])] = v
        return box(*c)                                     # noqa: F405

    ask = robot(                                           # noqa: F405
        'Ask for a place', cond(h3=ANYNUM),                # noqa: F405
        [newbox, holes(3), put('s0'),                      # noqa: F405
         take('given', 3), put('s0', 0),                   # my number -- taken, so I ask once  # noqa: F405
         copy('given', 8), put('s0', 1),                   # my group  # noqa: F405
         copy('given', 2), put('s0', 2),                   # ...and a bird of my own to answer  # noqa: F405
         take('s0'), put('given', 0)],                     # off to the desk  # noqa: F405
        trained_on=work,
        note='Leads. My number is still in the box, so I have nowhere to live: sends [my number, my group, my own bird] to the desk and takes my number out as it goes, so I never ask twice.')
    stand = robot(                                         # noqa: F405
        'Stand at my address', cond(h1=ANYNUM),            # noqa: F405
        [copy('given', 5), put('s0'),                      # noqa: F405
         newbox, holes(2), put('s0', 2),                   # noqa: F405
         takeTop('given', 1), put('s0', 2, 0),             # noqa: F405
         copy('s0', 2, 0), put('given', 4),                # noqa: F405
         ] + dropf(STEP_N, STEP_D, '*', 's0', 2, 0)
        + dropf(OFF_N, OFF_D, '-', 's0', 2, 0)
        + [newnum, setv(ROW_N, '+', ROW_D), put('s0', 2, 1),   # noqa: F405
           take('s0'), put('perch')],                      # noqa: F405
        note='A number has landed on my nest: that is my address. Works out where that cottage stands along the row, remembers it as my place, and walks there.')
    move = robot(                                          # noqa: F405
        'Move when told to', cond(h1=WILDTEXT, h4=ANYNUM),   # noqa: F405
        [takeTop('given', 1), put('s1'), vac('s1'),        # noqa: F405
         newbox, holes(2), put('s0'),                      # noqa: F405
         take('given', 4), put('s0', 0),                   # noqa: F405
         copy('given', 2), put('s0', 1),                   # noqa: F405
         take('s0'), put('given', 6)],                     # noqa: F405
        note='A pad has landed on my nest: the bell, rung for every guest. Sends [where I live, my own bird] to the moving office and takes my place out of the box, so that the answer puts a new one in.')
    move_kept = robot(                                     # noqa: F405
        'Move on the bell I kept', cond(h7=WILDTEXT, h4=ANYNUM),   # noqa: F405
        [take('given', 7), put('s1'), vac('s1'),           # noqa: F405
         newbox, holes(2), put('s0'),                      # noqa: F405
         take('given', 4), put('s0', 0),                   # noqa: F405
         copy('given', 2), put('s0', 1),                   # noqa: F405
         take('s0'), put('given', 6)],                     # noqa: F405
        note='The bell rang before I had a place, and the pad was kept in hole 7. Now that I have one: the same as Move when told to, on the kept pad.')
    hold = robot(                                          # noqa: F405
        'Keep the bell for later', cond(h1=WILDTEXT),      # noqa: F405
        [takeTop('given', 1), put('given', 7)],            # noqa: F405
        note='The bell rang before I had a place (Move when told to did not fit): takes the pad off my nest into hole 7, which uncovers the address under it.')
    who = ('guest %d' % number) if group == 1 else ('guest %d of group %d' % (number, group))
    return {'kind': 'text', 'text': who, 'gadget': True,
            'lid': gid, 'evt': 'evt-' + gid, 'boundTo': lid,
            'note': ('This guest\u2019s own robots: ask the desk where to live (with its group number), walk to '
                     'the cottage it is given, and ask the moving office again when the bell rings.'),
            'look': {'bg': '#2b2238', 'ink': '#ecd9ff', 'font': 'sans', 'h': 0.34},
            'panel': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {'stand': work},
                      'active': dict(ask, team=[move_kept, move, hold, stand])}}


# --- the front desk, for a three-hole letter --------------------------------
ANYROBOT = R.ANYROBOT
newroom, grass_ = R.newroom, R.grass_
tidy3 = robot(                                             # noqa: F405
    'Tidy', box(None, WILD, ANYBIRD),                      # the letter once your robot has taken its number  # noqa: F405
    [vac('given')],                                        # noqa: F405
    note='Rides in the little house behind your robot: once your robot has taken the number off the letter and answered it, sweeps the letter away, and the house folds itself up.')


def front_desk3():
    post = nest(DESK_ID, DESK_G, label='the post')         # noqa: F405
    rid, rguid = R.ROBOT_NESTS[DESK_G]
    holes_ = [post, nest(rid, rguid, label='your robot'), None, tidy3]   # noqa: F405
    c = lambda **at: box(*[at.get('h%d' % k) for k in range(4)])   # noqa: E731,F405
    take_in = robot(                                       # noqa: F405
        'Take the robot in', c(h1=ANYROBOT),
        [takeTop('given', 1), put('given', 2)],            # noqa: F405
        note='A robot has landed on its nest: yours. Takes it into hole 2.')
    run = robot(                                           # noqa: F405
        'Run your robot on the letter', c(h0=box(ANYNUM, ANYNUM, ANYBIRD), h2=ANYROBOT),   # noqa: F405
        [newroom, put('s1'),                               # noqa: F405
         takeTop('given', 0), put('s1'),                   # noqa: F405
         copy('given', 2), put('s2'),                      # noqa: F405
         copy('given', 3), put('s2'),                      # noqa: F405
         take('s2'), put('s1'),                            # noqa: F405
         take('s1'), grass_],                              # noqa: F405
        note='A letter [number | group | bird] lies on the post and your robot is in hole 2: takes a fresh little house, puts the letter in it, then a copy of your robot with a copy of Tidy behind it, and sets the house down on the grass to work.')
    return room('the front desk', box(*holes_), dict(run, team=[take_in]), opaque=True, dirty=True)   # noqa: F405


# --- the practice letters -----------------------------------------------------
PRACTICE_ID, PRACTICE_G = R.PRACTICE_ID, R.PRACTICE_G
LETTER3 = lambda i, j, label: dict(box(num(i), num(j), bird(PRACTICE_ID, PRACTICE_G, label='to the practice nest')),   # noqa: E731,F405
                                   label=label)
LETTER2 = R.LETTER


# --- the answers, by the fence -----------------------------------------------
to_bird = lambda hole: [take('given', 0), put('given', hole)]   # noqa: E731,F405

odd_robot = robot(                                         # noqa: F405
    'Odd cottages', box(ANYNUM, ANYNUM, ANYBIRD),          # noqa: F405
    dropf(2, 1, '*', 'given', 0) + dropf(1, 1, '-', 'given', 0) + to_bird(2),
    trained_on=LETTER3(1, 2, 'a letter'),
    note='Problem 3, answered: newcomer i takes cottage 2i - 1, an odd one. Given [number | group | bird], drops a x2 and then a -1 on the number, takes it and gives it to the bird. The group does not matter here.')
double_robot = robot(                                      # noqa: F405
    'Double', box(ANYNUM, ANYBIRD),                        # noqa: F405
    dropf(2, 1, '*', 'given', 0) + to_bird(1),
    trained_on=LETTER2(1, 'a letter'),
    note='Problems 3 and 5, answered: everybody housed moves from i to 2i, which empties every odd cottage. Given [where I live | bird], drops a x2 on the number, takes it and gives it to the bird.')
four_apart_robot = robot(                                  # noqa: F405
    'Four apart', box(ANYNUM, ANYNUM, ANYBIRD),            # noqa: F405
    dropf(4, 1, '*', 'given', 0)                           # 4i
    + [copy('given', 1), setop('-'), put('given', 0)]      # ... - j  # noqa: F405
    + to_bird(2),
    trained_on=LETTER3(1, 2, 'a letter'),
    note='Problem 4, answered: newcomer i of group j takes cottage 4i - j. Given [number | group | bird], drops a x4 on the number, then a copy of the group with a minus sign, takes the number and gives it to the bird.')
four_times_robot = robot(                                  # noqa: F405
    'Four times', box(ANYNUM, ANYBIRD),                    # noqa: F405
    dropf(4, 1, '*', 'given', 0) + to_bird(1),
    trained_on=LETTER2(1, 'a letter'),
    note='Problem 4, answered: everybody housed moves from i to 4i, which empties three cottages in every four. Given [where I live | bird], drops a x4 on the number, takes it and gives it to the bird.')

# Problem 5: growing squares. Weigh i against j on a scale; then one of two
# sums, and the odd cottage 2n - 1.
weigh = robot(                                             # noqa: F405
    'Weigh', box(ANYNUM, ANYNUM, ANYBIRD),                 # noqa: F405
    [newscale, put('s0'),                                  # noqa: F405
     take('given', 0), put('s0', 0),                       # my number on the left pan  # noqa: F405
     take('given', 1), put('s0', 1),                       # my group on the right  # noqa: F405
     take('s0'), put('given', 0)],                         # the scale takes the number's place  # noqa: F405
    trained_on=LETTER3(1, 2, 'a letter'),
    note='Leads. Given [number | group | bird]: puts the number on the left pan of a fresh scale and the group on the right, and the scale in the number\u2019s place. Which way it tips says which sum to use.')
odd = lambda: dropf(2, 1, '*', 's1') + dropf(1, 1, '-', 's1')   # 2n - 1  # noqa: E731
below = robot(                                             # noqa: F405
    'Number below group', box(tilt('R'), None, ANYBIRD),   # the right pan, the group, is heavier  # noqa: F405
    [copy('given', 0, 1), put('s1'),                       # j  # noqa: F405
     copy('given', 0, 1), setop('*'), put('s1'),           # j x j  # noqa: F405
     copy('given', 0, 0), setop('-'), put('s1'),           # - i  # noqa: F405
     ] + dropf(1, 1, '+', 's1')                            # + 1: n = j^2 - (i - 1)
    + odd()
    + [take('s1'), put('given', 2), vac('given', 0)],      # to the bird; the scale swept away  # noqa: F405
    note='The scale tips right: my number is below my group (i < j). n = j^2 - (i - 1): a copy of the group, the group times it, the number taken off, one added. Then the odd cottage 2n - 1, to the bird, and the scale swept away.')
above = robot(                                             # noqa: F405
    'Number above group', box(tilt('L'), None, ANYBIRD),   # noqa: F405
    [copy('given', 0, 0), put('s1'),                       # i  # noqa: F405
     ] + dropf(1, 1, '-', 's1')                            # i - 1
    + [copy('s1'), setop('*'), put('s1'),                  # (i - 1)^2  # noqa: F405
       copy('given', 0, 1), setop('+'), put('s1'),         # + j  # noqa: F405
       ] + odd()
    + [take('s1'), put('given', 2), vac('given', 0)],      # noqa: F405
    note='The scale tips left: my number is above my group (i > j). n = (i - 1)^2 + j: a copy of the number less one, times itself, the group added. Then the odd cottage 2n - 1, to the bird, and the scale swept away.')
level = dict(above, name='Number equals group', condition=box(tilt('='), None, ANYBIRD),   # noqa: F405
             note='The scale is level (i = j): either sum gives the same n; this is the second one.')
squares_robot = dict(weigh, team=[below, above, level])


# --- the yard -------------------------------------------------------------
def guest_model(name, lid, shirt):
    return R.guest(name, lid, shirt)


# EVERY GROUP HAS A COLOUR, and a guest is named by it -- "gold guest 3" --
# since group numbers start again with every problem (the original's did:
# each problem had a nest of its own) and "guest 1 of group 1" would name
# three different people by problem 5.
COLOURS = {'red': '#b8362b', 'blue': '#2b6fb8', 'gold': '#c9962a', 'green': '#3a8f4a',
           'plum': '#7a3f8f', 'teal': '#2aa1a1', 'rose': '#d46a8a', 'lime': '#8fb83a', 'brown': '#a15d2a'}


def housed(k, number, group, colour, place):
    """A guest at its cottage, listening."""
    lid, gid = 'GST%d' % k, 'G%d' % k
    return (guest_gadget(k, number, group, lid, gid, housed_at=place),
            {'thing': R.guest('%s guest %d' % (colour, number), lid, COLOURS[colour]),
             'x': cottage_x(place), 'z': 5.2})


def newcomer(k, number, group, colour, x, z):
    lid, gid = 'GST%d' % k, 'G%d' % k
    return (guest_gadget(k, number, group, lid, gid),
            {'thing': R.guest('%s guest %d' % (colour, number), lid, COLOURS[colour]),
             'x': x, 'z': z})


row = [{'thing': R.cottage(n), 'x': cottage_x(n), 'z': COTTAGE_Z} for n in range(1, 15)]
row.append({'thing': R.mist(), 'x': R.MIST_X, 'z': R.MIST_Z})

desk_things = lambda letters: [                            # noqa: E731
    {'thing': front_desk3(), 'x': -4.3, 'z': 3.4},
    {'thing': bird(*R.ROBOT_NESTS[DESK_G], label='to the front desk'), 'x': -3.6, 'z': 3.4},      # noqa: F405
    {'thing': R.moving_office, 'x': -2.6, 'z': 3.4},
    {'thing': bird(*R.ROBOT_NESTS[OFFICE_G], label='to the moving office'), 'x': -1.9, 'z': 3.4},   # noqa: F405
] + letters + [
    {'thing': nest(PRACTICE_ID, PRACTICE_G, label='the practice nest'), 'x': 0.5, 'z': 3.4},   # noqa: F405
]

TRAIN = ('HOW TO TRAIN ONE\n'
         '\n'
         'Take a little robot from its\n'
         'stack and set it on the grass.\n'
         'Drop a practice letter ON it:\n'
         'its thought bubble opens and\n'
         'you are teaching it.\n'
         '\n'
         'A number from the stack, typed\n'
         'and dropped on the letter\u2019s\n'
         'number, adds; Ctrl with the\n'
         'number held makes it multiply\n'
         'or subtract (the badge). Then\n'
         'the number to the bird.\n'
         '\n'
         'Ruby erases the numbers in\n'
         'its thought: any will do.\n'
         'Leave the bubble, click the\n'
         'robot to pick it up, and give\n'
         'it to the bird.')

FENCE = R.FENCE


def grass(housed_list, newcomers, macro):
    """The resort itself: the row, everybody, the two macros, the desks and
    their birds, the practice nest -- what a teacher world needs too."""
    gadgets_housed = [g for g, _ in housed_list]
    models = [m for _, m in housed_list] + [m for _, m in newcomers]
    housed_macro = R.macro('the guests already housed', 'MH', gadgets_housed,
                           {'bg': '#1f3b2c', 'ink': '#d9ffe8', 'font': 'sans', 'h': 0.42},
                           note=('The resort\u2019s own machinery for everybody already housed, one behaviour per '
                                 'guest, switched on: they are listening for the bell. Nothing in them knows '
                                 'how many guests there are.'))
    housed_macro['running'] = True
    return (row + models + [{'thing': housed_macro, 'x': 3.3, 'z': 6.2}, {'thing': macro, 'x': 3.3, 'z': 7.0}]
            + desk_things([]))


def write(name, about, problem, letters, housed_list, newcomers, macro, answers, extra_pads):
    bench_yard = (grass(housed_list, newcomers, macro) + letters + [
        {'thing': txt(about), 'x': 1.4, 'z': 3.2},        # noqa: F405
        {'thing': txt(problem), 'x': 2.6, 'z': 3.2},      # noqa: F405
        {'thing': txt(TRAIN), 'x': 2.0, 'z': 3.9},        # noqa: F405
        {'thing': txt(FENCE), 'x': 3.2, 'z': 3.9},        # noqa: F405
    ] + extra_pads + answers)
    world = {'kind': 'world', 'v': 3, 'bench': [{'thing': txt(R.INSIDE), 'x': -0.2, 'z': 1.6}],   # noqa: F405
             'stations': {}, 'active': None, 'yard': {'bench': bench_yard}}
    import json, io
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), name + '.world.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1, ensure_ascii=False))
    print('wrote', os.path.basename(out))


ABOUT3 = ('RESORT INFINITY 3\n'
          '\n'
          'You are the clerk again. The\n'
          'eleven cottages are full: the\n'
          'six red guests live at 6 to\n'
          '11, the five blue at 1 to 5,\n'
          'and the row goes on into the\n'
          'mist.\n'
          '\n'
          'A newcomer writes [my number\n'
          '| my group | bird] to the\n'
          'front desk now: the group\n'
          'says which arrival it came\n'
          'with. A housed guest still\n'
          'writes [where I live | bird]\n'
          'to the moving office.\n'
          '\n'
          'Set the Speed to 4x or 8x.')
P3 = ('PROBLEM 3\n'
      'A new infinite group\n'
      '\n'
      'Six gold guests wait at the\n'
      'gate -- group 2 -- and more\n'
      'are behind them for ever.\n'
      'Every cottage is taken, and\n'
      'adding five will not do: the\n'
      'group has no end.\n'
      '\n'
      'First a mover: given [where I\n'
      'live | bird], where does a\n'
      'housed guest go so that\n'
      'infinitely many cottages come\n'
      'free? Give it to the bird "to\n'
      'the moving office".\n'
      'Then a clerk for the desk:\n'
      'given [number | group | bird],\n'
      'which free cottage does\n'
      'newcomer i take? Give it to\n'
      '"to the front desk", then SPACE\n'
      'on "the gold group".\n'
      '\n'
      'Hint: think even and odd.')

ABOUT4 = ('RESORT INFINITY 4\n'
          '\n'
          'Problem 3 is solved: the guests\n'
          'who were here moved from i to\n'
          '2i (the even cottages, and on\n'
          'into the mist), and the gold\n'
          'group took the odd ones,\n'
          '2i - 1. The eleven you can see\n'
          'are full again.\n'
          '\n'
          'A newcomer writes [my number\n'
          '| my group | bird] to the\n'
          'front desk; a housed guest\n'
          'writes [where I live | bird]\n'
          'to the moving office.\n'
          '\n'
          'Set the Speed to 4x or 8x.')
P4 = ('PROBLEM 4\n'
      'Three infinite groups\n'
      '\n'
      'Three groups arrive at once --\n'
      'green is group 1, plum group\n'
      '2, teal group 3 -- each\n'
      'without end; three of each are\n'
      'at the gate.\n'
      '\n'
      'A mover for the office: given\n'
      '[where I live | bird], where\n'
      'does a housed guest go so\n'
      'that THREE cottages in every\n'
      'four come free?\n'
      'A clerk for the desk: given\n'
      '[number | group | bird], where\n'
      'does guest i of group j go?\n'
      'Then SPACE on "three groups".\n'
      '\n'
      'Hint: 4i, and 4i - j. Or\n'
      'do problem 3 three times.')

ABOUT5 = ('RESORT INFINITY 5\n'
          '\n'
          'Problem 4 is solved: the guests\n'
          'who were here moved from i to\n'
          '4i, and guest i of group j\n'
          'took 4i - j. The eleven you\n'
          'can see are full again.\n'
          '\n'
          'A newcomer writes [my number\n'
          '| my group | bird] to the\n'
          'front desk; a housed guest\n'
          'writes [where I live | bird]\n'
          'to the moving office.\n'
          '\n'
          'Set the Speed to 4x or 8x.')
P5 = ('PROBLEM 5\n'
      'Infinitely many infinite groups\n'
      '\n'
      'Groups 1, 2, 3, ... arrive --\n'
      'rose, lime, brown, and on\n'
      'without end -- each group\n'
      'itself without end. Three of\n'
      'the first three are at the\n'
      'gate.\n'
      '\n'
      'Move everybody from i to 2i:\n'
      'the odd cottages come free.\n'
      'Now number the newcomers:\n'
      'every (i, j) needs one whole\n'
      'number n of its own, and\n'
      'takes cottage 2n - 1.\n'
      '\n'
      'Count the grid by growing\n'
      'squares: n = j^2 - (i - 1) if\n'
      'i is at most j, and\n'
      '(i - 1)^2 + j if i is at\n'
      'least j. A robot that weighs\n'
      'i against j on a scale can\n'
      'tell the two apart. "Weigh",\n'
      'by the fence, does.')

SQUARES = ('WHY GROWING SQUARES\n'
           '\n'
           'Picture the newcomers as a\n'
           'grid: group j is row j, guest\n'
           'i is column i. Count the\n'
           'square of side 1, then the\n'
           'L that makes it a square of\n'
           'side 2, then the L for side\n'
           '3 ... Every (i, j) is reached\n'
           'in finite time, and no two\n'
           'get the same n.\n'
           '\n'
           '  (1,1)=1  (2,1)=2  (2,2)=3\n'
           '  (1,2)=4  (3,1)=5  (3,2)=6\n'
           '  (3,3)=7  (2,3)=8  (1,3)=9\n'
           '\n'
           'The classic answer -- the ith\n'
           'power of the jth prime --\n'
           'works too, and leaves most\n'
           'cottages empty for ever.')

GATE = lambda i, j: (-4.2 + 0.5 * (i - 1) + 1.7 * (j - 1), 7.0)   # noqa: E731
MACRO_LOOK = {'bg': '#3b2c1f', 'ink': '#ffe8d9', 'font': 'sans', 'h': 0.42}

def spec(n):
    """Problem n as data: who is housed where when it opens, who waits at the
    gate, the macro that lets them in, the answers, the pads."""
    if n == 3:
        # after problem 2: six red at 6..11, five blue at 1..5
        housed_ = [housed(k, k, 1, 'red', k + 5) for k in range(1, 7)] \
            + [housed(10 + k, k, 1, 'blue', k) for k in range(1, 6)]
        new = [newcomer(20 + k, k, 2, 'gold', *GATE(k, 1)) for k in range(1, 7)]
        macro = R.macro('the gold group', 'M3', [g for g, _ in new], MACRO_LOOK,
                        note='The same machinery for the six gold newcomers, group 2. Switch it on once your mover has moved everybody and the odd cottages stand empty.')
        return dict(name='\U0001f3e8 resort-infinity-3', about=ABOUT3, problem=P3, housed=housed_, new=new, macro=macro,
                    letter3=(4, 2), letter2=3, mover=double_robot, clerk=odd_robot, extra=[], group_colours='gold')
    if n == 4:
        # after problem 3: blue at 2i (2..10), gold at 2i - 1 (1..11); red 1 and 2 at 12 and 14 in the mist
        housed_ = [housed(10 + k, k, 1, 'blue', 2 * k) for k in range(1, 6)] \
            + [housed(20 + k, k, 2, 'gold', 2 * k - 1) for k in range(1, 7)] \
            + [housed(k, k, 1, 'red', 2 * (k + 5)) for k in (1, 2)]
        new = [newcomer(30 + 10 * j + i, i, j, c, *GATE(i, j)) for j, c in ((1, 'green'), (2, 'plum'), (3, 'teal')) for i in (1, 2, 3)]
        macro = R.macro('three groups', 'M4', [g for g, _ in new], MACRO_LOOK,
                        note='The same machinery for the nine newcomers: three green (group 1), three plum (group 2), three teal (group 3). Switch it on once your mover has moved everybody.')
        return dict(name='\U0001f3e8 resort-infinity-4', about=ABOUT4, problem=P4, housed=housed_, new=new, macro=macro,
                    letter3=(2, 3), letter2=3, mover=four_times_robot, clerk=four_apart_robot, extra=[], group_colours='green, plum and teal')
    # after problem 4: blue 1 at 8, gold 1 at 4, gold 2 at 12 (the mist), the nine at 4i - j
    housed_ = [housed(11, 1, 1, 'blue', 8), housed(21, 1, 2, 'gold', 4), housed(22, 2, 2, 'gold', 12)] \
        + [housed(30 + 10 * j + i, i, j, c, 4 * i - j) for j, c in ((1, 'green'), (2, 'plum'), (3, 'teal')) for i in (1, 2, 3)]
    new = [newcomer(60 + 10 * j + i, i, j, c, *GATE(i, j)) for j, c in ((1, 'rose'), (2, 'lime'), (3, 'brown')) for i in (1, 2, 3)]
    macro = R.macro('the groups', 'M5', [g for g, _ in new], MACRO_LOOK,
                    note='The same machinery for the newcomers at the gate: three rose (group 1), three lime (group 2), three brown (group 3) -- and there is no end of groups. Switch it on once your mover has moved everybody.')
    return dict(name='\U0001f3e8 resort-infinity-5', about=ABOUT5, problem=P5, housed=housed_, new=new, macro=macro,
                letter3=(2, 3), letter2=3, mover=double_robot, clerk=squares_robot, extra=[{'thing': txt(SQUARES), 'x': 4.4, 'z': 3.9}],   # noqa: F405
                group_colours='rose, lime and brown')


if __name__ == '__main__':
    for n in (3, 4, 5):
        S = spec(n)
        write(S['name'], S['about'], S['problem'],
              [{'thing': LETTER3(*S['letter3'], 'a practice letter'), 'x': -0.9, 'z': 3.4},
               {'thing': LETTER2(S['letter2'], 'a practice letter'), 'x': -0.2, 'z': 3.4}],
              S['housed'], S['new'], S['macro'],
              [{'thing': S['mover'], 'x': -4.4, 'z': 2.5},
               {'thing': S['clerk'], 'x': (1.0 if n == 5 else -3.6), 'z': 2.5}],   # a team stands deeper: clear of the desk's bird
              S['extra'])
