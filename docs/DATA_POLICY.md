# CorBo data policy

The sentence generator treats CorBo as an evolving external research corpus.

## Source of truth

The generator does not maintain an authoritative copy of CorBo. A researcher may
point the tools at any local CorBo CoNLL-U version. Reports should therefore record
the input path and, when releases are prepared, the CorBo version or commit used.

## Changing annotation

Newer CoNLL-U versions may change sentence boundaries, tokenization, lemmas,
dependency relations, morphology or translations. Derived patterns, valency
statistics and generated material must consequently be considered version-bound.

## Validation gate

Sentence generation must not use a CoNLL-U version as trusted evidence until the
structural diagnostic has been inspected. In particular, abnormally long units,
multiple roots, repeated token IDs and missing sentence metadata are reported
rather than silently normalized.

The generator must never write corrections back into CorBo automatically.
