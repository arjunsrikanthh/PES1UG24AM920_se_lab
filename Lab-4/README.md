# Lab 4 Vibe Coding Helicopter

Arjun Srikanth | PES1UG24AM920 | Section H

Assigned repository: https://github.com/SETAPESU26/08_helicopter
Original starter commit: `4402faa66a1f3ee701c1dbdece783a08bc8c241e`.

## Submission files

- `before.mp4`: 10 seconds of the unchanged starter, captured from its native
  Pygame window. Direction reversal lags and the helicopter leaves the screen.
- `after.mp4`: 10 seconds demonstrating the completed game.
- `helicopter/`: updated Python source with separate commits for Tasks 1-4.
- `PES1UG24AM920.pdf`: actual Lab 4 conversation export.
- `chat_history.md`: readable transcript page.
- `STATE.md`: durable progress and resume notes.

The course handout is at
https://github.com/RuthuHK/software-engineering-lab-material_sec_h/blob/main/lab4/Lab_4_VibeCoding_Student_handout.pdf.
The assignment spreadsheet maps PES1UG24AM920 to serial 8, this Helicopter game.
`STARTER_README.md` preserves the instructor's complete task specifications.

## Run

Python 3.10 or newer is required. Tested with Python 3.12 and Pygame 2.6.1;
Python 3.12 is recommended for the setup commands below.

```sh
cd Lab-4/helicopter
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Tasks

1. Fix unlimited vertical speed and missing bottom boundary.
2. Add wall collision and a game-over display.
3. Add distance scoring with reset on a new game.
4. Add a visibly active shield that absorbs exactly one contact.

All four tasks are implemented in separate commits:

| Task | Commit | Result |
| --- | --- | --- |
| Original starter and evidence | `ad2ae50` | Unchanged source and before video |
| 1 Movement and boundaries | `f18e311` | Speed cap, immediate reversal, complete body containment |
| 2 Collision and game over | `8af216a` | Either wall, exact edge contact, restart with R |
| 3 Distance scoring | `76bacf6` | Pixels traveled, final distance, reset on new game |
| 4 Shield | `c4eeefa` | Space activates, blue outline, one contact absorbed |
| Feedback correction | `480f4ab` | Only the shield-hit wall is visibly cleared; HUD stays outside the playfield |

## Controls and behavior

- Up and Down move the helicopter; both together act as released input.
- Space activates the shield. The blue outline and HUD show when it is active.
- One wall contact immediately consumes the shield and removes only the struck
  top or bottom wall, with a visible "SHIELD HIT" message. The other wall stays
  solid. Any remaining solid wall is lethal unless Space is pressed again.
- The helicopter's entire body stays in the 700 x 500 playfield. A separate
  100-pixel HUD below it keeps the boundary, distance and shield status visible.
- R starts a fresh game after game over. Distance is measured in scrolled pixels.
- Close the window to exit.

## Verification and evidence

```sh
cd Lab-4/helicopter
python -m unittest discover -s tests -v
```

All 18 deterministic behavioral tests pass. Checks cover velocity caps, immediate
reversal, both screen edges, exact wall contact, safe gap margins, frozen game
over, restart, distance, one-wall shield consumption and reactivation. The tests
include all 477 legal vertical positions at wall contact and 1,800 held-key frames.
A separate read-only review passed 20 seeded simulations with rendering.

Both MP4 videos are native macOS screen recordings of the running Pygame window,
encoded at 30 fps with their original timing and exactly 10.000 seconds duration.
The after video uses a reproducible random obstacle seed (3) and ordinary native
keyboard input. No gameplay is bypassed, sped up, or replaced with drawn evidence.
The live game retains random obstacles on normal launch.

The corrected after video shows the helicopter held against the bottom boundary,
immediate reversal upward, a safe gap crossing without a shield, a shielded
hit that visibly clears one wall and turns the shield off, a subsequent solid-wall
collision with a frozen final distance, and a restart. The final encoded video
was decoded without errors and inspected around the collision transitions.

## Chat link

[Complete Lab 4 user and assistant transcript](https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab/blob/main/Lab-4/chat_history.md)

The PDF and Markdown export contain the real visible conversation beginning at
the Lab 4 request through their stated export time. Internal reasoning and tool
logs are excluded. The user selected this Lab 4-only transcript instead of sharing
earlier conversation content.

No pull request is created against the instructor's repository. Accepted Labs 1-3
remain identical to commit `4223a00`.
