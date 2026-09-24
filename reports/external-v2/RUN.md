# Running the registered external-v2 extraction

From the repository root:

```bash
python3 -m pip install openai
export OPENAI_API_KEY="..."
python3 scripts/run_external_extraction.py
python3 scripts/validate_external_outputs.py
```

The registered run uses `gpt-5.6-sol` with `reasoning.effort=none`, matching
the model registration of the original experiment. The runner refuses to
overwrite an existing non-empty output file.

Do not edit the prompt, input JSONL, gold file, or grammar-v1 between freezing
the experiment and completing the registered run.

After a successful run, commit
`reports/external-v2/extraction-outputs.jsonl` unchanged before scoring.
