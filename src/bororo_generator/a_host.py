"""Reviewed person forms used as the separate A/operator host in divalent indicatives.

This is deliberately independent of lexical stem classes. Only cells explicitly
supported by the current grammar review are licensed here.
"""
A_INDICATIVE_HOSTS={
    "2SG":"are",
    "3SG":"ure",
    "3PL":"ere",
}

def reviewed_a_indicative(person):
    return A_INDICATIVE_HOSTS.get(person)

def reviewed_a_persons():
    return tuple(A_INDICATIVE_HOSTS)
