# Article

Working paper associated with the controlled Bororo sentence generator.

## Baseline

The first frozen experimental baseline uses:

- corpus: `data/corbo/trusted.conllu`
- lexemes: `nudu meru kodu mako maku`
- evaluation report: `reports/v1-baseline.json`
- report schema: 1.2

Reproduce with:

```bash
python3 scripts/evaluation_report.py \
  data/corbo/trusted.conllu \
  nudu meru kodu mako maku \
  --output reports/v1-baseline.json
```

The paper must preserve the distinction between corpus observation, human-reviewed grammatical licensing, generated candidates, and corpus attestation.
