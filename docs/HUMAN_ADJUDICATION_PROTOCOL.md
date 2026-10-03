# Human adjudication protocol

## Scope

This protocol applies to manual review of predicate tokens in a frozen held-out evaluation of the Bororo Sentence Generator. Human adjudication interprets evaluation outcomes; it does not modify the grammar being evaluated.

## Unit of judgement

The unit is one held-out predicate token (UPOS VERB or AUX) together with its sentence context. Multiple predicate tokens in the same sentence are judged separately.

## Materials shown to the reviewer

For each token, the review sheet should contain:

1. stable sentence identifier and documentary source identifier, when available;
2. Bororo sentence and available Portuguese/English translation;
3. target predicate form and lemma;
4. relevant CoNLL-U morphology and dependency relations;
5. the frozen lexical/constructional license used by the generator, if the token is covered;
6. the system decision and a short machine-readable reason.

The reviewer must not be shown a desired/gold outcome label.

## Stage 1: lexical coverage

Assign exactly one label:

- **COVERED** — the predicate lemma has a frozen lexical license.
- **OUT_OF_COVERAGE** — no frozen lexical license exists.
- **LEXICAL_IDENTITY_UNRESOLVED** — annotation or analysis does not permit a reliable lemma-to-license mapping.

Only COVERED tokens proceed to compatibility adjudication. OUT_OF_COVERAGE is a coverage result, not a generation error.

## Stage 2: compatibility of covered tokens

Assign exactly one label:

- **COMPATIBLE** — the attested token/context is licensed by the frozen analysis.
- **CONFLICT** — the attested token/context contradicts a specific frozen lexical, valency, morphological, or constructional constraint.
- **UNRESOLVED** — the available evidence does not support either COMPATIBLE or CONFLICT.

A CONFLICT must additionally receive one primary subtype:

- **LEXICAL_FRAME**
- **ARGUMENT_REALIZATION**
- **MORPHOLOGY**
- **CONSTRUCTION**
- **ANNOTATION_MAPPING**
- **OTHER**

## Annotation and implicit arguments

An apparent mismatch is not automatically a grammar conflict. If the documentary translation, discourse context, or Bororo construction supports an implicit argument not represented by the dependency annotation, label the case UNRESOLVED unless the frozen grammar itself is demonstrably contradicted. Suspected annotation errors are recorded separately and must not be silently corrected during the run.

## Independence from grammar revision

The grammar, lexical inventory, and evaluation split are frozen before adjudication. Review observations may motivate a later grammar version, but no observation from the held-out partition may alter the licenses used to score the same experiment.

## Review procedure

1. Produce the complete review sheet before linguistic adjudication.
2. Review all covered predicate tokens using the closed labels above.
3. Record a concise evidence note for every CONFLICT and UNRESOLVED case.
4. Group repeated surface conflicts by underlying linguistic cause after token-level labels are complete.
5. Report both token-level conflicts and the number of distinct underlying license errors.
6. Preserve the original system output and reviewer labels in a versioned artifact.

## Second review and disagreement

When a second qualified reviewer is available, independently double-review all CONFLICT and UNRESOLVED cases and a predetermined sample of COMPATIBLE cases. Record both labels before discussion. Resolve disagreements by explicit adjudication and retain the pre-adjudication labels. Report the double-reviewed sample size and agreement; do not report inter-annotator agreement when only one reviewer has independently labelled the data.

## Reporting

At minimum report:

- total predicate tokens;
- COVERED / OUT_OF_COVERAGE / LEXICAL_IDENTITY_UNRESOLVED;
- COMPATIBLE / CONFLICT / UNRESOLVED among covered tokens;
- conflict subtypes;
- token-level conflicts and distinct underlying license errors separately;
- number of cases affected by suspected annotation or implicit-argument issues;
- amount of prior exposure to held-out material;
- whether independent second review was performed.

Compatibility is reported only over adjudicable covered tokens. It must not be described as unrestricted accuracy or as performance over all unseen Bororo.
