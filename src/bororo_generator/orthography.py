"""Bororo orthographic normalization.

Project orthography does not use <y>.  Legacy Bororo <y>/<Y> is normalized to
<u>/<U>.  Apply this only to fields known to contain Bororo.
"""
def normalize_bororo(text):
    return str(text or "").replace("Y","U").replace("y","u")

def form_key(form):
    return normalize_bororo(form or "_").casefold()

def normalize_bororo_y(text):
    """Backward-compatible alias."""
    return normalize_bororo(text)
