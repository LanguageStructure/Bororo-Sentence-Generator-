"""Observed root-predicate valency frames. Descriptive evidence, not prescriptive grammar."""
from collections import Counter,defaultdict
from .corpus import read_conllu
CORE={"nsubj","csubj","obj","iobj","obl","xcomp","ccomp"}
def extract_valency(path):
 out=defaultdict(Counter);examples=defaultdict(lambda:defaultdict(list))
 for s in read_conllu(path):
  root=next((t for t in s.tokens if t.get("head")==0),None)
  if not root:continue
  lemma=str(root.get("lemma") or root.get("form") or "?")
  frame=tuple(sorted(str(t.get("deprel")).split(":")[0] for t in s.tokens if t.get("head")==root["id"] and str(t.get("deprel")).split(":")[0] in CORE))
  out[lemma][frame]+=1
  if len(examples[lemma][frame])<5:examples[lemma][frame].append(s.sent_id)
 return {lemma:[{"frame":list(frame),"frequency":n,"sent_ids":examples[lemma][frame]} for frame,n in frames.most_common()] for lemma,frames in out.items()}
