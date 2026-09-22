#!/usr/bin/env python3
"""Demonstrate provenance-bearing reviewed morphology for ako."""
import json
from bororo_generator.morph_candidate import ako_candidate

requests=[
 dict(person=1,number="Sing",mood="Ind"),
 dict(person=1,number="Sing",mood="Ind",polarity="Neg"),
 dict(person=1,number="Plur",clusivity="Ex",mood="Ind"),
 dict(person=1,number="Sing",usage="nominal_possessive"),
 dict(person=2,number="Sing",mood="Ind"),
]
for request in requests:
 c=ako_candidate(**request)
 if c is None:
  print(json.dumps({"request":request,"status":"BLOCKED","reason":"unreviewed morphology"},ensure_ascii=False))
 else:
  print(json.dumps({"request":request,**c.record()},ensure_ascii=False))
