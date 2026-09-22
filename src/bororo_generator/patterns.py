"""Extract corpus-grounded dependency templates from CorBo."""
from collections import Counter,defaultdict
from dataclasses import dataclass
from .corpus import read_conllu
@dataclass(frozen=True)
class Pattern:
 signature:str; frequency:int; examples:tuple; sent_ids:tuple; complexity:int
def _rel(t):return str(t.get("deprel") or "dep").split(":")[0]
def signature(s):
 """Linear POS+dependency signature: useful for exact surface templates."""
 return " ".join(f"{t.get('upos') or 'X'}:{t.get('deprel') or 'dep'}" for t in s.tokens)
def construction_signature(s):
 """Abstract clause signature centered on the root and its direct dependents."""
 by_head=defaultdict(list);root=None
 for t in s.tokens:
  if t.get("head")==0:root=t
  by_head[t.get("head")].append(t)
 if not root:return "NO_ROOT"
 rid=root["id"]; deps=sorted((_rel(t),t.get("upos") or "X") for t in by_head.get(rid,[]) if _rel(t)!="punct")
 return f"ROOT={root.get('upos') or 'X'}|"+"|".join(f"{r}:{p}" for r,p in deps)
def valency_signature(s):
 """Core complement frame of the root predicate."""
 root=next((t for t in s.tokens if t.get("head")==0),None)
 if not root:return "NO_ROOT"
 core={"nsubj","csubj","obj","iobj","obl","xcomp","ccomp"}
 deps=sorted(_rel(t) for t in s.tokens if t.get("head")==root["id"] and _rel(t) in core)
 return f"{root.get('lemma') or root.get('form') or '?'}:" + ("+".join(deps) if deps else "Ø")
def complexity(s):
 """Provisional transparent 1–5 scale; not a grammaticality judgment."""
 n=len(s.tokens);deps={_rel(t) for t in s.tokens};score=1
 if n>=4:score+=1
 if n>=7 or {"obj","obl"}&deps:score+=1
 if {"ccomp","xcomp","advcl","acl"}&deps:score+=1
 if n>=12 or {"conj","parataxis"}&deps:score+=1
 return min(score,5)
def extract_patterns(path,min_frequency=1,example_limit=5,mode="construction"):
 fn={"surface":signature,"construction":construction_signature,"valency":valency_signature}[mode]
 counts=Counter();examples=defaultdict(list);ids=defaultdict(list);levels=defaultdict(list)
 for s in read_conllu(path):
  sig=fn(s);counts[sig]+=1;levels[sig].append(complexity(s))
  if len(examples[sig])<example_limit:examples[sig].append(s.text);ids[sig].append(s.sent_id)
 return [Pattern(sig,n,tuple(examples[sig]),tuple(ids[sig]),round(sum(levels[sig])/len(levels[sig]))) for sig,n in counts.most_common() if n>=min_frequency]
