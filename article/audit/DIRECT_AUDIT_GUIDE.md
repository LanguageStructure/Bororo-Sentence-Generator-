# Direct-condition audit guide — v1

Audit direct LLM outputs only against the grammar frozen before model outputs
were collected. Experimental outputs must not create or promote rules.

## Two independent questions

Every output is evaluated on two independent dimensions:

1. **Form well-formedness:** is the produced Bororo form itself morphologically
   licensed by frozen reviewed knowledge?
2. **Task/construction adequacy:** does that form realize the construction,
   coding frame, and person values requested by the task?

A form may therefore be grammatical but still fail the task. For example,
`i=nudu` can be a well-formed non-indicative/nominal expression ('my
sleeping / my sleep'), whereas the requested ordinary indicative predication is
`i=nudu-re` ('I sleep / slept'). Absence of `-re` must not by itself be
reported as a morphological violation.

## Decision order

1. Determine whether the direct form has an independently licensed analysis.
2. Separately check whether it realizes the requested construction.
3. Check whether the requested coding frame is respected.
4. Check reviewed person realization for the requested structural position.
5. Check reviewed constructional morphology and morphophonology.
6. Check the exclusive suffix slot only when segmentation is independently
   justified: `-re, -wo, -iagu, -ie, -ia` do not co-occur.
7. Use `unsupported_but_plausible=yes` only when an analysis is plausible but
   lacks frozen reviewed licensing.

## Labels

- `morphological_violation`: the produced form itself violates reviewed
  morphological realization. Do not use this merely because the requested
  indicative morphology is absent.
- `construction_mismatch`: the produced form may be well-formed, but does not
  realize the construction requested by the experimental task.
- `frame_violation`: requested monovalent, extended-intransitive, or divalent
  coding is violated.
- `constructional_overgeneralization`: morphology licensed in another reviewed
  construction is extended into the requested construction without license.
- `complementary_distribution_violation`: independently justified segmentation
  places more than one member of the exclusive suffix set in the same slot.
- `unsupported_but_plausible`: plausible analogy, but not licensed by frozen v1.

Values are `yes`, `no`, or `unresolved`. More than one label may apply.

## Important cautions

A surface nonmatch is not automatically an error. Hyphens, spacing, punctuation,
or capitalization must not be treated as morphological violations without
linguistic justification. Likewise, a grammatical Bororo expression can be the
wrong answer to an experimental task.

For divalent predicates, audit A and O separately. Frozen v1 represents the
requested construction as `A=re + O=LEX`; do not reinterpret a direct output as
a nominative/accusative template.

For extended intransitives, an additional participant is oblique and does not
become O. Absence of an oblique phrase in these v1 tasks does not itself
constitute a frame violation.

Record justification in `notes`. Do not edit reviewed grammar files during the
audit.
