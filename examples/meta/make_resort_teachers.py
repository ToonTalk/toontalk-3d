# -*- coding: utf-8 -*-
# The resort teachers for problems 3, 4 and 5 -- a robot solves each of the
# other three Resort Infinity problems in front of you (Ken, 19 Sep 2026:
# "do the missing resort teacher examples"), the way make_resort_teacher.py's
# does problems 1 and 2. One robot at the table out in the yard, given a
# ten-hole box:
#
#   0 a pad it reads out first
#   1 a little robot: the mover to be     2 a practice letter, [3 | bird to the practice nest]
#   3 a little robot: the clerk to be     4 another practice letter, [i | j | bird]
#   5 the bird "to the moving office"     6 the bird "to the front desk"
#   7 a bird to the newcomers' macro      8 [set | switch | on], the letter that throws a switch
#   9 a pad it reads out last
#
# It reads the first pad; teaches the mover on the two-hole letter (a x2 or
# x4 dropped on the number, then the number to the bird; Ruby erases the
# number in its thought) and gives it to the office bird -- the office rings
# the bell and everybody housed moves; teaches the clerk on the three-hole
# letter (problem 3: x2 then -1; problem 4: x4, then a copy of the group
# wearing a minus sign) and gives it to the desk bird; throws the newcomers'
# switch; reads the last pad. PROBLEM 5's CLERK IS A TEAM -- Weigh and its
# three sums on a scale -- and a lesson trains one robot, so the teacher
# brings the team ready-made in hole 3 and hands it over, and says so.
import sys, os, json, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'infinity'))
from _tt import *                                          # noqa: F403
import make_resort as R
import make_resort_more as M

WILDTEXT = {'kind': 'wildText'}
ANYROBOT = {'kind': 'anyRobot'}
live_bird = lambda lid, label: {'kind': 'bird', 'nestId': 0, 'nestGuid': None,   # noqa: E731
                                'liveId': lid, 'label': label}
msg = lambda *words: box(*[txt(w) for w in words])        # noqa: E731,F405
speak = {'type': 'speak'}
teach = lambda *p: {'type': 'teach', 'at': at('given', *p)}            # noqa: E731,F405
taught = lambda step: {'type': 'taught', 'step': step}                 # noqa: E731
erase = lambda *path: {'type': 'erase', 'path': list(path)}           # noqa: E731
pupil = lambda k: {'type': 'take', 'at': {'c': 't%d' % k, 'path': [], 'bot': True}}   # noqa: E731
RQ = '’'


def fresh(bot, note):
    return {'kind': 'robot', 'name': bot['name'], 'program': [], 'condition': None,
            'trainedOn': None, 'team': [], 'note': 'A pupil. ' + note}


def lesson(k, letter_hole, bot, erase_holes):
    """Teach the little robot in the hole before letter_hole, on that letter,
    the robot's own steps; then Ruby on the numbers in its thought."""
    return ([take('given', letter_hole), teach(letter_hole - 1)]       # noqa: F405
            + [taught(st) for st in bot['program']]
            + [taught(erase(h)) for h in erase_holes] + [{'type': 'endTeach'}])


def teacher_for(n):
    S = M.spec(n)
    mover, clerk = S['mover'], S['clerk']
    handed = n == 5                                        # the clerk comes ready-made
    FIRST = txt({3: 'Watch. Everybody doubles their address, and the gold group takes the odd cottages.',
                 4: 'Watch. Everybody moves to four times their address, and guest i of group j takes 4i minus j.',
                 5: 'Watch. Everybody doubles, and the newcomers are numbered by growing squares: a team weighs i against j on a scale.'}[n])   # noqa: F405
    LAST = txt({3: 'Done: the even cottages are the old guests, the odd ones the gold group, and every group to come has room.',
                4: 'Done: three cottages in every four were freed, and the three groups took them.',
                5: 'Done: every pair (i, j) got a number of its own, and an odd cottage -- infinitely many groups, one row.'}[n])   # noqa: F405
    given = box(                                           # noqa: F405
        FIRST,
        fresh(mover, 'The teacher shows it the mover' + RQ + 's job on a practice letter: the number times ' + ('four' if n == 4 else 'two') + ', then to the bird.'),
        M.LETTER2(S['letter2'], 'a practice letter'),
        (json.loads(json.dumps(clerk)) if handed
         else fresh(clerk, 'The teacher shows it the clerk' + RQ + 's job on a practice letter [number | group | bird].')),
        M.LETTER3(*S['letter3'], 'a practice letter'),
        bird(*R.ROBOT_NESTS[R.OFFICE_G], label='to the moving office'),     # noqa: F405
        bird(*R.ROBOT_NESTS[R.DESK_G], label='to the front desk'),          # noqa: F405
        live_bird(S['macro']['lid'], 'to the newcomers'),
        msg('set', 'switch', 'on'),
        LAST,
        # the bell, heard here too: the newcomers are let in only once the office has rung it
        dict(nest(9799, 'resort-teacher-bell', label='the bell, heard here'), aliases=[R.BELL]))   # noqa: F405
    program = ([take('given', 0), speak, put('given', 0)]          # noqa: F405
               + lesson(1, 2, mover, [0])
               + [take('t1'), put('given', 2), pupil(1), put('given', 5)])     # the mover to the office: the bell rings, everybody moves  # noqa: F405
    # ...and when the bell has rung (the pad on the teacher's own nest, hole 10): the clerk, the newcomers
    after_bell = ([{'type': 'take', 'at': {'c': 'given', 'path': [10], 'nest': True}}, put('s1'), vac('s1')]   # noqa: F405
                  + ([take('given', 3), put('given', 6)] if handed            # noqa: F405
                     else lesson(2, 4, clerk, [0, 1]) + [take('t2'), put('given', 4), pupil(2), put('given', 6)])   # noqa: F405
                  + [copy('given', 8), put('given', 7)]                # the newcomers' switch  # noqa: F405
                  + [take('given', 9), speak, put('given', 9)])        # noqa: F405
    cond = box(WILDTEXT, ANYROBOT, ANYBOX, ANYROBOT, ANYBOX, ANYBIRD, ANYBIRD, ANYBIRD, ANYBOX, WILDTEXT, None)   # noqa: F405
    after = robot(                                         # noqa: F405
        'When the bell has rung', box(WILDTEXT, None, ANYBOX, ANYROBOT, ANYBOX, ANYBIRD, ANYBIRD, ANYBIRD, ANYBOX, WILDTEXT, WILDTEXT),   # noqa: F405
        after_bell, trained_on=given,
        note='The mover is gone from the box and the bell' + RQ + 's pad has landed on the nest in hole 10: the office has rung it and everybody housed is on the move. ' + ('Hands the growing-squares team' if handed else 'Teaches the clerk and gives it') + ' to the front desk, throws the newcomers' + RQ + ' switch, and reads the last pad out.')
    teacher = robot(                                       # noqa: F405
        'the teacher', cond, program, trained_on=given, team=[after],
        note='A robot that solves Resort Infinity %d: teaches a little robot the mover%ss job on a practice letter and gives it to the bird to the moving office, %s, then throws the newcomers%s switch. Nothing here is new: a teaching, Ruby, a robot given to a bird and a switch thrown by mail are steps like any other.'
             % (n, RQ, ('hands the growing-squares team to the bird to the front desk' if handed else 'teaches another the clerk' + RQ + 's job on a three-hole letter and gives it to the bird to the front desk'), RQ))
    ABOUT = ('THE RESORT TEACHER %d\n\n'
             'A robot that solves Resort\n'
             'Infinity %d in front of you.\n\n'
             'Give it the ten-hole box:\n'
             'the drop sets it to work.\n'
             'Then watch the grass: a\n'
             'mover is taught and given\n'
             'to the moving office, and\n'
             'everybody housed moves; a\n'
             'clerk %s\n'
             'the front desk; and the\n'
             'newcomers (%s)\n'
             'walk to their cottages.\n\n'
             'Set the Speed to 4x: a\n'
             'resort takes a while at\n'
             'walking pace.') % (n, n, ('-- the growing-squares\nteam, ready-made -- goes to' if handed else 'is taught and given to'), S['group_colours'])
    WHAT = {3: ('WHAT IT DOES\n\n'
                '1. Teaches the first little\nrobot on a practice letter:\na x2 dropped on the number,\nthen the number to the bird.\nRuby erases the number.\n'
                '2. Gives it to "to the moving\noffice": the bell rings and\nevery housed guest doubles.\n'
                '3. Teaches the second on a\n[number | group | bird]\nletter: x2, then -1, then to\nthe bird. Ruby erases both\nnumbers.\n'
                '4. Gives it to "to the front\ndesk", and throws the gold\ngroup' + RQ + 's switch: 1, 3, 5, ...'),
            4: ('WHAT IT DOES\n\n'
                '1. Teaches the mover: a x4\ndropped on the number, then\nto the bird. Ruby erases it.\n'
                '2. Gives it to the moving\noffice: everybody moves to\n4i, three in four come free.\n'
                '3. Teaches the clerk on\n[number | group | bird]: x4\non the number, then a copy\nof the group wearing a minus\nsign, then to the bird. Ruby\nerases both numbers.\n'
                '4. Gives it to the front\ndesk, and throws the three\ngroups' + RQ + ' switch: 4i - j.'),
            5: ('WHAT IT DOES\n\n'
                '1. Teaches the mover: x2,\nthen to the bird.\n'
                '2. Gives it to the moving\noffice: everybody doubles.\n'
                '3. The clerk is a TEAM -- a\nrobot that weighs i against\nj on a scale, and three that\ndo the right sum -- and a\nlesson trains one robot. So\nit brings the team ready in\nits box and hands it to the\nfront desk.\n'
                '4. Throws the groups' + RQ + '\nswitch: (i, j) to 2n - 1.')}[n]
    HOW = ('HOW THE DESKS WORK\n\n'
           'The front desk and the moving\n'
           'office are houses, closed.\n'
           'Inside, a robot waits for a\n'
           'letter on the post and a\n'
           'robot of yours in its box;\n'
           'for each letter it takes a\n'
           'fresh little house, puts the\n'
           'letter and a copy of your\n'
           'robot in it, and sets it\n'
           'down: the house works on its\n'
           'own. Your robot is never\n'
           'used up.\n\n'
           'The little robots the teacher\n'
           'taught stay among its things:\n'
           'click one with an empty claw\n'
           'to pick it up and read what\n'
           'it learned.')
    INSIDE = txt('THE RESORT TEACHER %d\n\n'                 # noqa: F405
                 'Everything is out the back\n'
                 'door: the cottages, the\n'
                 'guests, the teacher at the\n'
                 'table.\n\n'
                 'Go outside.' % n)
    yard = M.grass(S['housed'], S['new'], S['macro']) + [
        {'thing': txt(R.FENCE), 'x': 3.2, 'z': 3.9},        # noqa: F405
        {'thing': teacher, 'x': -1.45, 'z': 1.35},
        {'thing': given, 'x': -0.10, 'z': 1.55},
        {'thing': txt(ABOUT), 'x': -1.15, 'z': 2.25},        # noqa: F405
        {'thing': txt(WHAT), 'x': -0.45, 'z': 2.25},         # noqa: F405
        {'thing': txt(HOW), 'x': 0.25, 'z': 2.25},           # noqa: F405
    ] + S['extra']
    return {'kind': 'world', 'v': 3, 'bench': [{'thing': INSIDE, 'x': -0.2, 'z': 1.6}],
            'stations': {}, 'active': None, 'yard': {'bench': yard}}


if __name__ == '__main__':
    for n in (3, 4, 5):
        out = os.path.join(HERE, '\U0001f393 resort-teacher-%d.world.json' % n)
        io.open(out, 'w', encoding='utf-8').write(json.dumps(teacher_for(n), indent=1, ensure_ascii=False))
        print('wrote', os.path.basename(out))
