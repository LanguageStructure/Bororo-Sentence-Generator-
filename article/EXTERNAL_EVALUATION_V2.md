# External evaluation v2: preregistered holdout protocol

## Purpose

This evaluation is distinct from the original 28-task experiment and from the
grammar-derived decision-boundary tests. Its purpose is to test the frozen
grammar on documentary Bororo material that was not selected from the grammar's
licensed cells.

The primary holdout source is `Boe Ero` in CorBo. `Adugo Biri` is reserved
and must not be inspected for item selection, grammar repair, or prompt tuning
before the confirmatory evaluation.

## Leakage rule

No output of the frozen grammar or generation pipeline may be consulted while
selecting, annotating, or adjudicating the holdout items. No rule, lexical
license, frame, paradigm cell, prompt, or decision policy may be changed in
response to a holdout item before the evaluation is complete.

If it can be established from repository history that the holdout source was
added after the grammar-v1 freeze and was not used in constructing v1, the
evaluation may be described as a temporal holdout. Otherwise it must be
described more conservatively as a document-level independently selected
holdout.

## Sampling unit

Sampling is by documentary unit ID, not by predicate, lemma, person cell, or
construction. This prevents the grammar inventory from determining which cases
enter the test.

The primary sample contains 32 units: four units from each of the eight
documentary sections of `Boe Ero`.

Selection is reproducible and fixed before linguistic annotation:

1. Parse all rows of `boe_ero_parallel.tsv`.
2. Group rows by the `section` field (1--8).
3. Sort each section by documentary `id`.
4. Apply Python `random.Random(20260924).sample(rows, 4)` independently to
   each section, processing sections in numeric order with the same RNG
   instance.
5. Sort the resulting 32 selected rows by documentary ID.
6. Save the selected IDs and source text before any gold linguistic analysis.

If a sampled row is unusable for a purely documentary reason (empty Bororo
source, duplicate documentary unit, corrupted encoding that prevents
interpretation, or demonstrable source/translation alignment error), it is not
silently replaced. The exclusion and reason are recorded, and a replacement is
drawn from the remaining rows of the same section using the continuing RNG
state. Linguistic difficulty is never a reason for exclusion.

## Gold annotation

Gold annotation is produced from the documentary unit and its available
translation/reviewed reading without consulting grammar-v1 output.

For every item record:

- documentary ID and section;
- Bororo source;
- reviewed form, if present;
- Portuguese translation;
- linguistic question/hypothesis;
- human reference analysis;
- evidence span(s);
- adjudication status;
- uncertainty note.

Questions are formulated from the observed documentary evidence rather than
from the set of licenses already encoded in grammar-v1.

After annotation, each item receives an evidence-level reference decision:

- SUPPORT: the documentary evidence supports the stated analysis;
- CONTRADICT: the documentary evidence contradicts the stated analysis;
- INSUFFICIENT: the available evidence does not warrant either conclusion.

CONTRADICT does not mean that a construction is impossible in Bororo. It means
that the specific claim being evaluated is contradicted by the held-out
evidence.

## Freeze

Before running the pipeline, commit:

- the 32 sampled documentary IDs;
- the source snapshot/commit identifier;
- the annotation schema;
- all gold questions and reference analyses;
- the grammar-v1 identifier;
- the pipeline/prompt/model configuration.

Gold labels and reference analyses must not be included in model input.

## Evaluation

The frozen system is evaluated without grammar repair. Report separately:

1. decision agreement (SUPPORT / CONTRADICT / INSUFFICIENT);
2. evidence correctness;
3. linguistic-analysis correctness;
4. unsupported generalization / overclaiming;
5. abstention behavior;
6. failure type.

A confusion matrix and macro-averaged class metrics may be reported for the
three-way decision only after the independent gold labels have been frozen.
Free-form linguistic analyses are human-audited separately.

## Human review

The reviewer sees the documentary item, system response, and cited evidence,
but not the gold decision during first-pass review. Record at minimum:

- evidence_present;
- evidence_relevant;
- analysis_supported;
- contradiction_ignored;
- overclaiming;
- appropriate_uncertainty;
- reviewer_note.

Use a second reviewer for all 32 items if feasible; otherwise preregister a
stratified subset before system outputs are examined.

## Reserved confirmatory set

`Adugo Biri` is not part of development or the primary `Boe Ero` evaluation.
It remains sealed for a later confirmatory document-level test. Its results must
not be used to revise the already reported `Boe Ero` evaluation.

## Interpretation

The original 28 tasks test functional correctness against phenomena represented
in the frozen grammar. Grammar-derived boundary/coverage cases test internal
decision behavior and regression safety. The present holdout tests behavior on
independently selected documentary material.

Claims of out-of-sample or temporal generalization require provenance evidence
showing that the relevant holdout material was unavailable to grammar
construction.