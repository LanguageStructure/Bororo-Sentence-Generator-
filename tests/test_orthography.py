from bororo_generator.orthography import form_key
def test_case_only_normalization():
 assert form_key("Inagore")==form_key("inagore")
 assert form_key("Akore")=="akore"
