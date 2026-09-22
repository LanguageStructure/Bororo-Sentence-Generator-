# Review packet: `ako`

This stage deliberately does **not** assign a morphological interpretation to forms whose
lemma is `ako`.

The review packet records, per surface form:

- frequency in structurally trusted units;
- UPOS and dependency relation;
- existing FEATS;
- governor, when present;
- direct dependents;
- complete attested sentence and sentence ID.

The purpose is to make contrasts such as `akore`, `egore`, `inagore`, and other
attested realizations inspectable without treating `ako:ccomp` as a generation rule.

Generate the packet with:

```bash
python3 scripts/ako_review_packet.py data/corbo/trusted.conllu
```

Only a linguistically reviewed analysis should subsequently be copied into
`config/morphology_review.yaml`.
