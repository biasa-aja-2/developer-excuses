#!/usr/bin/env python3
"""Make the AI Judge Laugh: Developer Excuses.

Writes one funny single-line excuse a developer gives when code breaks
in production to $MAKEFUN_OUTPUT_DIR/entry.txt.

The excuse: the classic "it worked in staging" defence, turned by
spelling out exactly why staging is a fantasy world — polite data,
fictional users, servers that have never met a real customer. The joke
lands on the last clause: the servers' innocence is the punchline.

Pure Python standard library only. Deterministic: the same bytes on
every run.
"""

import os
import sys

# The entry. One line, 120 characters, well inside the 1-200 gate.
EXCUSE = (
    "It worked in staging, where the data is polite, the users are "
    "fictional, and the servers have never met a real customer."
)

MAX_CHARS = 200


def gate_ok(text):
    """Check the competition gate: UTF-8, 1-200 chars, single line,
    not only whitespace, no control characters."""
    if not text or text.strip() == "":
        return False, "entry is blank"
    if len(text) > MAX_CHARS:
        return False, "entry is %d chars, over the 200-char gate" % len(text)
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    for ch in text:
        code = ord(ch)
        if code < 0x20 or code == 0x7F:
            return False, "entry holds a control character U+%04X" % code
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return False, "entry is not UTF-8: %s" % exc
    return True, ""


def main():
    ok, why = gate_ok(EXCUSE)
    if not ok:
        print("gate failed: %s" % why, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    # Atomic write: temp file in the same directory, then rename.
    tmp = target + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(EXCUSE)
    os.replace(tmp, target)

    # Read back and verify what landed on disk.
    with open(target, "r", encoding="utf-8") as fh:
        landed = fh.read()
    if landed != EXCUSE:
        print("verification failed: entry.txt differs", file=sys.stderr)
        return 1

    print("wrote %d chars to %s" % (len(EXCUSE), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
