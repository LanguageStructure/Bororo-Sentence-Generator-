# Generation evidence states

The generator keeps **generation provenance** and **corpus attestation** separate.

- `generated`: the form was constructed by reviewed grammar rules.
- `attestation.attested=true`: the resulting complete surface string also occurs in the supplied CorBo sentence index.
- `blocked`: required reviewed evidence is missing.
- `recombined`: reserved for corpus-pattern substitution workflows and is not assigned by the grammar generator.

An exact corpus match does not retroactively make a generated candidate an
`attested` provenance object.  It adds independent corpus evidence and records
the matching sentence ids. This prevents corpus occurrence, derivational history,
and grammaticality from being conflated.


## Evidence layers

Evaluation output keeps three independent layers:

1. `reviewed_grammar`: facts explicitly admitted by human review, such as coding frame and stem class.
2. `generated_candidate`: the controlled output licensed by the reviewed generation rules.
3. `corpus_evidence`: observational predicate-form occurrence in the supplied CorBo corpus.

Corpus occurrence is not grammatical review and does not promote a generated or unresolved analysis to reviewed status. Conversely, lack of corpus attestation is not evidence that a generated candidate is ungrammatical.
