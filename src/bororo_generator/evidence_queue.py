"""Evidence-first queue for expanding the reviewed lexicon.

This module does not assign coding frames or stem classes. It ranks corpus
lemmas by the amount of person-index/form evidence available for human review.
"""
from collections import Counter,defaultdict
from .corpus import read_conllu
from .orthography import form_key
from .valency_review import reviewed_frame
from .person_index import reviewed_stem_class
from .lexical_review import review_status, lexical_review


def lexical_evidence_queue(corpus_path, minimum_tokens=2):
    stats=defaultdict(lambda:{"tokens":0,"forms":Counter(),"sent_ids":set()})
    for s in read_conllu(corpus_path):
        for t in s.tokens:
            lemma=t.get("lemma"); form=t.get("form")
            if not lemma or not form or lemma=="_": continue
            key=form_key(str(lemma))
            d=stats[key]; d["tokens"]+=1
            d["forms"][form_key(str(form))]+=1; d["sent_ids"].add(s.sent_id)
    rows=[]
    for lemma,d in stats.items():
        if d["tokens"]<minimum_tokens: continue
        frame=reviewed_frame(lemma); cls=reviewed_stem_class(lemma)
        if frame is not None and cls is not None: continue
        forms=d["forms"]
        # Descriptive review signal only: diversity/frequency, not a class inference.
        rows.append({
            "lemma":lemma,"tokens":d["tokens"],"distinct_forms":len(forms),
            "top_forms":forms.most_common(8),
            "sent_ids":sorted(d["sent_ids"])[:12],
            "reviewed_frame":frame,"reviewed_stem_class":cls,
            "needs":["coding_frame"]*(frame is None)+["stem_class"]*(cls is None),
            "review_status":review_status(lemma,frame,cls),
            "review_note":(lexical_review(lemma) or {}).get("note"),
        })
    rows.sort(key=lambda r:(-r["distinct_forms"],-r["tokens"],r["lemma"]))
    return rows
