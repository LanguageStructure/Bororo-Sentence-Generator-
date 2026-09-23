# Linguistic review policy

A frequent CoNLL-U lemma is not automatically a lexical or morphological unit suitable for generation.

Before approval, inspect:

- its attested surface forms;
- UPOS distribution;
- dependency-relation distribution;
- sentence examples;
- existing FEATS;
- whether the lemma reflects a lexical item, grammatical element, morphological family, or an annotation decision still under review.

Punctuation is excluded from the morphology queue.

No item is promoted to `approved` by frequency, distributional similarity, or an automatic clustering procedure. Automatic reports are evidence for human linguistic analysis, not analyses themselves.


## Review packets

A review packet may aggregate corpus contexts for a specific lemma/form pair.
It is an inspection aid, not an analysis. Fields for person, segmentation,
stem class, and coding frame remain unset until explicitly reviewed by a human.
Frequency, translation, UPOS, dependency relation, and formal resemblance must
not populate those fields automatically.
