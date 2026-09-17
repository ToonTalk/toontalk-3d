# Meta: robots that train robots

🎓 **teacher** — a robot trained to train a robot, the way ToonTalk Reborn's
first tour did it: no new kind of thing, and nothing new a robot can be
given. In a lesson, the robot's claw takes a box and is dropped on a little
robot among its things. That is the step *teach*: the little robot (the
pupil) steps up to a desk of its own beside the teacher with the box on it,
and everything done next is the *pupil's* lesson — recorded into the pupil as
its own steps and into the teacher as *taught* steps carrying them, Ruby's
loosening of the pupil's thought included. *Stop teaching it* ends the
pupil's lesson; the teacher's own goes on. A robot may teach a robot, not a
robot that teaches a robot.

Run, the teacher does it for real: it reads the first pad out (a pad in the
claw is read aloud by the step *read aloud what it holds*; *[speak]* given to
a pad's bird does the same), gives the box [a count | a 1] to the little
robot, has it drop a copy of that 1 on the count, has Ruby loosen the count
in its thought so it counts on from any number, and reads the last pad out.
The pupil stands trained at its desk with its box reading 1; click it and
press Start: 2, 3, 4, … The teacher itself runs once — with the pupil gone
from its box, its thought no longer fits.

Regenerate with `python make_teacher.py`.

🎓 **telling** — a robot teaches a robot to *tell its thing*. The pedestal
beside the robot's desk is the perch: on a thing's panel it holds a bird to
that thing, and out here a bird of your own, to the nest "what it told". The
teacher gives Tell a box — a nest with a reading on it and a
`[set | value | _]` letter — and shows it how to copy the letter, put the
reading in it and give it to the bird on the perch; Ruby loosens the reading
so any will do. Run, the lesson lands `[set | value | 5]` on "what it told".
Then take a number from the stack, open its panel with the gear, drop a copy
of the box and the trained pupil on the panel, and press SPACE on the number:
the same robot, on the number's own panel, tells the number. It never learned
what it tells — the perch means the thing whose panel it is on, and that is
what makes a behaviour. Regenerate with `python make_telling.py`.

🎓 **timer-teacher** — a robot builds the stopwatch's four robots, the way
you would, and puts them on a number's panel. They are the very robots of
`devices/make_timer.py`, taught step by step, each on the box in the state
that robot works in: Started (an "on" on the number's switch nest), Ask (the
go token in hole 6), Zero (a fresh reading, and what the number showed), Tell
(a reading and a start). Every lesson is done for real in the run — Ask's
computer answer lands on the nest in its box, and the letters the others give
to the bird on the perch land on "what it told". After each pupil's steps the
teacher has Ruby loosen the holes that must fit any reading, value, start or
token, and Dusty take out the holes a robot must not look in at all (the
token may be in either of two holes) — Dusty on a pupil's thought is a taught
step now, like Ruby. Then the teacher takes the number's panel out onto a
work spot, puts three boxes back in their holes, sets Started's box on the
panel, then Started, Ask, Zero and Tell (a team, in that order), folds the
panel away and reads the last pad. Take the number out of the box and press
SPACE: it counts the milliseconds from 0; "." rests it; SPACE goes on from
there. A pupil whose lesson is over stands half size at its desk. The little
robots a teacher taught stay among its things ("the first little robot it
taught", at its own desk, with its box), which is how it reaches them again.
Regenerate with `python make_timer_teacher.py`.
