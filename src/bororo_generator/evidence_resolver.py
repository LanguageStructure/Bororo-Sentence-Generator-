"""Resolve lexical evidence without collapsing evidence sources.

Dictionary evidence is private/local; grammar review is explicit; corpus evidence
is observational.  Conflicts and gaps remain visible instead of being guessed.
"""
from dataclasses import dataclass, field
from typing import Any
from .private_dictionary import lookup_private, lexical_evidence
from .valency_review import valency_entry
from .person_index import reviewed_stem_class

@dataclass
class LexicalEvidence:
    lemma: str
    dictionary: list[dict[str,Any]]=field(default_factory=list)
    grammar: dict[str,Any]=field(default_factory=dict)
    corpus: dict[str,Any]=field(default_factory=dict)
    ambiguities: list[str]=field(default_factory=list)

    @property
    def generation_ready(self):
        return bool(self.grammar.get("frame")) and not self.ambiguities

def resolve_lexeme(lemma, dictionary_entries=None, corpus_evidence=None, valency_path=None):
    dictionary_entries=dictionary_entries or []
    matches=[lexical_evidence(x) for x in lookup_private(dictionary_entries,lemma)]
    kwargs={} if valency_path is None else {"path":valency_path}
    val=valency_entry(lemma,**kwargs)
    grammar={}
    if val:
        grammar["frame"]=val.get("frame")
        grammar["valency_status"]=val.get("status")
    cls=reviewed_stem_class(lemma)
    if cls:
        grammar["stem_class"]=cls
    ambiguities=[]
    if len(matches)>1:
        ambiguities.append("dictionary_homography")
    return LexicalEvidence(
        lemma=lemma,dictionary=matches,grammar=grammar,
        corpus=corpus_evidence or {},ambiguities=ambiguities
    )
