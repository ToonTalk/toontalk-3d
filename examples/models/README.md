# Models

Things made of solid shapes, the way Marty makes them, saved as `.thing.json`
files you can import: ✈️ a toy airplane and 🪰 a dragonfly, both facing the
way they fly. `make_models.py` writes them.

## ✈️ airplane-flight.world.json

The toy airplane takes off, flies and loops. Two behaviours are bound to the
one plane -- the 3D turtle (giving it move/yaw/pitch/roll) and "the pilot"
(which speaks them) -- so one SPACE on the airplane starts both. The pilot has
no counter: its round is `move 10, move 10, pitch 30`, and a constant turn per
constant stride is a circle. Twelve rounds close it. The pen is down, so it
draws its own flight path; the plane starts mid-table because the loop needs a
radius of room behind it as well as in front.

`make_flight.py` writes the flight (moved here from `behaviours/` on 13 Sep,
to sit beside the airplane it flies).
