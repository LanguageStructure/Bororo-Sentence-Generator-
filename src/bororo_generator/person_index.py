"""Reviewed Bororo person-index allomorphy.

The class system is reviewed from the descriptive grammar, but lexical class
assignments carry their own provenance. Representative full paradigms and
assignments supported only by constructional examples are not conflated.
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

# Only roots explicitly presented as representative paradigms in the reviewed
# stem-class table are licensed as full lexical classes here.
REVIEWED_STEM_CLASSES={
    "tugo":"C",
    "nudu":"U",
    "aregodu":"O",
    "ogwa":"N",
    "ie":"I",
}

# Other roots may have reviewed individual forms in constructional examples.
# These cells are useful evidence but do not establish a complete lexical class.
REVIEWED_PERSON_CELLS={
    "meru":{"2SG":"ameru","1PL.EXCL":"cemeru","3PL":"emeru"},
    "kodu":{"1SG":"ikodu","1PL.EXCL":"cegodu","3PL":"ekodu","CORF":"tugodu"},
    "maragodu":{"2PL":"tamaragodu"},
    "mako":{"1SG":"imago","2SG":"amago","3SG":"mako","1PL.EXCL":"cemago","2PL":"tamago","3PL":"emago"},
    "kudu":{"2SG":"akudu"},
    "maku":{"3SG":"maku","3PL":"emagu"},
}

def reviewed_stem_class(stem):
    return REVIEWED_STEM_CLASSES.get(stem)

REVIEWED_PERSON_ANALYSES={
    ("maku","3PL"):{"index":"e","lexeme":"maku","surface":"emagu"},
}

def reviewed_person_cell(stem,person):
    return REVIEWED_PERSON_CELLS.get(stem,{}).get(person)

def reviewed_person_analysis(stem,person):
    return REVIEWED_PERSON_ANALYSES.get((stem,person))

def indexed_reviewed_stem(stem,person):
    cell=reviewed_person_cell(stem,person)
    if cell is not None: return cell
    cls=reviewed_stem_class(stem)
    if cls is None: return None
    return indexed_stem(stem,person,cls)

def reviewed_persons(stem):
    cls=reviewed_stem_class(stem)
    if cls is not None: return tuple(INDEXES[cls])
    return tuple(REVIEWED_PERSON_CELLS.get(stem,{}))


# Construction-specific reviewed cells must not be promoted to the ordinary
# person paradigm. Surface includes the constructional morphology.
REVIEWED_CONSTRUCTION_CELLS={
    "mako":{
        "imperative":{
            "2SG":"amagodo",
            "2PL":"tamagodo",
        },
        "negative_indicative":{
            "1SG":"imagokare",
            "3SG":"makokare",
            "3PL":"emagokare",
        },
        "irrealis_indicative":{
            "1SG":"imagomode",
        },
    },
    "kodu":{
        "irrealis_indicative":{
            "1SG":"ikodumode",
            "1PL.INCL":"pagodumode",
        },
        "imperative":{
            "2SG":"akodudo",
        },
        "gerund":{
            "1SG":"ikodui",
        },
        "optative":{
            "1SG":"ikoduia",
        },
        "subjunctive":{
            "1SG":"ikoduwo",
        },
        "irrealis_negative_indicative":{
            "3SG":"kodumodukare",
        },
    },
}

def reviewed_construction_cell(stem,construction,person):
    return REVIEWED_CONSTRUCTION_CELLS.get(stem,{}).get(construction,{}).get(person)

def reviewed_construction_persons(stem,construction):
    return tuple(REVIEWED_CONSTRUCTION_CELLS.get(stem,{}).get(construction,{}))
