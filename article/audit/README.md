# Human audit — experiment v1

This audit is separate from the reviewed grammar. Auditing an LLM output must
not update or extend the frozen v1 grammar.

## direct-audit-v1.tsv

One row per direct-condition task. Keep the raw model surface unchanged.
`segmentation` is filled only when the auditor can justify it from the frozen
reviewed analysis. Violation columns use `yes`, `no`, or `unresolved`.
`auditor_status` uses `pending` or `reviewed`.

An experimental discovery that motivates a new Bororo analysis belongs to a
later grammar version, not this audit.