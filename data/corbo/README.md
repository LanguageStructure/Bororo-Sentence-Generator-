# Derived CorBo evidence

This directory contains derived evidence only. CorBo remains the documentary source of truth.

A manually or conservatively filtered CoNLL-U subset can be used for development while the
larger corpus is being revised. Such a subset must be identified as provisional and must not
replace CorBo.

Example:

```bash
python3 scripts/diagnose_conllu.py data/corbo/trusted.conllu
python3 scripts/analyze_corbo.py data/corbo/trusted.conllu
python3 scripts/recombine_demo.py data/corbo/trusted.conllu
```

The analysis writes:
- `evidence.json`: diagnostic evidence from the complete parsed input.
- `trusted-evidence.json`: units that pass the conservative readiness gate.
- `readiness.json`: excluded units and explicit reasons.

The readiness gate is operational, not a claim about Bororo grammar. Generated or recombined
material is never written back into CorBo automatically.
