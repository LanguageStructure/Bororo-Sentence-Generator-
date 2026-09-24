"""Context audit for lexical review candidates.

Shows corpus sentences and token analyses without assigning a coding frame,
stem class, or morphological segmentation.
"""
from collections import Counter
from .corpus import read_conllu
from .orthography import form_key

def audit_lemma_contexts(corpus_path, lemma, limit=30, form=None):
    key=form_key(lemma); form_filter=form_key(form) if form else None; rows=[]
    for s in read_conllu(corpus_path):
        hits=[t for t in s.tokens if form_key(str(t.get("lemma","")))==key and
              (form_filter is None or form_key(str(t.get("form","")))==form_filter)]
        if not hits: continue
        for t in hits:
            rows.append({
                "sent_id":s.sent_id,
                "text":s.text,
                "text_por":getattr(s,"translation_por",None),
                "form":str(t.get("form","")),
                "upos":str(t.get("upos","")),
                "deprel":str(t.get("deprel","")),
                "head":t.get("head"),
            })
            if len(rows)>=limit: return rows
    return rows

def audit_summary(rows):
    return {
        "occurrences":len(rows),
        "forms":Counter(r["form"] for r in rows).most_common(),
        "upos":Counter(r["upos"] for r in rows).most_common(),
        "deprel":Counter(r["deprel"] for r in rows).most_common(),
    }
