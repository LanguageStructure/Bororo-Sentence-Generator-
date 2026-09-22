"""Non-destructive analytical normalization.

The source CoNLL-U is never rewritten. Normalized forms are comparison keys only.
"""
def form_key(form):
    return str(form or "_").casefold()
