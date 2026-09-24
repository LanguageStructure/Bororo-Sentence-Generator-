import argparse,json
from .corpus import corpus_summary
from .patterns import extract_patterns
def main():
 p=argparse.ArgumentParser(description="Inspect CorBo and extract attested syntactic patterns.");p.add_argument("conllu");p.add_argument("--top",type=int,default=30);p.add_argument("--min-frequency",type=int,default=1);p.add_argument("--json",action="store_true");a=p.parse_args()
 result={"summary":corpus_summary(a.conllu),"patterns":[x.__dict__ for x in extract_patterns(a.conllu,a.min_frequency)[:a.top]]}
 if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
 else:
  s=result["summary"];print(f"Sentences: {s['sentences']} | tokens: {s['tokens']} | types: {s['types']}")
  for i,x in enumerate(result["patterns"],1):print(f"{i:>2}. n={x['frequency']:<4} level={x['complexity']} {x['signature']}")
if __name__=="__main__":main()
