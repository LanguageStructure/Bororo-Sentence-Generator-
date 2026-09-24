# External extraction adapter

The frozen grammar-v1 consumes structural requests rather than raw documentary
sentences. Therefore the external evaluation uses a separate extraction layer.

The adapter does not modify grammar-v1. Its sole purpose is to map unseen
documentary input to a partially specified structural proposal, with nulls and
abstention permitted.

## Information boundary

The extraction model receives only:

- sample/documentary ID;
- Bororo source;
- reviewed orthographic reading when one was already present in CorBo;
- aligned Portuguese translation.

It does not receive:

- gold question, analysis, label, evidence span, or uncertainty;
- grammar-v1 files, licenses, paradigms, valency tables, generated examples;
- the original 28 experimental tasks;
- the grammar-derived boundary/challenge cases.

The extraction prompt explicitly prohibits outside Bororo knowledge and prefers
null/abstention to unsupported inference.

## Two separate outcomes

Do not collapse extraction and grammar behavior.

1. **Extraction evaluation:** compare the extracted observations with the
   independently frozen human analysis. Record supported fields, unsupported
   fields, omissions, and appropriate abstentions.
2. **Grammar compatibility evaluation:** only structurally complete extracted
   proposals may be passed unchanged to grammar-v1. Record whether v1
   generates or blocks them and why.

If an observation lacks fields required by the frozen grammar interface, this
is an extraction abstention/partial analysis, not a grammar failure.

This distinction prevents manual conversion of the held-out sentences into the
grammar's own representation after inspecting the test data.

## Freeze order

The following order is mandatory:

1. holdout IDs;
2. documentary source snapshot;
3. independent human gold;
4. extraction prompt and adapter;
5. extraction run;
6. automatic handoff of complete proposals to unchanged grammar-v1;
7. audit and reporting.

No grammar repair or prompt revision is permitted between steps 5 and 7 for the
registered run.
