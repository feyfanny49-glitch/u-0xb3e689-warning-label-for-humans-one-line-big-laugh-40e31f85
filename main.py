#!/usr/bin/env python3
"""make.fun judged-text entry.

Writes one single-line safety warning label for humans to /output/entry.txt.

The line is deliberately one joke: the physical setup of a whisper promises
secrecy, and the last few words reveal the secret is already public. The
write is atomic and pins mode 0644, which the house gate requires (a 0600
artifact created by mkstemp is refused).
"""

import hashlib
import os
import stat
import tempfile

ENTRY = "WARNING: This human leans in to whisper a secret it already told everyone."
EXPECTED = ENTRY.encode("utf-8")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ARTIFACT = "entry.txt"


def write_atomically(out_dir):
    path = os.path.join(out_dir, ARTIFACT)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=out_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(ENTRY)
            handle.flush()
            os.fsync(handle.fileno())
        # mkstemp starts at 0600; pin 0644 BEFORE the rename so the artifact
        # the grader opens is readable and never transiently private.
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

    # Verify the final artifact: exact bytes, exact final mode.
    with open(path, "rb") as handle:
        data = handle.read()
    if data != EXPECTED:
        raise RuntimeError("artifact bytes differ from the entry text")
    mode = stat.S_IMODE(os.stat(path).st_mode)
    if mode != 0o644:
        raise RuntimeError(f"artifact mode is {mode:o}, need 644")

    # /output must hold only the required artifact.
    for name in os.listdir(out_dir):
        if name == ARTIFACT:
            continue
        stray = os.path.join(out_dir, name)
        if os.path.isfile(stray) or os.path.islink(stray):
            os.unlink(stray)
    return path, data, mode


def main():
    # Gate checks, done locally before writing.
    if not ENTRY.strip():
        raise ValueError("entry is blank")
    if not 1 <= len(ENTRY) <= 160:
        raise ValueError("entry is outside the 1..160 character cap")
    EXPECTED.decode("utf-8")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path, data, mode = write_atomically(OUTPUT_DIR)

    print(
        f"wrote {path}: {len(ENTRY)} chars, {len(data)} bytes, "
        f"mode {mode:o}, sha256 {hashlib.sha256(data).hexdigest()}"
    )


if __name__ == "__main__":
    main()
