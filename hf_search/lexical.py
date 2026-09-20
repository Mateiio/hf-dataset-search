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
from hf_search.trace import NULL

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
        self.attr_terms = (np.array(self.attr_vec.get_feature_names_out())
                           if adocs else np.array([]))
        if verbose:
            print(f"lexical index: {len(docs)} datasets, "
                  f"{len(adocs):,} attribute definitions")

    @staticmethod
    def _query_terms(terms, q, limit: int = 12) -> list:
        """(term, weight) for the nonzero entries of a transformed query.

        This is the query as the index sees it: the unigrams and bigrams that
        exist in the vocabulary, weighted by idf. Anything absent here
        contributes nothing to any score, which is the whole explanation for
        lexical's 0.00 on paraphrase.
        """
        row = q.toarray().ravel()
        nz = [i for i in np.argsort(-row)[:limit] if row[i] > 0]
        return [(str(terms[i]), round(float(row[i]), 3)) for i in nz]

    def _attr_best(self, query: str, st=None) -> dict:
        if self.A is None:
            return {}
        q = self.attr_vec.transform([normalise(query)])
        s = (self.A @ q.T).toarray().ravel()
        best: dict[str, tuple[float, str]] = {}
        top = np.argsort(-s)[:400]
        for i in top:
            if s[i] <= 0:
                break
            d = str(self.attr_owner[i])
            if d not in best:
                best[d] = (float(s[i]), self.attr_labels[i])
        if st is not None:
            st.fact("column definitions indexed", f"{self.A.shape[0]:,}")
            st.fact("vocabulary (uni+bigrams)", f"{len(self.attr_terms):,}")
            st.fact("definitions with a nonzero score", int((s > 0).sum()))
            st.fact("distinct datasets promoted", len(best))
            qt = self._query_terms(self.attr_terms, q)
            st.fact("query terms in this vocabulary",
                    " / ".join(f"{t} ({w})" for t, w in qt) or "(none)")
            rows = []
            for i in top[:8]:
                if s[i] <= 0:
                    break
                fn, _, col = self.attr_labels[i].partition("::")
                rows.append([str(self.attr_owner[i]), col, fn,
                             round(float(s[i]), 3)])
            st.table("Best-matching column definitions",
                     ["dataset", "column", "table", "cosine"], rows,
                     "Only a dataset's single best column counts. Six copies "
                     "of one sensor's definition would not make it six times "
                     "as relevant.")
        return best

    def search(self, query: str, k: int = 20, trace=NULL) -> list[Hit]:
        with trace.stage("lex_tfidf", f"TF-IDF over {len(self.ids)} dataset documents") as st:
            q = self.vec.transform([normalise(query)])
            scores = (self.X @ q.T).toarray().ravel()
            idx_of = {d: i for i, d in enumerate(self.ids)}
            if trace.on:
                qt = self._query_terms(self.terms, q)
                toks = set(re.findall(TOKEN_RE, normalise(query).lower()))
                oov = sorted(t for t in toks if t not in self.vec.vocabulary_)
                st.fact("matrix", f"{self.X.shape[0]} datasets x "
                                  f"{self.X.shape[1]:,} terms (sparse)")
                st.fact("field weights",
                        "title x4 / keywords x3 / abstract x2 / tables x1")
                st.fact("query terms in vocabulary",
                        " / ".join(f"{t} ({w})" for t, w in qt) or "(none)")
                if oov:
                    st.fact("query terms NOT in vocabulary", " / ".join(oov))
                    st.note("Out-of-vocabulary terms contribute nothing. This "
                            "is where lexical loses on paraphrase: no shared "
                            "words, no score.")
                st.fact("datasets with a nonzero score", int((scores > 0).sum()))
                top = [i for i in np.argsort(-scores)[:8] if scores[i] > 0]
                st.table("Top TF-IDF cosines",
                         ["rank", "dataset", "title", "score"],
                         [[r + 1, self.ids[i], self.by_id[self.ids[i]].title[:60],
                           round(float(scores[i]), 4)] for r, i in enumerate(top)])

        # Slots are RESERVED for the attribute signal, not left over. A generic
        # query gives hundreds of datasets a nonzero score, so an "append to
        # spare slots" scheme never fires -- there are never spare slots.
        with trace.stage("lex_attrs", "TF-IDF over column definitions") as st:
            boost = self._attr_best(query, st if trace.on else None)

        with trace.stage("lex_merge", "Reserve slots, merge column matches") as st:
            reserved = min(max(2, k // 4), len(boost)) if boost else 0
            order = [i for i in np.argsort(-scores)[:k - reserved] if scores[i] > 0]
            have = {self.ids[i] for i in order}
            floor = scores[order[-1]] if order else 1.0
            injected = []
            for d, _ in sorted(boost.items(), key=lambda x: -x[1][0]):
                if len(order) >= k:
                    break
                if d in have:
                    continue
                order.append(idx_of[d])
                have.add(d)
                scores[idx_of[d]] = floor * 0.99
                injected.append(d)
            if trace.on:
                st.fact("k", k)
                st.fact("slots reserved for column matches", reserved)
                st.fact("kept from dataset TF-IDF", len(order) - len(injected))
                st.fact("injected from column index",
                        ", ".join(injected) if injected else "none")
                st.fact("score floor for injected", round(float(floor * 0.99), 4))
                st.note("Reserved slots are max(2, k/4), capped by how many "
                        "datasets the column index promoted. Injected datasets "
                        "are pinned just below the lowest TF-IDF score kept, so "
                        "they rank last among lexical hits -- but they do rank.")
                if injected:
                    st.table("Injected by their best column",
                             ["dataset", "column", "column cosine"],
                             [[d, boost[d][1].split("::")[-1], round(boost[d][0], 3)]
                              for d in injected])

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
