"""Reviewed Bororo person-index allomorphy.

Source: author's Bororo grammar draft, §4.4.1.2, especially the concrete
representative paradigms in Table 4.35. Earlier/provisional paradigm material
in the draft is not silently reconciled where it differs. Only explicitly
reviewed stem classes are realized; class is never inferred from spelling.
"""
INDEXES={
"C":{"1SG":"i","2SG":"a","3SG":"","1PL.INCL":"pa","1PL.EXCL":"ce","2PL":"ta","3PL":"e","CORF":"tu"},
"U":{"1SG":"i","2SG":"a","3SG":"u","1PL.INCL":"pa","1PL.EXCL":"ce","2PL":"ta","3PL":"e","CORF":"tu"},
"O":{"1SG":"it","2SG":"ak","3SG":"","1PL.INCL":"pag","1PL.EXCL":"ceg","2PL":"tag","3PL":"et","CORF":"t"},
"N":{"1SG":"in","2SG":"ak","3SG":"","1PL.INCL":"pag","1PL.EXCL":"ce","2PL":"tag","3PL":"en","CORF":"t"},
"I":{"1SG":"ik","2SG":"ak","3SG":"","1PL.INCL":"pag","1PL.EXCL":"ceg","2PL":"tag","3PL":"e","CORF":"tug"},
}
def indexed_stem(stem,person,stem_class):
    if stem_class not in INDEXES: raise ValueError(f"unknown Bororo stem class: {stem_class}")
    if person not in INDEXES[stem_class]: raise ValueError(f"unreviewed person/index cell: {person}")
    return INDEXES[stem_class][person]+stem


# Lexical class assignments must be reviewed independently of the paradigm.
# Representative roots below are explicitly exemplified in the grammar.
REVIEWED_STEM_CLASSES = {
    "tugo": "C",
    "nudu": "U",
    "meru": "C",
    "kodu": "C",
    "aregodu": "O",
    "ogwa": "N",
    "ie": "I",
}

def reviewed_stem_class(stem):
    """Return a human/grammar-reviewed class, or None if unresolved."""
    return REVIEWED_STEM_CLASSES.get(stem)

def indexed_reviewed_stem(stem, person):
    """Realize only roots whose class has already been reviewed."""
    cls = reviewed_stem_class(stem)
    if cls is None:
        return None
    return indexed_stem(stem, person, cls)
