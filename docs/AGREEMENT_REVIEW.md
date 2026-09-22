# Dependency and agreement review

Changing the morphology of a predicate inside an attested dependency template is
not yet licensed as sentence generation. A person/number change may require
changes elsewhere in the clause.

The current audit therefore compares the attested contexts of surface forms of
the same lemma. It records dependency relation, head, direct dependents and
their FEATS. These distributions are descriptive evidence only.

A dependency correlation must not become a generation rule until it is reviewed
linguistically. In particular, frequency is not evidence by itself that a
dependent agrees with the predicate.

Run:

```bash
python3 scripts/audit_ako_dependencies.py data/corbo/trusted.conllu
```

The next review question is narrow: when `ako` changes person/number, which
other constituents, if any, must change with it?
