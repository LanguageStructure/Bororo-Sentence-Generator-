"""Reviewed compositional morphology.

This module realizes ONLY analyses explicitly recorded in morphology_review.yaml.
It does not infer unseen paradigms or generalize rules to other lemmas.
"""
from .review import lemma_review

def _match_analysis(entry, required):
    return entry and entry.get("status")=="reviewed" and entry.get("analysis")==required

def realize_ako(person=None,number=None,clusivity=None,mood=None,polarity=None,status=None,derivation=None,usage=None,review_path="config/morphology_review.yaml"):
    """Return a reviewed form of ako, or None when the requested cell is not licensed."""
    r=lemma_review("ako",review_path) or {}
    forms=r.get("analyzed_forms",{}) or {}

    # Reviewed nominal/possessive forms.
    if usage=="nominal_possessive" and person==1 and number=="Sing" and not any([mood,polarity,status,derivation]):
        e=forms.get("inago")
        if _match_analysis(e,["1SG","ako"]): return "inago"
    if usage=="nominal_possessive" and person==3 and number=="Plur" and not any([mood,polarity,status,derivation]):
        e=forms.get("ego")
        if _match_analysis(e,["3PL","ako"]): return "ego"

    # Explicitly reviewed complex forms.
    if person==1 and number=="Sing" and mood=="Ind" and polarity=="Neg" and not any([status,derivation]):
        e=forms.get("inagokare")
        if _match_analysis(e,["1SG","ako","NEG","IND"]): return "inagokare"
    if person==1 and number=="Plur" and clusivity=="Ex" and mood=="Ind" and not any([polarity,status,derivation]):
        e=forms.get("cenagore")
        if _match_analysis(e,["1PL.EXCL","ako","IND"]): return "cenagore"
    if person==3 and number=="Sing" and mood=="Ind" and status=="Irr" and not any([polarity,derivation]):
        e=forms.get("akomode")
        if _match_analysis(e,["ako","IRR","IND"]): return "akomode"

    # High-frequency exact corpus cells already human-approved.
    if mood=="Ind" and not any([polarity,status,derivation,usage,clusivity]):
        from .review import approved_form
        feats={"Mood":"Ind","Number":number,"Person":str(person)}
        return approved_form("ako",feats,review_path)

    # akodo is intentionally NOT realized: -do is reviewed as CAUS or IMP,
    # but the contextual condition selecting either value has not been supplied.
    return None
