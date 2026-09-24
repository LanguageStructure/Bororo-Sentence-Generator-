# Grammar-v2 freeze record

Grammar-v2 was frozen on 2026-09-24 before test evaluation.

- Operational config: `config/valency_review_v2_frozen.yaml`
- Freeze commit: `de85158fd8ac56650348cb7383c42613694c42cb`
- Review source blob SHA at freeze: `9ba98d41459eb4dd4ddbc816e7368bb1f18f1bd8`
- Development partition: 627 sentences
- Sealed test partition: 157 sentences (ABE 141 + BEBE 10 + C.O 6)
- Licensed lexical entries/constructions: 28
- Pending: 0
- Explicitly uncertain/excluded: `jorudu`, `joruduwa`, `ciri`

Only entries with review_status=accepted are operational licenses. Corpus attestation alone is not a license. Postpositional complementation is represented independently from extended-intransitive class membership.

Special reviewed constraints preserved in the frozen config include: zero exponence of 3SG object where relevant; causative valency changes for `akedu > akedudo`, `pega > pegado`, and `pemega > pemegado`; homophony of verbal and postpositional `to`; identificational-copula `rema`; reflexive-divalent `aimo` with obligatory subject-object coindexation and reviewed form `Cere cedaimo`; and selected postpositions where explicitly reviewed.

## Blinding note

The intended test collections are ABE, BEBE, and C.O. During development review, a small number of test examples were accidentally surfaced by broad corpus queries (including ABE examples while examining `tugu` and BEBE examples while examining `okwage`/`pega`). They were explicitly not used as evidence for grammar decisions. Therefore the final report must describe the test as partially unblinded rather than claiming pristine blindness, and must report this contamination transparently. No further test annotations should be inspected before the frozen evaluation procedure is executed.
