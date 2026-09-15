# Evaluation

Rendered 2026-09-14 by `python -m edisearch.measure.report` from `data/results.jsonl`. Indexed: 10,639 current EDI packages across 37 scopes (`data/records.jsonl`). Methods: `lexical`, `bm25`, `semantic`, `hybrid`, `hybrid-bm25`. Retrieval depth 100; a query's rank is the first position of any package in its relevant series (series = `scope.identifier`). Overlap is the pinned measure in `measure/overlap.py`: stemmed, stopword-free query tokens found anywhere in the indexed document, over query tokens.

## citation queries, n = 3

**Stage: demonstration.** Ten-ish queries is an existence proof. The table below is the whole result: no percentages, no correlation, no test, no claim about which method is better.

| Query | Target | Overlap | `lexical` | `bm25` | `semantic` | `hybrid` | `hybrid-bm25` |
|---|---|---:|---:|---:|---:|---:|---:|
| As a proof-of-concept demonstration, here we apply endmember splitting analysis to Campbell and Green’s (2019)… | `10.6073/pasta/f5740876b68ec42b695c39d8ad790cee` | 0.33 | 31 | – | 45 | 31 | 93 |
| Coral community structure on the fore reef is quantified using photoquadrats (0.25 m 2 ) taken at 40 fixed loc… | `10.6073/pasta/1f05f1f52a2759dc096da9c24e88b1e8` | 0.48 | 31 | 18 | 11 | 14 | 10 |
| Three studies (Byrnes 2019, 2021, 2022) were conducted at the Plum Island Ecosystems LTER, where permanent plo… | `10.6073/pasta/ab7c87401f08db2e682b428e524fec03` | 0.39 | 6 | 88 | – | 15 | – |
| **in top 5, count of 3** | | | 0 | 0 | 0 | 0 | 0 |

**Disagreement cases (0):** queries some methods put in the top 5 and others did not.


## What this report does not support

- `citation`, n = 3: no statement about which method is better, no correlation with overlap, no effect size. A demonstration only
- No human-written query set exists yet (M4c is blocked on the human-subjects route), so nothing here says how these queries relate to what people type
