# Gold annotation worksheet

The 32 source units below were copied only after membership in the holdout was
frozen. This stage does not contain grammar-v1 outputs.

Annotate each item independently from the documentary evidence. Do not consult
the frozen grammar or pipeline output while filling the gold fields.

Fields to complete in `boe_ero_gold.tsv`:

- `question`: a linguistically explicit claim/question grounded in the unit;
- `reference_analysis`: human analysis supported by the documentary evidence;
- `evidence_span`: minimal Bororo span relevant to the analysis;
- `gold_decision`: SUPPORT, CONTRADICT, or INSUFFICIENT;
- `uncertainty`: NONE, LOW, MATERIAL;
- `reviewer_note`: justification, ambiguity, or source problem.

Do not force a SUPPORT/CONTRADICT decision when the documentary evidence is
insufficient. The gold concerns the claim posed for that item, not a
language-wide claim about Bororo.
