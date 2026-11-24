#!/usr/bin/env python3
"""Write one absurd invention pitch sentence to /output/entry.txt.

Stdlib only, no network. The output directory comes from
MAKEFUN_OUTPUT_DIR (fallback /output) and never depends on the
current working directory.
"""

import os
import sys
from pathlib import Path

SENTENCE = (
    "The Mirror With Standards stays fogged until you've finished "
    "your coffee, ending the daily argument with your own reflection "
    "by refusing to introduce you to yourself before you're caffeinated."
)


def validate(text: str) -> None:
    """Gate: exactly one sentence, 1-220 characters, no extra lines."""
    stripped = text.strip()
    if not (1 <= len(stripped) <= 220):
        raise ValueError(f"entry must be 1-220 characters, got {len(stripped)}")
    if text != stripped:
        raise ValueError("entry must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not stripped.endswith("."):
        raise ValueError("entry must end with a full stop")
    if stripped.count(".") != 1:
        raise ValueError("entry must contain exactly one sentence")
    if any(ch in stripped for ch in "!?;"):
        raise ValueError("entry must contain exactly one sentence")


def main() -> int:
    validate(SENTENCE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(out_dir, 0o755)
    except OSError:
        pass
    target = out_dir / "entry.txt"
    # umask 022 so the file is world-readable (0644) for collection.
    old_umask = os.umask(0o022)
    try:
        target.write_text(SENTENCE, encoding="utf-8", newline="")
    finally:
        os.umask(old_umask)
    os.chmod(target, 0o644)
    # Read back and verify byte-for-byte before exiting.
    roundtrip = target.read_text(encoding="utf-8")
    if roundtrip != SENTENCE:
        raise ValueError("verification failed: entry.txt does not match")
    validate(roundtrip)
    print(f"Wrote {target} ({len(SENTENCE)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
