"""Private-dictionary adapter.

The dictionary itself must remain outside version control.  This module reads a
local TSV only when an explicit path is supplied.  It deliberately preserves
homographs as multiple records and does not infer valency or stem class.
"""
import csv
from pathlib import Path

def load_private_dictionary(path):
    path=Path(path)
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))

def lookup_private(entries,form):
    key=form.casefold()
    return [r for r in entries if (r.get("entry") or "").casefold()==key]

def lexical_evidence(record):
    return {
        "entry":record.get("entry") or None,
        "ipa":record.get("ipa") or None,
        "pos":record.get("pos") or None,
        "definition":record.get("definition") or None,
        "example_sent":record.get("example_sent") or None,
        "source":"private_dictionary",
    }
