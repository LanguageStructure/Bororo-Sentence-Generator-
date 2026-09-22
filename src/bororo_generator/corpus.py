"""Read CorBo CoNLL-U data without modifying the source corpus."""
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from conllu import parse_incr
@dataclass(frozen=True)
class CorpusSentence:
 sent_id:str; text:str; translation_por:str; tokens:tuple
def read_conllu(path):
 with Path(path).open(encoding="utf-8") as stream:
  for i,sent in enumerate(parse_incr(stream),1):
   m=sent.metadata or {}; toks=tuple(dict(t) for t in sent if isinstance(t.get("id"),int))
   yield CorpusSentence(str(m.get("sent_id",f"sentence-{i}")),str(m.get("text","")),str(m.get("text_por","")),toks)
def corpus_summary(path):
 ss=list(read_conllu(path)); forms=Counter();lemmas=Counter();upos=Counter();rels=Counter()
 for s in ss:
  for t in s.tokens:
   forms[str(t.get("form","")).lower()]+=1
   if t.get("lemma"):lemmas[str(t["lemma"]).lower()]+=1
   if t.get("upos"):upos[str(t["upos"])]+=1
   if t.get("deprel"):rels[str(t["deprel"])]+=1
 return {"sentences":len(ss),"tokens":sum(forms.values()),"types":len(forms),"lemmas":len(lemmas),"upos":dict(upos.most_common()),"relations":dict(rels.most_common())}
