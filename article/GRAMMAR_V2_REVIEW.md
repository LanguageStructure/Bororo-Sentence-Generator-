# Grammar-v2 review workflow

This stage uses only the frozen 627-sentence development partition.

1. Build the development CoNLL-U with `build_grammar_v2_development.py`.
2. Run `derive_grammar_v2_evidence.py` on that artifact.
3. Treat every derived lemma/frame/person pattern as **corpus evidence only**.
4. Human review may promote an observation to a grammar-v2 license only when the
   Bororo analysis is supported by the development evidence and the relevant
   grammatical analysis. Record the supporting development sentence IDs.
5. Do not consult ABE, BEBE, C.O, their annotations, or test-derived errors.
6. Freeze the reviewed grammar-v2 config and commit before test evaluation.

The evidence inventory deliberately records observed forms, dependency
relations, person/number features, and up to five development examples per
predicate lemma. It does not infer valency directly from UD relation counts:
UD annotation is evidence to inspect, not a substitute for linguistic review.

A review decision should record: lemma, proposed coding frame, construction,
licensed person/paradigm information, supporting development IDs, reviewer,
status (accepted/rejected/uncertain), and note. Rejected and uncertain
candidates remain visible so that the selection process is auditable.
