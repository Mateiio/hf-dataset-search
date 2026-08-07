# Demo

Captured verbatim from a real run on 2026-08-06. Windows 11, Python 3.14.4,
Ollama serving `bge-m3` from WSL, RTX 5080 laptop (16 GB).

---

## The one that makes the case

Query: **"how much leaf material falls each autumn"** — no dataset in the
archive uses those words.

```
$ python -m hf_search.hybrid --mode lexical "how much leaf material falls each autumn" -k 3
  0.0433  hf342    Gene Expression and Tree Growth in the CTFS-ForestGE   <- (distributed match)
  0.0429  hf252    Social Network Survey of Forest Landowners in New Ha   <- column time.on.land
  0.0429  hf352    Lymantria dispar Defoliation and Mortality Survey at   <- column dieback_2022

$ python -m hf_search.hybrid --mode semantic "how much leaf material falls each autumn" -k 3
  0.6084  hf151    Litterfall at Harvard Forest HEM and LPH Towers sinc   <- semantic similarity
  0.5581  hf344    Leaf and Soil Nitrogen Following Lymantria dispar De   <- semantic similarity
  0.5557  hf003    Phenology of Woody Species at Harvard Forest since 1   <- semantic similarity
```

Keyword search returns gene expression and a landowner survey. Semantic search
returns **hf151, "Litterfall at Harvard Forest HEM and LPH Towers"**, which is
the answer.

---

## Corpus

```
$ python -m hf_search.corpus
datasets            458
tables            1,462
attributes       24,948
```

## Hybrid queries

```
$ python -m hf_search.hybrid "understory light sensors" -k 5
  0.0952  hf249  Radiometric and Meteorological Data from Harvard For  <- sensors, of sensors + semantic
  0.0900  hf206  Microclimate at Harvard Forest HEM, LPH and EMS Towe  <- understory air, understory hf206 + semantic
  0.0825  hf138  Microclimate in CRUI Land Use Project at Harvard For  <- (distributed match) + semantic
  0.0823  hf107  Light Environment in Hemlock Removal Experiment at H  <- light environment, light disturbance + semantic
  0.0774  hf140  Herbaceous Stratum Sunfleck Regimes in CRUI Land Use  <- sensors, the sensors + semantic

$ python -m hf_search.hybrid "diffuse and direct solar radiation" -k 5
  0.1000  hf102  Radiation Measurements at Harvard Forest EMS Tower 1  <- radiation measurements, radiation solar + semantic
  0.0952  hf283  Continuous Measurement of Canopy Fluorescence at Har  <- solar induced, solar radiation, is direct + semantic
  0.0909  hf249  Radiometric and Meteorological Data from Harvard For  <- radiometric and, humidity solar + semantic
  0.0817  hf282  Microclimate at Harvard Forest HDW Tower since 2014   <- net radiation, temperature solar + semantic
  0.0805  hf231  Photosynthetically Active Radiation in the Clearcut   <- active radiation, radiation + semantic

$ python -m hf_search.hybrid "hemlock woolly adelgid damage" -k 5
  0.0871  hf124  Deer and Moose Browsing in Hemlock Removal Experimen  <- deer hemlock, adelgid moose + semantic
  0.0845  hf319  Impacts of Hemlock Woolly Adelgid After Preventative  <- adelgid after, adelgid roots + semantic
  0.0805  hf161  Litterfall in Hemlock Removal Experiment at Harvard   <- adelgid litterfall + semantic
  0.0792  hf054  Community and Ecosystem Impacts in Hemlock Removal E  <- adelgid nitrogen, the adelgid + semantic
  0.0750  hf107  Light Environment in Hemlock Removal Experiment at H  <- cover hemlock, adelgid leaf + semantic
```

---

## Benchmark

```
$ python -m hf_search.benchmark

natural  (10 queries)
                                                       lex   sem   hyb
  30-minute below-canopy understory PAR at the EMS t     6     5     4
  plot coordinates latitude longitude for long-term      1     1     1
  eddy covariance net ecosystem exchange carbon flux     2     1     1
  leaf area index measured at HEM and LPH towers         2     1     1
  biomass inventory biometric plots EMS tower coarse     2     1     2
  harmonized Landsat Sentinel vegetation indices NDV     1     1     1
  measured direct and diffuse solar radiation            1     1     1
  microclimate at the hemlock and upper-slope towers     4     9     3
  microclimate at the hardwood walk-up tower             2     1     1
  spectral vegetation indices at 30 m resolution for     1     1     1
  recall@5                                            0.90  0.90  1.00

paraphrase  (7 queries)
                                                       lex   sem   hyb
  light below the canopy                                20    11    19
  how much sunlight reaches the forest floor          None  None  None
  where exactly are the research plots located          11     3     2
  carbon dioxide breathing in and out of the forest   None  None    20
  how much leaf material falls each autumn              11     1     1
  satellite greenness of the forest over time         None     2    14
  cloudy versus clear sky sunlight split              None  None  None
  recall@5                                            0.00  0.43  0.29
```

Two of the seven paraphrase queries fail every engine. They are left in the set
rather than quietly dropped.

---

## The web search bar

```
$ python -m hf_search.server
loaded 458 datasets and 3 engines in 6.4s

  search bar:  http://127.0.0.1:8000
  api:         http://127.0.0.1:8000/api/search?q=understory+light
  ctrl-c to stop
```

```
$ curl "http://127.0.0.1:8000/api/status"
{"datasets": 458, "ollama": true, "model_pulled": true}

$ curl "http://127.0.0.1:8000/api/search?q=understory+light+sensors&mode=hybrid&k=4"
query='understory light sensors' mode=hybrid ms=180

id     score  why                                          title
hf249  0.0952 sensors, of sensors + semantic                Radiometric and Meteorological...
hf206  0.0900 understory air, understory hf206 + semantic   Microclimate at Harvard Forest...
hf138  0.0825 (distributed match) + semantic                Microclimate in CRUI Land Use...
hf107  0.0823 light environment, light disturbance + sem.   Light Environment in Hemlock...
```

**180 ms per query**, including the embedding round-trip to Ollama.

---

## Building the index from scratch

```
$ python -m hf_search.semantic --build
  0/458  ...
  400/458  (11.3/s, ~4s left)

embedded 458 datasets into 1024-d vectors in 38s -> embeddings.npy (1.88 MB)
```
