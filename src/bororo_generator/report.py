"""Build a JSON evidence report before any sentence generation is enabled."""
import json
from pathlib import Path
from .corpus import corpus_summary
from .patterns import extract_patterns
from .lexicon import build_lexicon
from .valency import extract_valency
def build_report(conllu,out=None,top=100):
 data={"source":str(conllu),"summary":corpus_summary(conllu),"construction_patterns":[p.__dict__ for p in extract_patterns(conllu,mode="construction")[:top]],"surface_patterns":[p.__dict__ for p in extract_patterns(conllu,mode="surface")[:top]],"lexicon":build_lexicon(conllu),"valency":extract_valency(conllu)}
 if out:
  p=Path(out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
 return data
