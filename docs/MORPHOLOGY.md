# Morphology workflow

The project separates three layers:

1. **Corpus evidence** — lemma, surface form and FEATS exactly as found in a trusted CoNLL-U unit.
2. **Human-reviewed analysis** — explicit analyses stored in `config/morphology_review.yaml`.
3. **Generation permission** — a lemma is usable by morphology-aware generation only when its review status is `approved`.

Corpus frequency never changes a review status automatically.

For example, the lemma `ako` may have several surface realizations. Their distribution can
be audited computationally, but their morphological interpretation must be entered only after
linguistic review.

Run:

```bash
python3 scripts/morphology_review_report.py data/corbo/trusted.conllu ako
```
