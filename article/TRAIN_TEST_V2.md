# CorBo train/test evaluation protocol (v2)

## Aim

Estimate generalization to annotated Bororo examples that are not available
during grammar construction. This evaluation is distinct from the original
28-task functional validation and from grammar-derived regression tests.

## Unit and leakage boundary

The split unit is a documentary/source group, not an individual sentence.
Sentences from the same source group must not occur in both development and
test partitions. This reduces leakage from near-duplicates, repeated discourse,
speaker-specific formulae, and neighboring sentences.

No test sentence, token, lemma/frame annotation, translation, dependency
analysis, or error discovered on the test partition may be consulted while
constructing grammar-v2.

## Data eligibility

A sentence is eligible for the confirmatory split only if it has sufficiently
reviewed annotation for the evaluation target. At minimum retain:

- stable sentence ID and source provenance;
- Bororo surface form;
- tokenization;
- lemma/POS for the target predicate;
- relevant person/features;
- dependency relations needed to recover the coding frame;
- translation or documentary context sufficient for human audit.

Automatically converted or known-unreviewed analyses must be flagged and may
be used for development but not silently treated as gold test data.

## Split

1. Inventory eligible source/document groups.
2. Freeze the inventory and provenance.
3. Assign whole groups to development and test with a fixed seed.
4. Target approximately 80% development / 20% test by eligible sentence count,
   while preserving whole-document grouping.
5. Do not rebalance after looking at grammar-v2 performance.
6. If a later-added, independently annotated document was demonstrably absent
   from the evidence base used for grammar construction, preserve it as an
   additional temporal test rather than mixing it into development.

## Grammar construction

Grammar-v2 is built from development only. It may use development annotation,
translations, corpus evidence, and human linguistic review. Record every
license/frame added and its development evidence.

Before opening test annotations for evaluation, freeze:

- development/test IDs and source groups;
- grammar-v2 commit;
- valency/licenses;
- generation code;
- evaluation script and metrics.

## Evaluation

For each eligible test predicate occurrence, derive the request mechanically
from the frozen test annotation. Do not manually rewrite the request to fit the
grammar.

Report separately:

- coverage: proportion of test requests for which grammar-v2 has the required
  lexical/constructional license;
- correct realization among licensed requests;
- correct blocking/abstention where evidence is insufficient;
- frame/person-feature mismatches;
- unsupported overgeneration;
- overall end-to-end success, with denominator stated explicitly.

Also report counts, not only percentages.

## Human audit

A reviewer checks test-derived requests and system outcomes against the frozen
annotation. Record evidence correctness, frame correctness, person-feature
correctness, overclaiming, and unresolved annotation issues. Annotation errors
found after unblinding are reported separately and are not silently repaired
to improve the score.

## Existing external-v2 pilot

The 32-item Boe Ero extraction run is retained as a diagnostic pilot. Its
near-universal abstention shows that sentence-level translation alone, under a
strict no-outside-knowledge constraint, is insufficient to populate the
grammar-v1 structural interface. It is not reported as grammar-v1 performance.


## Frozen corpus inventory before partition assignment

The current tagged CorBo snapshot contains 788 sentences. Legacy sentence-level
sourcefile labels were normalized to documentary collections before splitting.
The resulting major collections are:

| collection | sentences |
|---|---:|
| EncIE | 205 |
| PessGr | 145 |
| ABE | 141 |
| IETKB | 57 |
| CGPB | 47 |
| FWFFG | 35 |
| sabia | 29 |
| KJB | 19 |
| KoeMakarewudo | 19 |
| RaimundoItogoga | 17 |
| criacao | 16 |
| RO | 16 |
| BEBE | 10 |
| KuiejedogeEiodudo | 10 |
| C.O | 6 |
| NT.CG | 5 |
| dialogomulherAeB | 4 |
| NT.GO | 3 |

Four singleton legacy labels remain and must be provenance-adjudicated before
confirmatory partition assignment. No test collection is selected merely to
optimize lexical overlap or expected grammar performance.

Because the three largest collections account for a large fraction of CorBo,
a naive random assignment of collections can produce a highly unbalanced test.
The confirmatory partition will therefore be chosen by a deterministic
size-targeting algorithm fixed in advance: among eligible whole-collection
partitions, select the subset whose sentence count is closest to 20% of the
eligible corpus; resolve exact ties lexicographically. This uses collection
size only, never linguistic content or system performance.


## Partition assignment

The four unresolved singleton legacy items (OBE-p75.1, OBE-p75.2,
00FFW.001-antonioWWA.1, and 00CrowellThesis-sent71) are excluded from the
confirmatory partition pending provenance adjudication. They are not assigned
to development or test.

This leaves 784 eligible sentences. The preregistered target is 156.8
sentences (20%). Applying the frozen size-only subset rule yields:

**TEST:** ABE (141) + BEBE (10) + C.O (6) = **157 sentences (20.03%)**.

**DEVELOPMENT:** all other eligible collections = **627 sentences (79.97%)**.

The test assignment was obtained without consulting grammar-v2 performance.
ABE, BEBE, and C.O are henceforth sealed for confirmatory grammar-v2
evaluation. Their linguistic analyses must not be used to construct or repair
grammar-v2.
