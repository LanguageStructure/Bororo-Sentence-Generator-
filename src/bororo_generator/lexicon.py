"""Lexical inventory derived strictly from attested CoNLL-U tokens."""
from collections import Counter,defaultdict
from .corpus import read_conllu
def build_lexicon(path):
 acc=defaultdict(lambda:{"forms":Counter(),"upos":Counter(),"deprels":Counter(),"examples":[]})
 for s in read_conllu(path):
  for t in s.tokens:
   lemma=str(t.get("lemma") or t.get("form") or "").strip()
   if not lemma or lemma=="_":continue
   a=acc[lemma];a["forms"][str(t.get("form") or lemma)]+=1;a["upos"][str(t.get("upos") or "X")]+=1;a["deprels"][str(t.get("deprel") or "dep")]+=1
   if len(a["examples"])<5:a["examples"].append(s.sent_id)
 return {lemma:{"frequency":sum(a["forms"].values()),"forms":dict(a["forms"].most_common()),"upos":dict(a["upos"].most_common()),"deprels":dict(a["deprels"].most_common()),"sent_ids":a["examples"]} for lemma,a in acc.items()}
