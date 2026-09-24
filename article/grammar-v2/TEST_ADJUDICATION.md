# Grammar-v2 test adjudication

Date: 2026-09-24

This document records post-freeze human adjudication. It does not modify the frozen grammar-v2.

## Evaluator correction before adjudication

Six apparent frame mismatches were caused by the evaluator applying the valency of a monovalent base directly to forms annotated `Voice=Cau` (`okwagedo`, `kodudo`). The evaluator was corrected generically so that a causative derived from a licensed monovalent base is evaluated as divalent. After rerunning the same frozen test, these six false mismatches disappeared.

## annotation_or_implicit_object cases

The rerun produced 10 such tokens.

- `0.5.BEBE`, `bito`: compatible with the frozen divalent analysis. The first occurrence lacks an overt object, while immediately following parallel clauses contain overt `karo` and `kiogo` objects. Adjudication: `SUPPORTED_CONTEXTUAL_OMISSION`.
- `ABE-21`, `maku`: compatible with the frozen divalent analysis. The translation explicitly has “dê-o aos jovens”; the theme is implicit and the recipient is oblique. Adjudication: `SUPPORTED_IMPLICIT_OBJECT`.
- Eight `ro` tokens: post-test linguistic adjudication by the Bororo grammar reviewer establishes that `ro` is not transitive. The frozen grammar-v2 license `ro: divalent` is therefore an error. These are recorded as eight token-level conflicts arising from one lexical-license error. The frozen configuration must not be changed retrospectively.

The ABE examples `rore` ‘(isso) é gostoso’, `rorewu` and `rorewuge` additionally show that the test material contains uses that made the frozen divalent analysis untenable. The BEBE forms `erore` and `rokare` likewise occur without an object.

## Current status

Frozen-test aggregate after the causative evaluator correction:

- test sentences: 157
- predicate tokens: 194
- licensed predicate tokens: 64
- unlicensed predicate tokens: 130
- mechanical matches: 41
- manual-required: 13
- annotation-or-implicit-object: 10
- mechanical frame mismatches: 0

Human adjudication of the 10 annotation-or-implicit-object tokens:

- supported contextual/implicit object: 2
- genuine token-level conflicts with frozen grammar: 8
- underlying frozen lexical-license errors: 1 (`ro`)

These results are not yet a final accuracy figure. The 13 `manual_required` tokens remain to be adjudicated.
