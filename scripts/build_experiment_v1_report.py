#!/usr/bin/env python3
"""Build a compact v1 experiment report from frozen outputs and audits."""
import argparse,json
from pathlib import Path

def load_json(p): return json.loads(Path(p).read_text(encoding="utf8"))
def load_jsonl(p): return [json.loads(x) for x in Path(p).read_text(encoding="utf8").splitlines() if x.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--direct-summary",required=True)
    ap.add_argument("--proposal-alignment",required=True)
    ap.add_argument("--proposal-scored",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    d=load_json(a.direct_summary)
    align=load_jsonl(a.proposal_alignment)
    scored=load_jsonl(a.proposal_scored)
    n=d["rows"]
    exact_yes=int(d["exact_match"].get("yes",0))
    fully_aligned=sum(bool(x["aligned"]) for x in align)
    generated=sum(not bool((x.get("score") or x).get("blocked",False)) for x in scored)
    report={
      "schema_version":"1.0",
      "experiment_version":"v1",
      "n_tasks":n,
      "condition_A_direct":{
        "exact_surface_match":{"yes":exact_yes,"no":n-exact_yes,"rate":exact_yes/n if n else None},
        "auditor_status":d["auditor_status"],
        "dimensions":d["dimensions"],
        "interpretation_note":"Exact surface nonmatch is not equivalent to ungrammaticality. Audit dimensions remain independent."
      },
      "condition_B_evidence_bounded":{
        "proposal_task_alignment":{"fully_aligned":fully_aligned,"mismatch":len(align)-fully_aligned,"rate":fully_aligned/len(align) if align else None},
        "deterministic_realization":{"generated":generated,"blocked":len(scored)-generated,"rate":generated/len(scored) if scored else None},
        "interpretation_note":"Generation means the frozen reviewed system licensed and realized the submitted structural proposal; it is not an independent native-speaker grammaticality judgment."
      },
      "comparison_note":"Do not collapse the multidimensional direct audit and bounded-system realization into a single accuracy score."
    }
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(f"tasks: {n}")
    print(f"direct_exact_surface_match: {exact_yes}/{n}")
    print(f"proposal_fully_aligned: {fully_aligned}/{len(align)}")
    print(f"bounded_generated: {generated}/{len(scored)}")
    print(f"output: {out}")

if __name__=="__main__": main()
