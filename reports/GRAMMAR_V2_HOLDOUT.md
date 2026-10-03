# Grammar-v2 source-group holdout

This file documents the frozen source-group split reported in the accompanying manuscript. The machine-readable specification is `reports/grammar-v2-holdout-manifest.json`.

The eligible annotated corpus contained 784 sentences after four singleton records with unresolved provenance were excluded. The split was made by whole documentary source group rather than by individual sentence. Development contains 627 sentences (79.97%). The held-out partition contains 157 sentences (20.03%) from ABE, BEBE, and C.O.

The test is partially unblinded: three ABE examples and two BEBE examples had been seen during earlier corpus inspection. They were not used to create or revise a grammar-v2 license. Grammar-v2 contained 28 accepted lexical licenses; `jorudu`, `joruduwa`, and `ciri` remained uncertain and were excluded before systematic test evaluation.

## Evaluation rule

The split and grammar remain fixed while held-out cases are evaluated. A predicate absent from the frozen lexical inventory is reported as outside lexical coverage, not as an error. Human adjudication may classify a covered token as compatible, conflicting, or unresolved, but may not change a lexical or constructional license during the same experiment.

## Historical reported result

The 157 held-out sentences contain 194 VERB/AUX predicate tokens. Sixty-four have a frozen lexical license and 130 are outside lexical coverage. Of the 64 covered tokens, 54 were compatible, eight conflicting, and two unresolved. The eight conflicts instantiate one underlying lexical-license error involving `ro`.

The resulting 54/62 value is a compatibility rate among adjudicable covered predicate tokens. It is not an accuracy estimate over unseen Bororo.

## Re-evaluation

A future run against a changed CorBo release or revised annotation must preserve this record and create a new manifest version. It must not overwrite this historical split or its reported result. Exact sentence-level reconstruction additionally requires the original source-to-sentence mapping or an equivalent versioned corpus artifact.
