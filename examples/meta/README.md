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

🎓 **timer-teacher** — a robot builds the timer's two robots, the way you
would, and puts them on a number's panel: a stopwatch. Ask is taught on a box
with the "go" pad in hole 6: ask the computer the time, answered to my
readings, and move the pad to hole 7. Tell is taught on a box with a reading
on the nest and the pad in hole 7: put the reading in a `[set | value | _]`
letter, give it to the bird on the perch, move the pad back. Both lessons are
done for real in the run — the computer's answer lands on the nest in Ask's
box, and Tell's letter reaches "what it told". Then the teacher takes the
number's panel out onto a work spot, puts Ask's box back in its hole, sets
Tell's box on the panel, then Ask, then Tell (a team), folds the panel away
and reads the last pad. Take the number out of the box and press SPACE: it
counts the milliseconds; "." rests it. The little robots a teacher taught stay
among its things ("the first little robot it taught", at its own desk, with
its box), which is how it reaches them again. A robot cannot wait mid-round
for an answer, which is why there are two; a pad crossing between two holes
lets them take turns. Regenerate with `python make_timer_teacher.py`.
