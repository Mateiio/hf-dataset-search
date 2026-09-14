# Reproduction: the original 17 queries over the EDI harvest

Run 2026-09-14 by `python -m edisearch.measure.reproduce`. Both corpora scored in the same process on the same machine: the archive corpus is the repo's shipped `data/records.json` (458 datasets, tag `v1-hf-only`); the EDI corpus is the M1 harvest of `knb-lter-hfr` (459 packages) parsed by the same `eml.py`. Engines are `hf_search`'s, unchanged; `bm25` is the new baseline.

## Recall@5

| Query set | n | `archive/lexical` | `archive/semantic` | `archive/hybrid` | `edi/lexical` | `edi/bm25` | `edi/semantic` | `edi/hybrid` | `edi/hybrid-bm25` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| natural | 10 | 0.90 | 0.90 | 1.00 | 0.90 | 1.00 | 0.90 | 1.00 | 1.00 |
| paraphrase | 7 | 0.00 | 0.43 | 0.29 | 0.00 | 0.00 | 0.43 | 0.29 | 0.29 |
| all | 17 | 0.53 | 0.71 | 0.71 | 0.53 | 0.59 | 0.71 | 0.71 | 0.71 |

**Like for like:** every unchanged engine scores the same on the EDI harvest as on the archive corpus, rank for rank, and the archive column matches the README's table (lexical 0.90 / 0.00, semantic 0.90 / 0.43, hybrid 1.00 / 0.29). The corpus and the index reproduce. The plan's "recall@5 of 1.00 on 17 queries" was the natural column of that table; there was never a 1.00 on all 17.

## Per-query rank of the target (lower is better, `-` = not in the top 25)

| Query | Family | `archive/lexical` | `archive/semantic` | `archive/hybrid` | `edi/lexical` | `edi/bm25` | `edi/semantic` | `edi/hybrid` | `edi/hybrid-bm25` |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 30-minute below-canopy understory PAR at the EMS tower | natural | 6 | 5 | 4 | 6 | 5 | 5 | 4 | 4 |
| plot coordinates latitude longitude for long-term research sites | natural | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| eddy covariance net ecosystem exchange carbon flux tower | natural | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 1 |
| leaf area index measured at HEM and LPH towers | natural | 2 | 1 | 1 | 2 | 1 | 1 | 1 | 1 |
| biomass inventory biometric plots EMS tower coarse woody debris | natural | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 |
| harmonized Landsat Sentinel vegetation indices NDVI EVI2 | natural | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| measured direct and diffuse solar radiation | natural | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| microclimate at the hemlock and upper-slope towers | natural | 4 | 9 | 3 | 4 | 2 | 9 | 3 | 3 |
| microclimate at the hardwood walk-up tower | natural | 2 | 1 | 1 | 2 | 3 | 1 | 1 | 1 |
| spectral vegetation indices at 30 m resolution for plots | natural | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| light below the canopy | paraphrase | 20 | 11 | 19 | 20 | - | 11 | 19 | - |
| how much sunlight reaches the forest floor | paraphrase | - | - | - | - | - | - | - | - |
| where exactly are the research plots located | paraphrase | 11 | 3 | 2 | 11 | 18 | 3 | 2 | 3 |
| carbon dioxide breathing in and out of the forest | paraphrase | - | - | 20 | - | 14 | - | 20 | 15 |
| how much leaf material falls each autumn | paraphrase | 11 | 1 | 1 | 11 | 19 | 1 | 1 | 1 |
| satellite greenness of the forest over time | paraphrase | - | 2 | 14 | - | - | 2 | 14 | 10 |
| cloudy versus clear sky sunlight split | paraphrase | - | - | - | - | - | - | - | - |

## What BM25 adds

`bm25` is plain Okapi BM25 (k1 1.2, b 0.75, unigrams) over the same document text the TF-IDF engine indexes, with none of the TF-IDF engine's extras: no bigrams, no second index over column definitions, no reserved result slots. It is the textbook lexical baseline the published dataset-search work reports against, which is why it is recorded here beside the engine that actually made the demo work. `hybrid-bm25` fuses it with the same dense vectors by the same reciprocal rank fusion.

Seventeen queries is a regression check, not a measurement. The author of these queries built the system, so they cannot serve as the human arm of the evaluation (decision 0009); they exist to show the port did not break anything.
