"""Constructional imperative constraints documented in the grammar draft."""

def positive_imperative(frame):
    # Extended intransitives pattern with monovalents for imperative formation.
    if frame in {"monovalent","extended_intransitive"}:
        return {"addressee_index":"2", "suffix":"-do"}
    if frame=="divalent":
        return {"addressee_index":None, "suffix":None, "note":"predicate retains O-indexing"}
    return None

def negative_imperative(frame):
    if frame in {"monovalent","extended_intransitive"}:
        return {"pattern":"2=LEX-ka-ba"}
    if frame=="divalent":
        return {"pattern":"2A=ka-ba O=LEX"}
    return None
