# Frozen prompts — experiment v1

These prompt texts are frozen before model-output collection.

- `direct-v1.txt`: condition A, direct Bororo surface generation.
- `proposal-v1.txt`: condition B, abstract proposal only.

Both conditions consume the same `tasks.jsonl` inventory. Model identifier,
provider, date, decoding settings, and raw responses must be recorded alongside
the outputs. Any later prompt change creates a new experiment version.
