"""Non-destructive analytical normalization."""
def form_key(form):
    return str(form or "_").casefold()


def normalize_bororo_y(text):
    """Normalize legacy/non-target Bororo y to u, preserving case."""
    return text.replace("Y","U").replace("y","u")
