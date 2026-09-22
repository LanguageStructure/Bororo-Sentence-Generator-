"""Extract reproducible syntactic templates from dependency-annotated CorBo sentences."""
from collections import Counter,defaultdict
from dataclasses import dataclass
from .corpus import read_conllu
@dataclass(frozen=True)
class Pattern:
 signature:str; frequency:int; examples:tuple; sent_ids:tuple; complexity:int
def signature(s):
 return " ".join(f"{t.get('upos') or 'X'}:{t.get('deprel') or 'dep'}" for t in s.tokens)
def complexity(s):
 n=len(s.tokens); deps={str(t.get("deprel","")).split(":")[0] for t in s.tokens};score=1
 if n>=4:score+=1
 if n>=7 or {"obj","obl"}&deps:score+=1
 if {"ccomp","xcomp","advcl","acl"}&deps:score+=1
 if n>=12 or {"conj","parataxis"}&deps:score+=1
 return min(score,5)
def extract_patterns(path,min_frequency=1,example_limit=5):
 counts=Counter();examples=defaultdict(list);ids=defaultdict(list);levels=defaultdict(list)
 for s in read_conllu(path):
  sig=signature(s);counts[sig]+=1;levels[sig].append(complexity(s))
  if len(examples[sig])<example_limit:examples[sig].append(s.text);ids[sig].append(s.sent_id)
 return [Pattern(sig,n,tuple(examples[sig]),tuple(ids[sig]),round(sum(levels[sig])/len(levels[sig]))) for sig,n in counts.most_common() if n>=min_frequency]
