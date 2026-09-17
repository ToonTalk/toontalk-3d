# Resort Infinity -- Hilbert's hotel, in the yard.
#
# The original is a ToonTalk CITY: you are the clerk, guests arrive for ever,
# and you train a robot that says where each new guest's cottage is built --
# and, from problem 2, a second robot that tells the guests already housed
# where to move to. The city was an addressing scheme. This workshop has no
# cities; it has the yard, which suits the story better: a cottage is a house
# standing on the grass, an address is a place along the row, and the whole
# row shuffling up is something you watch happen.
#
# ONE NEST EACH, WHICH IS THE WHOLE DESIGN. A robot team stops at the first
# member whose thought is waiting on an empty nest -- that is what dozing IS
# -- so nobody here may doze on two nests. Everything a guest hears arrives on
# one nest of its own (under its own name, and the bell's, by ALIAS), and
# everything the clerk hears arrives on one nest on the desk. What lands says
# who runs:
#
#   a guest's nest    a NUMBER is an address to stand at
#                     a PAD is the bell: ask the moving office where to move to
#   the desk's nest   [number | bird]   -- a new guest asking where to live
#   the office's nest [number | bird]   -- a housed guest asking where to move
#
# WHAT IS GIVEN AND WHAT IS YOURS. Every cottage carries its own robots (in
# the macro pad "the guests", one behaviour per cottage): that is the resort's
# machinery and you never need to touch it. Each one asks the desk once, and
# stands wherever it is told -- x = n * 0.6 - 4.5 along the row.
#
# What is YOURS is the arithmetic, three steps of it: take the [number, bird]
# box off the post and give the bird the address. Problem 2's robot does the
# same with five added -- and it works in the MOVING OFFICE, a glass house by
# the desk with a post of its own, since the bench holds one working robot and
# the clerk is standing there. Ring the bell and every housed guest writes
# [where I live | bird] to the office post; drop your robot on the office and
# it answers each. (Ken: "the point of this activity is the user should come
# up with the solution... trains a robot that receives [cottage-number | bird]
# and computes cottage-number+5 and gives it to the bird. This robot is sent
# to the clerk who asks each guest for its number and then runs the robot
# with the appropriate box.") Both answers lie on the grass, by the fence, if
# you would rather read one than write one.
#
#   Problem 1  the first infinite group. Address = the guest's own number.
#   Problem 2  five more guests, and no empty cottages. Everyone already
#              housed moves up five; the newcomers take 1 to 5.
#
# Six and five are what fits on the grass. The fence pad says what the row
# does after that.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tt import *                                          # noqa: F403

WILDTEXT = {'kind': 'wildText'}
DESK_G = 'resort-desk'
BELL = 'resort-bell'
DESK_ID = 9790

# where cottage n stands: x = n * 0.6 - 4.5, along the row at z = 4.5; a
# guest housed there stands in front of it, at z = 5.2
STEP_N, STEP_D = 6, 10
OFF_N, OFF_D = 45, 10
ROW_N, ROW_D = 52, 10
COTTAGE_Z = 4.5

live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,
                                'liveId': lid, 'label': label}
msg = lambda verb, what: box(txt(verb), txt(what), None)   # noqa: F405
dropf = lambda n, d, op, *where: [newnum, setv(n, op, d), put(*where)]   # noqa: F405

DESK = lambda: box(nest(DESK_ID, DESK_G, label='the post'))   # noqa: F405,E731
OFFICE_ID, OFFICE_G = 9795, 'resort-office'
OFFICE = lambda: box(nest(OFFICE_ID, OFFICE_G, label='the office post'))   # noqa: F405,E731


# --- one guest's behaviour ---------------------------------------------------
# 0 the desk | 1 my nest | 2 my own bird | 3 my number
# 4 my place | 5 [set | position | _] | 6 the moving office | 7 a bell kept for later
#
# THE BELL BEFORE THE ADDRESS. Everything a guest hears lands on the one nest,
# and only the top of the pile can be seen. Rung before a guest was housed
# (the resort teacher rings it the moment the clerk is at work, and at
# Instant the clerk's answer is still in the air), the bell's pad lay on TOP
# of the address, and nobody's thought fitted: Stand wants a number on top,
# Move wants a place already set. So a fourth robot keeps the pad in hole 7
# for later, which uncovers the address, and a fifth moves on a KEPT pad once
# there is a place. The order matters, since a thought looking at the empty
# nest waits and stops the round there: the kept-pad robot looks only at holes
# and comes first; Move looks at the nest and waits when it is bare, which is
# how the guest dozes.
# (my thing -- the guest -- is the bird on the perch: the panel's own)
def guest_gadget(k, number, lid, gid):
    mail = (9700 + k, 'resort-guest-%d' % k)
    mine = nest(*mail, label='my post')                    # noqa: F405
    mine['aliases'] = [BELL]                               # ...and the bell reaches it too
    work = box(bird(DESK_ID, DESK_G, label='the desk'),    # noqa: F405
               mine,
               bird(*mail, label='my own bird'),           # noqa: F405
               num(number),                                # noqa: F405
               None,                                       # my place: empty until I am housed
               msg('set', 'position'),
               bird(OFFICE_ID, OFFICE_G, label='the moving office'),   # noqa: F405
               None)                                       # a bell heard before I had a place, kept
    any_ = [ANYBIRD, None, ANYBIRD, None, None, ANYBOX, ANYBIRD, None]   # noqa: F405

    def cond(**at):
        c = list(any_)
        for i, v in at.items():
            c[int(i[1:])] = v
        return box(*c)                                     # noqa: F405

    ask = robot(                                           # noqa: F405
        'Ask for a place', cond(h3=ANYNUM),                # noqa: F405
        [newbox, holes(2), put('s0'),                      # noqa: F405
         take('given', 3), put('s0', 0),                   # my number -- taken, so I ask once  # noqa: F405
         copy('given', 2), put('s0', 1),                   # ...and a bird of my own to answer  # noqa: F405
         take('s0'), put('given', 0)],                     # off to the desk  # noqa: F405
        trained_on=work,
        note='Leads. My number is still in the box, so I have nowhere to live: sends [my number, my own bird] to the desk and takes my number out as it goes, so I never ask twice.')

    stand = robot(                                         # noqa: F405
        'Stand at my address', cond(h1=ANYNUM),            # noqa: F405
        [copy('given', 5), put('s0'),                      # the [set | position | _] message  # noqa: F405
         newbox, holes(2), put('s0', 2),                   # an empty [across | away]  # noqa: F405
         takeTop('given', 1), put('s0', 2, 0),             # the address they gave me  # noqa: F405
         copy('s0', 2, 0), put('given', 4),                # ...which is my place from now on  # noqa: F405
         ] + dropf(STEP_N, STEP_D, '*', 's0', 2, 0)        # x = n * 0.6 ...
        + dropf(OFF_N, OFF_D, '-', 's0', 2, 0)             # ... - 4.5
        + [newnum, setv(ROW_N, '+', ROW_D), put('s0', 2, 1),   # the row  # noqa: F405
           take('s0'), put('perch')],                      # and I walk there: to the bird on the perch  # noqa: F405
        note='A number has landed on my nest: that is my address. Works out where that cottage stands along the row, remembers it as my place, and walks there.')

    move = robot(                                          # noqa: F405
        'Move when told to', cond(h1=WILDTEXT, h4=ANYNUM),   # noqa: F405
        [takeTop('given', 1), put('s1'), vac('s1'),        # the bell's pad, heard and thrown away  # noqa: F405
         newbox, holes(2), put('s0'),                      # noqa: F405
         take('given', 4), put('s0', 0),                   # where I live now -- taken  # noqa: F405
         copy('given', 2), put('s0', 1),                   # ...and my own bird  # noqa: F405
         take('s0'), put('given', 6)],                     # off to the moving office  # noqa: F405
        note='A pad has landed on my nest: the bell, rung for every guest. Sends [where I live, my own bird] to the moving office and takes my place out of the box, so that the answer puts a new one in.')

    move_kept = robot(                                     # noqa: F405
        'Move on the bell I kept', cond(h7=WILDTEXT, h4=ANYNUM),   # noqa: F405
        [take('given', 7), put('s1'), vac('s1'),           # the kept pad, thrown away  # noqa: F405
         newbox, holes(2), put('s0'),                      # noqa: F405
         take('given', 4), put('s0', 0),                   # noqa: F405
         copy('given', 2), put('s0', 1),                   # noqa: F405
         take('s0'), put('given', 6)],                     # noqa: F405
        note='The bell rang before I had a place, and the pad was kept in hole 7. Now that I have one: the same as Move when told to, on the kept pad.')

    hold = robot(                                          # noqa: F405
        'Keep the bell for later', cond(h1=WILDTEXT),      # noqa: F405
        [takeTop('given', 1), put('given', 7)],            # noqa: F405
        note='The bell rang before I had a place (Move when told to did not fit): takes the pad off my nest into hole 7, which uncovers the address under it.')

    return {'kind': 'text', 'text': 'guest %d' % number, 'gadget': True,
            'lid': gid, 'evt': 'evt-' + gid, 'boundTo': lid,
            'note': ('Guest %d\u2019s own three robots: ask the desk where to live, walk to '
                     'the cottage it is given, and ask again when the bell rings. They work on '
                     'guest %d, and on nothing else.' % (number, number)),
            'look': {'bg': '#2b2238', 'ink': '#ecd9ff', 'font': 'sans', 'h': 0.34},
            'panel': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {'stand': work},
                      'active': dict(ask, team=[move_kept, move, hold, stand])}}


def cottage(n):
    return {'kind': 'room', 'label': 'cottage %d' % n, 'opaque': True, 'dirty': False,
            'world': {'kind': 'world', 'v': 3, 'bench': [], 'stations': {}, 'active': None}}


# A GUEST IS A LITTLE PERSON: a model of solid shapes, the way Marty builds
# them, with a name plate. The first six wear red, the five who come later
# blue -- Ken: "make the guests a simple model of a person - the two colors
# (maybe clothing) are a good idea". Under 0.3 wide, since the cottages stand
# 0.6 apart.
SKIN, HAIR, TROUSERS, SHOES = '#e8b48c', '#4a2f1e', '#2f3140', '#1a1a1a'
def person(shirt):
    P = lambda shape, size, at, color: {'shape': shape, 'size': size, 'at': at, 'color': color}
    return [P('sphere', [0.062], [0, 0.44, 0], SKIN),                 # head
            P('sphere', [0.058], [0, 0.465, -0.012], HAIR),           # hair, a cap of it
            P('box', [0.16, 0.18, 0.09], [0, 0.29, 0], shirt),        # shirt
            P('box', [0.045, 0.16, 0.05], [-0.1, 0.29, 0], shirt),    # sleeves
            P('box', [0.045, 0.16, 0.05], [0.1, 0.29, 0], shirt),
            P('sphere', [0.024], [-0.1, 0.2, 0], SKIN),               # hands
            P('sphere', [0.024], [0.1, 0.2, 0], SKIN),
            P('box', [0.06, 0.17, 0.07], [-0.04, 0.115, 0], TROUSERS),   # legs
            P('box', [0.06, 0.17, 0.07], [0.04, 0.115, 0], TROUSERS),
            P('box', [0.065, 0.03, 0.09], [-0.04, 0.015, 0.01], SHOES),  # shoes
            P('box', [0.065, 0.03, 0.09], [0.04, 0.015, 0.01], SHOES)]


def guest(name, lid, shirt):
    return {'kind': 'model', 'parts': person(shirt), 'label': name,
            'lid': lid, 'evt': 'evt-' + lid}


def macro(name, lid, gadgets, look, note=None):
    return {'kind': 'text', 'text': name, 'gadget': True, 'lid': lid, 'evt': 'evt-' + lid,
            'look': look, 'note': note,
            'panel': {'kind': 'world', 'v': 3, 'stations': {}, 'active': None,
                      'bench': [{'thing': g, 'x': -0.6 + 0.3 * (i % 4), 'z': 1.3 + 0.3 * (i // 4)}
                                for i, g in enumerate(gadgets)]}}


# --- what is yours: two robots on a plain letter ----------------------------
# THE ORIGINAL'S SHAPE (Ken: "I have the feeling you've made it more complex
# than it needs to be. Maybe you can load the original city and the
# solutions"). In the city the player's Address Robot receives [guest # |
# group # | bird] and its whole program is two actions, pick up hole 1 and
# give it to the bird; the Move Robot receives [address | bird], types a 5
# onto the address and gives it to the bird; both go in a box to the Solution
# bird, and the robots on the back of a pad do the rest -- copy the robot,
# hand each copy a guest's box, run it. Nobody but the machinery touches a
# nest. So here: a robot is trained on a PRACTICE LETTER, [number | bird to
# the practice nest], and given to the bird "to the front desk" or "to the
# moving office". The office rings the bell itself when your robot arrives.
PRACTICE_ID, PRACTICE_G = 9794, 'resort-practice'
ANYROBOT = {'kind': 'anyRobot'}
LETTER = lambda n, label: dict(box(num(n), bird(PRACTICE_ID, PRACTICE_G, label='to the practice nest')),   # noqa: E731,F405
                               label=label)

address_robot = robot(                                     # noqa: F405
    'Next address', box(ANYNUM, ANYBIRD),                  # noqa: F405
    [take('given', 0), put('given', 1)],                   # the number, to the bird  # noqa: F405
    trained_on=LETTER(1, 'a letter'),
    note='Problem 1, answered: guest i lives at cottage i. Given a [number | bird] letter, takes the number and gives it to the bird.')

move_robot = robot(                                        # noqa: F405
    'Move up five', box(ANYNUM, ANYBIRD),                  # noqa: F405
    dropf(5, 1, '+', 'given', 0)                           # five more, dropped on the number
    + [take('given', 0), put('given', 1)],                 # ...and to the bird  # noqa: F405
    trained_on=LETTER(1, 'a letter'),
    note='Problem 2, answered: everybody moves up five, which empties cottages 1 to 5 for the newcomers. Given a [where I live | bird] letter, drops a +5 on the number, takes it and gives it to the bird.')

clerk = address_robot


# --- the machinery: two houses that run your robot ---------------------------
# 0 the post | 1 the robot's nest | 2 your robot | 3 Tidy | (4 the bird to every guest | 5 the bell's pad)
# Your robot flies to a nest of its own, not the post: a nest is a queue with
# the OLDEST on top, so a robot landing under six letters would never be
# seen. A robot on its nest is taken into hole 2 (and the office rings the
# bell then: the pad to every guest, whose nests answer to the bell's name).
# Every letter after that is run through a COPY of your robot in a fresh
# little house -- the truck of the original: a house from the stack onto a
# work spot, the letter into it (onto its stand), a copy of your robot with
# a copy of Tidy dropped on it (a team) into it -- a robot dropped on a house
# with a box on its stand sets the house going -- and the house set down on
# the grass, where it works on its own. Your robot answers the letter; then
# Tidy, whose thought fits the emptied letter, sweeps it away, and a house
# whose robot has swept its box away folds itself up. Your robot itself is
# never used up. (A house has no floor of its own: what a robot inside sets
# down goes on the grass, which is where the original's trucks built.)
newroom = {'type': 'newRoom'}
grass_ = {'type': 'put', 'at': {'c': 'ground', 'path': []}}
ROBOT_NESTS = {DESK_G: (9796, 'resort-front-robot'), OFFICE_G: (9797, 'resort-office-robot')}

tidy = robot(                                              # noqa: F405
    'Tidy', box(None, ANYBIRD),                            # the letter once your robot has taken its number  # noqa: F405
    [vac('given')],                                        # noqa: F405
    note='Rides in the little house behind your robot: once your robot has answered the letter, sweeps the empty letter away, and the house folds itself up.')


def machinery(post, bell):
    rid, rguid = ROBOT_NESTS[post['guid']]
    holes = [post, nest(rid, rguid, label='your robot'), None, tidy]   # noqa: F405
    if bell:
        holes += [bird(9792, BELL, label='to every guest'), txt('a move, please')]   # noqa: F405
    n = len(holes)
    c = lambda **at: box(*[at.get('h%d' % k) for k in range(n)])   # noqa: E731,F405
    take_in = robot(                                       # noqa: F405
        'Take the robot in', c(h1=ANYROBOT),
        [takeTop('given', 1), put('given', 2)]             # noqa: F405
        + ([copy('given', 5), put('given', 4)] if bell else []),   # the bell: the pad, to every guest  # noqa: F405
        note='A robot has landed on its nest: yours. Takes it into hole 2' + (', and rings the bell: the pad "a move, please" to every guest, who then writes where it lives.' if bell else '.'))
    run = robot(                                           # noqa: F405
        'Run your robot on the letter', c(h0=box(ANYNUM, ANYBIRD), h2=ANYROBOT),   # noqa: F405
        [newroom, put('s1'),                               # a fresh little house on a work spot  # noqa: F405
         takeTop('given', 0), put('s1'),                   # the letter, onto its stand  # noqa: F405
         copy('given', 2), put('s2'),                      # a copy of your robot...  # noqa: F405
         copy('given', 3), put('s2'),                      # ...with a copy of Tidy dropped on it: a team  # noqa: F405
         take('s2'), put('s1'),                            # into the house: it goes to work  # noqa: F405
         take('s1'), grass_],                              # ...and off the spot, onto the grass  # noqa: F405
        note='A letter lies on the post and your robot is in hole 2: takes a fresh little house, puts the letter in it, then a copy of your robot with a copy of Tidy behind it, and sets the house down on the grass to work.')
    # RUN FIRST. A team stops at the first member whose thought waits on an
    # empty nest, and once your robot is in hole 2 its nest is bare for good:
    # with Take in first, nothing behind it ever ran. Run first waits on the
    # post instead, which is the dozing a desk should do -- and before your
    # robot has come, hole 2 is empty, which is a plain no, so Take in gets
    # its turn. (The desk keeps the first robot it is given; to change it,
    # go in and swap hole 2 by hand.)
    return box(*holes), dict(run, team=[take_in])


FRONT_BOX, front_team = machinery(nest(DESK_ID, DESK_G, label='the post'), bell=False)      # noqa: F405
OFFICE_BOX, office_team = machinery(nest(OFFICE_ID, OFFICE_G, label='the office post'), bell=True)   # noqa: F405
front_desk = room('the front desk', FRONT_BOX, front_team, opaque=True, dirty=True)        # noqa: F405
moving_office = room('the moving office', OFFICE_BOX, office_team, opaque=True, dirty=True)   # noqa: F405

ABOUT = ('RESORT INFINITY\n'
      '\n'
      'You are the clerk. Eleven\n'
      'cottages stand in a row,\n'
      'numbered from the left. Guests\n'
      'arrive at the gate; every\n'
      'guest needs a cottage, and no\n'
      'two may share one.\n'
      '\n'
      'The guests write to the FRONT\n'
      'DESK, the house by the gate.\n'
      'The desk answers with a robot\n'
      'of yours: a robot given a\n'
      'letter, [number | bird], that\n'
      'gives the bird the cottage\n'
      'number. Train it, and give it\n'
      'to the bird "to the front\n'
      'desk". The desk does the rest.\n'
      '\n'
      'Set the Speed to 4x or 8x: a\n'
      'resort takes a while at\n'
      'walking pace.')


P1 = ('PROBLEM 1\n'
      'The first infinite group\n'
      '\n'
      'Six guests wait at the gate,\n'
      'numbered 1 to 6, and more are\n'
      'behind them for ever.\n'
      '\n'
      'Point at the pad "the guests",\n'
      'hand empty, and press SPACE:\n'
      'every guest writes to the\n'
      'front desk, [my number |\n'
      'bird], and waits.\n'
      '\n'
      'Train a robot that answers\n'
      'with a cottage number (see\n'
      'HOW TO TRAIN ONE), pick it up\n'
      'and give it to the bird "to\n'
      'the front desk". Or give her\n'
      '"Next address", by the fence.\n'
      'Each guest walks to its\n'
      'cottage.\n'
      '\n'
      'Which cottage should guest 1\n'
      'have?')


P2 = ('PROBLEM 2\n'
      'Five more, and no room\n'
      '\n'
      'Five more guests arrive and\n'
      'every cottage is taken. Nobody\n'
      'is turned away: everybody\n'
      'housed moves along, and the\n'
      'newcomers take 1 to 5.\n'
      '\n'
      'Train a robot that, given\n'
      '[where a guest lives | bird],\n'
      'gives the bird where to move\n'
      'to. Give it to the bird "to\n'
      'the moving office": the\n'
      'office rings the bell, every\n'
      'housed guest writes where it\n'
      'lives, and your robot answers\n'
      'each. Then SPACE on "five\n'
      'more guests".\n'
      '\n'
      'Why does this work here, and\n'
      'not in a hundred-room hotel?')


TRAIN = ('HOW TO TRAIN ONE\n'
      '\n'
      'Take a little robot from its\n'
      'stack and set it on the grass.\n'
      'Drop a practice letter ON it:\n'
      'its thought bubble opens and\n'
      'you are teaching it.\n'
      '\n'
      'Problem 1: click the number,\n'
      'then click the bird: it flies\n'
      'to the practice nest.\n'
      'Problem 2: take a number from\n'
      'the stack, type 5, drop it on\n'
      'the letter\u2019s number; then the\n'
      'number to the bird.\n'
      '\n'
      'Ruby erases the number in its\n'
      'thought: any number will do.\n'
      'Leave the bubble, click the\n'
      'robot to pick it up, and give\n'
      'it to the bird.')


FENCE = ('THE ROW GOES ON\n'
      '\n'
      'Eleven cottages stand in\n'
      'the clear, counted from the\n'
      'left, and a guest given a\n'
      'number walks to that cottage.\n'
      '\n'
      'The row does not stop at 11:\n'
      'it goes on into the mist.\n'
      'Cottages 12, 13 and 14 are\n'
      'in there, and all the rest\n'
      'behind them, as far as you\n'
      'like. A guest sent to 15\n'
      'walks in and is lost to view.\n'
      '\n'
      'Nothing in these robots knows\n'
      'how many guests there are.\n'
      'That is the whole of it.')


# THE MIST. Ken: a cloud obscuring cottages 12 and up, so the row is seen to
# go on rather than told to. A model of see-through puffs from just past
# cottage 11 to the fence, thin at the near edge and thicker with every step
# in, over the row and the guests' line in front of it. Cottages 12, 13 and
# 14 stand inside, real houses half-seen; a guest sent further walks in and
# is lost to view. Ghost, so guests walk through it; stuck, so a hand cannot
# carry the weather away.
MIST_X, MIST_Z = 3.75, 5.05


def mist():
    parts = []
    seed = [7]

    def rnd():                                             # the same puffs every build
        seed[0] = (seed[0] * 16807) % 2147483647
        return seed[0] / 2147483647
    x0, x1 = 2.5, 4.95
    for c in range(10):
        depth = c / 9
        for (z, spread) in ((4.3, 0.2), (4.8, 0.25), (5.3, 0.25), (5.75, 0.2)):
            for k in range(2):
                x = x0 + (x1 - x0) * depth + (rnd() - 0.5) * 0.3
                zz = z + (rnd() - 0.5) * spread
                y = 0.22 + 0.3 * k + rnd() * 0.25
                r = 0.22 + rnd() * 0.16 + 0.06 * depth
                op = 0.14 + 0.28 * depth + rnd() * 0.05      # thin at the near edge, thicker in
                parts.append({'shape': 'sphere', 'size': [round(r, 3)],
                              'at': [round(x - MIST_X, 3), round(y, 3), round(zz - MIST_Z, 3)],   # about the model's own middle
                              'color': '#ffffff', 'opacity': round(min(op, 0.48), 3)})
    return {'kind': 'model', 'parts': parts, 'label': 'the mist', 'ghost': True, 'stuck': True,
            'note': ('The row goes on into the mist: cottages 12, 13 and 14 stand in it, and all the rest '
                     'behind them. A guest sent past 14 walks in and is lost to view. Nothing in the resort '
                     'knows how many cottages there are.')}


INSIDE = ('RESORT INFINITY\n\n'
          'Everything is out the back\n'
          'door: the cottages, the front\n'
          'desk, the guests.\n\n'
          'Go outside.')

# the row: eleven cottages in the clear, numbered from the left, and three
# more in the mist
row = [{'thing': cottage(n), 'x': n * 0.6 - 4.5, 'z': COTTAGE_Z} for n in range(1, 15)]
row.append({'thing': mist(), 'x': MIST_X, 'z': MIST_Z})

g1, g2, gates = [], [], []
for k in range(1, 7):                                      # the first six, at the gate
    lid = 'GST1%d' % k
    g1.append(guest_gadget(k, k, lid, 'G1%d' % k))
    gates.append({'thing': guest('guest %d' % k, lid, '#b8362b'), 'x': -4.2 + 0.5 * (k - 1), 'z': 6.6})
for k in range(1, 6):                                      # ...and five more behind them
    lid = 'GST2%d' % k
    g2.append(guest_gadget(10 + k, k, lid, 'G2%d' % k))
    gates.append({'thing': guest('new guest %d' % k, lid, '#2b6fb8'), 'x': -4.2 + 0.5 * (k - 1), 'z': 7.4})

bench_yard = row + gates + [
    {'thing': macro('the guests', 'M1', g1,
                    {'bg': '#1f3b2c', 'ink': '#d9ffe8', 'font': 'sans', 'h': 0.42},
                    note=('The resort\u2019s own machinery, which you never need to touch: '
                          'six behaviours, one per guest, three robots each. SPACE here is the '
                          'six guests arriving at once \u2014 they write to the post and walk to '
                          'their cottages as soon as a clerk answers. Nothing in them knows how '
                          'many guests there are.')),
     'x': 3.3, 'z': 6.6},
    {'thing': macro('five more guests', 'M2', g2,
                    {'bg': '#3b2c1f', 'ink': '#ffe8d9', 'font': 'sans', 'h': 0.42},
                    note=('The same machinery for problem 2\u2019s five newcomers. Switch it '
                          'on once your mover has moved everybody up and cottages 1 to 5 '
                          'stand empty.')),
     'x': 3.3, 'z': 7.4},

    {'thing': front_desk, 'x': -4.3, 'z': 3.4},
    {'thing': bird(*ROBOT_NESTS[DESK_G], label='to the front desk'), 'x': -3.6, 'z': 3.4},      # noqa: F405
    {'thing': moving_office, 'x': -2.6, 'z': 3.4},
    {'thing': bird(*ROBOT_NESTS[OFFICE_G], label='to the moving office'), 'x': -1.9, 'z': 3.4},   # noqa: F405

    # to train on: two practice letters, and the nest their bird flies to
    {'thing': LETTER(7, 'a practice letter'), 'x': -0.9, 'z': 3.4},
    {'thing': LETTER(3, 'a practice letter'), 'x': -0.2, 'z': 3.4},
    {'thing': nest(PRACTICE_ID, PRACTICE_G, label='the practice nest'), 'x': 0.5, 'z': 3.4},   # noqa: F405

    {'thing': txt(ABOUT), 'x': 1.4, 'z': 3.2},                                   # noqa: F405
    {'thing': txt(P1), 'x': 2.6, 'z': 3.2},                                      # noqa: F405
    {'thing': txt(TRAIN), 'x': 2.0, 'z': 3.9},                                   # noqa: F405
    {'thing': txt(P2), 'x': 3.8, 'z': 3.2},                                      # noqa: F405
    {'thing': txt(FENCE), 'x': 3.2, 'z': 3.9},                                   # noqa: F405

    # the answers, by the fence, for the clerk who would rather read one
    {'thing': clerk, 'x': -4.4, 'z': 2.5},
    {'thing': move_robot, 'x': -3.6, 'z': 2.5},
]

bench = [{'thing': txt(INSIDE), 'x': -0.2, 'z': 1.6}]      # noqa: F405

if __name__ == '__main__':
    import json, io
    world = {'kind': 'world', 'v': 3, 'bench': bench, 'stations': {}, 'active': None,
             'yard': {'bench': bench_yard}}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '\U0001f3e8 resort-infinity.world.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1, ensure_ascii=False))
    print('wrote', os.path.basename(out))
