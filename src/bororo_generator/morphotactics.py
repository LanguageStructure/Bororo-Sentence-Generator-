"""Evidence-bound morphotactic constraints from the Bororo grammar draft.

Only ordering relations directly supported by examples are encoded as constraints.
This is deliberately not a universal fixed-slot template.
"""
ATTESTED_ORDER = (
    ("PERSON","LEX"),
    ("LEX","CAUS"),
    ("CAUS","PASS"),
    ("IRR","NEG"),
    ("NEG","DECL"),
    ("ASPECT","DECL"),
    ("NEG","QUOT"),
)

def ordering_violations(sequence):
    pos={x:i for i,x in enumerate(sequence)}
    return [(a,b) for a,b in ATTESTED_ORDER if a in pos and b in pos and pos[a]>=pos[b]]

def ordering_licensed(sequence):
    return not ordering_violations(sequence)

def working_schema():
    return ("PERSON","LEX","CAUS","PASS","IRR","NEG","ASPECT","ILLOC","REL")
