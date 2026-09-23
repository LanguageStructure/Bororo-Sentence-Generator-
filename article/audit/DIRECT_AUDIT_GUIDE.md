# Direct-condition audit guide — v1

Audit direct LLM outputs only against the grammar frozen before model outputs
were collected. Experimental outputs must not create or promote rules.

## Independent dimensions

Every output is evaluated separately for:

1. **Form well-formedness** — whether the produced form itself is morphologically
   licensed.
2. **Construction match** — whether it realizes the requested construction.
3. **Person match** — whether the requested S, A, and/or O person values are
   realized in the reviewed structural positions.
4. **Coding-frame match** — whether the requested monovalent,
   extended-intransitive, or divalent coding is respected.

A grammatical form can therefore fail the task. For example, `i=nudu` can be
well formed ('my sleeping / my sleep') while the requested ordinary indicative
predication is `i=nudu-re` ('I sleep / slept'). Absence of `-re` does not by
itself make `i=nudu` morphologically ill formed.

Likewise, `meru-re` can instantiate indicative predication while failing a task
that specifically requests 3PL `e=meru-re`. This is a person mismatch, not
automatically a construction mismatch.

## Labels

- `morphological_violation`: the produced form itself violates reviewed
  morphological realization.
- `construction_mismatch`: the form does not realize the requested
  construction, even if it is otherwise well formed.
- `person_mismatch`: the requested S/A/O person value is absent, replaced, or
  realized in an incompatible reviewed structural position.
- `frame_violation`: the requested coding frame is violated.
- `constructional_overgeneralization`: morphology licensed in another reviewed
  construction is extended without license.
- `complementary_distribution_violation`: independently justified segmentation
  places more than one of `-re, -wo, -iagu, -ie, -ia` in the exclusive slot.
- `unsupported_but_plausible`: an analysis is plausible by analogy but lacks
  frozen reviewed licensing.

Values are `yes`, `no`, or `unresolved`; labels may co-occur.

## Decision procedure

Determine an independently licensed analysis of the direct form first. Then
check construction, person values, coding frame, constructional morphology,
morphophonology, and finally the exclusive suffix slot when segmentation is
independently justified. Do not infer grammaticality from exact string match,
frequency, spacing, hyphenation, capitalization, or similarity to an attested
token.

For divalent predicates, audit A and O independently. Frozen v1 represents the
requested construction as `A=re + O=LEX`. For extended intransitives, an
additional participant is oblique and does not become O; absence of an oblique
phrase in these v1 tasks is not itself a frame violation.

Record justification in `notes`. Do not edit reviewed grammar files during the
audit.
