# Generates bank-account.world.json -- a bank account as a message-passing
# object, sealed inside a house.
#
# The account lives on the Teller's desk INSIDE the house, so nothing out here
# can touch the balance: the only way in is to send a request to the bird. That
# is encapsulation you can walk around.
#
# The account box has five holes:
#   0 balance   1 the requests nest   2 room for a scale
#   3 the request being served        4 the "not enough money" slip
#
# A request is a box [amount, a bird to reply to]. Negative means take money
# out. Give one to the bird marked "requests" and she flies it into the house.
#
# The Teller's team, first thought that matches wins:
#   ok / ok too  [scale tipping left | balanced]:
#       the sum works out at zero or better, so bank it and send the new
#       balance home with the request's own bird.
#   sorry        [scale tipping right]:
#       the sum comes out below zero -- copy the slip and send that instead.
#   take one     [the nest holds a request]:
#       take the request, fetch a scale, and weigh what the balance WOULD be
#       against nothing at all. The tilt is the decision.
#
# With no scale on the desk only "take one" can match, and with one there only
# the three verdicts can, so the team walks through weigh-then-decide without
# any step counter: the scale itself is the state.
import json, io, os

REQ_GUID, REQ_ID = 'bank-request-nest', 9201
REP_GUID, REP_ID = 'bank-reply-nest', 9202
START = 100

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
at = lambda *p: {'c': 'given', 'path': list(p)}
top = lambda *p: {'c': 'given', 'path': list(p), 'nest': True}
copy = lambda *p: {'type': 'copy', 'at': at(*p)}
take = lambda *p: {'type': 'take', 'at': at(*p)}
put = lambda *p: {'type': 'put', 'at': at(*p)}
vac = lambda *p: {'type': 'vacuum', 'at': at(*p)}
WILD, ANYBIRD = {'kind': 'wildNumber'}, {'kind': 'anyBird'}
REQUEST = {'kind': 'box', 'holes': [WILD, ANYBIRD]}

def account_cond(nest=None, scale=None, working=None, slip=None):
    return {'kind': 'box', 'holes': [WILD, nest, scale, working, slip]}

tilt = lambda t: {'kind': 'scaleTilt', 'tilt': t}

# --- weigh: what would the balance become, against nothing at all? ----------
weigh = {'kind': 'robot', 'name': 'take one',
         'condition': account_cond(nest=REQUEST),
         'program': [
             {'type': 'take', 'at': top(1)},     # the oldest request off the nest
             put(3),
             {'type': 'newScale'}, put(2),
             copy(0), put(2, 0),                 # the balance as it stands
             copy(3, 0), put(2, 0),              # plus the amount asked for
             {'type': 'newNumber'},
             {'type': 'setValue', 'value': {'n': '0', 'd': '1'}, 'op': '+'},
             put(2, 1),                          # weighed against nothing
         ],
         'trainedOn': None, 'team': []}

# --- the verdicts ----------------------------------------------------------
def verdict_ok(name, t):
    return {'kind': 'robot', 'name': name,
            'condition': account_cond(scale=tilt(t), working=REQUEST),
            'program': [
                take(3, 0), put(0),              # the amount joins the balance
                copy(0), put(3, 1),              # the new balance flies home
                vac(3), vac(2),                  # request and scale swept away
            ],
            'trainedOn': None, 'team': []}

sorry = {'kind': 'robot', 'name': 'sorry',
         'condition': account_cond(scale=tilt('R'), working=REQUEST,
                                   slip={'kind': 'wildText'}),
         'program': [
             copy(4), put(3, 1),                 # the slip flies home instead
             vac(3), vac(2),
         ],
         'trainedOn': None, 'team': []}

ok = verdict_ok('Teller', 'L')
teller = dict(ok, team=[verdict_ok('ok too', '='), sorry, weigh])

account = {'kind': 'box', 'holes': [
    num(START),
    {'kind': 'nest', 'id': REQ_ID, 'guid': REQ_GUID, 'hasEgg': False, 'pile': []},
    None, None,
    txt('not enough money'),
]}

reply_bird = lambda: {'kind': 'bird', 'nestId': REP_ID, 'nestGuid': REP_GUID}
request = lambda amount: {'kind': 'box', 'holes': [num(amount), reply_bird()]}

bank = {'kind': 'world', 'v': 1, 'bench': [],
        'stations': {'stand': account}, 'active': teller}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': {'kind': 'room', 'label': 'The Bank', 'opaque': False,
               'dirty': False, 'world': bank}, 'x': -0.45, 'z': 1.55},
    {'thing': {'kind': 'bird', 'nestId': REQ_ID, 'nestGuid': REQ_GUID,
               'label': 'requests'}, 'x': 0.55, 'z': 1.50},
    {'thing': {'kind': 'nest', 'id': REP_ID, 'guid': REP_GUID, 'hasEgg': False,
               'pile': [], 'label': 'statements'}, 'x': 1.20, 'z': 1.75},
    {'thing': request(50), 'x': -1.20, 'z': 2.15},
    {'thing': request(-30), 'x': -0.60, 'z': 2.15},
    {'thing': request(-500), 'x': 0.00, 'z': 2.15},
    {'thing': txt('THE BANK\n\nThe account lives on the\nTeller\'s desk inside the\n'
                  'house. Nothing out here can\nreach it — the only way in\n'
                  'is to send a request.\n\nA request is a box: an\n'
                  'amount and a bird to reply\nto. Negative takes money out.'),
     'x': 0.62, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nDrop a request on the bird\nmarked "requests". She flies\n'
                  'it into the house.\n\nThe Teller weighs what the\nbalance WOULD be against\n'
                  'nothing: tipping left or\nlevel, he banks it and sends\n'
                  'the new balance back.\nTipping right, he sends the\n'
                  '"not enough money" slip.\n\nTry the −500 one.'),
     'x': 1.25, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'bank-account.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
