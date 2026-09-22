# CorBo-derived data

This directory is for **derived evidence reports**, not a second authoritative copy of CorBo.

The source of truth remains the CorBo repository. Run the analyzer against the canonical CoNLL-U file, for example:

```bash
pip install -e .
python scripts/analyze_corbo.py ../Bororo-Corpus/CorBo/Corpus_Files/Bororo_UD_enriched_v5_plus_scripture.conllu
```

The resulting `evidence.json` records corpus summary, attested construction patterns, exact surface patterns, lexical distributions and observed predicate valency frames.

No generated sentence is admitted to CorBo automatically.
