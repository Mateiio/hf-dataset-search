# Demo: EDI

Captured verbatim from a real run on 2026-09-19. Windows 11, Python 3.14.4,
Ollama serving `bge-m3` from WSL. Corpus: all 10,639 current data packages in
EDI's 37 research scopes, harvested 2026-09-14.

![the EDI search bar: keyword vs meaning on one query, a scope filter, and the evaluation view](docs/edi-demo.gif)

---

## Keyword matching against meaning matching

Query: **"how much sunlight reaches the forest floor"**. No dataset in the
corpus uses this wording. BM25 matches the common words and returns a
salamander survey; the dense engine returns light-environment datasets.

```
$ python -m edisearch.search "how much sunlight reaches the forest floor" --method bm25 --k 3
  1. knb-lter-hfr.132.12         20.5635  Eastern Redback Salamander Abundance at the Arnold Arboretum 2004-2005
     floor, forest, how, much
  2. knb-lter-hfr.99.14          19.8738  Stream Periphyton Response to Hemlock Mortality in Central Massachuset
     floor, forest, how, much
  3. knb-lter-and.5316.4         19.5881  Forest metrics derived from the 2008 Lidar point clouds, includes cano
     floor, forest, how, much

$ python -m edisearch.search "how much sunlight reaches the forest floor" --method semantic --k 3
  1. knb-lter-hfr.107.35          0.5614  Light Environment in Hemlock Removal Experiment at Harvard Forest sinc
     semantic similarity
  2. knb-lter-hfr.357.4           0.5484  Effects of Forest Fragmentation on Carbon Sequestration and Respiratio
     semantic similarity
  3. knb-lter-arc.20073.2         0.5459  Effects of shading on tundra vegetation senescence at Toolik Lake, Col
     semantic similarity
```

Neither engine places Harvard Forest's understory-PAR dataset
(`knb-lter-hfr.206`) in the top 100 at this scale; on the 458-dataset Harvard
Forest corpus the dense engine ranked it 11th. The evaluation set exists to
measure effects of this kind.

---

## Hybrid, and the scope filter

```
$ python -m edisearch.search "weekly temperature profiles in a lake" --k 3
  1. edi.552.1                    0.0935  Weekly and high frequency temperature profile data and Secchi depth, M
     mohonk lake, in mohonk, when temperature, temperature profiles, profiles shawangunk + sema
  2. edi.705.5                    0.0931  Global data set of long-term summertime vertical temperature profiles 
     vertical temperature, temperature profiles, limnology temperature, corresponding lake, con
  3. knb-lter-ntl.211.6           0.0779  North Temperate Lakes LTER: Spatially Distributed Water Temperature (2
     sediment temperature, lake wingra, temperature profiles, temperature of, underwater temper

$ python -m edisearch.search "weekly temperature profiles in a lake" --k 3 --scope knb-lter-ntl
  1. knb-lter-ntl.211.6           0.0935  North Temperate Lakes LTER: Spatially Distributed Water Temperature (2
     sediment temperature, temperature of, temperature profiles, lake wingra, underwater temper
  2. knb-lter-ntl.95.9            0.0917  Landscape Position Project at North Temperate Lakes LTER: Vertical Lak
     vertical lake, lake profiles, profiles landscape, lake vertical, of temperature + semantic
  3. knb-lter-ntl.441.1           0.0911  Cascade Project at North Temperate Lakes LTER: Weekly dissolved methan
     weekly dissolved, methane profiles, lter weekly, profiles and, weekly profiles + semantic

$ python -m edisearch.search "citizen collected secchi depth measurements" --k 3
  1. knb-lter-ntl.300.3           0.1000  Upper Midwest Great Lakes Region Citizen Secchi Data 1938 - 2012
     citizen secchi, citizen lake, region citizen, secchi data, citizen + semantic
  2. knb-lter-cce.152.2           0.0931  Mean annual Secchi depth measurements in the period starting in 1969 p
     annual secchi, secchi depth, measurements light, light secchi, secchi + semantic
  3. knb-lter-ntl.416.3           0.0893  Lake Mendota Microbial Observatory Secchi Disk Measurements 2012-2025
     observatory secchi, the secchi, disk measurements, secchi disc, secchi + semantic
```

The first query's top hit is the Mohonk Lake dataset that pair #242 of the
citation probe cites; the third is the Upper Midwest citizen Secchi dataset
behind pair #142.

---

## Trace

`--trace` prints what every stage did. Three of the eight stages for
**"understory light sensors at the walk-up tower"**, over the full corpus:

```
[3/0] TF-IDF over 10639 dataset documents
      14.42 ms
      matrix                               10639 datasets x 871,631 terms (sparse)
      field weights                        title x4 / keywords x3 / abstract x2 / tables x1
      query terms in vocabulary            understory light (0.441) / light sensors (0.326) / sensors at (0.303) / the walk (0.26) / tower understory (0.26) ...
      query terms NOT in vocabulary        at / the
      datasets with a nonzero score        4403
      -- Top TF-IDF cosines
            rank |    dataset |      title |      score
               1 | knb-lter-h | Microclima |     0.0844
               2 | knb-lter-g | Climate da |     0.0842
               3 | knb-lter-g | Climate da |     0.0842
               4 | knb-lter-g | Climate da |     0.0842
               5 | knb-lter-h | Canopy Phe |     0.0827
               6 | knb-lter-g | Climate da |     0.0818
               7 | knb-lter-g | Climate da |     0.0817
               8 | knb-lter-g | Climate da |     0.0817
      note: Out-of-vocabulary terms contribute nothing. This is where lexical loses on paraphrase: no shared words, no score.
[5/0] Reserve slots, merge column matches
      0.20 ms
      k                                    60
      slots reserved for column matches    15
      kept from dataset TF-IDF             45
      injected from column index           edi.2218.1, knb-lter-hfr.103.37, edi.1069.4, knb-lter-pie.535.1, edi.1966.1, knb-lter-nwt.191.8, knb-lter-hfr.323....
      score floor for injected             0.0279
      -- Injected by their best column
         dataset |     column | column cosine
      edi.2218.1 |       site |      0.274
      knb-lter-h | tsoil_10cm |      0.218
      edi.1069.4 | Flag_LvlPr |      0.213
      knb-lter-p |    Sensors |        0.2
      edi.1966.1 |  StartTime |      0.175
      knb-lter-n | soil_senso |      0.155
      knb-lter-h | understory |      0.144
      knb-lter-n |      depth |      0.141
      knb-lter-n |      depth |      0.141
      knb-lter-h |      light |      0.136
      edi.2142.1 |      light |      0.136
      knb-lter-h |      light |      0.136
      knb-lter-h |   light.1m |      0.133
      knb-lter-h | understory |      0.131
      knb-lter-n |       deck |      0.129
      note: Reserved slots are max(2, k/4), capped by how many datasets the column index promoted. Injected datasets are pinned just below the lowest TF-IDF ...
[6/0] Reciprocal rank fusion
      7.53 ms
      formula                              score = 1/(20+rank_sem) + 1/(20+rank_lex)
      RRF_K                                20
      candidates fused                     10639 (10639 semantic, 60 lexical, 60 in both)
      max possible score                   0.1
      -- How the final ranking was produced
           final |    dataset |      title |   sem rank |   sem part |   lex rank |   lex part |      fused
               1 | knb-lter-h | Microclima |          1 |       0.05 |          1 |       0.05 |        0.1
               2 | knb-lter-h | Canopy Phe |         12 |     0.0323 |          5 |     0.0417 |     0.0739
               3 |  edi.395.2 | Underwater |          5 |     0.0417 |         21 |      0.025 |     0.0667
               4 | knb-lter-h | Radiometri |          8 |      0.037 |         44 |     0.0159 |     0.0529
               5 | knb-lter-g | Climate da |        829 |     0.0012 |          2 |     0.0476 |     0.0488
      -- Where each engine's top 5 ended up
          engine |   its rank |    dataset |      title |      final
        semantic |          1 | knb-lter-h | Microclima |          1
        semantic |          2 | knb-lter-h | Microclima | dropped (#
        semantic |          3 | knb-lter-a | Meteorolog | dropped (#
        semantic |          4 | knb-lter-h | Hubbard Br | dropped (#
        semantic |          5 |  edi.395.2 | Underwater |          3
         lexical |          1 | knb-lter-h | Microclima |          1
         lexical |          2 | knb-lter-g | Climate da |          5
         lexical |          3 | knb-lter-g | Climate da | dropped (#
         lexical |          4 | knb-lter-g | Climate da | dropped (#
         lexical |          5 | knb-lter-h | Canopy Phe |          2
      note: Ranks, not scores, so a 0.58 cosine and a 0.12 TF-IDF never have to be compared. Every dataset has a semantic rank (all 10639 are scored); only t...
hybrid over 10639 packages: 'understory light sensors at the walk-up tower'
  1. knb-lter-hfr.282.15          0.1000  Microclimate at Harvard Forest HDW Tower since 2014
     hdw tower, microclimate at, tower since, tower understory, the hdw + semantic
  2. knb-lter-hfr.183.9           0.0739  Canopy Phenology, Remote Sensing and Microclimate at Harvard Forest 20
     microclimate at + semantic
  3. edi.395.2                    0.0667  Underwater temperature, light, and dissolved oxygen data from 3 mini-b
     datetime light, temperature light, light tempstring, light depth
  4. knb-lter-hfr.249.7           0.0529  Radiometric and Meteorological Data from Harvard Forest Barn Tower 201
     barn tower, tower radiometric, long up, tower beginning, sensors is
  5. knb-lter-gce.415.5           0.0488  Climate data from the SINERR/GCE/UGAMI weather station at Marsh Landin
     at marsh, the sinerr, sensors at, station at, top light + semantic
```

---

## Corpus

```
$ python -c "from edisearch.index import store; ..."
packages         10,639
tables           21,212
attributes      394,343
distinct column definitions indexed   277,055
```

## Reproduction and evaluation

- `docs/reproduction.md` — the original 17 queries on the 459 Harvard Forest
  packages (identical ranks to the archive corpus) and on all 10,639.
- `docs/evaluation.md` — citation-grounded queries scored by every engine,
  reported only to the extent the current n allows.
- `docs/edi-search-report.html` — how the engine compares to Harvard Forest's
  site search and EDI's portal search on the same queries.
