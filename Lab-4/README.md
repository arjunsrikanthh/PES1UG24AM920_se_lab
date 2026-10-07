# Lab 4: Vibe Coding - Helicopter

Arjun Srikanth | PES1UG24AM920 | Section H

Assigned starter: [SETAPESU26/08_helicopter](https://github.com/SETAPESU26/08_helicopter).
Original commit: `4402faa66a1f3ee701c1dbdece783a08bc8c241e`.

## Deliverables

- [before.mp4](before.mp4): 10 seconds of the unchanged starter.
- [after.mp4](after.mp4): 10 seconds showing the completed game.
- [helicopter/](helicopter/): updated Python source and behavioral tests.
- [PES1UG24AM920.pdf](PES1UG24AM920.pdf): actual Codex/subagent conversation export.

[Conversation page - GitHub PDF preview](https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab/blob/main/Lab-4/PES1UG24AM920.pdf).

Conversation scope: Codex authored the delegation prompts and implemented the
game; subagents provided tests and review. Student messages are omitted, not
reattributed. This delegation-only export may not satisfy the instructor's
complete student-to-AI chat-history requirement.

## Completed tasks

1. Cap vertical speed, reverse direction immediately, and keep the full player body within both screen boundaries.
2. Detect contact with either obstacle wall and show game over; passage through a clear gap remains safe.
3. Show distance during play and the final distance at game over; restart resets it to zero.
4. Activate a visible shield that absorbs one obstacle hit and immediately turns off.

Separate task commits: movement `f18e311`, collision `8af216a`,
distance `76bacf6`, and shield `c4eeefa`. Subsequent corrections keep the solution minimal.

## Run

Tested with Python 3.12 and Pygame 2.6.1.

```sh
cd Lab-4/helicopter
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Up/Down moves the player. Space activates the shield. R restarts after game over.
A shielded hit consumes protection and removes the hit obstacle; the next
unshielded hit ends the game.

## Verification

```sh
python -m unittest discover -s tests -v
```

All 18 behavioral tests pass. Both videos are genuine native-window recordings,
exactly 10.000 seconds at 30 fps. The after demonstration uses obstacle seed 3;
normal play retains random obstacles. Gameplay and timing are not bypassed.

The original starter draws the helicopter as a dark rounded rectangle.
A helicopter image is not supplied or required. The shield is explicitly required
by Task 4 of the [starter instructions](https://github.com/SETAPESU26/08_helicopter#tasks-to-complete).

Submitted files follow the [Lab 4 handout](https://github.com/RuthuHK/software-engineering-lab-material_sec_h/blob/main/lab4/Lab_4_VibeCoding_Student_handout.pdf).
No pull request is made to SETAPESU26. Accepted Labs 1-3 are unchanged.
