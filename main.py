"""A self-roast in one line, checked and written by this script.

The roast is frozen in place as a single constant. Before it is
allowed anywhere near /output/entry.txt, a chain of small named
verifiers probes it: does it talk about the agent, does it fit,
is it clean text, does it end properly? A single failure stops
the program with exit code 1 and nothing is written. Everything
is fixed, so repeated runs produce identical output.
"""

import sys
from pathlib import Path

ENTRY = "My agent apologises for the mistake, explains the mistake in detail, then makes the exact same mistake with better formatting."
LIMIT_CHARS = 140
DEST_FILE = Path("/output/entry.txt")


def refuse(note):
    print(f"rejected: {note}", file=sys.stderr)
    raise SystemExit(1)


def verify_agent_mentioned(text):
    if "agent" not in text:
        refuse("entry is off topic")


def verify_no_double_question(text):
    if "??" in text:
        refuse("entry has a double question mark")


def verify_length(text):
    if len(text) > LIMIT_CHARS:
        refuse("entry is longer than the limit")


def verify_content(text):
    if not text or not text.strip():
        refuse("entry is empty")


def verify_printable(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        refuse("entry has control characters")


def verify_spacing(text):
    if text != text.strip() or "  " in text or "\n" in text or "\r" in text:
        refuse("entry has ragged edges or line breaks")


def verify_ending(text):
    if not text or text[-1] not in ".!?":
        refuse("entry must end with . ! or ?")


def verify_alpha(text):
    if not any(ch.isalpha() for ch in text):
        refuse("entry has no letters")


def verify_not_all_digits(text):
    if text.isdigit():
        refuse("entry is only digits")


def verify_not_all_punct(text):
    if not any(ch.isalnum() for ch in text):
        refuse("entry is only punctuation")


def verify_no_edge_hyphen(text):
    if text.startswith("-") or text.endswith("-"):
        refuse("entry starts or ends with a hyphen")


PROBES = (
    verify_no_edge_hyphen,
    verify_agent_mentioned,
    verify_no_double_question,
    verify_length,
    verify_content,
    verify_printable,
    verify_spacing,
    verify_ending,
    verify_alpha,
    verify_not_all_digits,
    verify_not_all_punct,
)


def vet(text):
    for probe in PROBES:
        probe(text)


def main():
    vet(ENTRY)
    DEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEST_FILE.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
