# Challenge Set v1 Protocol

## Purpose
This challenge set evaluates the evidence boundary of the frozen v1 grammar. It is separate from the original 28 licensed-domain experiment. The grammar must not be changed after inspecting challenge outcomes; new analysis enters a later version.

## Pre-registered classes
Each class contains 28 tasks.

- **positive / GENERATE**: frozen grammar contains the reviewed frame and morphological licenses required by the request.
- **negative / BLOCK**: requested core-argument configuration contradicts a reviewed coding frame. BLOCK means incompatible with the frozen computational grammar, not a context-free claim of speaker unacceptability.
- **boundary / ABSTAIN**: request is plausible or has partial/construction-specific evidence, but v1 lacks the license required for the requested realization. Insufficient evidence is not converted into a negative grammatical judgment.

Expected decision and evidence basis are written into the task file before runtime evaluation. Generator output is not used to assign the gold class.

## Primary evaluation
Report a 3 x 3 decision matrix over GENERATE / BLOCK / ABSTAIN against positive / negative / boundary. Report positive generation rate, negative blocking rate, boundary abstention rate, and macro-average decision accuracy. Report off-diagonal cases individually. Never collapse BLOCK and ABSTAIN.

## Human linguistic audit protocol
For each audited surface, the auditor sees the frozen task specification, raw output, relevant frozen v1 reviewed evidence, and corpus context only when used as observational evidence. The controlled surface, corpus frequency, and LLM explanations are not proof of grammaticality.

Decide independently:
1. segmentation_supported
2. morphological_violation
3. construction_mismatch
4. s_person_mismatch
5. a_person_mismatch
6. o_person_mismatch
7. frame_violation
8. complementary_distribution_violation
9. unsupported_but_plausible

Allowed values: yes / no / unresolved / not_applicable. Every substantive decision gets a short evidence note. Unresolved means the frozen evidence does not license a stronger judgment.

## Second reviewer
Prefer independent double audit of all items requiring linguistic surface judgment. If infeasible, preselect at least 28 items (one third), stratified across gold classes, before seeing second-reviewer decisions. Report raw agreement per field; use an agreement statistic only where category distribution makes it meaningful. Adjudicate only after independent annotations are frozen and retain both originals.

## Leakage control
- v1 grammar is frozen.
- challenge classes are assigned before runtime evaluation.
- no challenge outcome may add a v1 license.
- later analyses are v2+.
- private grammar, dictionary, and unreleased corpus material are not included in LLM prompts.
