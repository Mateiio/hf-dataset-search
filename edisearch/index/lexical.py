"""BM25, added beside the repo's TF-IDF, not in place of it.

The repo's `hf_search.lexical.LexicalIndex` is field-weighted TF-IDF with
bigrams and a second index over column definitions. It is the engine behind
the recall@5 of 1.00 the README reports, and it is the only reference point
this project has, so it is reused unchanged.

BM25 is what the published dataset-search work uses as the lexical baseline
(Kolyada et al. 2025, Terrenzi et al. 2025), so it is the number a reader will
want beside the dense and hybrid ones. This is plain Okapi BM25 over the same
document text the TF-IDF engine indexes (`corpus.lexical_doc`, so the field
repetition it uses for weighting is present here too), unigrams, same token
pattern and hyphen handling, k1 = 1.2, b = 0.75. No column-definition second
index and no reserved slots: a baseline should be the textbook thing.

Scoring is a sparse matrix product: the term weights are precomputed once
into a (documents x terms) matrix, and a query is a 0/1 vector over the
vocabulary, so `search` is one multiply.
"""

from __future__ import annotations

import re

import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer

from hf_search import corpus
from hf_search.lexical import TOKEN_RE, Hit, normalise
from hf_search.trace import NULL


class BM25Index:
    def __init__(self, records, k1: float = 1.2, b: float = 0.75):
        self.records = records
        self.ids = [r.id for r in records]
        self.by_id = {r.id: r for r in records}
        self.k1, self.b = k1, b

        docs = [normalise(corpus.lexical_doc(r)) for r in records]
        self.vec = CountVectorizer(lowercase=True, token_pattern=TOKEN_RE)
        C = self.vec.fit_transform(docs).tocsr().astype("float32")   # counts
        self.terms = np.array(self.vec.get_feature_names_out())

        N = C.shape[0]
        dl = np.asarray(C.sum(axis=1)).ravel()
        avgdl = dl.mean() if N else 1.0
        df = np.asarray((C > 0).sum(axis=0)).ravel()
        idf = np.log((N - df + 0.5) / (df + 0.5) + 1.0)

        # BM25 term weight for every nonzero (doc, term) cell
        C = C.tocoo()
        tf = C.data
        denom = tf + k1 * (1.0 - b + b * dl[C.row] / avgdl)
        w = idf[C.col] * tf * (k1 + 1.0) / denom
        self.W = sparse.csr_matrix((w, (C.row, C.col)), shape=C.shape)
        self.idf = idf

    def _query_vector(self, query: str):
        toks = re.findall(TOKEN_RE, normalise(query).lower())
        vocab = self.vec.vocabulary_
        cols = sorted({vocab[t] for t in toks if t in vocab})
        q = sparse.csr_matrix(
            (np.ones(len(cols), "float32"), ([0] * len(cols), cols)),
            shape=(1, len(vocab)))
        return q, cols, toks

    def search(self, query: str, k: int = 20, trace=NULL) -> list[Hit]:
        with trace.stage("lex_bm25", f"BM25 over {len(self.ids)} dataset documents") as st:
            q, cols, toks = self._query_vector(query)
            scores = (self.W @ q.T).toarray().ravel()
            order = [i for i in np.argsort(-scores)[:k] if scores[i] > 0]
            matched = [self.terms[c] for c in cols]
            if trace.on:
                oov = sorted(set(toks) - set(matched))
                st.fact("k1, b", f"{self.k1}, {self.b}")
                st.fact("query terms in vocabulary",
                        " / ".join(f"{t} (idf {self.idf[self.vec.vocabulary_[t]]:.2f})"
                                   for t in matched) or "(none)")
                if oov:
                    st.fact("query terms NOT in vocabulary", " / ".join(oov))
                st.fact("datasets with a nonzero score", int((scores > 0).sum()))
                st.table("Top BM25 scores", ["rank", "dataset", "title", "score"],
                         [[r + 1, self.ids[i], self.by_id[self.ids[i]].title[:60],
                           round(float(scores[i]), 3)] for r, i in enumerate(order[:8])])
        why = ", ".join(matched[:4]) if matched else ""
        return [Hit(self.ids[i], float(scores[i]), self.by_id[self.ids[i]].title, why)
                for i in order]
