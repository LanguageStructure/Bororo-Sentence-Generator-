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


## Manual-required adjudication

The 13 manually scorable tokens were reviewed against their sentence, translation and annotation, without modifying the frozen grammar.

- 0.1.BEBE, `aidu`: supported. Propositional content is compatible with the reviewed extended-intransitive lexical analysis.
- ABE-30, `mako`: supported. Absolute use does not contradict the reviewed lexical class.
- ABE-48, ABE-49, ABE-219, ABE-291, ABE-292, and C.O.82-2b, `ako`: supported. Clausal or nominal speech content without an overt interlocutor does not contradict the reviewed lexical license; selection of an interlocutor with `ji` does not require that participant to be overt in every occurrence.
- ABE-305 and ABE-306, `aiwo`: supported. `kuiejedoge i` provides a postpositionally coded complement with `ji`, matching the reviewed analysis.
- ABE-316, `rema`: supported. The annotation `Pred=AtrEq` and translation are compatible with the frozen identificational-copula analysis.
- ABE-241, `mako ... bapera to`: unresolved. The `to` phrase may reflect a distinct construction/semantic relation and is not sufficient to revise the frozen lexical license.
- ABE-246, causative `aiwodo`: unresolved for lexical-frame scoring. A causative construction should not be used directly to revise the valency of the base.

Manual-required totals: 11 supported, 2 unresolved, 0 newly established conflicts.

## Final covered-token accounting

Of 194 test predicate tokens, 64 (32.99%) have a frozen grammar-v2 lexical license and 130 (67.01%) are outside lexical coverage.

Among the 64 covered tokens:

- 41 mechanical matches
- 2 supported contextual/implicit-object cases
- 11 manually supported cases
- 8 genuine token-level conflicts, all attributable to one frozen lexical-license error (`ro: divalent`)
- 2 unresolved cases

Thus 54/64 covered tokens (84.38%) are positively compatible with the frozen grammar, 8/64 (12.50%) conflict, and 2/64 (3.12%) remain unresolved. Restricting the denominator to adjudicable covered tokens gives 54/62 = 87.10% compatibility.

The preferred description is **compatibility rate among adjudicable covered predicate tokens**, not accuracy. Coverage and compatibility must be reported separately. The eight conflicting tokens must also be distinguished from the single underlying lexical-license error.
