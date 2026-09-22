"""Non-destructive analytical normalization."""
def form_key(form):
    return str(form or "_").casefold()
