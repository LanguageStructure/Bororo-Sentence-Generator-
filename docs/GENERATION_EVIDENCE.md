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
