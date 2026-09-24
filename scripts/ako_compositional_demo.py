#!/usr/bin/env python3
from bororo_generator.compositional import realize_ako

cases=[
 ("1SG.IND",dict(person=1,number="Sing",mood="Ind")),
 ("3SG.IND",dict(person=3,number="Sing",mood="Ind")),
 ("3PL.IND",dict(person=3,number="Plur",mood="Ind")),
 ("1SG.NEG.IND",dict(person=1,number="Sing",mood="Ind",polarity="Neg")),
 ("1PL.EXCL.IND",dict(person=1,number="Plur",clusivity="Ex",mood="Ind")),
 ("3SG.IRR.IND",dict(person=3,number="Sing",mood="Ind",status="Irr")),
 ("1SG.POSS",dict(person=1,number="Sing",usage="nominal_possessive")),
 ("3PL.POSS",dict(person=3,number="Plur",usage="nominal_possessive")),
 ("2SG.IND (unreviewed)",dict(person=2,number="Sing",mood="Ind")),
 ("CAUS (ambiguous -do)",dict(person=3,number="Sing",derivation="Cau")),
]
for label,args in cases:
 print(f"{label:22} -> {realize_ako(**args) or '[BLOCKED]'}")
