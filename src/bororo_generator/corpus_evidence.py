"""Corpus-only observations for reviewed lexical targets.

This module reports what CorBo contains without licensing generation or
assigning unreviewed person cells.  It deliberately keeps corpus observation
separate from human-reviewed morphology.
"""
from collections import defaultdict
from .corpus import read_conllu
from .orthography import form_key

def corpus_lemma_forms(lemma, corpus_path):
    key=form_key(lemma)
    grouped=defaultdict(lambda: {"count":0,"sent_ids":[],"upos":set(),"deprels":set()})
    for sent in read_conllu(corpus_path):
        for tok in sent.tokens:
            if form_key(tok.get("lemma")) != key:
                continue
            form=str(tok.get("form") or "")
            row=grouped[form]
            row["count"]+=1
            if sent.sent_id not in row["sent_ids"]: row["sent_ids"].append(sent.sent_id)
            if tok.get("upos"): row["upos"].add(str(tok["upos"]))
            if tok.get("deprel"): row["deprels"].add(str(tok["deprel"]))
    return [
        {"form":form,"count":row["count"],"sent_ids":row["sent_ids"],
         "upos":sorted(row["upos"]),"deprels":sorted(row["deprels"]),
         "status":"corpus_observation",
         "licenses_generation":False}
        for form,row in sorted(grouped.items(),key=lambda x:(-x[1]["count"],form_key(x[0])))
    ]

def corpus_lexeme_inventory(lemmas, corpus_path):
    return {
        "corpus_path":str(corpus_path),
        "interpretation":"Corpus observations only; forms do not become reviewed morphology or license generation.",
        "lexemes":[{"lemma":lemma,"forms":corpus_lemma_forms(lemma,corpus_path)}
                   for lemma in lemmas],
    }
