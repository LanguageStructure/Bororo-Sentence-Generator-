# Derived CorBo evidence

This directory contains derived evidence only. CorBo remains the documentary source of truth.

Run:

```bash
python3 scripts/diagnose_conllu.py ../Bororo-Corpus/CorBo/Corpus_Files/Bororo_UD_enriched_v5_plus_scripture.conllu
python3 scripts/analyze_corbo.py ../Bororo-Corpus/CorBo/Corpus_Files/Bororo_UD_enriched_v5_plus_scripture.conllu
```

The analysis writes three distinct products:

- `evidence.json`: diagnostic evidence from the complete parsed input; it is **not automatically trusted for generation**.
- `trusted-evidence.json`: only units that pass the conservative readiness gate.
- `readiness.json`: excluded units and the explicit reasons for exclusion.

The default readiness gate excludes units over 100 tokens, units without exactly one root,
duplicate token IDs, missing text metadata, and obvious Word/XML contamination. The threshold
is operational, not a claim about Bororo grammar.

As CorBo annotation improves, rerun the same commands against the newest CoNLL-U version.
No generated sentence or correction is written back to CorBo automatically.
