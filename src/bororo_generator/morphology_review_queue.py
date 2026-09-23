"""Evidence-first queue for reviewing corpus-observed forms.

Observed forms are ranked for human review.  No person value, segmentation,
stem class, or coding frame is inferred from corpus shape or frequency.
"""
from .corpus_evidence import corpus_lemma_forms
from .person_index import reviewed_stem_class
from .paradigm_generation import paradigm_requests
from .generate import generate_indicative
from .person_index import REVIEWED_CONSTRUCTION_CELLS
from .context_audit import audit_lemma_contexts

def reviewed_predicate_surfaces(lemma):
    """Exact reviewed generated predicate surfaces, indexed by request.

    This is construction-aware: indicative -re is present for monovalent and
    extended predicates, while divalent predicate realization follows its own
    generator. No suffix is stripped or appended heuristically.
    """
    out={}
    for request in paradigm_requests(lemma):
        result=generate_indicative(**request)
        if result.blocked or result.candidate is None:
            continue
        form=result.candidate.predicate_form
        if not form:
            continue
        out.setdefault(form,[]).append(dict(request))
    return out


def reviewed_construction_surfaces(lemma):
    """Explicitly reviewed construction-specific surfaces for corpus matching."""
    out={}
    for construction,cells in REVIEWED_CONSTRUCTION_CELLS.get(lemma,{}).items():
        for person,surface in cells.items():
            out.setdefault(surface.casefold(),[]).append({
                "lemma":lemma,
                "construction":construction,
                "person":person,
            })
    return out


def morphology_review_queue(lemmas, corpus_path):
    rows=[]
    for lemma in lemmas:
        reviewed_surfaces=reviewed_predicate_surfaces(lemma)
        reviewed_surfaces_folded={form.casefold():requests for form,requests in reviewed_surfaces.items()}
        construction_surfaces=reviewed_construction_surfaces(lemma)
        full=reviewed_stem_class(lemma)
        for obs in corpus_lemma_forms(lemma,corpus_path):
            # The current morphology queue reviews verbal predicate morphology.
            # Same-spelling tokens annotated only as another UPOS are retained
            # as corpus evidence, but are not treated as missing verbal cells.
            upos=set(obs.get("upos",[]))
            lexical_homograph = bool(upos) and "VERB" not in upos
            mixed_upos = "VERB" in upos and any(tag!="VERB" for tag in upos)
            # A full reviewed class is already generative; corpus forms still
            # remain observations, but are not queued as missing morphology.
            exact_surface=obs["form"] in reviewed_surfaces
            matched_requests=reviewed_surfaces_folded.get(obs["form"].casefold(),[])
            construction_matches=construction_surfaces.get(obs["form"].casefold(),[])
            construction_exact=any(
                obs["form"]==surface
                for cells in REVIEWED_CONSTRUCTION_CELLS.get(lemma,{}).values()
                for surface in cells.values()
            )
            if mixed_upos:
                state="token_identity_review"
            elif lexical_homograph:
                state="nonverbal_homograph"
            elif matched_requests:
                state="full_class_reviewed" if full is not None else "exact_cell_reviewed"
            elif construction_matches:
                state="construction_cell_reviewed"
            else:
                state="needs_human_review"
            rows.append({
                "lemma":lemma,
                "form":obs["form"],
                "tokens":obs["count"],
                "sent_ids":obs["sent_ids"],
                "upos":obs["upos"],
                "deprels":obs["deprels"],
                "review_state":state,
                "inferred_person":None,
                "inferred_segmentation":None,
                "inferred_stem_class":None,
                "licenses_generation":state in {"full_class_reviewed","exact_cell_reviewed","construction_cell_reviewed"},
                "lexical_identity_status":(
                    "mixed_upos_requires_token_review" if mixed_upos else
                    "nonverbal_homograph" if lexical_homograph else
                    "verbal_candidate"
                ),
                "reviewed_requests":matched_requests,
                "reviewed_construction_cells":construction_matches,
                "operator_analysis":(
                    ["IRR","IND"] if any(
                        m.get("construction")=="irrealis_indicative"
                        for m in construction_matches
                    ) else None
                ),
                "analysis_scope":(
                    "construction_cell" if construction_matches else
                    "full_stem_class" if matched_requests and full is not None else
                    "exact_person_cell" if matched_requests else
                    None
                ),
                "match_type":(("exact_surface" if construction_exact else "capitalization_variant") if construction_matches else (("exact_surface" if exact_surface else "capitalization_variant") if matched_requests else None)),
            })
    rank={"token_identity_review":0,"needs_human_review":1,"construction_cell_reviewed":2,"exact_cell_reviewed":3,"full_class_reviewed":4,"nonverbal_homograph":5}
    return sorted(rows,key=lambda r:(rank[r["review_state"]],-r["tokens"],r["lemma"],r["form"]))


def review_packet(lemma, form, corpus_path, limit=12):
    """Return corpus contexts for one queued form without adding an analysis."""
    contexts=audit_lemma_contexts(corpus_path,lemma,limit=limit,form=form)
    return {
        "lemma":lemma,
        "form":form,
        "contexts":contexts,
        "analysis":{
            "person":None,
            "segmentation":None,
            "stem_class":None,
            "coding_frame":None,
        },
        "licenses_generation":False,
        "instruction":"Human review required; corpus context is evidence, not an inferred analysis.",
    }


def review_queue_summary(rows):
    """Summarize review workload without converting observations into analyses."""
    unresolved=[r for r in rows if r.get("review_state") in {"needs_human_review","token_identity_review"}]
    return {
        "observed_forms":len(rows),
        "needs_human_review":len(unresolved),
        "token_identity_review":sum(r.get("review_state")=="token_identity_review" for r in unresolved),
        "tokens_needing_review":sum(r.get("tokens",0) for r in unresolved),
        "lemmas_needing_review":len({r.get("lemma") for r in unresolved}),
        "top_unresolved":[
            {"lemma":r["lemma"],"form":r["form"],"tokens":r["tokens"]}
            for r in unresolved[:10]
        ],
    }
