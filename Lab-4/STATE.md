# Software Engineering Lab State

Updated: 2026-10-07 (Asia/Kolkata)

## Current objective

Complete Lab 4 for Arjun Srikanth, PES1UG24AM920, Section H.
Labs 1-3 earned full marks and are accepted; their submitted artifacts are frozen.

## Authoritative repositories

- Personal lab submissions: https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab
- Accepted Labs 1-3 commit: 4223a00bcd1beb6796362c5720c42ffecb60633a
- Course materials: https://github.com/RuthuHK/software-engineering-lab-material_sec_h
- Assigned Lab 4 starter: https://github.com/SETAPESU26/08_helicopter
- Assignment spreadsheet: course repository lab4/Section_H_Vibe_Coding_Assignments.xlsx, row for PES1UG24AM920, serial 8.

## Workspace cautions

The outer SE_lab checkout has historical uncommitted changes and an obsolete origin.
Implement Lab 4 in an isolated personal-repository checkout at .lab4-work/submission.
Do not stage the outer checkout wholesale or overwrite accepted Labs 1-3.
The old temp_clone and slide_images were moved to Trash in the preceding task.

## Required deliverables and acceptance

Under personal repository Lab-4/: updated Pygame code, genuine 10-second before
and after gameplay videos, complete Lab 4 chat export as PDF, and chat-page link.
Keep a separate commit for each task. Push only to the personal repository;
the handout prohibits a PR to SETAPESU26.

1. Movement: bounded speed, immediate reversal, top and bottom containment.
2. Collision: walls end game; flying through a gap is safe; game over is clear.
3. Score: distance grows during play, final distance shown, new game resets zero.
4. Shield: visibly activate, absorb exactly one collision, disappear on use.

## Progress

- [x] Read complete Lab 4 handout and assigned starter README.
- [x] Verify assignment identity and correct personal repository.
- [x] Clone starter and personal repository; run unchanged starter.
- [x] Record and verify original 10-second gameplay video before editing.
- [x] Implement and commit tasks 1-4 separately, with behavioral checks.
- [x] Record and verify completed 10-second gameplay video.
- [x] Export actual Lab 4 conversation and package deliverables.
- [ ] Push personal repository and verify remote content and accepted-file hashes.

## Next action

Implementation and evidence complete. Commit the final package, push the personal
repository, verify remote commit/files, and mark publication complete here.

## Verified evidence

- Starter commit: 4402faa66a1f3ee701c1dbdece783a08bc8c241e (unmodified).
- Python environment: .lab4-work/venv (Python 3.12, Pygame 2.6.1).
- Native macOS capture verified; before.mp4 is exactly 10.000 seconds.
- Initial evidence/source commit: ad2ae50.
- Four deterministic movement tests pass: speed, reversal, bounds, release drag.
- Task 1 commit: f18e311; Task 2: 8af216a; Task 3: 76bacf6.
- Task 4 commit: c4eeefa.
- Full suite: 14 tests pass (movement, wall/gap contact, freeze/reset, distance,
  single contact shield, reentry, second wall, reactivation).
- after.mp4: exactly 10.000 seconds; native screen recording, original speed,
  seeded obstacle sequence (seed 3), standard Up/Down/Space/R input only.
  Shows containment, shield on/absorption/off, a second lethal wall, final score,
  restart with reset distance, and safe passage through the next gap.
- Read-only independent review found no concrete implementation bugs.
- PDF transcript: PES1UG24AM920.pdf, actual Lab 4 user/assistant messages only.
- Both PDF pages visually inspected; final transcript will be refreshed before push.

## Decisions

Use this single STATE.md as the durable project-state system (equivalent to Jarvis
state files). Update after each milestone and include exact test/commit evidence.
Follow the game README's four tasks, without unrelated gameplay redesign.
Use the Lab 4 handout's required code/document/video package plus the starter
README's chat-link requirement. Export real conversation messages; do not invent
user prompts or present a reconstructed discussion as an actual transcript.
User selected a Lab 4-only transcript page on GitHub; do not share the full chat.

## Blockers

None established. Native game recording and chat export must still be verified.
