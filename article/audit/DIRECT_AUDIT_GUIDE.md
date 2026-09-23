# Direct-condition audit guide — v1

Audit the direct LLM outputs only against the grammar frozen before model
outputs were collected. Experimental outputs must not create or promote rules.

## Decision order

1. Check whether the requested coding frame is respected.
2. Check the reviewed person realization for the requested structural position.
3. Check constructional morphology, including ordinary indicative `-re`.
4. Check reviewed morphophonological surface realization.
5. Check the exclusive suffix slot only when segmentation is independently
   justified: `-re, -wo, -iagu, -ie, -ia` do not co-occur.
6. Use `unsupported_but_plausible=yes` only when an analysis is structurally
   plausible but lacks frozen reviewed licensing.

## Labels

- `morphological_violation`: reviewed person/stem/operator realization is violated.
- `frame_violation`: monovalent, extended-intransitive, or divalent coding is violated.
- `constructional_overgeneralization`: morphology licensed in another reviewed
  construction is extended into the requested construction without license.
- `complementary_distribution_violation`: independently justified segmentation
  places more than one member of the exclusive suffix set in the same slot.
- `unsupported_but_plausible`: plausible analogy, but not licensed by frozen v1.

Values are `yes`, `no`, or `unresolved`. More than one violation may apply.

## Important cautions

A surface nonmatch is not automatically an error. Hyphens, spacing, punctuation,
or capitalization must not be treated as morphological violations without
linguistic justification. Conversely, similarity to an attested token does not
license a requested structural cell.

For divalent predicates, audit A and O separately. Frozen v1 represents the
construction as `A=re + O=LEX`; do not reinterpret a direct output as a
nominative/accusative template.

For extended intransitives, an additional participant is oblique and does not
become O. The absence of an oblique phrase in these v1 tasks does not itself
constitute a frame violation.

Record the justification in `notes`. Do not edit reviewed grammar files during
this audit.
