"""Lexical search: field-weighted TF-IDF over 458 datasets.

Fast, deterministic, and unbeatable at exact identifiers -- "hf206",
"par_ac_down", "MCD15A2H" -- which is precisely where dense embeddings fumble.
It is also completely helpless at paraphrase: on queries sharing no vocabulary
with their target it scores 0.00. Hence the hybrid.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from hf_search import corpus

# Keep underscores and digits attached so "par_ac_down" survives as one token
# instead of three useless fragments.
TOKEN_RE = r"[A-Za-z][A-Za-z0-9_]{1,}"


def normalise(text: str) -> str:
    """Fold hyphenation before tokenising.

    Scientific prose is inconsistent about it -- a query for "walk-up tower"
    scored hf282 sixth even though its abstract opens "The HDW (Hardwood)
    microclimate and walkup tower", because "walk-up" tokenises to
    ["walk","up"] and never matches "walkup". Emitting both forms costs nothing
    and removes the whole family ("above-canopy"/"above canopy").
    """
    joined = re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", "", text)
    return text + " " + joined if joined != text else text


@dataclass
class Hit:
    dataset: str
    score: float
    title: str
    why: str = ""


class LexicalIndex:
    def __init__(self, records=None, verbose: bool = False):
        self.records = records if records is not None else corpus.load()
        self.ids = [r.id for r in self.records]
        self.by_id = {r.id: r for r in self.records}
        docs = [normalise(corpus.lexical_doc(r)) for r in self.records]
        self.vec = TfidfVectorizer(lowercase=True, token_pattern=TOKEN_RE,
                                   sublinear_tf=True, ngram_range=(1, 2),
                                   min_df=1, max_df=0.6)
        self.X = self.vec.fit_transform(docs)
        self.terms = np.array(self.vec.get_feature_names_out())

        # Second granularity: one document per distinct attribute definition.
        # A dataset's title may never say what it measures -- hf206 is titled
        # "Microclimate at ... Towers" and only its column definitions mention
        # understory PAR.
        self.attr_labels, adocs, owners = [], [], []
        for r in self.records:
            for label, text in corpus.attribute_docs(r):
                self.attr_labels.append(label)
                adocs.append(normalise(text))
                owners.append(r.id)
        self.attr_vec = TfidfVectorizer(lowercase=True, token_pattern=TOKEN_RE,
                                        sublinear_tf=True, ngram_range=(1, 2),
                                        min_df=1, max_df=0.5)
        self.A = self.attr_vec.fit_transform(adocs) if adocs else None
        self.attr_owner = np.array(owners)
        if verbose:
            print(f"lexical index: {len(docs)} datasets, "
                  f"{len(adocs):,} attribute definitions")

    def _attr_best(self, query: str) -> dict:
        if self.A is None:
            return {}
        q = self.attr_vec.transform([normalise(query)])
        s = (self.A @ q.T).toarray().ravel()
        best: dict[str, tuple[float, str]] = {}
        for i in np.argsort(-s)[:400]:
            if s[i] <= 0:
                break
            d = str(self.attr_owner[i])
            if d not in best:
                best[d] = (float(s[i]), self.attr_labels[i])
        return best

    def search(self, query: str, k: int = 20) -> list[Hit]:
        q = self.vec.transform([normalise(query)])
        scores = (self.X @ q.T).toarray().ravel()
        idx_of = {d: i for i, d in enumerate(self.ids)}

        # Slots are RESERVED for the attribute signal, not left over. A generic
        # query gives hundreds of datasets a nonzero score, so an "append to
        # spare slots" scheme never fires -- there are never spare slots.
        boost = self._attr_best(query)
        reserved = min(max(2, k // 4), len(boost)) if boost else 0
        order = [i for i in np.argsort(-scores)[:k - reserved] if scores[i] > 0]
        have = {self.ids[i] for i in order}
        floor = scores[order[-1]] if order else 1.0
        for d, _ in sorted(boost.items(), key=lambda x: -x[1][0]):
            if len(order) >= k:
                break
            if d in have:
                continue
            order.append(idx_of[d])
            have.add(d)
            scores[idx_of[d]] = floor * 0.99

        qterms = set(re.findall(TOKEN_RE, query.lower()))
        out = []
        for i in order:
            row = self.X[i].toarray().ravel()
            top = self.terms[np.argsort(-row)[:40]]
            overlap = [t for t in top
                       if t in qterms or any(w in qterms for w in t.split())]
            ds = self.ids[i]
            why = ", ".join(overlap[:5])
            if not overlap and ds in boost:
                why = f"column {boost[ds][1].split('::')[-1]}"
            out.append(Hit(ds, float(scores[i]), self.by_id[ds].title,
                           why or "(distributed match)"))
        return out


if __name__ == "__main__":
    import sys
    idx = LexicalIndex(verbose=True)
    q = " ".join(sys.argv[1:]) or "understory light sensors"
    for h in idx.search(q, k=8):
        print(f"  {h.score:.3f}  {h.dataset:8s} {h.title[:56]:58s} <- {h.why}")
