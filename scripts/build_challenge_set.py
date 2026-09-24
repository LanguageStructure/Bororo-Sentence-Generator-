#!/usr/bin/env python3
import argparse,json
from pathlib import Path
P,N,B="positive","negative","boundary"
def task(i,cls,lemma,*,s=None,a=None,o=None,construction="indicative",oblique=None,basis=""):
 return {"task_id":f"challenge-v1-{i:03d}","gold_class":cls,"expected_decision":{P:"GENERATE",N:"BLOCK",B:"ABSTAIN"}[cls],"lemma":lemma,"construction":construction,"s_person":s,"a_person":a,"o_person":o,"oblique_phrase":oblique,"evidence_basis":basis,"grammar_version":"v1"}
def build():
 rows=[]; i=1
 pos=[("nudu",x,None,None) for x in ("1SG","2SG","3SG","1PL.INCL","1PL.EXCL","2PL","3PL","CORF")]+[("meru",x,None,None) for x in ("2SG","1PL.INCL","1PL.EXCL","3PL")]+[("kodu",x,None,None) for x in ("1SG","1PL.EXCL","3PL","CORF")]+[("mako",x,None,None) for x in ("1SG","2SG","3SG","1PL.EXCL","2PL","3PL")]
 for lemma,s,a,o in pos: rows.append(task(i,P,lemma,s=s,basis="reviewed frame + reviewed ordinary-indicative person cell/class")); i+=1
 for a,o in (("2SG","3SG"),("2SG","3PL"),("3SG","3SG"),("3SG","3PL"),("3PL","3SG"),("3PL","3PL")): rows.append(task(i,P,"maku",a=a,o=o,basis="reviewed divalent frame + reviewed A host + reviewed O cell")); i+=1
 neg=[]
 for lemma in ("nudu","meru","kodu"):
  for a,o in (("2SG","3SG"),("3SG","3PL"),("3PL","3SG")): neg.append((lemma,None,a,o,None))
 for s in ("1SG","2SG","3SG","1PL.INCL","1PL.EXCL","2PL","3PL","CORF"): neg.append(("maku",s,None,None,None))
 for a,o in (("2SG","3SG"),("3SG","3PL"),("3PL","3SG"),("2SG","3PL"),("3SG","3SG"),("3PL","3PL")): neg.append(("mako",None,a,o,None))
 for a,o in (("2SG","1SG"),("3SG","1SG"),("3PL","1SG"),("2SG","2PL"),("3SG","2PL")): neg.append(("mako",None,a,o,"Boe"))
 assert len(neg)==28
 for lemma,s,a,o,obl in neg: rows.append(task(i,N,lemma,s=s,a=a,o=o,oblique=obl,basis="requested core-argument configuration contradicts reviewed coding frame")); i+=1
 boundary=[("meru","1SG","indicative"),("meru","3SG","indicative"),("meru","2PL","indicative"),("meru","CORF","indicative"),("kodu","2SG","indicative"),("kodu","3SG","indicative"),("kodu","1PL.INCL","indicative"),("kodu","2PL","indicative"),("mako","1PL.INCL","indicative"),("mako","CORF","indicative"),("kudu","1SG","indicative"),("kudu","3SG","indicative"),("kudu","1PL.EXCL","indicative"),("kudu","3PL","indicative"),("nudu","1PL.EXCL","subjunctive"),("nudu","1SG","negative_indicative"),("mako","2SG","imperative"),("mako","2PL","imperative"),("mako","1SG","negative_indicative"),("mako","3SG","negative_indicative"),("mako","3PL","negative_indicative"),("mako","1SG","irrealis_indicative"),("mako","CORF","gerund"),("kodu","2SG","imperative"),("kodu","1SG","gerund"),("kodu","1SG","optative"),("kodu","1SG","subjunctive"),("kodu","3SG","irrealis_negative_indicative")]
 assert len(boundary)==28
 for lemma,s,construction in boundary:
  basis="reviewed construction-specific cell is not an ordinary-indicative license" if construction!="indicative" else "reviewed frame exists but requested ordinary-indicative person cell lacks frozen v1 license"
  rows.append(task(i,B,lemma,s=s,construction=construction,basis=basis)); i+=1
 assert len(rows)==84
 return rows
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--output",default="reports/challenge-v1/tasks.jsonl"); a=ap.parse_args(); rows=build(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rows),encoding="utf8")
 from collections import Counter
 print("rows:",len(rows)); print("classes:",dict(Counter(r["gold_class"] for r in rows))); print("decisions:",dict(Counter(r["expected_decision"] for r in rows))); print("output:",out)
if __name__=="__main__": main()
