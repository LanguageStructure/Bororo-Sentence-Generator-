"""Evidence-bound morphotactic constraints from the Bororo grammar draft.

Only ordering relations directly supported by examples are encoded as constraints.
This is deliberately not a universal fixed-slot template.
"""
ATTESTED_ORDER = (
    ("PERSON","LEX"),
    ("LEX","CAUS"),
    ("CAUS","PASS"),
    ("IRR","NEG"),
    ("NEG","IND"),
    ("ASPECT","IND"),
    ("NEG","QUOT"),
)

def ordering_violations(sequence):
    pos={x:i for i,x in enumerate(sequence)}
    return [(a,b) for a,b in ATTESTED_ORDER if a in pos and b in pos and pos[a]>=pos[b]]

def ordering_licensed(sequence):
    return not ordering_violations(sequence)

def working_schema():
    return ("PERSON","LEX","CAUS","PASS","IRR","NEG","ASPECT","ILLOC","REL")


# Reviewed surface realization of adjacent operators. This is kept separate
# from ordering constraints: it states how an already reviewed combination is
# realized, not where operators may occur in general.
REVIEWED_OPERATOR_SURFACES={
    ("IRR","IND"):"mode",
    ("IRR","NEG","IND"):"modukare",  # -modu + -re -> -mode
}

def reviewed_operator_surface(*operators):
    return REVIEWED_OPERATOR_SURFACES.get(tuple(operators))


def realize_irrealis_indicative(indexed_stem):
    """Realize reviewed indexed predicate + IRR + IND surface."""
    surface=reviewed_operator_surface("IRR","IND")
    if surface is None:
        return None
    return indexed_stem+surface
