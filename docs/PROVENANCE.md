# Provenance and validation

Every sentence exposed by the project must carry a status.

- **attested** — copied from an identified CorBo sentence.
- **recombined** — a new candidate made by controlled substitution in one or more attested structures.
- **generated** — a new candidate licensed by an explicit construction pattern or reviewed rule.

These labels are documentary claims, not grammaticality judgments.

Each record may contain the CorBo version, source `sent_id` values, the construction
pattern, lexical substitutions, explicit rules and editorial notes.

## Validation layers

1. **Structural readiness**: is the source CoNLL-U unit usable?
2. **Provenance validation**: can the candidate be traced to evidence/rules?
3. **Computational constraints**: do later morphology, valency and dependency checks pass?
4. **Linguistic/community review**: a separate human decision, never inferred merely from a passing computational check.

A generated or recombined candidate must never be displayed as an attested Bororo sentence.
