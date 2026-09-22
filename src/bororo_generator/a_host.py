"""Reviewed person forms used as the separate A/operator host in divalent declaratives.

This is deliberately independent of lexical stem classes. Only cells explicitly
supported by the current grammar review are licensed here.
"""
A_DECLARATIVE_HOSTS={
    "2SG":"are",
    "3SG":"ure",
    "3PL":"ere",
}

def reviewed_a_declarative(person):
    return A_DECLARATIVE_HOSTS.get(person)

def reviewed_a_persons():
    return tuple(A_DECLARATIVE_HOSTS)
