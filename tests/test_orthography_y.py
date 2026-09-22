from bororo_generator.orthography import normalize_bororo, form_key
from bororo_generator.private_dictionary import lookup_private

def test_y_is_canonicalized_to_u():
    assert normalize_bororo("Tygo")=="Tugo"
    assert form_key("TYGO")==form_key("tugo")

def test_legacy_dictionary_y_matches_current_u():
    rows=[{"entry":"tygo","definition":"legacy spelling"}]
    assert lookup_private(rows,"tugo")[0]["entry"]=="tygo"

def test_non_y_text_unchanged():
    assert normalize_bororo("aregodu")=="aregodu"
