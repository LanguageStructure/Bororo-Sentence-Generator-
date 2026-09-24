# Review decision policy

The review table distinguishes three states:

- **accepted**: the coding-frame decision is already independently reviewed and
  is supported by development-only evidence.
- **pending**: development evidence suggests an analysis, but an explicit
  linguistic decision is still required.
- **rejected/uncertain**: the proposed license is not warranted.

For grammar-v2, corpus frequency alone cannot change `pending` to `accepted`.
New lexical licenses that were not independently reviewed in grammar-v1 require
the linguist's explicit approval. This prevents the automated workflow from
silently making new claims about Bororo grammar.

## Decisions ready for confirmation

Development-only inspection currently supports the following proposals:

| lemma | proposed analysis | development evidence | status |
|---|---|---|---|
| mako | extended intransitive | FWFFG-010: `boe ewadaru ji` as oblique participant | accepted (v1-reviewed + development-supported) |
| maragodu | monovalent | FWFFG-008; CGPB-p61.1a | accepted (v1-reviewed + development-supported) |
| kodu | monovalent | FWFFG-0107; CGPB-p13.1/2 | accepted (v1-reviewed + development-supported) |
| maku | divalent + recipient oblique | FWFFG-0102 | accepted (v1-reviewed + development-supported) |
| mugu | monovalent existential/locative | FWFFG-020/022/023 | **awaiting linguist confirmation** |
| aregodu | unresolved | FWFFG-007/011/0107 | **awaiting linguistic analysis** |

The last two are deliberately not promoted by the software.
