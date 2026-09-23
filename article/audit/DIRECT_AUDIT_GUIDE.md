# Direct-condition audit guide — v1

Audit direct LLM outputs only against the grammar frozen before model outputs
were collected. Experimental outputs must not create or promote rules.

## Independent dimensions

Every output is evaluated separately for form well-formedness, construction
match, argument-person match, and coding-frame match.

Argument-person matching is position-specific:
- `s_person_mismatch` for S in monovalent/extended-intransitive tasks;
- `a_person_mismatch` for A in divalent tasks;
- `o_person_mismatch` for O in divalent tasks.

A non-requested position is `not_applicable`, not `no`. This prevents a
single person score from hiding cases where A fails but O succeeds.

A grammatical form can still fail the task. For example, `i=nudu` can be well
formed ('my sleeping / my sleep') while the requested ordinary indicative
predication is `i=nudu-re` ('I sleep / slept'). Absence of `-re` does not by
itself make `i=nudu` morphologically ill formed. Likewise, `meru-re` may
instantiate indicative predication while failing a task requesting 3PL
`e=meru-re`; that is specifically an S-person mismatch.

## Labels

- `morphological_violation`: the produced form itself violates reviewed
  morphological realization.
- `construction_mismatch`: the form does not realize the requested
  construction, even if otherwise well formed.
- `s_person_mismatch`, `a_person_mismatch`, `o_person_mismatch`: the
  requested person value for that structural position is absent, replaced, or
  realized incompatibly.
- `frame_violation`: the requested coding frame is violated.
- `constructional_overgeneralization`: morphology licensed in another reviewed
  construction is extended without license.
- `complementary_distribution_violation`: independently justified segmentation
  places more than one of `-re, -wo, -iagu, -ie, -ia` in the exclusive slot.
- `unsupported_but_plausible`: an analysis is plausible by analogy but lacks
  frozen reviewed licensing.

Values are `yes`, `no`, or `unresolved`; person dimensions may additionally
be `not_applicable`. Labels may co-occur.

## Decision procedure

Determine an independently licensed analysis of the direct form first. Then
check construction, each requested person position, coding frame,
constructional morphology, morphophonology, and finally the exclusive suffix
slot when segmentation is independently justified. Do not infer grammaticality
from exact string match, frequency, spacing, hyphenation, capitalization, or
similarity to an attested token.

For divalent predicates, audit A and O independently. Frozen v1 represents the
requested construction as `A=re + O=LEX`. Thus an output can fail A while
correctly realizing O. For extended intransitives, an additional participant is
oblique and does not become O; absence of an oblique phrase in these v1 tasks is
not itself a frame violation.

Record justification in `notes`. Do not edit reviewed grammar files during the
audit.
