#!/usr/bin/env python3
import sys
from bororo_generator.corpus import read_conllu
from bororo_generator.dependency_audit import audit_lemma_context

path=sys.argv[1] if len(sys.argv)>1 else "data/corbo/trusted.conllu"
a=audit_lemma_context(read_conllu(path),"ako")
for form,d in sorted(a.items(),key=lambda x:-x[1]["count"]):
 print(f"\n{form}: {d['count']}")
 print("  relations:",dict(d["deprel"].most_common()))
 print("  heads:",dict(d["head"].most_common(8)))
 print("  dependents:")
 for k,n in d["dependents"].most_common(15):print(f"    {n:>3}  {k}")
 print("  examples:")
 for e in d["examples"][:3]:print(f"    {e['sent_id']}: {e['text']}")
