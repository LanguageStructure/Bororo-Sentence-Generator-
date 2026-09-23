# AI proposal experiment

This protocol is intentionally frozen separately from later linguistic review.

## Conditions

### A — direct generation
The model receives a task specification and returns Bororo surface output.

### B — evidence-bounded generation
The model returns an abstract request. The deterministic reviewed grammar either
realizes the request or blocks it.

The model may not update the reviewed grammar in either condition.

## Unit of comparison

Use the same sampled task inventory in both conditions:

- lemma
- coding frame
- participant/person features
- construction
- requested polarity/modality where applicable

Record prompt, model identifier, model settings, raw response, parsed proposal,
generated surface (if any), and all licenses used.

## Outcome labels

Keep these independent:

- morphological_violation
- frame_violation
- constructional_overgeneralization
- complementary_distribution_violation
- unsupported_but_plausible
- blocked
- sentence_attested
- predicate_form_attested
- unattested

Corpus attestation is never a grammatical license.

## Leakage control

The v1 grammar and baseline report are frozen before collecting experimental
LLM outputs. An analysis discovered while inspecting experimental errors must
enter a later grammar version and must not retroactively alter v1 scoring.

## Primary reporting

Report counts/rates by condition for each violation category, plus the number
and proportion of blocked proposals. Do not collapse all categories into one
accuracy score.

Abstention/blocking is reported separately from error: a block may correctly
represent insufficient reviewed evidence.

## Baseline

- corpus: data/corbo/trusted.conllu
- report: reports/v1-baseline.json
- schema: 1.2
- target lexemes: nudu meru kodu mako maku

## Frozen task file

Build before collecting model outputs:

```bash
python3 scripts/build_experiment_tasks.py --output reports/experiment-v1/tasks.jsonl
```

The v1 inventory must contain exactly 28 tasks, with stable IDs v1-001 through v1-028. Both experimental conditions consume this same file.

## Model registration for the first run

The first OpenAI run uses the exact model ID `gpt-5.6-sol` through the Responses API.
Use the same model and reasoning setting in both conditions. The runner must
record the model ID returned by the API, UTC execution time, reasoning effort,
prompt hash, task ID, raw response, and parsed response.

Do not substitute the moving alias `gpt-5.6` for the recorded experimental
identifier. If the API exposes a more specific snapshot identifier in the
response, preserve it in the raw metadata.

Initial setting: `reasoning.effort = none`. This minimizes hidden reasoning as
an uncontrolled difference between conditions; the structural proposal
condition is testing the architecture, not additional inference budget.
