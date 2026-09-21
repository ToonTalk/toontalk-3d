# ToonTalk 3D regression follow-up — 19 September 2026

Tested the local working version at http://localhost:8311, with audio muted. App source was not changed. Used actual workshop interactions plus isolated, frame-stepped fixtures using the app's existing `__nano` test interface. These are local-build results, not verification of the currently deployed GitHub Pages build.

## Results against the nine requests

1. **Fibonacci by houses, 1× and 4× — wording condition not established.** Both runs stopped with the ordinary “every robot on the team looked” message. I could not establish that houses were still working at that exact moment, so this does not prove the new wording is broken. The onward-work clause did appear for the Resort teacher: “Its part is done — 2 houses are still at work.” A deterministic regression should hold a child house busy past the parent stop and assert the count at both speeds.

2. **Stand-in bird — delivery passes; mid-flight saving is blocked.** In Activity 8, three Sequence boxes given eight simulated frames apart arrived in order 1, 2, 3; the nest stores newest first, hence its serialized pile reads 3, 2, 1. A separate numbered test delivered 5, 6, 7, left no numbers behind on the bench, and retained one bird. During delivery the normal Save handler refuses with **“Leave the thought bubble first”**, although the app is in world mode. This is misleading: say “Wait for the bird to finish delivering,” or defer the save until delivery completes. Direct `worldOut` → `worldIn` round-tripping during flight loses the cargo and pending queue. That demonstrates a serializer limitation, but **not data loss through a successful normal Save command**, which is guarded by `busy`. My earlier interim description of this as an ordinary save-loss bug was too broad. If mid-flight saving is intended, persist cargo, destination, FIFO queue and bird home, then test reload through the public Save/Import path.

3. **House levers — sampled targets pass.** Near-lever clicks on Zeno and several pipeline houses operated the lever without picking up the house. Wall/roof areas away from the lever still allowed pickup. This was representative sampling, not an exhaustive hit-map test. Chimneys were a reliable target for changing solid/glass state.

4. **Teachers 54–57 — mostly improved.** All four were run at Instant. Counting leads with “Now it counts”; Telling with “Now it tells”; Stopwatch with “The number is a stopwatch now.” Those read as success. Resort still leads with the introductory **“Watch. I seat the guests, teach a clerk…”**, which sounds as though the demonstration is about to begin. Give it a final success pad/read step. The appended mismatch-stop explanation also weakens otherwise positive completion messages; put success first and make the reason secondary. Counting and Telling pupils had trained steps and appropriate descriptions. No “Untrained” text was found in the four source worlds; I did not inspect every Resort-created robot individually.

5. **Instant pipelines and Grammar — no unrecoverable freeze reproduced.** Actual UI Pause worked in Grammar, Squares, All Fractions and Activity 8. Grammar visibly produced “boys kick silly dogs.” All seven numbered pipelines 45–51 completed bounded runs and produced outputs in the fixture. Grammar completed 100 internal rounds and produced four sentences. These are infinite generators in ordinary use, so “finish” here means finish a bounded test, not naturally terminate an unlimited stream. Significant single-step stalls remain; see benchmarks below.

6. **Solid → glass — active reveal passes, strict display deadline not proved.** The counter was run with solid houses and switched to glass. In the controlled 4× check it was still active at reveal (dirty, 81 rounds reached), and the number 82 had a mesh: zero number objects without meshes. Entering the house reached depth 1 and resumed its robot. Thirty stepped frames including reveal took 266 ms of harness wall time. That is supportive but is not a calibrated foreground screen-paint latency measurement, so I cannot certify the requested half-second bound or absence of every hidden duplicate after entry. An earlier completed eight-round check likewise showed number 9 and no missing mesh.

7. **Notebook aside and media cards — usable, with an album trap.** “Move my notebook aside” moved it successfully, including while my hand held another item. Pictures could be picked up, resized and put in a box; their held description was “a picture.” Album tabs and arrow navigation worked, filing a spare star on an empty page worked, and the spine picked up the album. But taking a picture gives a *copy*, and dropping that copy directly on the existing picture says **“Your hand is full”**; dropping on the page margin files it correctly. Let the picture forward a held-item drop to its page, or explicitly direct children to the margin. Use “copy” consistently in the card. I did not exercise the optional picture-width message program.

8. **Narrow viewport — upper-left title/message panel obstructs the door.** With the Resort world and the camera zoomed out one scroll, obstruction was visible at 800×450 and 640×480. At 800×450, `#title` occupied x=14, y=14, width=250, height≈262, ending at y≈276. It covers most of the green back door; this is the title/instruction card, not the right-hand trained-actions panel. At 800×720 the door was accessible below it. Collapse long instructions on short viewports, or add an accessible “Go outside” control. Screenshots are supplied alongside this report. The capture surface scales the rendered page within the image; viewport dimensions above come from DOM measurements, not the outer image margins.

9. **Projects and Settings with a new name — sampled flow passes.** Created “Regression audit September 19.” First-time Settings appeared, audio stayed off, and later world loads did not repeat onboarding. Drop hints persisted across a world load; restored them afterward. Completed “A box of two numbers” and reached “A robot on a box.” The first project's completion could be clearer: picking up the completed box advances directly into the next project; a success banner and explicit Continue would make the transition easier to understand. This was one completed project, not a full test of all projects.

## Performance observations

The bounded fixtures run the real engine while manually advancing frames and yielding to the browser. Values below are the **largest measured engine-frame call**, not average FPS or end-to-end interactive latency. They include environment/JIT variability and are single-run observations, so do not interpret small differences as rankings.

| Workload | Bound | Largest frame |
|---|---:|---:|
| Even numbers (45) | 8 rounds | 103 ms |
| All integers (46) | 8 rounds | 69 ms |
| Squares (47) | 8 rounds | 137 ms |
| Fractions between 0 and 1 (48) | 8 rounds | 58 ms |
| Fractions above 1 (49) | 8 rounds | 85 ms |
| All positive rationals (50) | 8 rounds | 71 ms |
| Counting sequences (51) | 8 rounds | 173 ms |
| Grammar | 100 rounds | 402 ms |

Pause remained usable in the foreground samples, but a 402 ms synchronous step can still make it feel unresponsive. Recommended optimization: give unseen-house work a small elapsed-time budget per task, yield between chunks, and check pause/cancellation at chunk boundaries. Queue-draining should also have a budget so increasing output queues cannot monopolize the main thread. Preserve round-robin fairness and delivery order. Keep mesh creation lazy for solid houses, and add a deterministic materialization test when revealing/entering a house.

The active glass fixture's whole-world serialization changed while paused. That is not by itself a robot-pause failure: birds and other motion intentionally continue. Future pause tests should compare robot instruction/round progress rather than byte-for-byte world snapshots.

## Evidence and reproducibility

- `activity8-bird.html` / `activity8-bird-results.txt`: real Sequence boxes, ordering, save refusal and internal reload.
- `bird.html` / `bird-results.txt`: numbered FIFO, no bench leftovers, serializer behavior.
- `pipelines.html`, `pipeline-worlds.json`, `pipeline-results.txt`: seven bounded pipelines.
- `grammar-results.txt`: 100-round Grammar result; run `pipelines.html?only=e24`.
- `glass-midrun.html?only=e45` / `glass-midrun-results.txt`: active 4× reveal.
- `teacher54-finish.txt` through `teacher57-finish.txt`: UI completion evidence.
- `back-door-800x450.png`, `back-door-640x480.png`: obstruction screenshots.

`serve.cjs` serves these fixtures at `/audit/` with the local source app. Fixtures mute audio and do not change the application source. App SHA-256 during testing: `F58492E5EDE21068B2BCA358978DBBABC7C962C8B66F57070E6797B28F840D15`.
