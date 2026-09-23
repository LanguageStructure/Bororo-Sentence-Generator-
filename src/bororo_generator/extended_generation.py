"""Controlled generation for reviewed extended-intransitive predicates.

The lexical predicate remains monovalent for core participant coding.  An
additional participant may be realized in a separately reviewed postpositional
construction.  No transitive A/O template is introduced here.
"""
from .person_index import indexed_reviewed_stem
from .valency_review import reviewed_frame, reviewed_oblique
from .candidate import Candidate
from .provenance import Provenance

def extended_intransitive_declarative(
    lemma, s_person, oblique_phrase=None,
    valency_path="config/valency_review.yaml"
):
    if reviewed_frame(lemma,valency_path)!="extended_intransitive":
        return None
    stem=indexed_reviewed_stem(lemma,s_person)
    if stem is None:
        return None

    marker=reviewed_oblique(lemma,valency_path)
    if oblique_phrase is not None and marker is None:
        # The existence of an oblique frame does not license guessing its marker.
        return None

    text=stem+"re"
    rules=["reviewed_extended_intransitive_frame","reviewed_person_cell_or_class","declarative_re"]
    if oblique_phrase is not None:
        text += " " + oblique_phrase.strip() + " " + marker
        rules.append("reviewed_selected_oblique")

    predicate=stem+"re"
    return Candidate(text,Provenance(
        status="generated",
        pattern="reviewed extended intransitive: S=LEX-re (... RP POSTP)",
        rules=rules,
        notes=[f"lemma={lemma}",f"S={s_person}",
               "Additional participant is oblique, not O."],
    ),predicate_form=predicate)
