# Frozen Boe Ero holdout sample

This file records the primary external-evaluation sample selected before gold
linguistic annotation and before running grammar-v1 on the sampled units.

- Sampling date: 2026-09-24
- Seed: 20260924
- RNG: Python random.Random
- Method: 4 IDs sampled independently from each section, sections processed 1--8
  with one continuing RNG instance; IDs sorted within the final sample.
- Source repository: LanguageStructure/Bororo-Corpus
- Source path: CorBo_vNext/texts/boe-ero/boe_ero_parallel.tsv
- Source blob SHA: 971147a2d3c1bd050ac8dfdfa0daf7b445701e4d
- Section population sizes: 1=43, 2=43, 3=38, 4=21, 5=11, 6=17, 7=69, 8=34
- Sample size: 32

The sampled IDs are frozen in `boe_ero_holdout_ids.tsv`. Do not replace an
item for linguistic difficulty or because of grammar-v1 behavior. Documentary
exclusions, if any, must follow EXTERNAL_EVALUATION_V2.md and be logged.

At this stage the file intentionally contains IDs only. Source sentences,
questions, gold analyses, and labels are added in a subsequent annotation
stage. This separation records that item membership was fixed before linguistic
gold construction.
