"""Reviewed Bororo person-index allomorphy.

Source: author's Bororo grammar draft, §4.4.1.2, Table 4.8.
Only explicitly described stem classes are realized. Stem class is never
inferred from spelling.
"""
INDEXES={
"C":{"1SG":"i","2SG":"a","3SG":"","1PL.INCL":"pa","1PL.EXCL":"ce","2PL":"ta","3PL":"e","CORF":"tu"},
"U":{"1SG":"i","2SG":"a","3SG":"u","1PL.INCL":"pa","1PL.EXCL":"ce","2PL":"ta","3PL":"e","CORF":"tu"},
"O":{"1SG":"it","2SG":"ak","3SG":"","1PL.INCL":"pag","1PL.EXCL":"ceg","2PL":"tag","3PL":"et","CORF":"t"},
"N":{"1SG":"in","2SG":"ak","3SG":"","1PL.INCL":"pag","1PL.EXCL":"cen","2PL":"tag","3PL":"en","CORF":"t"},
"I":{"1SG":"ik","2SG":"ak","3SG":"","1PL.INCL":"pag","1PL.EXCL":"ceg","2PL":"tag","3PL":"e","CORF":"tug"},
}
def indexed_stem(stem,person,stem_class):
    if stem_class not in INDEXES: raise ValueError(f"unknown Bororo stem class: {stem_class}")
    if person not in INDEXES[stem_class]: raise ValueError(f"unreviewed person/index cell: {person}")
    return INDEXES[stem_class][person]+stem
