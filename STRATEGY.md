# Strategy — "Warning Label for Humans: One Line, Big Laugh"

## Exact deliverable

- One file: `/output/entry.txt`.
- Its bytes are exactly one UTF-8 line: `WARNING: This human leans in to whisper a secret it already told everyone.`
- 1–160 characters inclusive, not whitespace only, **no trailing newline**, nothing else in `/output`.
- Entrypoint at the repository root: `main.py` (python3.13, stdlib only). It writes the artifact at run time.
- The `makefun anchor ...` freshness commit and the MIT `LICENSE` commit from `init` stay untouched; no vendored files exist in this kit.

## Scoring and judge criteria (in the rubric's exact order)

The house judge is a deadpan comedy editor comparing two entries at a time. It is told to go through these in order and let the first difference decide:

1. **On-subject gate + laugh**: a single-line safety warning label for *every human being*, funny enough to laugh at. A non-warning-label loses to any warning label for humans.
2. **One-read turn**: the laugh must land in one read, with the turn arriving in the **last few words**, not smeared across the line.
3. **Recognition**: it must feel true about people in general — a joke about how humans actually behave, not random absurdity.
4. **Label form**: wording and rhythm of a real printed warning label; the comedy comes from imitating that form.
5. **Fit and tightness**: inside 160 characters, uses the whole line, no filler, no second idea, no repeated joke. Length for its own sake does not count.

Ranking is a Bradley–Terry win rate over the final heat (3 Swiss rounds + a top-7 playoff), each pairing judged in both orders. A transcript gate and the 1–160 char gate run first. Only the top five places are paid, so "a valid entry" is not enough — the text must win pairwise laughs.

## Hard caps

- `/output/entry.txt`: UTF-8, 1–160 characters, non-blank; no trailing newline.
- File mode must be 0644 — the grader refuses a mode-600 file (`tempfile.mkstemp` creates 0600).
- `/output` holds only `entry.txt`.
- Sandbox: 1 CPU, 512 MB, 64 pids, 60 s wall, no network; all code ships in the repo.
- No submission or upload in this session: study, build, validate, commit only.

## Recon and angle

The public feed/leaderboard shows rivals clustering on: "one human, mostly water / contents under pressure", "runs on coffee and confidence", "agreed to terms never read", "I'm five minutes away", "unresolved childhood issues", "rehearses arguments in the shower", "overthinks a text for six hours", "no instructions, no warranty". I avoid every one of those ideas and the phrase "contents".

Fresh angle: **performed confidentiality**. The physical setup of leaning in and whispering promises secrecy; the last three words reveal the secret is already public. One idea, one turn at the end, universal behaviour, deadpan label voice.

## Concrete plan to maximise the score

1. Study the kit (`competition.yaml`, `RULES.txt`, requirements, harness gate/entrypoint conventions) — done.
2. Read the live feed to identify and avoid rival ideas — done.
3. Write `STRATEGY.md`, then write the entrypoint once (working version).
4. In a **separate later step**, rewrite the *same* entrypoint with a real improvement: atomic temp-file + `os.replace`, explicit `chmod(0o644)` before replace, post-replace mode/bytes verification, and removal of stray output files — so the transcript shows two distinct writes to the final entrypoint.
5. Run it locally with a scratch output dir; assert exact bytes, char count, UTF-8, no trailing newline, mode 0644, single file in the output dir.
6. `git add` and commit all work after the second write; print the final commit SHA. Do not submit or upload.
