# Generates account.world.json -- Sally's account, after the ToonTalk 3
# "divisiontester" notebook: an object that answers messages by NAME.
#
# The account is a three-hole box:
#
#     [ Requests: a nest,   Balance: 100,   Owner: "Sally" ]
#
# The first hole is a NEST, and that is the whole mechanism. Messages land on
# it one at a time; a robot lifts the top one off, does what it says, and the
# nest is bare again -- so the team dozes until the next message arrives. A
# robot facing a bare nest waits, which is what makes this an object that
# SERVES requests rather than a program that runs once.
#
# A message is a box whose FIRST hole is a word saying what to do:
#
#     [ "deposit",  50 ]      put 50 in
#     [ "withdraw", 30 ]      take 30 out
#     [ "query",    a bird ]  tell me the balance
#
# Drop one on the bird marked "requests" and she carries it to the nest.
#
#   deposit   sees [["deposit", any number], any number, "Sally"]
#             lift the message off the nest, drop its amount on the balance,
#             sweep the empty message away
#   withdraw  the same, but the robot types a minus sign on the amount first,
#             exactly as you would -- so it subtracts whatever it is given
#   query     sees [["query", a bird], any number, "Sally"]
#             copy the balance and hand the copy to the bird that came with
#             the message; she flies it to the nest marked "answers"
#
# The Owner pad is part of every thought, so these robots serve Sally's
# account and no one else's. Write a different name on the pad and they all
# stop recognising it -- which is the point of putting it there.
import json, io, os

REQ_ID, REQ_GUID = 9400, 'account-request-nest'
REP_ID, REP_GUID = 9401, 'account-reply-nest'
START = 100
OWNER = 'Sally'

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *holes: {'kind': 'box', 'holes': list(holes)}
at = lambda c, *p: {'c': c, 'path': list(p)}
top = lambda c, *p: {'c': c, 'path': list(p), 'nest': True}
take = lambda a: {'type': 'take', 'at': a}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}

WILD, ANYBIRD = {'kind': 'wildNumber'}, {'kind': 'anyBird'}


def account_cond(request):
    """[Requests, Balance, Owner] -- the owner's name is part of the thought."""
    return box(request, WILD, txt(OWNER))


def robot(name, word, second, middle):
    """Each one lifts the message off the nest first and sweeps the husk away
    last; only the middle differs."""
    return {'kind': 'robot', 'name': name,
            'condition': account_cond(box(txt(word), second)),
            'program': [take(top('given', 0)), put('s0')] + middle + [vac('s0')],
            'trainedOn': None, 'team': []}


deposit = robot('deposit', 'deposit', WILD, [
    take(at('s0', 1)), put('given', 1),      # the amount joins the balance
])

# A withdrawal is a deposit that subtracts. The robot takes the amount and
# types a minus sign on it, exactly as the original does -- typing only an
# operation is remembered as an operation, so it works for any amount.
withdraw = robot('withdraw', 'withdraw', WILD, [
    take(at('s0', 1)),                       # the amount, in hand
    {'type': 'setOp', 'op': '-'},            # "make it subtract"
    put('given', 1),                         # dropped on the balance, it takes it away
])

query = robot('query', 'query', ANYBIRD, [
    copy('given', 1), put('s0', 1),          # a copy of the balance, into the bird's wings
])

teller = dict(deposit, name='Teller', team=[withdraw, query])

request_nest = lambda pile=None: {'kind': 'nest', 'id': REQ_ID, 'guid': REQ_GUID,
                                  'hasEgg': False, 'pile': pile or [],
                                  'label': 'requests'}
account = box(request_nest(), num(START), txt(OWNER))
# reaching into the Teller's thought hands you an account with a message on it
teller['trainedOn'] = box(request_nest([box(txt('deposit'), num(50))]),
                          num(START), txt(OWNER))

requests_bird = lambda: {'kind': 'bird', 'nestId': REQ_ID, 'nestGuid': REQ_GUID,
                         'label': 'requests'}
reply_bird = lambda: {'kind': 'bird', 'nestId': REP_ID, 'nestGuid': REP_GUID}

world = {'kind': 'world', 'v': 1, 'bench': [
    # the object itself, and the robots that serve it
    {'thing': account, 'x': -0.35, 'z': 1.72},
    {'thing': teller, 'x': -1.45, 'z': 1.95},
    # the way in, and the way answers come back
    {'thing': requests_bird(), 'x': 0.42, 'z': 1.72},
    {'thing': {'kind': 'nest', 'id': REP_ID, 'guid': REP_GUID, 'hasEgg': False,
               'pile': [], 'label': 'answers'}, 'x': 1.15, 'z': 1.72},
    # messages ready to send
    {'thing': box(txt('deposit'), num(50)), 'x': -0.70, 'z': 1.18},
    {'thing': box(txt('withdraw'), num(30)), 'x': -0.05, 'z': 1.18},
    {'thing': box(txt('query'), reply_bird()), 'x': 0.60, 'z': 1.18},
    {'thing': box(txt('deposit'), num(20)), 'x': -0.70, 'z': 2.28},
    {'thing': box(txt('withdraw'), num(7)), 'x': -0.05, 'z': 2.28},
    {'thing': box(txt('query'), reply_bird()), 'x': 0.60, 'z': 2.28},
    # a spare egg: set it down and it hatches another bird for the answers nest
    {'thing': {'kind': 'nest', 'id': REP_ID + 1, 'guid': REP_GUID, 'hasEgg': True,
               'pile': [], 'label': 'spare'}, 'x': 1.20, 'z': 1.18},
    {'thing': txt("SALLY'S ACCOUNT\n\n [ Requests, Balance,\n   Owner ]\n\n"
                  'The first hole is a NEST.\nMessages land on it one at a\n'
                  'time; a robot lifts the top\none off, does what it says,\n'
                  'and the nest is bare again --\nso the team dozes until the\n'
                  'next message comes.\n\nA message says what to do:\n\n'
                  ' [ "deposit",  50 ]\n [ "withdraw", 30 ]\n [ "query", a bird ]'),
     'x': 1.25, 'z': 2.28},
    {'thing': txt('TO RUN IT\n\nGive the account box to the\nTeller. It waits.\n\n'
                  'Drop a message on the bird\nmarked "requests" and she\n'
                  'carries it to the nest. The\nrobot whose thought carries\n'
                  'that word wakes, serves it,\nand dozes again.\n\n'
                  'A query answers on the nest\nmarked "answers". Its bird\n'
                  'goes with the message, so\nfor more, set the spare nest\n'
                  'down: its egg hatches\nanother.'),
     'x': -1.35, 'z': 1.18},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'account.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
