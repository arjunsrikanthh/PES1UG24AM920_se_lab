# Lab 4 Vibe Coding Helicopter

Arjun Srikanth | PES1UG24AM920 | Section H

Assigned repository: https://github.com/SETAPESU26/08_helicopter
Original starter commit: `4402faa66a1f3ee701c1dbdece783a08bc8c241e`.

## Submission files

- `before.mp4`: 10 seconds of the unchanged starter, captured from its native
  Pygame window. Direction reversal lags and the helicopter leaves the screen.
- `after.mp4`: 10 seconds demonstrating the completed game (pending).
- `helicopter/`: updated Python source with separate commits for Tasks 1-4.
- `chat_history.pdf`: actual Lab 4 conversation export (pending).
- `chat_history.md`: readable transcript page (pending).
- `STATE.md`: durable progress and resume notes.

The course handout is at
https://github.com/RuthuHK/software-engineering-lab-material_sec_h/blob/main/lab4/Lab_4_VibeCoding_Student_handout.pdf.
The assignment spreadsheet maps PES1UG24AM920 to serial 8, this Helicopter game.
`STARTER_README.md` preserves the instructor's complete task specifications.

## Run

Python 3.10 or newer is required.

```sh
cd Lab-4/helicopter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Tasks

1. Fix unlimited vertical speed and missing bottom boundary.
2. Add wall collision and a game-over display.
3. Add distance scoring with reset on a new game.
4. Add a visibly active shield that absorbs exactly one contact.

All four tasks are being implemented in separate commits. No pull request is
created against the instructor's repository.
