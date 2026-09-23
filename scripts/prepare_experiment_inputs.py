#!/usr/bin/env python3
import argparse,json,hashlib
from pathlib import Path

def sha256_text(s): return hashlib.sha256(s.encode("utf8")).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("tasks")
    ap.add_argument("--direct-prompt",default="article/prompts/direct-v1.txt")
    ap.add_argument("--proposal-prompt",default="article/prompts/proposal-v1.txt")
    ap.add_argument("--output-dir",required=True)
    a=ap.parse_args()
    tasks=[json.loads(x) for x in Path(a.tasks).read_text(encoding="utf8").splitlines() if x.strip()]
    direct=Path(a.direct_prompt).read_text(encoding="utf8")
    proposal=Path(a.proposal_prompt).read_text(encoding="utf8")
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    for condition,prompt in [("direct",direct),("proposal",proposal)]:
        with (out/f"{condition}-inputs.jsonl").open("w",encoding="utf8") as fh:
            for t in tasks:
                fh.write(json.dumps({"condition":condition,"task":t,"prompt":prompt},ensure_ascii=False)+"\n")
    manifest={
      "experiment_version":"v1",
      "tasks":len(tasks),
      "direct_prompt_sha256":sha256_text(direct),
      "proposal_prompt_sha256":sha256_text(proposal),
      "note":"No model outputs are contained in this manifest."
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print(json.dumps(manifest,indent=2))

if __name__=="__main__": main()
