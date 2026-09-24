"""Construction layer for Bororo generation.

Lexical identity is kept separate from constructional function.  A root is not
duplicated into noun/verb lexemes merely because it occurs referentially or
predicatively.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Construction:
    name: str
    function: str
    predicate_marking: Optional[str] = None
    person_realization: Optional[str] = None

CONSTRUCTIONS = {
    "bare_reference": Construction("bare_reference","reference"),
    "ordinary_predication": Construction(
        "ordinary_predication","predication",
        predicate_marking="construction-dependent",
        person_realization="bound_index",
    ),
    "declarative_predication": Construction(
        "declarative_predication","predication",
        predicate_marking="-re",
        person_realization="bound_index",
    ),
}

def construction(name):
    return CONSTRUCTIONS.get(name)
