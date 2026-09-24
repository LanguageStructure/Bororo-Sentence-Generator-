# Grammar-v2 evidence inventory — first review tranche

The frozen 627-sentence development partition contains **726 VERB/AUX tokens
representing 230 distinct annotated lemmas**. These counts are descriptive
corpus evidence, not grammar licenses.

The first review tranche contains the 15 lemmas with at least 11 development
predicate tokens. High frequency is used only to prioritize human review; it
does not determine acceptance.

Important annotation flags discovered before review:
- `aregodu` must not be automatically identified with the grammar-v1 lemma
  `arego`;
- `to` and similar short forms may contain category/homography issues;
- repeated occurrences in a single sentence/source do not constitute
  independent grammatical evidence;
- existing v1 licenses remain hypotheses to be re-supported from development
  evidence for grammar-v2 rather than copied as test-informed facts.

The machine inventory therefore precedes, but does not replace, linguistic
review. Review decisions are recorded in `grammar_v2_review.tsv`.
