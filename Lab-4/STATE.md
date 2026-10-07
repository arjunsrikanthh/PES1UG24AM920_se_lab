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
- [x] Push personal repository and verify remote content and accepted-file hashes.
- [x] Resolve reported wall passage, expand tests, and publish a clearer after video.

## Next action

User requested a minimal solution and playable before/after versions. Simplification
and matching video/transcript are verified and published. Both native games are
open for manual play. Await user feedback; keep any further changes focused on
the four assigned tasks. The local final folder mirrors tracked Lab-4 files.
No LMS submission or grading is claimed here.
Keep accepted Labs 1-3 frozen. On resuming, inspect this file, personal main and
the working checkout before making changes; do not use the obsolete outer origin.

## Verified evidence

Current simplified version:
- Removed per-wall destruction state, contact-set helper and hit timer. A shield
  hit consumes the shield and removes that obstacle; the next obstacle is lethal.
- 33 fewer runtime lines than the previous version. Obstacle class is identical
  to the original starter. Keep only the four assigned tasks; no gameplay redesign.
- 18 tests pass, including touching, safe gaps, bounds, reversal, distance/reset,
  single-hit shield, reactivation and two simultaneous obstacle hits.
- Matching native after video: 10.000 seconds, 300 frames, 30 fps, 1400 x 1184.
  Full decode passes; visually inspected the complete ten seconds. Original before
  video remains unchanged. Demonstrates bottom containment, reversal, safe gap,
  one shield hit, next lethal wall and restart. No gameplay or timing is bypassed.
- Transcript: 29 visible entries, five pages, exported 2026-10-07 13:56:51 IST.
  Every rendered page inspected. Actual Lab 4 conversation, no invented prompts.
- Manual play: BEFORE - Original lab starter and AFTER - Fixed lab game launched
  with native titles and positions. Up/Down in both; Space shield and R restart
  after game over in the completed game. On resume, do not assume they still run.
- Simplification package commit: 92b5f3a. Published Lab-4 tree matches local HEAD.
  After video blob: 1cae0c0caefdd0749ebb07848c72600dbb296a7b.
  Labs 1-3 remain identical to accepted 4223a00.

Previous publication evidence (superseded locally by the simplification above):
- Old shield behavior granted immunity during continued contact with a solid wall;
  user correctly flagged its confusing visible pass-through.
- Replaced it with explicit single-wall destruction on shield impact, immediate
  shield consumption, and a one-second hit message. No solid-wall immunity remains.
- Moved HUD below the playfield so the helicopter is visible at both boundaries.
- 18 tests pass, including every one of 477 legal vertical positions at wall contact,
  unprotected scrolling wall blockage, 1,800 held-key frames, and top/bottom shield hits.
- Correction commit: 480f4ab (separate from the original four task commits).
- Read-only independent review passed 20 seeded simulations with rendering.
- Five revised native recording trials inspected; final take is trial 5.
  Other takes remain private and are not submission artifacts.
- Final after.mp4: 10.000 seconds, 300 frames, 30 fps, H.264, 1400 x 1264.
  Full decode passes. Genuine native window and keyboard input, original timing;
  seeded obstacles (3) for the demonstration only. Normal launch stays random.
- Final take shows bottom containment, immediate upward reversal, safe unshielded
  gap crossing, visibly cleared shield-hit wall with immediate shield OFF, next
  solid wall causing game over at 1122 px, and restart with reset distance.
- Transcript: 22 actual visible Lab 4 entries, exported 2026-10-07 13:44:40 IST;
  four-page PDF rendered and every page visually inspected. Automated context and
  earlier lab discussion excluded; media/app links are rendered as readable links.
- Revised package commit 6b8c847882214a69bcbd12ea4195d98439b4e214 pushed to
  personal main. Remote SHA and all 15 Lab-4 file blobs matched the local checkout.
- Published before video remains unchanged: cf6dda37c02635bb57798d01ec9f8fb6c66d82dd.
- Published after video: 9e0c0e39ce40596ab9371f111d57b038f697b933.
- Accepted Labs 1-3 remain identical to 4223a00 (git diff exit 0).
- Local final package is synchronized from tracked Lab-4 files; unexpected Finder
  icon metadata is preserved and is not a submission requirement.

Earlier publication evidence (superseded after video and shield model):

- Starter commit: 4402faa66a1f3ee701c1dbdece783a08bc8c241e (unmodified).
- Python environment: .lab4-work/venv (Python 3.12, Pygame 2.6.1).
- Native macOS capture verified; before.mp4 is exactly 10.000 seconds.
- Initial evidence/source commit: ad2ae50.
- Four deterministic movement tests pass: speed, reversal, bounds, release drag.
- Task 1 commit: f18e311; Task 2: 8af216a; Task 3: 76bacf6.
- Task 4 commit: c4eeefa.
- Original shield model and after video are superseded by the correction above.
- PDF transcript: PES1UG24AM920.pdf, actual Lab 4 user/assistant messages only.
- Earlier PDF: two pages, visually inspected; transcript contains 10 actual visible
  conversation entries through 2026-10-07 13:21:37 IST.
- Submission package commit dae314b0defcf8b72910ce6f7fb7af5b2ee79e68 pushed
  successfully to personal main. Remote SHA matched; GitHub lists all Lab-4 files.
- Accepted Labs 1-3 compare identically against commit 4223a00 (git diff exit 0).

## Deliverable locations

- Published: https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab/tree/main/Lab-4
- Chat page: https://github.com/arjunsrikanthh/PES1UG24AM920_se_lab/blob/main/Lab-4/chat_history.md
- Working checkout: .lab4-work/submission (the outer origin remains obsolete).
- Local final package: /Users/arjun/Downloads/sem5/01_Subjects/Software_Engineering/05_Labs/Lab_04
- Run locally: .lab4-work/venv/bin/python .lab4-work/submission/Lab-4/helicopter/main.py
  (set working directory to the helicopter folder, or launch from the outer workspace;
  main.py resolves its game package from its own directory).

## Decisions

Use this single STATE.md as the durable project-state system (equivalent to Jarvis
state files). Update after each milestone and include exact test/commit evidence.
Follow the game README's four tasks, without unrelated gameplay redesign.
Use the Lab 4 handout's required code/document/video package plus the starter
README's chat-link requirement. Export real conversation messages; do not invent
user prompts or present a reconstructed discussion as an actual transcript.
User selected a Lab 4-only transcript page on GitHub; do not share the full chat.

## Blockers

None. Both playable games are open and the minimal submission is published.
