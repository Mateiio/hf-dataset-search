"""Query-to-document lexical overlap, pinned.

The plan pins this definition and says not to change it later, so it lives
in one file with no knobs:

    tokenise query and document, lowercase, drop English stopwords, Porter
    stem, then overlap = |Q intersect D| / |Q|

It is continuous, in [0, 1], and never binned. The document is everything
any engine indexes for the package: the union of `corpus.lexical_doc` and
`corpus.semantic_doc` token sets, so a query word that any engine could
have matched counts as overlapping.

The stemmer is Porter's original algorithm (1980), written out here so the
measure has no dependency and no version drift. The stopword list is fixed
below for the same reason.
"""

from __future__ import annotations

import re

from hf_search import corpus

_TOKEN = re.compile(r"[a-z][a-z0-9]+")

STOPWORDS = frozenset("""
a about above after again against all am an and any are as at be because been
before being below between both but by can did do does doing down during each
few for from further had has have having he her here hers herself him himself
his how i if in into is it its itself just me more most my myself no nor not
now of off on once only or other our ours ourselves out over own same she
should so some such than that the their theirs them themselves then there
these they this those through to too under until up very was we were what when
where which while who whom why will with you your yours yourself yourselves
""".split())


# ------------------------------------------------------------ Porter stemmer

_V = "aeiou"


def _cons(w: str, i: int) -> bool:
    c = w[i]
    if c in _V:
        return False
    if c == "y":
        return i == 0 or not _cons(w, i - 1)
    return True


def _m(w: str) -> int:
    """The measure m of a word: number of VC sequences."""
    n, i, L = 0, 0, len(w)
    while i < L and _cons(w, i):
        i += 1
    while i < L:
        while i < L and not _cons(w, i):
            i += 1
        if i >= L:
            break
        n += 1
        while i < L and _cons(w, i):
            i += 1
    return n


def _has_vowel(w: str) -> bool:
    return any(not _cons(w, i) for i in range(len(w)))


def _double_cons(w: str) -> bool:
    return len(w) >= 2 and w[-1] == w[-2] and _cons(w, len(w) - 1)


def _cvc(w: str) -> bool:
    L = len(w)
    return (L >= 3 and _cons(w, L - 1) and not _cons(w, L - 2) and _cons(w, L - 3)
            and w[-1] not in "wxy")


def _replace(w: str, suffix: str, rep: str, cond=lambda s: True) -> str | None:
    if w.endswith(suffix):
        stem = w[:-len(suffix)] if suffix else w
        if cond(stem):
            return stem + rep
        return w
    return None


def porter(w: str) -> str:
    if len(w) <= 2:
        return w
    # step 1a
    for suf, rep in (("sses", "ss"), ("ies", "i"), ("ss", "ss"), ("s", "")):
        if w.endswith(suf):
            w = w[:-len(suf)] + rep
            break
    # step 1b
    if w.endswith("eed"):
        if _m(w[:-3]) > 0:
            w = w[:-1]
    else:
        done = False
        for suf in ("ed", "ing"):
            if w.endswith(suf) and _has_vowel(w[:-len(suf)]):
                w = w[:-len(suf)]
                done = True
                break
        if done:
            if w.endswith(("at", "bl", "iz")):
                w += "e"
            elif _double_cons(w) and w[-1] not in "lsz":
                w = w[:-1]
            elif _m(w) == 1 and _cvc(w):
                w += "e"
    # step 1c
    if w.endswith("y") and _has_vowel(w[:-1]):
        w = w[:-1] + "i"
    # step 2
    for suf, rep in (("ational", "ate"), ("tional", "tion"), ("enci", "ence"),
                     ("anci", "ance"), ("izer", "ize"), ("abli", "able"),
                     ("alli", "al"), ("entli", "ent"), ("eli", "e"), ("ousli", "ous"),
                     ("ization", "ize"), ("ation", "ate"), ("ator", "ate"),
                     ("alism", "al"), ("iveness", "ive"), ("fulness", "ful"),
                     ("ousness", "ous"), ("aliti", "al"), ("iviti", "ive"),
                     ("biliti", "ble")):
        if w.endswith(suf):
            if _m(w[:-len(suf)]) > 0:
                w = w[:-len(suf)] + rep
            break
    # step 3
    for suf, rep in (("icate", "ic"), ("ative", ""), ("alize", "al"), ("iciti", "ic"),
                     ("ical", "ic"), ("ful", ""), ("ness", "")):
        if w.endswith(suf):
            if _m(w[:-len(suf)]) > 0:
                w = w[:-len(suf)] + rep
            break
    # step 4
    for suf in ("al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement",
                "ment", "ent", "ion", "ou", "ism", "ate", "iti", "ous", "ive", "ize"):
        if w.endswith(suf):
            stem = w[:-len(suf)]
            if _m(stem) > 1 and (suf != "ion" or stem[-1:] in ("s", "t")):
                w = stem
            break
    # step 5a
    if w.endswith("e"):
        stem = w[:-1]
        if _m(stem) > 1 or (_m(stem) == 1 and not _cvc(stem)):
            w = stem
    # step 5b
    if _m(w) > 1 and _double_cons(w) and w.endswith("l"):
        w = w[:-1]
    return w


# ------------------------------------------------------------------ overlap

def tokens(text: str) -> set[str]:
    return {porter(t) for t in _TOKEN.findall(text.lower()) if t not in STOPWORDS}


def document_tokens(record) -> set[str]:
    return tokens(corpus.lexical_doc(record)) | tokens(corpus.semantic_doc(record))


def overlap(query: str, record) -> float:
    q = tokens(query)
    if not q:
        return 0.0
    return len(q & document_tokens(record)) / len(q)
