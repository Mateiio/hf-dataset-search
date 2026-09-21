<!-- Generated from edi-search-report.html by tools/html2md.py; edit the HTML, then regenerate. The HTML version has the styling. -->

<sub>Environmental Data Initiative · edisearch</sub>

# EDI Search and the Incumbents

*The design of the hybrid search engine over the Environmental Data Initiative, a comparison with the two search interfaces currently in use — the Harvard Forest data archive's and EDI's own portal — the measurements made to date, and the remaining work.*

## 1. What it searches

- **10,639** — data packages, every current one in EDI's research tier

- **37** — publishing scopes, from `edi` to `knb-lter-hfr`

- **277,055** — distinct column definitions indexed at column level (394,343 columns in 21,212 tables)

- **0.6 s** — typical hybrid query once warm; ~16 s to load

The corpus is the whole **contributed tier** of the Environmental Data Initiative — the research datasets, leaving out the ~36,000 bulk-loaded EcoTrends and Landsat products. Each package's EML metadata file was fetched from EDI's own API (PASTA+) with an authenticated key, parsed with the same parser the Harvard Forest engine used, and stored as one record: title, abstract, keywords, creators, coverage, methods, and every data table with every column's name, definition and unit. The 459 Harvard Forest packages are in there as one scope among 37.

Everything runs on one machine, offline once built. The embedding model is local (`bge-m3` through Ollama), the indexes are in memory, and the web page is served by Python's standard library. Nothing is sent anywhere.

## 2. How a query becomes a ranked list

Five engines share one search box. The three that matter are two ways of matching *words* and one way of matching *meaning*; "hybrid" merges a word engine with the meaning engine. (The companion report, *Fields and Search at Harvard Forest*, goes field by field; this is the short version.)

- **lexical field-weighted TF-IDF** — Each package is one document: title counted four times, keywords three, abstract two, then table descriptions, filenames and column names. A second index holds one tiny document per *column definition*; a match there lifts the parent package into reserved slots. Words and two-word phrases; hyphenated words indexed both ways. — *Finds: exact vocabulary, and datasets whose only mention of the thing you want is in a column.*

- **bm25 the textbook baseline** — Plain Okapi BM25 over the same text, single words, none of the extras. It is here so numbers can be compared with published work. — *Finds: what any standard search engine finds.*

- **semantic bge-m3 vectors** — Title, keywords, abstract and every distinct column definition become one 1,024-number vector per package. Your query becomes one too; packages are ranked by the angle between the two. — *Finds: datasets described in different words than yours. Weak at: exact names and *which site*.*

- **hybrid, hybrid-bm25 — reciprocal rank fusion** — Semantic ranks all 10,639; the word engine returns its top 60; each package scores `1/(20+rank<sub>sem</sub>) + 1/(20+rank<sub>lex</sub>)`, missing a term if it is absent from a list. Top 10 shown. Ranks, not scores, so a cosine and a TF-IDF value never have to be compared. — *Finds: what both engines like, ahead of what only one loves.*

Two things the page does that the incumbents do not: a **trace** mode that shows every stage of a query with real timings — which of your words the index knew, the top cosines, the fusion table — and an **evaluation** view that shows how each engine ranks the dataset behind real sentences taken from papers.

## 3. Against Harvard Forest's site search

This is the comparison that is clear-cut. The Harvard Forest archive's "search all" page describes itself: it *"displays datasets where the submitted string is contained in one or more of these fields"* — ID, title, abstract, methods, keywords, location, investigator, contact. Two consequences: your text must appear literally, and results are **not ranked**; they come back alphabetically by title. Probed live on 19 September 2026:

| Typed | HF results | Finds `hf206`? | New engine |
|---|---|---|---|
| microclimate | 18 | yes, 12th alphabetically | ranked; the tower microclimate sets first |
| `par1_ave` (a column name) | 0 | no | yes — column names are indexed |
| walk-up tower | 2 | no — the text says "walkup" | yes — hyphens folded |
| walkup tower | 2 | yes | yes |
| light below the canopy | 0 | no | semantic ranks it 11th of 458 |
| how much sunlight reaches the forest floor | — | no | not in the top 25 either, on the 458 |

Against this incumbent the new engine is better in four measurable ways: it **ranks**, it reads **column-level metadata**, it survives **spelling variants**, and it can match **meaning**. It is worse in one: it does not index **methods** or **people**, which the site search does.

## 4. Against EDI's portal search

This comparison is not clear-cut. EDI's portal runs Apache Solr with relevance ranking over title, abstract, keywords, methods, people, organisations, place names, coordinates, taxa, dates and funding. It is purely lexical, but it is a tuned ranking engine rather than a substring match. Like the Harvard Forest search, it does not index anything at the column level.

Eight queries were run through EDI's search API and through each engine described here on the same day, over the same 10,639 packages. The number is the rank at which the intended dataset appeared; "–" means not in the top 100. Green is top 5, amber is top 10.

| Query | Target | EDI portal | lexical | bm25 | semantic | hybrid |
|---|---|---|---|---|---|---|
| weekly temperature profiles in a lake | `edi.552` | 3 | 1 | 1 | 4 | 1 |
| coral community structure photoquadrats fore reef | `knb-lter-mcr.4` | 9 | 40 | 50 | 10 | 16 |
| citizen collected secchi depth measurements upper midwest | `knb-lter-ntl.300` | 1 | 1 | 1 | 1 | 1 |
| understory light sensors at the walk-up tower | `knb-lter-hfr.206` | 2 | – | 48 | 2 | 6 |
| how much sunlight reaches the forest floor | `knb-lter-hfr.206` | – | – | – | – | – |
| carbon dioxide breathing in and out of the forest | `knb-lter-hfr.4` | – | – | 36 | 87 | – |
| *the coral sentence from a Sci Rep paper* ("…quantified using photoquadrats taken at 40 fixed locations…") | `knb-lter-mcr.4` | 2 | – | – | 6 | 19 |
| *the Plum Island sentence from a preprint* ("…permanent plots at varying distances from the creekbank…") | `knb-lter-pie.539` | – | 7 | 89 | 74 | 13 |

On these eight queries, EDI's search places the target in the top 10 five times; the best single engine here (semantic) also five times; hybrid four. EDI ranks higher on the two coral queries and the walk-up tower query; the new engines rank higher on the Plum Island sentence and the temperature-profile query; neither system retrieves the target for the two pure paraphrases. Eight queries do not support a conclusion in either direction. They are reported to establish that the incumbent is a strong baseline, which the evaluation must treat it as.

| Capability | Harvard Forest search | EDI portal | New engine |
|---|---|---|---|
| Ranks results by relevance | no | yes | yes |
| Matches meaning, not only words | no | no | yes |
| Reads column names, definitions, units | no | no | yes |
| Reads methods, people, place names | yes | yes | not yet |
| Filters by map area, dates, taxon, funding | partly | yes | scope only |
| Explains why a result ranked where it did | no | no | trace |
| Comes with a benchmark from real citations | no | no | being built |
| Runs locally, no account, no server | — | — | yes |

## 5. What has actually been measured

Three results, each with its sample size.

### The port reproduces the original, exactly

On the 459 Harvard Forest packages, the engines give the same ranks on the EDI harvest as on the original archive files, and the same numbers as the project's README: recall@5 of **0.90 / 0.00** (lexical), **0.90 / 0.43** (semantic), **1.00 / 0.29** (hybrid) on 10 natural and 7 paraphrased queries. BM25, added as the baseline: 1.00 / 0.00.

### Scale hurts, and hurts the semantic engine most

| recall@5, the 10 natural queries | lexical | bm25 | semantic | hybrid | hybrid-bm25 |
|---|---|---|---|---|---|
| against 459 Harvard Forest packages | 0.90 | 1.00 | 0.90 | 1.00 | 1.00 |
| against all 10,639 EDI packages | 0.60 | 0.80 | 0.30 | 0.60 | 0.70 |

Those queries were written for a single site and mostly do not name it; "microclimate at the hemlock and upper-slope towers" now competes with tower microclimate from a dozen LTER sites. The semantic engine is the fuzziest about place, so it loses most. This is the clearest result the full corpus has produced, and it motivates the second item in section 6.

### Citation-grounded queries: n = 3, a demonstration

Three sentences taken from papers that cite EDI datasets, judged usable by a person, scored against all 10,639 packages: no engine puts the cited dataset in the top 5; ranks run from 6 to 93. The plan's rule is that fewer than 30 such queries supports no claim at all, so none is made. Thirteen more are judged and waiting to be scored; the pool holds 6,871 citation links.

## 6. Innovations left to build

In order, each tied to something measured above. The rule from the plan holds: nothing is added to the engines until the benchmark can show whether it helped, which means n ≥ 30 first.

1. **EDI's portal search as a baseline inside the benchmark.** Section 4 was produced by hand. The harness should run every query through EDI's search API as a sixth method, so that the incumbent appears in every table automatically. A small change with no research risk; it makes every later result comparative.
2. **Site awareness.** The engines index no place name, project or scope. Adding the geographic description, the site name and the project title to the lexical document — and boosting a package whose scope matches a site named in the query — targets the exact failure in the scale table. Cheap; measurable.
3. **Methods and people.** The one capability both incumbents have that the new engine lacks. The parser already extracts both; the question is whether adding them to TF-IDF helps or dilutes, which has gone both ways before. Test, don't assume.
4. **Field and phrase boosting for BM25.** EDI's Solr outranked the BM25 engine here on three of eight queries with the same words available. Its edismax configuration boosts title and keyword matches and rewards phrases; the BM25 here weights all fields equally. BM25F with the same field weights the TF-IDF engine uses is a known technique and a fair upgrade to the baseline.
5. **Series grouping in results.** Long-running studies are published as many packages; five near-identical hits should collapse to one with a "5 periods" badge. Also needed for scoring (the plan's M5).
6. **Controlled-vocabulary expansion.** EDI keywords come from the LTER controlled vocabulary. Expanding "PAR" to "photosynthetically active radiation" from that thesaurus at query time is domain-specific and has some novelty. It is idea 0008 in the project list — a separate piece of work.
7. **Later, with care: fine-tune the embedding model on citation pairs.** The pairs are training data as well as test data; using them for both needs a strict split and n well past 60. Not now.
> **Deliberately not on the list.** Cross-encoder reranking and column-level embeddings were both tried on Harvard Forest and both hurt. Query rewriting (HyDE, doc2query) is well covered elsewhere and would contaminate the overlap measurement the study depends on. None returns without a stated reason the EDI corpus differs.

## 7. Where the real contribution is

The question "is this search better?" is the natural one to ask of the system, and it is not the question the project is designed to answer. Hybrid retrieval — lexical and dense retrieval merged by rank fusion — is established practice and has been published for dataset search specifically (Terrenzi et al., 2025). The engine is therefore not a contribution in itself, and section 4 shows that the incumbent is a competent baseline.

What does not exist anywhere is a **test collection for ecological dataset search built from real citation links**: queries that are sentences from papers describing data they actually used, matched to the dataset they cited, with the word overlap between query and metadata measured as a continuous number. With such a collection, the result of interest is not whether hybrid retrieval wins in aggregate but *where* each method wins as query–metadata overlap falls; and the same collection can score EDI's portal search, the engines described here, and any future system on equal terms. The collection is the deliverable; the search engine is the instrument used to characterise it.

---

* Sources: `docs/acquisition.md`, `docs/reproduction.md`, `docs/evaluation.md`, `docs/yield_probe.md`; Harvard Forest search pages probed live 19 September 2026; EDI's search API (`searchDataPackages`, edismax) queried the same day with the same eight queries as the engines here, results in `data/edi_vs_ours.json`; decisions 0008–0010 in the project's `decisions/` folder. Companion report: *Fields and Search at Harvard Forest*. *
