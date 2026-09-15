# Yield probe: citation links to candidate query sentences

Run 2026-09-14 by `python -m edisearch.evalset.yield_probe`, n = 300, seed 0, sampled uniformly from 6,871 distinct (dataset, paper) pairs in DataCite. Mechanical yield only: whether the paper could be read and whether it names the dataset. **Whether a sentence describes what the dataset contains is a human call and the column for it is empty below.**

## Funnel

| Stage | Pairs | Share |
|---|---:|---:|
| Sampled | 300 | 100% |
| Full text read by the script | 76 | 25% |
| ... via Europe PMC XML | 30 | |
| ... via open PDF | 46 | |
| ... via a PDF saved by hand | 0 | |
| Dataset named unambiguously (DOI, package id or title) | 56 | 19% |
| ... with a query candidate in the body text | 32 | 11% |
| ...... of which found by resolving a reference-list marker | 10 | |
| ... hits only in the reference list (body sentence still to be resolved) | 38 | 13% |
| Only a weak pointer (author-year or a generic EDI mention) | 14 | 5% |
| Read, but no mention of the dataset found | 6 | 2% |
| Open in a browser, bot-walled for a script (recoverable by hand) | 105 | 35% |
| Closed | 79 | 26% |
| Not a paper, or not a DOI (theses, GBIF downloads) | 40 | 13% |

The walled row matters: those papers are open access, only the download is refused to a script. At the sizes this project needs (tens to low hundreds of pairs) a person can save them from a browser, so the reachable share for the evaluation set is up to 60%, not 25%.

By link source (a pair can be in both): `is-cited-by` none 156, doi 34, marker 8, author_year 6, package_id 3, generic 2, title 1; `references` none 107, doi 16, author_year 9, marker 3, package_id 1

198 of 300 citing papers cite more than one EDI dataset, which is where attribution can go wrong; those rows say how many.

## Every pair, for reading

**Verdicts so far:** 10 of 300 judged: use-only 5, usable 3, skip 2. Yield 3/10 of judged pairs, 3/300 of sampled links. Pre-screened by the coding agent, confirmed by the owner; verdicts live in `data/evalset/verdicts.json` and survive a regenerated report.

Read the sentence(s). Mark **usable** if a person who had never seen the dataset could tell from the sentence roughly what it contains; **use-only** if it says what the paper did with it but not what it is; **vague** if neither. Write the verdict in the last column and the yield is the count. A hit marked *reference list* is the bibliography entry, which proves the citation but is not a query; judge the *body* hits, and where there are none the body sentence has still to be found (M3's marker resolution).

### 1. `knb-lter-cdr.273.10` cited by `10.1111/ele.14262`

- **Dataset:** Plant aboveground biomass data: Biodiversity II: Effects of Plant Biodiversity on Population and Ecosystem Processes (2021)
- **Paper:** Plant chemical traits define functional and phylogenetic axes of plant biodiversity — *Ecology Letters*, 2023, OA hybrid; cites 3 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_ele.14262.pdf` and re-run
- **Verdict:** 

### 2. `edi.1713.1` cited by `10.1139/z90-056`

- **Dataset:** Twice weekly monitoring of a Microtus ochrogaster population and social behavior in alfalfa in eastern Illinois, 1982-1987. (2024)
- **Paper:** Potential for social interaction in a natural population of prairie voles (Microtus ochrogaster) — *Canadian Journal of Zoology*, 1990, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 3. `knb-lter-hbr.241.5` cited by `10.1175/jhm-d-24-0099.1`

- **Dataset:** Hubbard Brook Experimental Forest: Flux Tower Data, 2016-2024 (2025)
- **Paper:** Synoptic Patterns Associated with Turbulent Fluxes of Water Vapor and Carbon Dioxide in Northern New England — *Journal of Hydrometeorology*, 2025, OA bronze; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:journals.ametsoc.org:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1175_jhm-d-24-0099.1.pdf` and re-run
- **Verdict:** 

### 4. `knb-lter-luq.218.5` cited by `10.1016/j.epsl.2012.05.008`

- **Dataset:** Luquillo Critical Zone Observatory (LCZO) Data repository on HydroShare (2024)
- **Paper:** Rapid regolith formation over volcanic bedrock and implications for landscape evolution — *Earth and Planetary Science Letters*, 2012, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1016_j.epsl.2012.05.008.pdf` and re-run
- **Verdict:** 

### 5. `edi.1361.1` cited by `10.1029/2023jg007439`

- **Dataset:** Seasonality Drives Carbon Emissions along a Stream Network (2023)
- **Paper:** Seasonality Drives Carbon Emissions Along a Stream Network — *Journal of Geophysical Research Biogeosciences*, 2023, OA hybrid; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2023jg007439.pdf` and re-run
- **Verdict:** 

### 6. `knb-lter-hbr.210.1` cited by `10.1016/j.geoderma.2020.114495`

- **Dataset:** Hubbard Brook Experimental Forest: Pedon locations, 1995-present (2019)
- **Paper:** Predictive modeling of bedrock outcrops and associated shallow soil in upland glaciated landscapes — *Geoderma*, 2020, OA bronze; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.sciencedirect.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1016_j.geoderma.2020.114495.pdf` and re-run
- **Verdict:** 

### 7. `knb-lter-fce.1098.14` cited by `10.1007/s10021-026-01092-w`

- **Dataset:** Water Depths and Water Temperatures near Soil Surface from Taylor Slough, Everglades National Park (FCE LTER), Florida, USA, August 1999 - ongoing (2025)
- **Paper:** Divergent Trajectories: Freshwater Rehydration is Associated with Both Increasing and Decreasing Marsh Productivities in the Florida Everglades — *Ecosystems*, 2026, OA hybrid; cites 7 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:link.springer.com:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s10021-026-01092-w.pdf` and re-run
- **Verdict:** 

### 8. `knb-lter-ntl.301.2` cited by `10.1002/eco.2591`

- **Dataset:** North Temperate Lakes LTER Morphometry and Hypsometry data for core study lakes (2022)
- **Paper:** Ecohydrology of two northern Wisconsin bogs — *Ecohydrology*, 2023, OA hybrid; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_eco.2591.pdf` and re-run
- **Verdict:** 

### 9. `knb-lter-nwt.411.14` cited by `10.1371/journal.pclm.0000049`

- **Dataset:** Air temperature data for C1 chart recorder, 1952 - ongoing. (2022)
- **Paper:** Revisiting talus and free-air temperatures after 50 years of change at an American pika (Ochotona princeps) study site in the Southern Rockies — *PLOS Climate*, 2022, OA gold; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 69,414 chars
- **doi**, body [8486–8931]: Data used in analyses of surroundi ng sites can be found in the EDI Portal at the following DOI’s: https://doi.o rg/10. 6073/pasta/6 b8288f9498b 00cf4f2156a3f efc1b72; https://do i.org/10.6073/pa sta/1b62f2cd a71579c48 70ac5c1af71 e6f3; https:// doi.org/10.6073 /pasta/ edd9e457fd2 2a703a587c c8608d54bde; https:// doi.org/10.60 73/pasta/1e9 f40409e69 299b1a4 1f98ac767bc d7; https://doi.org/10 .6073/pasta / 0a786c99fe 3d4e1dfb8 c57424ce79 091. ← **query candidate**
- **marker** via ref 51, body [26460–26628]: Data from weather stations C1 and D1, including the daily maximum and minimum temperatures, were provided by the Niwot Ridge Long-Term Ecological Research site [49–52].
- **doi**, reference list [64763–64851]: Available from: https://doi.or g/10. 6073/pas ta/edd9e457f d22a703a587 cc8608d54 bde 52.
- **Verdict:** use-only data availability list, paper cites 5 EDI datasets

### 10. `edi.181.1` cited by `10.1111/cobi.12049`

- **Dataset:** Demographic measures of Hypericum cumulicola (Hypericaceae) in 15 populations in Florida Rosemary Scrub patches with different time-since-fire, at Archbold Biological Station, Highlands County, Florida from 1994-2015 (2018)
- **Paper:** Ability of Matrix Models to Explain the Past and Predict the Future of Plant Populations — *Conservation Biology*, 2013, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_cobi.12049.pdf` and re-run
- **Verdict:** 

### 11. `knb-lter-mcr.1035.10` cited by `10.1007/s00338-017-1597-2`

- **Dataset:** MCR LTER: Coral Reef: Benthic Water Temperature, ongoing since 2005 (2015)
- **Paper:** Complex and interactive effects of ocean acidification and temperature on epilithic and endolithic coral-reef turf algal assemblages — *Coral Reefs*, 2017, OA closed; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 12. `edi.272.8` cited by `10.22541/essoar.173082870.03607084/v1`

- **Dataset:** Time-series of high-frequency profiles of fluorescence-based phytoplankton spectral groups in Beaverdam Reservoir, Carvins Cove Reservoir, Falling Creek Reservoir, Gatewood Reservoir, and Spring Hollow Reservoir in southwestern Virginia, USA 2014-2023 (2024)
- **Paper:** Meteorological forcing shapes reservoir zooplankton communities over six summers — *?*, 2024, OA gold; cites 6 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.22541_essoar.173082870.03607084_v1.pdf` and re-run
- **Verdict:** 

### 13. `edi.563.1` cited by `10.1002/hyp.14092`

- **Dataset:** Marcell Experimental Forest daily precipitation, 1961 - ongoing (2020)
- **Paper:** Hydrological and meteorological data from research catchments at the Marcell Experimental Forest, Minnesota, USA — *Hydrological Processes*, 2021, OA closed; cites 14 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 14. `knb-lter-ntl.31.29` cited by `10.1002/lol2.10215`

- **Dataset:** North Temperate Lakes LTER: Secchi Disk Depth; Other Auxiliary Base Crew Sample Data 1981 - current (2019)
- **Paper:** Impact of salinization on lake stratification and spring mixing — *Limnology and Oceanography Letters*, 2021, OA gold; cites 6 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.10215.pdf` and re-run
- **Verdict:** 

### 15. `edi.1212.1` cited by `10.22541/au.166512787.73882380/v1`

- **Dataset:** National Forest and Soils Inventory of Mexico 2009-2014 (2022)
- **Paper:** Spatial predictions of tree density and tree height across Mexico´s forests using ensemble learning and forest inventory data (2009-2014) — *?*, 2022, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.authorea.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.22541_au.166512787.73882380_v1.pdf` and re-run
- **Verdict:** 

### 16. `knb-lter-arc.1406.8` cited by `10.5194/essd-2023-222`

- **Dataset:** Measurements of Leaf area, foliar C and N for 14 sites along a transect down the Kuparuk River basin, summer 1997, North Slope, Alaska. (2016)
- **Paper:** A synthesized field survey database of vegetation and active layer properties for the Alaskan tundra (1972–2020) — *?*, 2023, OA gold; cites 8 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 69,899 chars
- **doi**, reference list [57459–57608]: Environmental Data Initiative. https://doi.org/10.6073/pasta/a5a4d4154e0a8181a5523b4d9c49ed99 364 https://doi.org/10.5194/essd-2023-222 Preprint.
- **title**, reference list [57321–57457]: Measurements of Leaf area, foliar C and N for 14 sites along a transect down the Kuparuk River basin, summer 1997, North Slope, Alaska.
- **Verdict:** skip bibliography entry misread as body (Copernicus preprint)

### 17. `knb-lter-jrn.210013003.17` cited by `10.1002/ecy.70384`

- **Dataset:** Soil volumetric water content calculated from neutron hydroprobe data at 15 NPP study locations at the Jornada Basin LTER site, 1989-ongoing (2025)
- **Paper:** Shrub and grass soil‐resource partitioning as modulated by precipitation amount and size of individual — *Ecology*, 2026, OA closed; cites 1 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 18. `knb-lter-sbc.3011.9` cited by `10.1111/fwb.14212`

- **Dataset:** SBC LTER: Land: Hydrology: Stream discharge and associated parameters at Refugio Creek, Hwy 101 (RG01) (2019)
- **Paper:** Trout and invertebrate assemblages in stream pools through wildfire and drought — *Freshwater Biology*, 2024, OA hybrid; cites 3 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf; pdf:escholarship.org:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_fwb.14212.pdf` and re-run
- **Verdict:** 

### 19. `knb-lter-fce.1226.1` cited by `10.1002/ecy.2672`

- **Dataset:** The Salinity and phosphorus mesocosm experiment in freshwater sawgrass wetlands: Determining the trajectory and capacity of freshwater wetland ecosystems to recover carbon losses from saltwater intrusion (FCE LTER), Florida, USA from 2015 to 2018 (2019)
- **Paper:** Phosphorus alleviation of salinity stress: effects of saltwater intrusion on an Everglades freshwater peat marsh — *Ecology*, 2019, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 20. `edi.438.1` cited by `10.1111/1365-2435.13510`

- **Dataset:** Microbial decomposition of 13-C labeled substrates across a gradient of root density, Marcell Experimental Forest, Minnesota, USA, 2014 (2019)
- **Paper:** Plant roots stimulate the decomposition of complex, but not simple, soil carbon — *Functional Ecology*, 2019, OA bronze; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_1365-2435.13510.pdf` and re-run
- **Verdict:** 

### 21. `knb-lter-gce.286.26` cited by `https://uh-ir.tdl.org/handle/10657/4562`

- **Dataset:** Continuous salinity, temperature and depth measurements from moored hydrographic data loggers deployed at GCE7_Hydro (Altamaha River near Carrs Island, Georgia) from 01-Jan-2005 through 31-Dec-2005 (2015)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 29 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 22. `knb-lter-sbc.137.1` cited by `10.1002/ecy.70019`

- **Dataset:** SBC LTER : REEF: Ammonium excretion rates of macroinvertebrates (2021)
- **Paper:** Frequent disturbance to a foundation species disrupts consumer‐mediated nutrient cycling in giant kelp forests — *Ecology*, 2025, OA closed; cites 5 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 23. `edi.1324.2` cited by `10.1002/ecy.70262`

- **Dataset:** Temperature and concentration of dissolved oxygen in river water measured in the Upper Clark Fork River (Montana, USA) during 2020 and 2021 (2023)
- **Paper:** Algal assemblage drives patterns in ecosystem structure but not metabolism in a productive river — *Ecology*, 2025, OA closed; cites 1 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 24. `edi.2253.1` cited by `10.1002/lol2.70116`

- **Dataset:** Seasonality of in-lake and meteorological data from seven lakes, including daily measurements of water temperature, chlorophyll-a, dissolved oxygen, ice cover, air temperature, and solar radiation (2026)
- **Paper:** Seasons and seasonality in lakes: A synthesis amid global change — *Limnology and Oceanography Letters*, 2026, OA gold; cites 10 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.70116.pdf` and re-run
- **Verdict:** 

### 25. `knb-lter-hbr.67.25` cited by `10.1139/cjfr-2025-0105`

- **Dataset:** Long-term measurements of microbial biomass and activity at the Hubbard Brook Experimental Forest 1994 – ongoing (2025)
- **Paper:** Long-term declines in nitrogen and other nutrients in foliage of three northern hardwood species at the Hubbard Brook Experimental Forest — *Canadian Journal of Forest Research*, 2026, OA closed; cites 5 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 26. `knb-lter-ntl.90.33` cited by `10.1038/s41564-024-01888-3`

- **Dataset:** North Temperate Lakes LTER: Zooplankton - Madison Lakes Area 1997 - current (2022)
- **Paper:** Two decades of bacterial ecology and evolution in a freshwater lake — *Nature Microbiology*, 2025, OA green; cites 10 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:escholarship.org:403:not-pdf; pdf:www.nature.com:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1038_s41564-024-01888-3.pdf` and re-run
- **Verdict:** 

### 27. `knb-lter-hbr.223.1` cited by `10.5194/hess-24-17-2020`

- **Dataset:** Water isotope samples from Watershed 3 at Hubbard Brook Experimental Forest, 2006-2010 (2019)
- **Paper:** Seasonal partitioning of precipitation between streamflow and evapotranspiration, inferred from end-member splitting analysis — *Hydrology and earth system sciences*, 2020, OA gold; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 116,278 chars
- **author_year**, body [12738–12928]: As a proof-of-concept demonstration, here we apply endmember splitting analysis to Campbell and Green’s (2019) measurements of δ18O and δ2H at Hubbard Brook Experimental Forest, Watershed 3. ← **query candidate**
- **author_year**, body [12929–13235]: Campbell and Green (2019) measuredδ18O andδ2H in time-integrated bulk precipitation samples, and instantaneous streamwater grab samples, taken at Watershed 3 approximately every 2 weeks between October 2006 and June 2010 (Fig. 2); the isotope sampling and analysis procedures are documented in Green et al.
- **author_year**, body [18892–19102]: (a) Time series of daily water ﬂuxes and biweekly deuterium values in streamwater (dark blue) and precipitation (light blue) at Watershed 3, Hubbard Brook Experimental Forest (data of Campbell and Green, 2019).
- **doi**, reference list [109732–109862]: Watershed 3 at Hubbard Brook Experimental Forest, 2006–2010, https://doi.org/10.6073/pasta/f5740876b68ec42b695c39d8ad790cee, 2019.
- **title**, reference list [109684–109731]: L. and Green, M. B.: Water isotope samples from
- **Verdict:** usable

### 28. `edi.202.8` cited by `10.1002/essoar.10510558.1`

- **Dataset:** Discharge time series for the primary inflow tributary entering Falling Creek Reservoir, Vinton, Virginia, USA 2013-2021 (2022)
- **Paper:** Eddy covariance data reveal that a small freshwater reservoir emits a substantial amount of carbon dioxide and methane — *?*, 2022, OA gold; cites 5 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_essoar.10510558.1.pdf` and re-run
- **Verdict:** 

### 29. `knb-lter-arc.10092.4` cited by `10.1002/2017ms001028`

- **Dataset:** Nutrient and chemical data for various lakes near Toolik Research Station, Arctic LTER, Summer 2003. (2014)
- **Paper:** Modeling CO 2 emissions from A rctic lakes: Model development and site‐level study — *Journal of Advances in Modeling Earth Systems*, 2017, OA gold; cites 5 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:agupubs.onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_2017ms001028.pdf` and re-run
- **Verdict:** 

### 30. `knb-lter-cdr.384.10` cited by `10.1111/1365-2745.14111`

- **Dataset:** Plant aboveground biomass data: The influence of natural enemies on plant community composition and productivity (2022)
- **Paper:** Soil nutrients cause threefold increase in pathogen and herbivore impacts on grassland plant biomass — *Journal of Ecology*, 2023, OA hybrid; cites 2 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_1365-2745.14111.pdf` and re-run
- **Verdict:** 

### 31. `knb-lter-mcr.4.33` cited by `10.1038/s41598-018-25414-8`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Corals, ongoing since 2005 (2015)
- **Paper:** Recruitment Drives Spatial Variation in Recovery Rates of Resilient Coral Reefs — *Scientific Reports*, 2018, OA gold; cites 3 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** europepmc, 54,454 chars
- **marker** via ref 49, body [32125–32448]: Coral community structure on the fore reef is quantified using photoquadrats (0.25 m 2 ) taken at 40 fixed locations located along a 50 m long transect placed along the 10 m isobath at each of six sites; photoquadrat positions were randomly selected in 2005, but thereafter the same locations have been recorded [49],[50] . ← **query candidate**
- **marker** via ref 49, body [43710–43853]: Data for this study are available on the website of the Moorea Coral Reef Long Term Ecological Project: http://mcr.lternet.edu/data [49],[51] .
- **doi**, reference list [52880–53052]: MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Corals, ongoing since 2005. knb-lter-mcr.4.33 10.6073/pasta/1f05f1f52a2759dc096da9c24e88b1e8 (2015). 50.
- **Verdict:** usable

### 32. `edi.1811.1` cited by `10.1073/pnas.2502289122`

- **Dataset:** Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024 (2024)
- **Paper:** Chlorophyll trends are negative for lakes but positive for estuarine–coastal waters — *Proceedings of the National Academy of Sciences*, 2025, OA hybrid; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** europepmc, 47,534 chars
- **doi**, body [29261–29443]: Those data sources are listed and acknowledged in file Metadata- Sampling Locations.csv included in our data package: https://doi.org/10.6073/pasta/dd706bbd8bae2386517d3bf20be02396 . ← **query candidate**
- **marker** via ref 37, body [25323–25464]: The data are available at the Environmental Data Initiative ([37]), including a full description of each site and its associated data source.
- **doi**, reference list [30728–30957]: Data, Materials, and Software Availability All chlorophyll a time series data used in this study have been deposited at the Environmental Data Initiative ( https://doi.org/10.6073/pasta/dd706bbd8bae2386517d3bf20be02396 ) ([37]).
- **doi**, reference list [37791–37998]: Cloern J., Jassby A., “Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024”. Environmental Data Initiative. 10.6073/pasta/dd706bbd8bae2386517d3bf20be02396.
- **title**, reference list [37791–37919]: Cloern J., Jassby A., “Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024”.
- **title**, reference list [46207–46335]: Cloern J., Jassby A., “Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024”.
- **Verdict:** use-only deposited-at statement

### 33. `edi.911.1` cited by `10.21203/rs.3.rs-859794/v1`

- **Dataset:** First-order vertebrated mortality due the 2020 wildfires in the Pantanal wetland, Brazil (2021)
- **Paper:** Counting the Dead: 17 Million Vertebrates Directly Killed by the 2020’s Wildfires in the Pantanal Wetland, Brazil — *Research Square*, 2021, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 40,709 chars
- **doi**, body [26885–27044]: Data availability - the data used to conduct the analysis is available at https://doi.org/10.6073/pasta/1688bdf9c001c89972d2cb53d242c4ef (Accessed 2021-08-02). ← **query candidate**
- **Verdict:** use-only data availability statement

### 34. `edi.140.1` cited by `10.15468/dl.roahuy`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 35. `edi.1609.1` cited by `10.1093/biosci/biae089`

- **Dataset:** Macrosystems EDDIE Module 7: Using Data to Improve Ecological Forecasts (Instructor Materials) (2024)
- **Paper:** A modular curriculum to teach undergraduates ecological forecasting improves student and instructor confidence in their data science skills — *BioScience*, 2024, OA hybrid; cites 3 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:academic.oup.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1093_biosci_biae089.pdf` and re-run
- **Verdict:** 

### 36. `knb-lter-cap.667.1` cited by `https://www.proquest.com/openview/21c4e9a5ca68d2d7398da7862e5f57b7`

- **Dataset:** Phoenix Area Social Survey (PASS): 2017 (2019)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 1 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 37. `knb-lter-ntl.347.1` cited by `10.1002/lol2.10075`

- **Dataset:** North Temperate Lakes LTER Processed eddy covariance time series fluxes from tower located on roof of the CFL building oriented toward Lake Mendota 2012 - current (2017)
- **Paper:** Carbon sink and source dynamics of a eutrophic deep lake using multiple flux observations over multiple years — *Limnology and Oceanography Letters*, 2018, OA gold; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.10075.pdf` and re-run
- **Verdict:** 

### 38. `knb-lter-gce.457.11` cited by `10.1002/ecy.3278`

- **Dataset:** Fall 2013 plant monitoring survey -- biomass calculated from shoot height and flowering status of plants in permanent plots at GCE sampling sites 1-10 (2021)
- **Paper:** Variation in synchrony of production among species, sites, and intertidal zones in coastal marshes — *Ecology*, 2020, OA closed; cites 38 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 39. `knb-lter-nes.9.1` cited by `10.3897/biss.4.59082`

- **Dataset:** Abundance and biovolume of taxonomically-resolved phytoplankton and microzooplankton imaged continuously underway with an Imaging FlowCytobot along the NES-LTER Transect in winter 2018 (2020)
- **Paper:** Change in Pictures: Creating best practices in archiving ecological imagery for reuse — *Biodiversity Information Science and Standards*, 2020, OA diamond; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 6,576 chars
- **doi**, reference list [6396–6576]: Environmental Data Initiativ. URL: https://doi.org/10.6073/pasta/74775c4af51c237f2a20e4a8c011bc53 Change in Pictures: Creating best practices in archiving ecological imagery ... 3
- **author_year**, reference list [6127–6395]: Ecology https://doi.org/10.1002/ecy.3069 • Sosik HM, Peacock E, Santos M (2020) Abundance and biovolume of taxonomicallyresolved phytoplankton and microzooplankton imaged continuously underway with an Imaging FlowCytobot along the NES-LTER Transect in winter 2018. 1.
- **Verdict:** 

### 40. `knb-lter-bnz.175.20` cited by `10.1101/2022.07.05.498812`

- **Dataset:** Vegetation Plots of the Bonanza Creek LTER Control Plots: Species Count (1975 - 2004) (2016)
- **Paper:** Local changes dominate variation in biotic homogenization and differentiation — *bioRxiv (Cold Spring Harbor Laboratory)*, 2022, OA green; cites 35 EDI dataset(s); link source references/crossref
- **Text:** pdf, 59,646 chars
- **Mention:** none found
- **Verdict:** 

### 41. `knb-lter-hfr.210.5` cited by `10.1002/ecs2.4016`

- **Dataset:** Pre-Colonial and Modern Tree Data from Nine Northeastern States 1620-2008 (2021)
- **Paper:** Integrating historical observations alters projections of eastern North American spruce–fir habitat under climate change — *Ecosphere*, 2022, OA gold; cites 1 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4016.pdf` and re-run
- **Verdict:** 

### 42. `knb-lter-and.3222.26` cited by `10.5194/hess-23-3765-2019`

- **Dataset:** Meteorological data from benchmark stations at the Andrews Experimental Forest, 1957 to present (2016)
- **Paper:** The sensitivity of modeled snow accumulation and melt to precipitation phase methods across a climatic gradient — *Hydrology and earth system sciences*, 2019, OA gold; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 102,944 chars
- **doi**, body [72018–72173]: Andrews LTER: https://doi.org/10.6073/pasta/ c96875918bb9c86d330a457bf4295cd9 (McKee, 2015) and http://andlter.forestry.oregonstate.edu/data/ (last access: ← **query candidate**
- **doi**, reference list [91664–91866]: A.: Meteorological data from benchmark stations at the Andrews Experimental Forest, 1957 to present, Environmental Data Initiative, https://doi.org/10.6073/pasta/ c96875918bb9c86d330a457bf4295cd9, 2015.
- **Verdict:** use-only data availability list

### 43. `edi.633.1` cited by `10.1080/20442041.2020.1805261`

- **Dataset:** Ecosystem metabolism estimates from Lake Sunapee, NH, USA and meteorological driver data at the Newport, NH, USA NOAA NCDC weather station from August 2007 – December 2008 (2020)
- **Paper:** Under-ice respiration rates shift the annual carbon cycle in the mixed layer of an oligotrophic lake from autotrophy to heterotrophy — *Inland Waters*, 2020, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.tandfonline.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1080_20442041.2020.1805261.pdf` and re-run
- **Verdict:** 

### 44. `edi.510.1` cited by `10.5194/bg-2020-304`

- **Dataset:** High-frequency time series of stage height, stream discharge, and water quality (specific conductivity, dissolved oxygen, pH, temperature, turbidity) for Stroubles Creek in Blacksburg, Virginia, USA 2013-2018 (2020)
- **Paper:** Resistance and resilience of stream metabolism to high flow disturbances — *?*, 2020, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 66,396 chars
- **doi**, reference list [41986–42356]: Hession, W., Lehmann, L., Wind, L., and Lofton, M.: High-frequency time series of stage height, stream discharge, and water quality (speciﬁc conductivity, dissolved oxygen, pH, temperature, turbidity) for Stroubles Creek in Blacksburg, Virginia, USA 2013-2018 ver 1,365 Environmental Data Initiative, https://doi.org/10.6073/pasta/42727d38837cb4bdf04ce4e0d158ea92, 2020.
- **Verdict:** skip bibliography entry, the dataset's own title

### 45. `knb-lter-gce.697.6` cited by `10.1111/nph.16371`

- **Dataset:** Contrasting plant adaptation strategies to latitude in the native and invasive range of Spartina alterniflora: geographic survey (2014) and Common garden (2015-2017) (2019)
- **Paper:** Contrasting plant adaptation strategies to latitude in the native and invasive range of Spartina alterniflora — *New Phytologist*, 2019, OA bronze; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:nph.onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_nph.16371.pdf` and re-run
- **Verdict:** 

### 46. `knb-lter-knz.55.13` cited by `10.1098/rsbl.2021.0510`

- **Dataset:** PAB01 Aboveground Net Primary Productivity of Tallgrass Prairie Based on Accumulated Plant Biomass on Core LTER Watersheds (001d, 004b, 020b) (2020)
- **Paper:** How and why grasshopper community maturation rates are slowing on a North American tall grass prairie — *Biology Letters*, 2022, OA green; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (europepmc:PMC8790374:404)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1098_rsbl.2021.0510.pdf` and re-run
- **Verdict:** 

### 47. `knb-lter-hbr.208.14` cited by `10.1029/2024jg008489`

- **Dataset:** Continuous precipitation and stream chemistry data, Hubbard Brook Ecosystem Study, 1963 – ongoing. (2025)
- **Paper:** Nitrate Loads and Concentrations From Forested Watersheds and Implications for Long Island Sound — *Journal of Geophysical Research Biogeosciences*, 2025, OA hybrid; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2024jg008489.pdf` and re-run
- **Verdict:** 

### 48. `knb-lter-pie.539.1` cited by `10.32942/x2z31q`

- **Dataset:** PIE LTER predation and herbivory rates associated with marsh sites used in space for time sea level rise study, Rowley, MA. (2019)
- **Paper:** A call to expand global change research in LTER coastal wetlands — *?*, 2023, OA gold; cites 20 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 52,176 chars
- **author_year**, body [22448–22684]: Three studies (Byrnes 2019, 2021, 2022) were conducted at the Plum Island Ecosystems LTER, where permanent plots are arrang ed along the landscape at varying distances from the creekbank to simulate different stages of sea-level rise. ← **query candidate**
- **author_year**, body [23174–23501]: Using the space-for-time sea-level rise study salt marsh sites at PIE over a 5 -year period, Byrnes (2019, 2021, 2022) deployed fishing traps and collected identity and abundance data on 17 common fish and crab species, as well as data on predation and herbivory rates using tethered baits at established experimental plots.
- **doi**, reference list [41661–41756]: Environmental Data Initiative. https://doi.org/10.6073/pasta/ab7c87401f08db2e682b428e524fec03.
- **title**, reference list [41529–41660]: PIE LTER predation and herbivory rates associated with marsh sites used in space for time sea-level rise study, Rowley, MA. ver 1.
- **author_year**, reference list [51561–51624]: Bars represent standard error. Data from: Byrnes 2019 and 2021.
- **Verdict:** usable

### 49. `edi.306.2` cited by `10.1002/ecs2.4208`

- **Dataset:** American Residential Macrosystems - Soil chemistry data within residential yards in six major metropolitan areas, 2012-2013 (2019)
- **Paper:** Ecological homogenization of soil properties in the American residential macrosystem — *Ecosphere*, 2022, OA gold; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 73,697 chars
- **author_year**, body [18981–19105]: The data used in this paper are publicly available via the Environmental Data Initiative (EDI) Data Portal (Groffman, 2019). ← **query candidate**
- **doi**, reference list [51815–51924]: Data are available from the EDI Data Portal: https://doi. org/10.6073/pasta/5683662180499904732e654e3869f3e6.
- **doi**, reference list [56568–56705]: Metropolitan Areas, 2012–2013 Version 2.” Environmental Data Initiative. https://doi.org/10.6073/pasta/5683662180499904732e65 4e3869f3e6.
- **title**, reference list [56454–56514]: Groffman, P. 2019. “American Residential Macrosystems — Soil
- **Verdict:** use-only data availability statement

### 50. `knb-lter-hbr.406.1` cited by `10.1007/s10021-025-00965-w`

- **Dataset:** Hubbard Brook Experimental Forest and Adirondack Mountains: In-stream large wood and riparian forest structure, 2002-2019 (2025)
- **Paper:** An Emerging Carbon Sink in Headwater Streams and the Role of Large Wood and Riparian Forest Structure — *Ecosystems*, 2025, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 51. `edi.140.1` cited by `10.15468/dl.dmikhw`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 52. `knb-lter-sbc.6001.2` cited by `10.1016/j.ecoinf.2016.08.005`

- **Dataset:** SBC LTER: Ocean: Time-series: Mid-water SeaFET and CO2 system chemistry at Alegria (ALE), ongoing since 2011-06-21 (2018)
- **Paper:** Beyond the benchtop and the benthos: Dataset management planning and design for time series of ocean carbonate chemistry associated with Durafet®-based pH sensors — *Ecological Informatics*, 2016, OA hybrid; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1016_j.ecoinf.2016.08.005.pdf` and re-run
- **Verdict:** 

### 53. `knb-lter-luq.176.1180601` cited by `10.1046/j.1365-2427.2002.00785.x`

- **Dataset:** Lotic Intersite Nitrogen eXperiment I (LINX1): Stream nitrogen (N) dynamics in streams on the eastern side of Puerto Rico (2023)
- **Paper:** Characterizing nitrogen dynamics, retention and transport in a tropical rainforest stream using an in situ15N addition — *Freshwater Biology*, 2002, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 54. `knb-lter-mcr.8.28` cited by `10.1038/s41598-018-25414-8`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Benthic Algae and Other Community Components, ongoing since 2005 (2015)
- **Paper:** Recruitment Drives Spatial Variation in Recovery Rates of Resilient Coral Reefs — *Scientific Reports*, 2018, OA gold; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 54,454 chars
- **marker** via ref 51, body [33327–33498]: Additionally, the abundance of mobile invertebrates and percent cover of genera of macroalgae along the transects at each site are estimated in situ by scuba divers [51] . ← **query candidate**
- **marker** via ref 51, body [43710–43853]: Data for this study are available on the website of the Moorea Coral Reef Long Term Ecological Project: http://mcr.lternet.edu/data [49],[51] .
- **doi**, reference list [53341–53555]: MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Benthic Algae and Other Community Components, ongoing since 2005. knb-lter-mcr.8.28 10.6073/pasta/79a6edbcf3aa2380d43deed7788564162015 (2015). 52.
- **Verdict:** 

### 55. `knb-lter-and.2742.11` cited by `10.1002/eap.1560`

- **Dataset:** Long-term growth, mortality and regeneration of trees in permanent vegetation plots in the Pacific Northwest, 1910 to present (2017)
- **Paper:** Historical harvests reduce neighboring old‐growth basal area across a forest landscape — *Ecological Applications*, 2017, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 56. `knb-lter-hbr.59.10` cited by `10.1007/s10533-023-01105-z`

- **Dataset:** Hubbard Brook Experimental Forest: Daily Temperature Record, 1955 - present (2021)
- **Paper:** Combination of factors rather than single disturbance drives perturbation of the nitrogen cycle in a temperate forest — *Biogeochemistry*, 2023, OA closed; cites 16 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 57. `knb-lter-hbr.127.7` cited by `10.5194/bg-18-169-2021`

- **Dataset:** Longitudinal Stream Chemistry at the Hubbard Brook Experimental Forest, Watershed 6, 1982 - present (2016)
- **Paper:** Increased carbon capture by a silicate-treated forested watershed affected by acid deposition — *Biogeosciences*, 2021, OA gold; cites 12 EDI dataset(s); link source references/crossref
- **Text:** pdf, 91,921 chars
- **doi**, body [66901–67117]: The data include chemistry data for treated and reference watersheds (https://doi.org/10.6073/pasta/ fcfa498c5562ee55f6e84d7588a980d2, Driscoll, 2016a; https: //doi.org/10.6073/pasta/0033e820ff0e6a055382d4548dc5c90c, ← **query candidate**
- **author_year**, body [15417–15617]: PHREEQC version 3.3.12-12704 (Parkhurst and Appelo, 1999) and monthly long-term (1992–2014) stream-water (Driscoll, 2016b, a) and rain and snow precipitation (Likens, 2016b, a) chemistry measurements.
- **author_year**, body [22320–22456]: In our case, daily ﬂow measurements (Campbell, 2015) and approximately monthly stream-water samples (Driscoll, 2016b, a) were available.
- **doi**, reference list [75557–75762]: T.: Longitudinal Stream Chemistry at the Hubbard Brook Experimental Forest, Watershed 6, 1982–present, Environmental Data Initiative, https://doi.org/10.6073/pasta/ 0033e820ff0e6a055382d4548dc5c90c, 2016b.
- **Verdict:** 

### 58. `knb-lter-and.4020.23` cited by `https://ir.library.oregonstate.edu/concern/graduate_thesis_or_dissertations/9019s9306`

- **Dataset:** Stream and air temperature data from stream gages and stream confluences in the Andrews Experimental Forest, 1950 to present (2019)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 4 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 59. `knb-lter-nwt.187.3` cited by `10.1080/15230430.2026.2631217`

- **Dataset:** Infilled daily air temperature data for D1 chart recorder, 1952 - ongoing. (2024)
- **Paper:** Unraveling hydrologic and hydrochemical processes based on long-term concentration–discharge analysis in the Green Lake 4 catchment, Colorado Front Range, USA — *Arctic Antarctic and Alpine Research*, 2026, OA gold; cites 6 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:www.tandfonline.com:403:not-pdf; pdf:digitalcommons.mtu.edu:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1080_15230430.2026.2631217.pdf` and re-run
- **Verdict:** 

### 60. `knb-lter-arc.1062.4` cited by `https://deepblue.lib.umich.edu/bitstream/handle/2027.42/169988/bowenjc_1.pdf?sequence=1`

- **Dataset:** Water chemistry data for various lakes near Toolik Research Station, Arctic LTER. Summer 2010 to 2018 (2019)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 4 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 61. `knb-lter-sev.1.13` cited by `10.1016/j.envsoft.2019.03.020`

- **Dataset:** Meteorology Data from the Sevilleta National Wildlife Refuge, New Mexico (1988- present) (2016)
- **Paper:** Enabling Collaborative Numerical Modeling in Earth Sciences using Knowledge Infrastructure — *Environmental Modelling & Software*, 2019, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 112,404 chars
- **doi**, reference list [100830–100934]: Environmental Data Initiative. https://doi.org/10.6073/pasta/4d71c09b242602114fb684c843e9d6ac Moore, R.
- **title**, reference list [100738–100828]: Meteorology Data from the Sevilleta National Wildlife Refuge, New Mexico (1988- present) .
- **Verdict:** 

### 62. `knb-lter-knz.166.1` cited by `10.1002/eap.2830`

- **Dataset:** RIV07 Seeding rates woody removal of a tallgrass prairie stream and riparian zone after a decade of woody vegetation removal (2022)
- **Paper:** Trajectories and state changes of a grassland stream and riparian zone after a decade of woody vegetation removal — *Ecological Applications*, 2023, OA hybrid; cites 14 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_eap.2830.pdf` and re-run
- **Verdict:** 

### 63. `knb-lter-fce.1071.15` cited by `10.1007/s10530-024-03444-w`

- **Dataset:** Sawgrass Above and Below Ground Total Phosphorus from the Shark River Slough, Everglades National Park (FCE LTER), Florida, USA, September 2002 - ongoing (2023)
- **Paper:** Trophic niche of a nonnative invader and environmental drivers of its increasing populations in the coastal Everglades — *Biological Invasions*, 2024, OA hybrid; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:link.springer.com:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s10530-024-03444-w.pdf` and re-run
- **Verdict:** 

### 64. `knb-lter-fce.1198.6` cited by `10.1038/s41598-024-82158-4`

- **Dataset:** Movements of aquatic mesopredators within the Shark River estuary (FCE LTER), Everglades National Park, South Florida, USA, February 2012 - ongoing (2023)
- **Paper:** Cause and consequences of Common Snook (Centropomus undecimalis) space use specialization in a subtropical riverscape — *Scientific Reports*, 2025, OA gold; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 94,875 chars
- **doi**, reference list [47658–47755]: EnvironmentalData Initiative. 10.6073/pasta/dc3a992e2eb71472a89e70f837d3010f, and Rezek, R. 2024.
- **doi**, reference list [71759–71856]: EnvironmentalData Initiative. 10.6073/pasta/dc3a992e2eb71472a89e70f837d3010f, and Rezek, R. 2024.
- **title**, reference list [47503–47657]: Movements of aquatic mesopredators within the Shark River estuary (FCE LTER), Everglades National Park, South Florida, USA, February 2012 - ongoing ver 6.
- **title**, reference list [71604–71758]: Movements of aquatic mesopredators within the Shark River estuary (FCE LTER), Everglades National Park, South Florida, USA, February 2012 - ongoing ver 6.
- **Verdict:** 

### 65. `knb-lter-vcr.147.22` cited by `10.1016/j.ecoinf.2016.11.011`

- **Dataset:** Keywords and Terms from the LTER Network - 2006 (2013)
- **Paper:** A prototype system for multilingual data discovery of International Long-Term Ecological Research (ILTER) Network data — *Ecological Informatics*, 2016, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 66. `knb-lter-ntl.6.36` cited by `10.1101/2025.03.23.644810`

- **Dataset:** North Temperate Lakes LTER: Fish Lengths and Weights 1981 - current (2024)
- **Paper:** Warming and species richness weaken eco-phenotypic feedback loop in long-term natural ecosystems — *bioRxiv (Cold Spring Harbor Laboratory)*, 2025, OA closed; cites 6 EDI dataset(s); link source references/crossref
- **Text:** pdf, 57,569 chars
- **doi**, reference list [57036–57150]: Environmental Data Initiative 584 https://doi.org/10.6073/PASTA/E97E5046660A7144F4B6AADE41C2125D (2024). 585 70.
- **Verdict:** 

### 67. `edi.740.3` cited by `10.1002/tafs.10286`

- **Dataset:** CVPIA Predation Contact Point Study - 2019: Impacts of Artificial Light At Night in the Sacramento – San Joaquin Delta (2024)
- **Paper:** Effects of Artificial Lighting at Night on Predator Density and Salmonid Predation — *Transactions of the American Fisheries Society*, 2020, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_tafs.10286.pdf` and re-run
- **Verdict:** 

### 68. `knb-lter-mcr.6.58` cited by `10.1002/lom3.10557`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Fishes, ongoing since 2005 (2021)
- **Paper:** Using machine learning to achieve simultaneous, georeferenced surveys of fish and benthic communities on shallow coral reefs — *Limnology and Oceanography Methods*, 2023, OA bronze; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lom3.10557.pdf` and re-run
- **Verdict:** 

### 69. `knb-lter-mcr.5030.10` cited by `10.1038/s41598-018-34686-z`

- **Dataset:** MCR LTER: Coral Reef: Data in support of Edmunds 2018 Scientific Reports (2019)
- **Paper:** Implications of high rates of sexual recruitment in driving rapid reef recovery in Mo’orea, French Polynesia — *Scientific Reports*, 2018, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 62,635 chars
- **doi**, body [36694–36890]: Data for this study are available on the website of the Moorea Coral Reef Long Term Ecological Project: http://mcr.lternet.edu/data and data release 10.6073/pasta/9a32153038bb492da58666e9314bab4d. ← **query candidate**
- **Verdict:** 

### 70. `knb-lter-kbs.23.30` cited by `10.1002/ecy.3979`

- **Dataset:** Insect Population Dynamics on the Main Cropping System Experiment at the Kellogg Biological Station, Hickory Corners, MI (1989 to 2019) (2020)
- **Paper:** Coexistence between similar invaders: The case of two cosmopolitan exotic insects — *Ecology*, 2023, OA hybrid; cites 2 EDI dataset(s); link source references/crossref
- **Text:** pdf, 79,639 chars
- **doi**, reference list [68475–68624]: Station, Hickory Corners, MI (1989 to 2019) ver 30. ” Environmental Data Initiative. https://doi.org/10.6073/pasta/ f0776c1574808b08c484c1f7645a7357.
- **title**, reference list [68365–68421]: Landis, D. 2020. “Insect Population Dynamics on the Main
- **author_year**, reference list [55114–55267]: Organismal data sets (Landis, 2020) and weather data (Robertson, 2020) utilized for this research are mirrored within our Zenodo repository as CSV files.
- **Verdict:** 

### 71. `edi.898.1` cited by `10.1016/j.geoderma.2021.115353`

- **Dataset:** Repeated freeze-thaw cycles increase extractable, but not total, carbon and nitrogen in a Maine coniferous soil (2021)
- **Paper:** Repeated freeze–thaw cycles increase extractable, but not total, carbon and nitrogen in a Maine coniferous soil — *Geoderma*, 2021, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 72. `knb-lter-vcr.61.38` cited by `10.3389/fmars.2023.1129295`

- **Dataset:** Tide Data for Hog Island (1991-), Redbank (1992-), Oyster (2007-) (2024)
- **Paper:** Temperature amplification and marine heatwave alteration in shallow coastal bays — *Frontiers in Marine Science*, 2023, OA gold; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 58,601 chars
- **title**, reference list [57312–57393]: M (2022). Tide Data for Hog Island (1991-) Redbank (1992-) Oyster (2007-) ver 37.
- **Verdict:** 

### 73. `edi.291.5` cited by `10.3354/meps14999`

- **Dataset:** Virgin Islands National Park: Coral Reef: Population Dynamics: Scleractinian corals (2025)
- **Paper:** Persistent coral communities on degraded Caribbean reefs — *Marine Ecology Progress Series*, 2025, OA hybrid; cites 1 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.3354_meps14999.pdf` and re-run
- **Verdict:** 

### 74. `knb-lter-hbr.208.8` cited by `10.1007/s10533-023-01105-z`

- **Dataset:** Continuous precipitation and stream chemistry data, Hubbard Brook Ecosystem Study, 1963 – present. (2022)
- **Paper:** Combination of factors rather than single disturbance drives perturbation of the nitrogen cycle in a temperate forest — *Biogeochemistry*, 2023, OA closed; cites 16 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 75. `edi.243.2` cited by `10.1016/j.foreco.2017.04.040`

- **Dataset:** Forest tree, woody debris, and soil inventory data from long-term research plots at the University of Michigan Biological Station (2018)
- **Paper:** Physiographic factors underlie rates of biomass production during succession in Great Lakes forest landscapes — *Forest Ecology and Management*, 2017, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 76. `knb-lter-mcr.6.53` cited by `10.1002/ecy.1668`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Fishes, ongoing since 2005 (2016)
- **Paper:** Context‐dependent landscape of fear: algal density elicits risky herbivory in a coral reef — *Ecology*, 2016, OA closed; cites 1 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 77. `knb-lter-hbr.393.2` cited by `10.1002/ecs2.4949`

- **Dataset:** Hubbard Brook Experimental Forest: Annual measurements on marked northern red oak seedlings, 2014-ongoing (2024)
- **Paper:** Multi‐cohort survival of northern red oak seedlings at a northern hardwood forest transition — *Ecosphere*, 2024, OA gold; cites 6 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4949.pdf` and re-run
- **Verdict:** 

### 78. `knb-lter-sev.1.14` cited by `10.1002/ecy.70206`

- **Dataset:** Meteorology Data from the Sevilleta National Wildlife Refuge, New Mexico (2021)
- **Paper:** Small rainfall events increase belowground production in Chihuahuan Desert grassland — *Ecology*, 2025, OA closed; cites 3 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 79. `knb-lter-gce.313.31` cited by `10.1002/ecy.3278`

- **Dataset:** Fall 2008 plant monitoring survey -- biomass calculated from shoot height and flowering status of plants in permanent plots at GCE sampling sites 1-10 (2021)
- **Paper:** Variation in synchrony of production among species, sites, and intertidal zones in coastal marshes — *Ecology*, 2020, OA closed; cites 38 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 80. `knb-lter-ntl.29.29` cited by `10.1073/pnas.2211796120`

- **Dataset:** North Temperate Lakes LTER: Physical Limnology of Primary Study Lakes 1981 - current (2021)
- **Paper:** Species invasions shift microbial phenology in a two-decade freshwater time series — *Proceedings of the National Academy of Sciences*, 2023, OA hybrid; cites 9 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 58,562 chars
- **package_id**, body [27004–27405]: We combined our measurements with additional water temperature, dissolved oxygen, water clarity, and ice cover datasets made available by the North Temperate Lakes Long-Term Ecological Research program (NTL-LTER) under EDI identifiers knb-lter-ntl.29.29 ([39]), knb-lter-ntl.130.29 ([40]), knb-lter-ntl.335.1 ([41]), knb-lter-ntl.400.2 ([42]), knb-lter-ntl.31.30 ([43]), and knb-lter-ntl.33.35 ([44]). ← **query candidate**
- **doi**, reference list [46054–46196]: H., North Temperate Lakes lter: Physical limnology of primary study Lakes 1981–current (2021). 10.6073/PASTA/316203040EA1B8ECE89673985AB431B7.
- **doi**, reference list [56189–56331]: H., North Temperate Lakes lter: Physical limnology of primary study Lakes 1981–current (2021). 10.6073/PASTA/316203040EA1B8ECE89673985AB431B7.
- **Verdict:** 

### 81. `knb-lter-pal.48.7` cited by `https://csuepress.columbusstate.edu/theses_dissertations/470`

- **Dataset:** Bacterial properties in discrete water column samples at selected depths, collected aboard Palmer LTER annual cruises off the coast of the Western Antarctica Peninsula, 2003 - 2019. (2020)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 5 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 82. `edi.1141.1` cited by `10.1007/s10040-025-02874-7`

- **Dataset:** Geochemical data from sediments and porewaters from ferruginous and meromictic Brownie Lake, Minnesota, U.S.A. (2022)
- **Paper:** Local-scale hydrogeologic controls on groundwater discharge to a ferruginous meromictic kettle lake — *Hydrogeology Journal*, 2025, OA closed; cites 3 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 83. `knb-lter-hbr.239.1` cited by `10.21203/rs.3.rs-1362894/v1`

- **Dataset:** Forest Inventory of a Northern Hardwood Forest: Watershed 6, 2017, Hubbard Brook Experimental Forest (2019)
- **Paper:** An Equation of State Unifies Diversity, Productivity, Abundance and Biomass — *Research Square*, 2022, OA green; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 31,394 chars
- **doi**, reference list [24709–24806]: (https://doi.org/10.6073/pasta/0593ba15fb76a4f085797126a1bea3a7 (Accessed 2021-10-02). 20 29.
- **title**, reference list [24561–24669]: Forest Inventory of a Northern Hardwood Forest: Watershed 6, 2017, Hubbard Brook Experimental Forest ver 1.
- **Verdict:** 

### 84. `knb-lter-bes.5004.2` cited by `10.1371/journal.pone.0222630`

- **Dataset:** Baltimore Ecosystem Study: Household Telephone Survey in support of Locke et al 2019 in PLoS One (2019)
- **Paper:** Residential household yard care practices along urban-exurban gradients in six climatically-diverse U.S. metropolitan areas — *PLoS ONE*, 2019, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 40,990 chars
- **Mention:** none found
- **Verdict:** 

### 85. `knb-lter-sbc.50.10` cited by `10.1002/ecy.3673`

- **Dataset:** SBC LTER: Reef: Annual time series of biomass for kelp forest species, ongoing since 2000 (2021)
- **Paper:** Detrital supply suppresses deforestation to maintain healthy kelp forest ecosystems — *Ecology*, 2022, OA bronze; cites 3 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecy.3673.pdf` and re-run
- **Verdict:** 

### 86. `knb-lter-pal.24.10` cited by `10.1016/j.jembe.2020.151412`

- **Dataset:** Chlorophyll and phaeopigments from water column samples, collected at selected depths aboard Palmer LTER annual cruises off the coast of the Western Antarctic Peninsula, 1991 – 2019. (2020)
- **Paper:** Effects of temperature and food concentration on pteropod metabolism along the Western Antarctic Peninsula — *Journal of Experimental Marine Biology and Ecology*, 2020, OA closed; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 87. `edi.140.1` cited by `10.15468/dl.zqmys7`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 88. `msb-paleon.29.0` cited by `10.1017/qua.2025.10052`

- **Dataset:** Settlement Trees, Southeastern Michigan Level 0 (2020)
- **Paper:** Holocene moisture-variability impacts on forest composition and erosion at Pup Lake, northern Lower Michigan, USA — *Quaternary Research*, 2025, OA hybrid; cites 3 EDI dataset(s); link source references/crossref
- **Text:** pdf, 123,358 chars
- **author_year**, body [24921–25085]: ( 2021) and downloaded from the EDI online data repository ( https://portal.edirepository.org/nis/ home.jsp; McLachlan, 2020; McLachlan and Williams, 2020a, 2020b). ← **query candidate**
- **doi**, reference list [111343–111464]: Environmental Data Initiative. https://doi.org/10.6073/pasta/ 409ec6dfb218b6a3e98022916d2b4438 (accessed April 30, 2025).
- **title**, reference list [111262–111342]: McLachlan, J. , 2020. Settlement trees, southeastern Michigan level 0 version 0.
- **Verdict:** 

### 89. `knb-lter-hbr.58.7` cited by `10.5194/bg-18-169-2021`

- **Dataset:** Hubbard Brook Experimental Forest (USDA Forest Service): Daily Mean Temperature Data, 1955 - present (2016)
- **Paper:** Increased carbon capture by a silicate-treated forested watershed affected by acid deposition — *Biogeosciences*, 2021, OA gold; cites 12 EDI dataset(s); link source references/crossref
- **Text:** pdf, 91,921 chars
- **author_year**, body [17757–17895]: Air temperatures for the Hubbard Brook watersheds (Campbell, 2016) were converted to stream-water temperatures (Mohseni and Stefan, 1999). ← **query candidate**
- **doi**, reference list [67177–68185]: and reference watersheds (https://doi.org/10.6073/pasta/ 8d2d88dc718b6c5a2183cd88aae26fb1, Likens, 2016a; https: //doi.org/10.6073/pasta/df90f97d15c28daeb7620b29e2384bb9, Likens, 2016b), trace gas ﬂux data (https://doi.org/10. 6073/pasta/9d017f1a32cba6788d968dc03632ee03, Groffman, 2016), forest inventory data for 2006 and 2011 (https: //doi.org/10.6073/pasta/94f9084a3224c1e3e0ed38763f8dae02, Battles et al., 2015a; https://doi.org/10.6073/pasta/ 37c5a5868158e87db2d30c2d62a57e14, Battles et al., 2015b) and for 1999 and 2001 (https://doi.org/10.6073/pasta/ a2300121b6d594bbfcb3256ca1c300c8, Drisco
- **doi**, reference list [73029–73244]: Campbell, J.: Hubbard Brook Experimental Forest (USDA Forest Service): Daily Mean Temperature Data, 1955–present, Environmental Data Initiative, https://doi.org/10.6073/pasta/ 75b416d670de920c5ace92f8f3182964, 2016.
- **Verdict:** 

### 90. `knb-lter-hbr.258.1` cited by `10.1093/treephys/tpad043`

- **Dataset:** Physical, chemical, and metabolic leaf characteristics within sugar maple in the MELNHE study at Bartlett Experimental Forest, central NH USA, 2017 (2020)
- **Paper:** Patterns of physical, chemical, and metabolic characteristics of sugar maple leaves with depth in the crown and in response to nitrogen and phosphorus addition — *Tree Physiology*, 2023, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 91. `edi.1713.1` cited by `http://www.jstor.org/stable/29775598`

- **Dataset:** Twice weekly monitoring of a Microtus ochrogaster population and social behavior in alfalfa in eastern Illinois, 1982-1987. (2024)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 1 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 92. `knb-lter-mcm.9007.11` cited by `10.1029/2021jg006649`

- **Dataset:** McMurdo Dry Valleys LTER: High frequency seasonal stream gage measurements from Canada Stream at F1 in Taylor Valley, Antarctica from 1990 to present (2019)
- **Paper:** Dissolved Organic Carbon Chemostasis in Antarctic Polar Desert Streams — *Journal of Geophysical Research Biogeosciences*, 2022, OA closed; cites 10 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 93. `knb-lter-arc.10295.3` cited by `https://www.proquest.com/docview/2528833909`

- **Dataset:** Time-series of 5 minute water temperatures averages from Lake E6 near Toolik Field Station, Alaska Summer 2007. (2016)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 17 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 94. `knb-lter-cce.294.1` cited by `10.1002/lol2.10127`

- **Dataset:** Nano- and Microplastic Particle Lengths and Surface Areas, analyzed with Epifluorescence microscopy, collected aboard two student cruises, SKrillEx I (July 2014) and SKrillEx II (June 2015). (2019)
- **Paper:** Patterns of suspended and salp‐ingested microplastic debris in the North Pacific investigated with epifluorescence microscopy — *Limnology and Oceanography Letters*, 2019, OA gold; cites 6 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:aslopubs.onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.10127.pdf` and re-run
- **Verdict:** 

### 95. `knb-lter-pie.125.6` cited by `10.2112/jcoastresd1500153.1`

- **Dataset:** Marsh surface elevation data from control plots in a Spartina alterniflora-dominated salt marsh at Law's Point, Rowley River, Plum Island Ecosystem (PIE) LTER, MA. (2015)
- **Paper:** Hypsometry of Cape Cod Salt Marshes (Massachusetts, U.S.A.) and Predictions of Marsh Vegetation Responses to Sea-Level Rise — *Journal of Coastal Research*, 2016, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 96. `knb-lter-ntl.400.2` cited by `10.1038/s41564-024-01876-7`

- **Dataset:** Lake Mendota Multiparameter Sonde Profiles: 2017 - current (2021)
- **Paper:** Unravelling viral ecology and evolution over 20 years in a freshwater lake — *Nature Microbiology*, 2025, OA closed; cites 12 EDI dataset(s); link source references/crossref
- **Text:** closed (pdf:www.nature.com:200:not-pdf)
- **Verdict:** 

### 97. `knb-lter-arc.10531.10` cited by `10.1016/j.jhydrol.2024.132285`

- **Dataset:** Biogeochemistry data set for Imnavait Creek Weir on the North Slope of Alaska 2002-2022. (2023)
- **Paper:** Water and carbon fluxes from a supra-permafrost aquifer to a stream across hydrologic states — *Journal of Hydrology*, 2024, OA closed; cites 2 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 98. `knb-lter-ntl.364.2` cited by `10.1029/2019jg005186`

- **Dataset:** Spatial surface water chemistry of Lake Mendota with FLAMe: 2014-2016 (2019)
- **Paper:** Large Spatial and Temporal Variability of Carbon Dioxide and Methane in a Eutrophic Lake — *Journal of Geophysical Research Biogeosciences*, 2019, OA closed; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 99. `knb-lter-mcr.4.35` cited by `10.1002/ecy.4136`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Corals, ongoing since 2005 (2018)
- **Paper:** Diversity–stability relationships across organism groups and ecosystem types become decoupled across spatial scales — *Ecology*, 2023, OA bronze; cites 35 EDI dataset(s); link source references/crossref
- **Text:** pdf, 82,805 chars
- **author_year**, body [57997–58163]: 2022; Edmunds, 2018), Santa Barbara Coastal LTER (OCE-1831937) (Reed,2018), Sevilleta LTER (DEB-1655499) (Lightfoot, 2013, 2015;M u l d a v i n ,2015), and Shortgrass ← **query candidate**
- **doi**, reference list [68416–68616]: “MCR LTER: Coral Reef: Long-Term Population and Community Dynamics: Corals, Ongoing Since 2005 Ver 35. ” Environmental Data Initiative. https://doi.org/10. 6073/pasta/263faa48b520b7b2c964f158c184ef96.
- **Verdict:** 

### 100. `knb-lter-and.3222.36` cited by `10.1007/s00477-023-02495-0`

- **Dataset:** Meteorological data from benchmark stations at the Andrews Experimental Forest, 1957 to present (2019)
- **Paper:** Comparison of on-site versus NOAA’s extreme precipitation intensity-duration-frequency estimates for six forest headwater catchments across the continental United States — *Stochastic Environmental Research and Risk Assessment*, 2023, OA hybrid; cites 1 EDI dataset(s); link source references/crossref
- **Text:** europepmc, 70,369 chars
- **doi**, reference list [56478–56749]: Forest Science Data Bank , Corvallis, OR . 10.6073/pasta/c021a2ebf1f91adf0ba3b5e53189c84f Dhakal N , Jain S ( 2020 ) Nonstationary influence of the North Atlantic tropical cyclones on the spatio-temporal variability of the eastern United States precipitation extremes .
- **Verdict:** 

### 101. `knb-lter-nes.26.1` cited by `10.1073/pnas.2303356120`

- **Dataset:** Abundance and parasitoid infection dynamics of Guinardia delicatula on the Northeast U.S. Shelf from 2006 to 2022 determined by Imaging FlowCytobot. (2023)
- **Paper:** Temperature dependence of parasitoid infection and abundance of a diatom revealed by automated imaging and classification — *Proceedings of the National Academy of Sciences*, 2023, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 51,958 chars
- **doi**, reference list [51856–51936]: Environmental Data Initiative . 10.6073/pasta/7c43f9e037325e70ee736b7782327dd8 .
- **title**, reference list [51692–51789]: Sosik , Abundance and parasitoid infection dynamics of Guinardia delicatula on the Northeast U.S.
- **Verdict:** 

### 102. `knb-lter-bnz.515.10` cited by `10.1111/gcb.70609`

- **Dataset:** Eight Mile Lake Research Watershed, Thaw Gradient, The radiocarbon value of ecosystem respiration, 2004-2016 III: Atm. (2017)
- **Paper:** Permafrost Thaw Accelerates Old Soil Carbon Release, Outpacing New Plant Inputs During a 13‐Year Tundra Warming Experiment — *Global Change Biology*, 2025, OA green; cites 3 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_gcb.70609.pdf` and re-run
- **Verdict:** 

### 103. `edi.978.1` cited by `10.1002/esp.4547`

- **Dataset:** Turbidity of a Salt Marsh within the Altamaha River estuary, GA, USA, 2015-2017 (2021)
- **Paper:** The effect of a small vegetation dieback event on salt marsh sediment transport — *Earth Surface Processes and Landforms*, 2018, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 104. `knb-lter-luq.144.567756` cited by `10.1111/j.1365-2745.2010.01646.x`

- **Dataset:** Canopy Trimming Experiment (CTE) plants greater than 1 centimeter diameter at breast height (DBH) (2023)
- **Paper:** Plant responses to simulated hurricane impacts in a subtropical wet forest, Puerto Rico — *Journal of Ecology*, 2010, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 105. `knb-lter-nwt.185.2` cited by `10.1002/hyp.14320`

- **Dataset:** Infilled air temperature data for C1 chart recorder, 1952 - 2018, daily (2019)
- **Paper:** Catchment‐scale observations at the Niwot Ridge long‐term ecological research site — *Hydrological Processes*, 2021, OA hybrid; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_hyp.14320.pdf` and re-run
- **Verdict:** 

### 106. `knb-lter-vcr.210.9` cited by `10.1029/2019jg005416`

- **Dataset:** Integrated Topography and Bathymetry for the Eastern Shore of Virginia (2016)
- **Paper:** Impacts of Seagrass Dynamics on the Coupled Long‐Term Evolution of Barrier‐Marsh‐Bay Systems — *Journal of Geophysical Research Biogeosciences*, 2020, OA hybrid; cites 6 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf; pdf:scholarworks.wm.edu:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2019jg005416.pdf` and re-run
- **Verdict:** 

### 107. `edi.140.1` cited by `10.15468/dl.3suaje`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 108. `knb-lter-knz.112.4` cited by `10.1002/ecs2.4746`

- **Dataset:** CBS02 Nests of Grasshopper Sparrows on Konza Prairie (2023)
- **Paper:** Consequences of drought for grassland songbird reproduction — *Ecosphere*, 2024, OA gold; cites 5 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4746.pdf` and re-run
- **Verdict:** 

### 109. `edi.99.5` cited by `10.1093/gigascience/gix101`

- **Dataset:** LAGOS-NE-GEO v1.05: A module for LAGOS-NE, a multi-scaled geospatial and temporal database of lake ecological context and water quality for thousands of U.S. Lakes: 1925-2013 (2017)
- **Paper:** LAGOS-NE: a multi-scaled geospatial and temporal database of lake ecological context and water quality for thousands of US lakes — *GigaScience*, 2017, OA gold; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 104,818 chars
- **doi**, reference list [91986–92094]: Environmental Data Initiative; 2017; http://dx.doi.org/doi:10.6073/pasta/16f4bdaa9607c845c0b261a580730a7a .
- **doi**, reference list [104050–104158]: Environmental Data Initiative; 2017; http://dx.doi.org/doi:10.6073/pasta/16f4bdaa9607c845c0b261a580730a7a .
- **Verdict:** 

### 110. `edi.410.1` cited by `10.1080/10106049.2022.2071475`

- **Dataset:** Continuous Forest Inventory (CFI), 1970-2017, Long-term Forest Property Monitoring by State University of New York College of Environmental Science and Forestry, New York, USA (2019)
- **Paper:** Decision tree-based machine learning models for above-ground biomass estimation using multi-source remote sensing data and object-based image analysis — *Geocarto International*, 2022, OA closed; cites 1 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 111. `knb-lter-luq.227.2` cited by `10.1086/708808`

- **Dataset:** StreamFRE Abundance Macroinvertebrate (2023)
- **Paper:** When the rainforest dries: Drought effects on a montane tropical stream ecosystem in Puerto Rico — *Freshwater Science*, 2020, OA hybrid; cites 7 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.journals.uchicago.edu:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1086_708808.pdf` and re-run
- **Verdict:** 

### 112. `knb-lter-nwt.186.4` cited by `10.1029/2024jg008175`

- **Dataset:** Infilled daily precipitation data for D1 chart recorder, 1952 - ongoing. (2024)
- **Paper:** Quantifying Dust Nutrient Mobility Through an Alpine Watershed — *Journal of Geophysical Research Biogeosciences*, 2025, OA closed; cites 4 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 113. `knb-lter-pie.401.1` cited by `10.1029/2026jg009711`

- **Dataset:** Sediment porewater nutrients, sulfide, pH, and alkalinity in the Parker and Rowley River, Massachusetts (2013)
- **Paper:** Spatiotemporal Modulation of Alkalinity and DIC Outwelling From Saltmarsh Porewater in New England's Largest Marsh Complex — *Journal of Geophysical Research Biogeosciences*, 2026, OA closed; cites 9 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 114. `edi.1249.6` cited by `10.1111/gcb.16525`

- **Dataset:** Temperature and dissolved oxygen profiles for three Swiss lakes: 1972-2016 (2022)
- **Paper:** Longer duration of seasonal stratification contributes to widespread increases in lake hypoxia and anoxia — *Global Change Biology*, 2022, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 115. `edi.454.4` cited by `10.1111/gcb.16228`

- **Dataset:** Manually-collected discharge data for multiple inflow tributaries entering Falling Creek Reservoir and Beaverdam Reservoir, Vinton, Virginia, USA in 2019 (2019)
- **Paper:** Anoxia decreases the magnitude of the carbon, nitrogen, and phosphorus sink in freshwaters — *Global Change Biology*, 2022, OA hybrid; cites 7 EDI dataset(s); link source references/crossref
- **Text:** europepmc, 96,436 chars
- **doi**, reference list [77437–77539]: Environmental Data Initiative Repository . 10.6073/pasta/4d8e7b7bedbc6507b307ba2d5f2cf9a2 Carey , C.
- **title**, reference list [77274–77436]: Manually‐collected discharge data for multiple inflow tributaries entering Falling Creek Reservoir and Beaverdam Reservoir, Vinton, Virginia, USA in 2019, ver 4 .
- **Verdict:** 

### 116. `knb-lter-sbc.6002.5` cited by `https://escholarship.org/uc/item/3n13c78h`

- **Dataset:** SBC LTER: Ocean: Time-series: Mid-water SeaFET pH and CO2 system chemistry with surface and bottom Dissolved Oxygen at Arroyo Quemado Reef(ARQ), 2012-2017 (2020)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 5 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 117. `knb-lter-bes.3210.110` cited by `10.1016/j.landurbplan.2025.105374`

- **Dataset:** GIS Shapefile, Tree Canopy Change 2007 - 2015 - Baltimore City (2017)
- **Paper:** Whose woods are these? Forest patch characteristics and ownership across cities of the eastern United States — *Landscape and Urban Planning*, 2025, OA closed; cites 1 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 118. `knb-lter-hbr.62.18` cited by `10.1007/s10533-023-01105-z`

- **Dataset:** Chemistry of freely-draining soil solutions at the Hubbard Brook Experimental Forest, Watershed 6, 1982 - present (2022)
- **Paper:** Combination of factors rather than single disturbance drives perturbation of the nitrogen cycle in a temperate forest — *Biogeochemistry*, 2023, OA closed; cites 16 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 119. `knb-lter-gce.617.5` cited by `10.1002/ecs2.3723`

- **Dataset:** Effects of Small-scale Armoring and Residential Development on the Salt Marsh/Upland Ecotone in Coastal Georgia, USA (2021)
- **Paper:** Influences of land use and ecological variables on trematode prevalence and intensity at the salt marsh‐upland ecotone — *Ecosphere*, 2021, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.3723.pdf` and re-run
- **Verdict:** 

### 120. `knb-lter-ntl.238.3` cited by `10.1029/2019jg005186`

- **Dataset:** North Temperate Lakes LTER: Phytoplankton - Trout Lake Area 1984 - current (2013)
- **Paper:** Large Spatial and Temporal Variability of Carbon Dioxide and Methane in a Eutrophic Lake — *Journal of Geophysical Research Biogeosciences*, 2019, OA closed; cites 4 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 121. `knb-lter-ble.7.2` cited by `10.5194/bg-2020-358`

- **Dataset:** Circulation dynamics: currents, waves, temperature measurements from moorings in lagoon sites along the Alaska Beaufort Sea coast, 2018-ongoing (2020)
- **Paper:** The Seasonal Phases of an Arctic Lagoon Reveal Non-linear pH Extremes — *?*, 2020, OA gold; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 92,320 chars
- **doi**, reference list [64282–64440]: Environmental Data Initiative. 755 https://doi.org/10.6073/pasta/3475cdbb160a9f844aa5ede627c5f6fe 756 757 Beaufort Lagoon Ecosystems LTER, Core Program. 2020.
- **Verdict:** 

### 122. `knb-lter-hfr.1.26` cited by `10.21203/rs.3.rs-1093360/v1`

- **Dataset:** Fisher Meteorological Station at Harvard Forest since 2001 (2021)
- **Paper:** Warmer spring temperatures in temperate deciduous forests advance the timing of tree growth but have little effect on annual woody productivity — *Research Square*, 2021, OA green; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 55,568 chars
- **doi**, reference list [52521–52615]: (2021) 594 doi:10.6073/PASTA/69E92642B512897032446CFE795CFFB8. 595 57. van de Pol, M. et al.
- **title**, reference list [52451–52520]: Boose, E. Fisher Meteorological Station at Harvard Forest since 2001.
- **Verdict:** 

### 123. `knb-lter-and.5488.2` cited by `https://ir.library.oregonstate.edu/concern/graduate_thesis_or_dissertations/dv140195j`

- **Dataset:** Soil moisture and soil properties in Watershed 1 of the HJ Andrews Experimental Forest, 2016–2020 (2021)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 3 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 124. `knb-lter-knz.14.22` cited by `10.1007/s00442-024-05526-x`

- **Dataset:** AWE01 Meteorological data from the konza prairie headquarters weather station (2023)
- **Paper:** Combined effects of fire and drought are not sufficient to slow shrub encroachment in tallgrass prairie — *Oecologia*, 2024, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 125. `knb-lter-arc.10295.3` cited by `10.1080/20442041.2025.2461419`

- **Dataset:** Time-series of 5 minute water temperatures averages from Lake E6 near Toolik Field Station, Alaska Summer 2007. (2016)
- **Paper:** Prediction of future Alaskan lake methane emissions using a small-lake model coupled to a regional climate model — *Inland Waters*, 2025, OA closed; cites 17 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 126. `knb-lter-sev.106.214968` cited by `10.1126/science.aax9931`

- **Dataset:** Long-Term Core Site Grasshopper Dynamics for the Sevilleta National Wildlife Refuge, New Mexico (1992-2013) (2015)
- **Paper:** Meta-analysis reveals declines in terrestrial but increases in freshwater insect abundances — *Science*, 2020, OA closed; cites 13 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 127. `knb-lter-mcm.7007.16` cited by `10.5194/tc-14-769-2020`

- **Dataset:** McMurdo Dry Valleys LTER - High frequency measurements from Commonwealth Glacier Meteorological Station (COHM) - Taylor Valley, Antarctica - 1993 to present (2019)
- **Paper:** The seasonal evolution of albedo across glaciers and the surrounding landscape of Taylor Valley, Antarctica — *The cryosphere*, 2020, OA gold; cites 7 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 99,104 chars
- **author_year**, body [80147–80424]: Albedo datasets (Bergstrom and Gooseff, 2019) are available at https://mcm.lternet.edu/content/landscapealbedo-taylor-valley-antarctica-2015-2019 (https://doi.org/10.6073/pasta/728016d29b9a7df1eec1cf1ac9b17c23). Taylor Glacier meteorological datasets (Doran and Fountain, 2019) ← **query candidate**
- **author_year**, body [80762–80964]: Lake Hoare meteorological datasets (Doran and Fountain, 2019) are available at https://mcm.lternet.edu/content/high-frequency-measurementslake-hoare-meteorological-station-hoem-taylor-valley-antarctica.
- **author_year**, body [80762–81030]: Lake Hoare meteorological datasets (Doran and Fountain, 2019) are available at https://mcm.lternet.edu/content/high-frequency-measurementslake-hoare-meteorological-station-hoem-taylor-valley-antarctica. Canada Glacier meteorological datasets (Doran and Fountain, 2019)
- **doi**, reference list [85859–85963]: Antarctica from 1993 to present, https://doi.org/10.6073/pasta/ 16a9543aa5a72ead75c40a89038e8f0f, 2019b.
- **Verdict:** 

### 128. `edi.2032.1` cited by `10.1093/etojnl/vgaf162`

- **Dataset:** Outdoor mesocosm study evaluating how mass, NaCl tolerance, and pesticide tolerance affect oxidative stress biomarkers (CAT, SOD, GR, GPx, TBARS) in larval wood frogs (Rana sylvatica) exposed to baseline and NaCl-contaminated conditions, 2019 (2025)
- **Paper:** Effects of body mass and legacy of pesticide contamination on oxidative stress biomarkers in larval Rana sylvatica under baseline and sodium chloride–contaminated conditions — *Environmental Toxicology and Chemistry*, 2025, OA closed; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 129. `knb-lter-cap.626.1` cited by `https://www.proquest.com/openview/858a870f1113b625f4b0472b94d1839c`

- **Dataset:** Bird surveys along the Salt River in and near the greater Phoenix metropolitan area: 2012-2013 (2016)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 2 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 130. `edi.1404.1` cited by `10.21203/rs.3.rs-2874402/v1`

- **Dataset:** Cover crop application on dredged sediments increases corn yield through microorganism-associated enzyme-driven nutrient mineralization. (2023)
- **Paper:** Cover crop application on dredged sediments increases corn yield through microorganism-associated enzyme-driven nutrient mineralization. — *Research Square*, 2023, OA green; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 99,720 chars
- **doi**, reference list [78705–79016]: “Cover Crop Application on Dredged Sediments Increases Corn Yield through Microorganism-Associated Enzyme-Driven Nutrient Mineralization.” ver 1. https://portal.edirepository.org/nis/mapbrowse?packageid=edi.1404.1: Environment Data Initiative. https://doi.org/10.6073/pasta/6cf8f1903048b148e42deeae33478dd9. 53.
- **Verdict:** 

### 131. `knb-lter-hfr.300.5` cited by `10.1101/2023.08.14.553264`

- **Dataset:** Harvard Forest Climate Data since 1964 (2022)
- **Paper:** Seasonal effects of long-term warming on ecosystem function and bacterial diversity — *bioRxiv (Cold Spring Harbor Laboratory)*, 2023, OA green; cites 1 EDI dataset(s); link source references/crossref
- **Text:** pdf, 77,031 chars
- **author_year**, body [19665–19833]: An additional contributor to the higher EMF observed in fall could be a two-day rainfall event that occurred two days prior to the fall sampling (Boose and Gould 2022). ← **query candidate**
- **doi**, reference list [46136–46277]: Boose, Emery and Ernest Gould (2022).Harvard Forest Climate Data since 1964. https://doi.org/10. 6073/pasta/03dc1f107ca816675b4983daf7a97dbe.
- **Verdict:** 

### 132. `knb-lter-sbc.158.1` cited by `10.1002/ecy.4270`

- **Dataset:** Annual and monthly time series of estimated kelp spore dispersal times among ROMS cells in southern California, 1996 – 2006 (2023)
- **Paper:** Dispersal synchronizes giant kelp forests — *Ecology*, 2024, OA hybrid; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecy.4270.pdf` and re-run
- **Verdict:** 

### 133. `knb-lter-knz.128.3` cited by `10.1890/13-2186.1`

- **Dataset:** CEE01 The Climate Extremes Experiment (CEE): Assessing ecosystem resistance and resilience to repeated climate extremes at Konza Prairie (2020)
- **Paper:** Resistance and resilience of a grassland ecosystem to climate extremes — *Ecology*, 2014, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 134. `knb-lter-sbc.6004.3` cited by `10.1016/j.ecoinf.2016.08.005`

- **Dataset:** SBC LTER: Ocean: Time-series: Mid-water SeaFET pH and CO2 system chemistry with surface and bottom Dissolved Oxygen at Santa Barbara Harbor/Stearns Wharf(SBH), ongoing since 2012-09-15 (2018)
- **Paper:** Beyond the benchtop and the benthos: Dataset management planning and design for time series of ocean carbonate chemistry associated with Durafet®-based pH sensors — *Ecological Informatics*, 2016, OA hybrid; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1016_j.ecoinf.2016.08.005.pdf` and re-run
- **Verdict:** 

### 135. `knb-lter-luq.23.4630180` cited by `10.1101/766790`

- **Dataset:** Bird abundance - point counts (2015)
- **Paper:** Deviations from dynamic equilibrium in ecological communities worldwide — *bioRxiv (Cold Spring Harbor Laboratory)*, 2019, OA green; cites 6 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 84,655 chars
- **doi**, reference list [77063–77216]: Available at: https://doi.org/10.6073/pasta/0d96957379936a038ebbbcc6135b2fab, accessed 2012 (2010). not certified by peer review) is the author/funder.
- **title**, reference list [76988–77023]: B. “Bird abundance - point counts”.
- **Verdict:** 

### 136. `knb-lter-sgs.701.1` cited by `10.1016/j.rama.2017.06.007`

- **Dataset:** SGS-LTER Standard Production Data: 2009-2012 Annual Aboveground Net Primary Production on the Central Plains Experimental Range, Nunn, Colorado, USA 2009-2012, ARS Study Number 6 (2014)
- **Paper:** Productivity and CO 2 Exchange of Great Plains Ecoregions. I. Shortgrass Steppe: Flux Tower Estimates — *Rangeland Ecology & Management*, 2017, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.sciencedirect.com:403:not-pdf; pdf:repository.arizona.edu:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1016_j.rama.2017.06.007.pdf` and re-run
- **Verdict:** 

### 137. `edi.140.1` cited by `10.15468/dl.l8gin5`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 138. `knb-lter-arc.10284.3` cited by `10.1080/20442041.2025.2461419`

- **Dataset:** Time-series of 5 minute water temperatures averages from Lake E5 near Toolik Field Station, Alaska Summer 2003. (2016)
- **Paper:** Prediction of future Alaskan lake methane emissions using a small-lake model coupled to a regional climate model — *Inland Waters*, 2025, OA closed; cites 17 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 139. `knb-lter-and.4021.21` cited by `https://www.fs.fed.us/pnw/pubs/pnw_gtr981.pdf`

- **Dataset:** Stream chemistry concentrations and fluxes using proportional sampling in the Andrews Experimental Forest, 1968 to present (2016)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 3 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 140. `edi.1062.1` cited by `10.5194/essd-15-2879-2023`

- **Dataset:** Stream Restoration and Flood Impacts in the Kickapoo River Watershed, Wisconsin, 2019 (2022)
- **Paper:** GRiMeDB: the Global River Methane Database of concentrations and fluxes — *Earth system science data*, 2023, OA gold; cites 55 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 236,543 chars
- **doi**, reference list [127409–127600]: H.: Stream restoration and ﬂood impacts in the Kickapoo River Watershed, Wisconsin, 2019, Environmental Data Initiative, https://doi.org/10.6073/pasta/ 4905369228d80920974f555a2dd12229, 2022.
- **Verdict:** 

### 141. `knb-lter-sev.1.15` cited by `10.1002/ecm.1574`

- **Dataset:** Meteorology Data from the Sevilleta National Wildlife Refuge, New Mexico (2022)
- **Paper:** Demography and dispersal at a grass‐shrub ecotone: A spatial integral projection model for woody plant encroachment — *Ecological Monographs*, 2023, OA bronze; cites 2 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecm.1574.pdf` and re-run
- **Verdict:** 

### 142. `knb-lter-ntl.300.1` cited by `10.1371/journal.pone.0095769`

- **Dataset:** Upper Midwest Great Lakes Region Citizen Secchi Data 1938 - 2012 (2014)
- **Paper:** Long-Term Citizen-Collected Data Reveal Geographical Patterns and Temporal Trends in Lake Water Clarity — *PLoS ONE*, 2014, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 35,763 chars
- **marker** via ref 16, body [6094–6303]: Methods Data Acquisition We obtained 239,741 citizen-collected Secchi depth measurements from monitoring networks in eight states in the Upper Midwest region of the United States ( Fig. 2 ; Table 1 ) [[16]]. ← **query candidate**
- **doi**, reference list [32735–32831]: Long Term Ecological Research Network doi: 10.6073/pasta/5f94d3db0f3b7f1648579bf319aefacc . 17.
- **Verdict:** 

### 143. `knb-lter-luq.47.381051` cited by `10.1111/btp.13297`

- **Dataset:** Physical environment of the Luquillo Forest Dynamics Plot (LFDP), Puerto Rico (2018)
- **Paper:** Height–diameter allometry for a dominant palm to improve understanding of carbon and forest dynamics in forests of Puerto Rico — *Biotropica*, 2024, OA hybrid; cites 2 EDI dataset(s); link source references/crossref
- **Text:** pdf, 61,998 chars
- **author_year**, body [15322–15487]: For palms inside the LFDP, we used the LFDP census data to determine elevation (m) and slope (%) in their immediate area (Thompson et al., 2002 ; Zimmerman, 2018 ). ← **query candidate**
- **Verdict:** 

### 144. `knb-lter-jrn.2100126001.40` cited by `10.1002/ecs2.1631`

- **Dataset:** LTER Weather Station daily summary climate data (2015)
- **Paper:** Simulation of the effects of photodecay on long‐term litter decay using DayCent — *Ecosphere*, 2016, OA gold; cites 2 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf; pdf:scholarworks.uvm.edu:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.1631.pdf` and re-run
- **Verdict:** 

### 145. `knb-lter-vcr.210.9` cited by `10.1002/esp.4951`

- **Dataset:** Integrated Topography and Bathymetry for the Eastern Shore of Virginia (2016)
- **Paper:** Effect of offshore waves and vegetation on the sediment budget in the Virginia Coast Reserve (VA) — *Earth Surface Processes and Landforms*, 2020, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_esp.4951.pdf` and re-run
- **Verdict:** 

### 146. `knb-lter-bnz.174.20` cited by `10.1007/s10980-023-01733-8`

- **Dataset:** Vegetation Plots of the Bonanza Creek LTER Control Plots: Species Percent Cover (1975 - 2009) (2016)
- **Paper:** Future transitions from a conifer to a deciduous-dominated landscape are accelerated by greater wildfire activity and climate change in interior Alaska — *Landscape Ecology*, 2023, OA closed; cites 2 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 147. `knb-lter-and.4341.31` cited by `https://ir.library.oregonstate.edu/concern/graduate_thesis_or_dissertations/9019s9306`

- **Dataset:** Stream discharge in gaged watersheds at the Andrews Experimental Forest, 1949 to present (2019)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 4 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 148. `knb-lter-cdr.715.3` cited by `10.1111/ele.14262`

- **Dataset:** Species trait tissue chemistry: Biodiversity II: Effects of Plant Biodiversity on Population and Ecosystem Processes (2023)
- **Paper:** Plant chemical traits define functional and phylogenetic axes of plant biodiversity — *Ecology Letters*, 2023, OA hybrid; cites 3 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_ele.14262.pdf` and re-run
- **Verdict:** 

### 149. `knb-lter-gce.4.20` cited by `10.3354/ame032095`

- **Dataset:** Fall 2000 fungal monitoring -- marshgrass ergosterol content and ascospore release rates at 10 GCE sampling sites (2014)
- **Paper:** Fungal content and activities in standing-decaying leaf blades of plants of the Georgia Coastal Ecosystems research area — *Aquatic Microbial Ecology*, 2003, OA bronze; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.int-res.com:401:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.3354_ame032095.pdf` and re-run
- **Verdict:** 

### 150. `knb-lter-luq.107.9996736` cited by `10.1002/ecy.4136`

- **Dataset:** El Verde Grid long-term invertebrate data (2018)
- **Paper:** Diversity–stability relationships across organism groups and ecosystem types become decoupled across spatial scales — *Ecology*, 2023, OA bronze; cites 35 EDI dataset(s); link source references/crossref
- **Text:** pdf, 82,805 chars
- **author_year**, body [57834–57942]: Whitford, 2022), Konza Prairie LTER (DEB-20205849) (Joern, 2018), Luquillo LTER (DEB-1831952) (Willig,2018), ← **query candidate**
- **doi**, reference list [81137–81290]: “El Verde Grid Long-Term Invertebrate Data Ver 9996736. ” Environmental Data Initiative. https://doi.org/ 10.6073/pasta/ec88f3dd4ed8e172802b52ff3bb82aa8.
- **Verdict:** 

### 151. `edi.499.4` cited by `10.1002/lol2.70116`

- **Dataset:** Lake Sunapee Instrumented Buoy: High Frequency Water Quality Data - 2007-2022 (2023)
- **Paper:** Seasons and seasonality in lakes: A synthesis amid global change — *Limnology and Oceanography Letters*, 2026, OA gold; cites 10 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.70116.pdf` and re-run
- **Verdict:** 

### 152. `knb-lter-hfr.54.26` cited by `10.1002/eap.2957`

- **Dataset:** Community and Ecosystem Impacts in Hemlock Removal Experiment at Harvard Forest since 2003 (2021)
- **Paper:** Logging response alters trajectories of reorganization after loss of a foundation tree species — *Ecological Applications*, 2024, OA closed; cites 8 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 153. `knb-lter-cce.299.2` cited by `10.1029/2023jc019961`

- **Dataset:** Vertical profiles of in-situ biogenic silica (bSi) from discrete rosette bottle samples from CCE-LTER starting with cruise P1706. (2023)
- **Paper:** Iron Limitation and Biogeochemical Effects in Southern California Current Coastal Upwelling Filaments — *Journal of Geophysical Research Oceans*, 2023, OA hybrid; cites 5 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2023jc019961.pdf` and re-run
- **Verdict:** 

### 154. `edi.1136.3` cited by `http://digital.library.wisc.edu/1793/89744`

- **Dataset:** LAGOS-US GEO v1.0: Data module of lake geospatial ecological context at multiple spatial and temporal scales in the conterminous U.S. (2022)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 5 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 155. `edi.8.2` cited by `10.1007/s10452-024-10099-1`

- **Dataset:** Global Lake Ecological Observatory Network: Long term chloride concentration from 529 lakes and reservoirs around North America and Europe: 1940-2016 (2017)
- **Paper:** The impact of salinization on benthic macro-crustacean assemblages in a Mediterranean shallow lake — *Aquatic Ecology*, 2024, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 156. `edi.459.2` cited by `10.1371/journal.pone.0205211`

- **Dataset:** Female mouse 60d water uranium exposure (2020)
- **Paper:** Minimal uranium accumulation in lymphoid tissues following an oral 60-day uranyl acetate exposure in male and female C57BL/6J mice — *PLoS ONE*, 2018, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 24,617 chars
- **Mention:** none found
- **Verdict:** 

### 157. `knb-lter-bnz.747.2` cited by `10.1371/journal.pone.0238004`

- **Dataset:** Post-fire Variability in Siberian Alder in Interior Alaska: Distribution Patterns, Nitrogen Fixation Rates, and Ecosystem Consequences VII - Site Descriptions and Alder 2014 (2020)
- **Paper:** Can Siberian alder N-fixation offset N-loss after severe fire? Quantifying post-fire Siberian alder distribution, growth, and N-fixation in boreal Alaska — *PLoS ONE*, 2020, OA gold; cites 10 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 87,822 chars
- **doi**, reference list [62129–62723]: Data Availability The following DOIs all direct to the underlying data: doi: 10.6073/pasta/7f04d011ba2a39b08b794611b54b15ca doi: 10.6073/pasta/020191d3b9b72c88a8487b1684eba15c doi: 10.6073/pasta/0600e58dea74dd5df84153af35da6f56 doi: 10.6073/pasta/4694dfc87d322b4891a12e3c3fdabe18 doi: 10.6073/pasta/a8acc1f2107944a9e9ad91974c7aff91 doi: 10.6073/pasta/a5eed7ac3329a4aca7fb6e54185f0c50 doi: 10.6073/pasta/705056665d58f1138d9707f262487482 doi: 10.6073/pasta/f0b1cb6152f360c42a11db3d5cd2a61a doi: 10.6073/pasta/7496cd1d2f43929266e7feca934d1621 doi: 10.6073/pasta/37703e3d1a3aa6c41a491cbba91a3ce1 .
- **Verdict:** 

### 158. `knb-lter-hbr.136.5` cited by `10.1007/s10584-020-02943-8`

- **Dataset:** Snow depth, soil frost depth and snow water content along an elevation gradient at the Hubbard Brook Experimental Forest. (2019)
- **Paper:** Snowpack affects soil microclimate throughout the year — *Climatic Change*, 2020, OA closed; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 159. `knb-lter-vcr.404.1` cited by `10.3390/jmse12071037`

- **Dataset:** Flow dynamics and pump kinematics in polychaete burrows constructed in a transparent mud analog (2024)
- **Paper:** Pulsatile Ventilation Flow in Polychaete Alitta succinea Burrows — *Journal of Marine Science and Engineering*, 2024, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.3390_jmse12071037.pdf` and re-run
- **Verdict:** 

### 160. `edi.140.1` cited by `10.15468/dl.csihfu`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 161. `knb-lter-ble.30.1` cited by `10.1002/lno.70101`

- **Dataset:** Total suspended solids from river, lagoon, and open ocean sites along the Alaska Beaufort Sea coast, 2022-ongoing (2023)
- **Paper:** Carbon dioxide fluxes of Arctic coastal ecosystems controlled by seasonal patterns of land‐to‐ocean connectivity — *Limnology and Oceanography*, 2025, OA closed; cites 7 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 162. `knb-lter-luq.170.159351` cited by `10.1636/p13-65.1`

- **Dataset:** Phrynus habitat selection (2023)
- **Paper:** Seasonal patterns of microhabitat selection by a sub-tropical whip spider,Phrynus longipes, in the Luquillo Experimental Forest, Puerto Rico — *Journal of Arachnology*, 2014, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1636_p13-65.1.pdf` and re-run
- **Verdict:** 

### 163. `knb-lter-ntl.110.4` cited by `https://yorkspace-library-yorku-ca.ezproxy.library.wisc.edu/xmlui/handle/10315/37373`

- **Dataset:** Lake Metabolism at North Temperate Lakes LTER 2000 (2013)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 8 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 164. `edi.1540.1` cited by `10.1186/s13071-024-06258-w`

- **Dataset:** Supervised land cover classification using Google Earth Engine in Córdoba, Argentina, 2018-2020 (2023)
- **Paper:** Association between environmental gradient of anthropization and phenotypic plasticity in two species of triatomines — *Parasites & Vectors*, 2024, OA gold; cites 1 EDI dataset(s); link source references/crossref
- **Text:** europepmc, 67,749 chars
- **marker** via ref 43, body [11819–11947]: The database, codes and obtaining the thematic map from supervised classification are available on the online repository [[43]]. ← **query candidate**
- **marker** via ref 43, body [17643–17801]: Results Gradient of anthropization in the study area Thematic map with eight coverage classes was obtained (Fig. 1 a; Additional file 2 : Table S2) [[43]].
- **doi**, reference list [50041–50125]: Environmental Data Initiative. 2023. 10.6073/pasta/bd835a5be75fb14897679cb2b5d800cc.
- **doi**, reference list [64688–64772]: Environmental Data Initiative. 2023. 10.6073/pasta/bd835a5be75fb14897679cb2b5d800cc.
- **Verdict:** 

### 165. `edi.539.3` cited by `10.1371/journal.pone.0265402`

- **Dataset:** Interagency Ecological Program: Zooplankton abundance in the Upper San Francisco Estuary from 1972-2020, an integration of 5 long-term monitoring programs (2022)
- **Paper:** Five decades (1972–2020) of zooplankton monitoring in the upper San Francisco Estuary — *PLoS ONE*, 2022, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 111,858 chars
- **marker** via ref 55, body [18472–18976]: Dataset description and access The integrated dataset [[55]] includes a series of tables connected by keys that include sampling station locations (stations.csv and stations_EMP_EZ.csv), sample-level environmental and datetime data (environment.csv), information on taxa poorly sampled by micro and meso-zooplankton nets (undersampled.csv), biomass conversion values (biomass_mesomicro.csv), taxonomic information (taxonomy.csv) and zooplankton abundance data as catch per unit effort (zooplankton.csv). ← **query candidate**
- **marker** via ref 55, body [24589–25649]: Magnification Microscope magnification during sample processing Preservative Sample preservation medium CPUE_calculation CPUE calculation formula Biomass Biomass can be estimated Lengths_measured Lengths are measured Sample_archived Samples are archived Time Time of day is recorded Tidal_stage Tidal stage is recorded Depth_of_water The total depth of the water is recorded Surface_conductivity Conductivity at the surface is recorded Bottom_conductivity Conductivity at the surface is recorded Temperature Water temperature is recorded Secchi Secchi depth is recorded Turbidity Water turbidity is r
- **marker** via ref 55, body [47884–48026]: All code is available in the R package zooper version 2.3.1 [[56]] and in the R script “Data_processing.R” within the data publication [[55]].
- **doi**, reference list [67463–67699]: Data Availability All data files are available on the Environmental Data Initiative (doi:10.6073/pasta/89dbadd9d9dbdfc804b160c81633db0d and web link: https://portal.edirepository.org/nis/mapbrowse?scope=edi&identifier=539&revision=3 ).
- **doi**, reference list [80284–80378]: Environmental Data Initiative. 2022. doi: 10.6073/pasta/89dbadd9d9dbdfc804b160c81633db0d 56.
- **doi**, reference list [102318–102412]: Environmental Data Initiative. 2022. doi: 10.6073/pasta/89dbadd9d9dbdfc804b160c81633db0d 56.
- **title**, reference list [80121–80283]: Interagency Ecological Program: Zooplankton abundance in the Upper San Francisco Estuary from 1972–2020, an integration of 5 long-term monitoring programs. ver 3.
- **title**, reference list [102155–102317]: Interagency Ecological Program: Zooplankton abundance in the Upper San Francisco Estuary from 1972–2020, an integration of 5 long-term monitoring programs. ver 3.
- **Verdict:** 

### 166. `knb-lter-ntl.313.2` cited by `10.1002/2015wr017522`

- **Dataset:** WSC - Water surface elevation (WSE) and water table depth (WTD) from 14 points at the Wibu field site, 2012-2013 growing seasons (2015)
- **Paper:** Untangling the effects of shallow groundwater and soil texture as drivers of subfield‐scale yield variability — *Water Resources Research*, 2015, OA closed; cites 6 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 167. `knb-lter-gce.806.10` cited by `10.1073/pnas.2425501122`

- **Dataset:** Spartina alterniflora marsh vegetation data along the Georgia coast used in the Belowground Ecosystem Resiliency Model version 2.0 (2024)
- **Paper:** Early warning signs of salt marsh drowning indicated by widespread vulnerability from declining belowground plant biomass — *Proceedings of the National Academy of Sciences*, 2025, OA hybrid; cites 2 EDI dataset(s); link source references/crossref
- **Text:** europepmc, 50,553 chars
- **marker** via ref 81, body [31364–31471]: We compared modeled trends with field data at a long-term monitoring site on Sapelo Island, Georgia ([81]). ← **query candidate**
- **doi**, reference list [49375–49572]: Runion , Spartina alterniflora marsh vegetation data along the Georgia coast used in the Belowground Ecosystem Resiliency Model version 2.0 (2024) . 10.6073/pasta/4a0b715104849d98320fcc34e7cd63a4 .
- **Verdict:** 

### 168. `knb-lter-arc.1489.4` cited by `10.1007/s10021-022-00771-8`

- **Dataset:** A multi-year DAILY weather file for the Toolik Field Station at Toolik Lake, AK starting 1988 to present. (2019)
- **Paper:** From Intra-plant to Regional Scale: June Temperatures and Regional Climates Directly and Indirectly Control Betula nana Growth in Arctic Alaska — *Ecosystems*, 2022, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:link.springer.com:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s10021-022-00771-8.pdf` and re-run
- **Verdict:** 

### 169. `edi.1075.1` cited by `10.15447/sfews.2022v20iss3art2`

- **Dataset:** Fish abundance in the San Francisco Estuary (1959-2021), an integration of 9 monitoring surveys. (2022)
- **Paper:** Wakasagi in the San Francisco Bay Delta Watershed: Comparative Trends in Distribution and Life-History Traits with Native Delta Smelt — *San Francisco Estuary and Watershed Science*, 2022, OA diamond; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:escholarship.org:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.15447_sfews.2022v20iss3art2.pdf` and re-run
- **Verdict:** 

### 170. `edi.461.2` cited by `10.1002/eap.2649`

- **Dataset:** Long Term Research in Environmental Biology (LTREB): California vernal pool plant community ecology and restoration, 2000-2017 (2020)
- **Paper:** Application of modern coexistence theory to rare plant restoration provides early indication of restoration trajectories — *Ecological Applications*, 2022, OA hybrid; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** europepmc, 57,389 chars
- **author_year**, body [12625–12755]: In April, during approximate peak biomass, each year from 2000 to 2017, plant occurrence was monitored (Collinge & Faist, [2020]). ← **query candidate**
- **doi**, reference list [47177–47393]: “Long Term Research in Environmental Biology (LTREB): California Vernal Pool Plant Community Ecology and Restoration, 2000–2017 ver 2.” Environmental Data Initiative . 10.6073/pasta/1daedb3a3b601d0fd9ccb4120cfb504e .
- **Verdict:** 

### 171. `edi.591.2` cited by `10.1007/s10750-022-04886-w`

- **Dataset:** Hourly water temperature from the San Francisco Estuary, 1986 - 2019 (2020)
- **Paper:** Escape from the heat: thermal stratification in a well-mixed estuary and implications for fish species facing a changing climate — *Hydrobiologia*, 2022, OA hybrid; cites 5 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:link.springer.com:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s10750-022-04886-w.pdf` and re-run
- **Verdict:** 

### 172. `knb-lter-and.4525.9` cited by `10.1002/eap.2296`

- **Dataset:** Demonstration of Ecosystem Management Options (DEMO) Study, western Oregon and Washington (post-treatment data, 1998-2016) (2018)
- **Paper:** Level and spatial pattern of overstory retention impose trade‐offs for regenerating and retained trees — *Ecological Applications*, 2021, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_eap.2296.pdf` and re-run
- **Verdict:** 

### 173. `knb-lter-mcm.267.1` cited by `10.20944/preprints202209.0065.v1`

- **Dataset:** Soil geochemistry and microbial community data from glaciated and potential glacial refugia sites in the McMurdo Dry Valleys, Antarctica (1993-2019) (2021)
- **Paper:** Glacial Legacies: Microbial Communities of Antarctic refugia — *Preprints.org*, 2022, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.preprints.org:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.20944_preprints202209.0065.v1.pdf` and re-run
- **Verdict:** 

### 174. `edi.1016.2` cited by `10.1002/lol2.10299`

- **Dataset:** LAGOS-US RESERVOIR: Data module classifying conterminous U.S. lakes 4 hectares and larger as natural lakes or reservoirs (2022)
- **Paper:** LAGOS‐US RESERVOIR : A database classifying conterminous U.S. lakes 4 ha and larger as natural lakes or reservoir lakes — *Limnology and Oceanography Letters*, 2023, OA gold; cites 2 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.10299.pdf` and re-run
- **Verdict:** 

### 175. `knb-lter-hbr.51.13` cited by `10.1016/j.rse.2010.04.005`

- **Dataset:** Hubbard Brook Experimental Forest: Routine Seasonal Phenology Measurements, 1989 - present (2023)
- **Paper:** Land surface phenology from MODIS: Characterization of the Collection 5 global land cover dynamics product — *Remote Sensing of Environment*, 2010, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 176. `knb-lter-sev.13.270186` cited by `10.1002/ecs2.2770`

- **Dataset:** Rodent Parasite Data for the Sevilleta National Wildlife Refuge, New Mexico (1990-1998) (2016)
- **Paper:** To improve ecological understanding, collect infection data — *Ecosphere*, 2019, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.2770.pdf` and re-run
- **Verdict:** 

### 177. `knb-lter-pie.128.11` cited by `10.1016/j.envpol.2021.118657`

- **Dataset:** Aboveground biomass from control plots in a Spartina patens-dominated salt marsh at Law's Point, Rowley River, Plum Island Ecosystem LTER, MA. (2020)
- **Paper:** Inorganic and methylated mercury dynamics in estuarine water of a salt marsh in Massachusetts, USA — *Environmental Pollution*, 2021, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 178. `knb-lter-fce.1076.3` cited by `10.1007/s00267-017-0916-2`

- **Dataset:** Water Quality Data (Extensive) from the Taylor Slough, just outside Everglades National Park (FCE), from August 1998 to December 2006 (2015)
- **Paper:** Visioning the Future: Scenarios Modeling of the Florida Coastal Everglades — *Environmental Management*, 2017, OA closed; cites 9 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 179. `edi.140.1` cited by `10.15468/dl.w31yus`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 180. `knb-lter-arc.1646.9` cited by `10.5194/essd-15-2879-2023`

- **Dataset:** Toolik Inlet Discharge Data collected in summer 2006, Arctic LTER, Toolik Research Station, Alaska. (2016)
- **Paper:** GRiMeDB: the Global River Methane Database of concentrations and fluxes — *Earth system science data*, 2023, OA gold; cites 55 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 236,543 chars
- **doi**, reference list [151265–151478]: Kling, G.: Toolik Inlet discharge data collected in summer 2006, Arctic LTER, Toolik Research Station, Alaska, Environmental Data Initiative, https://doi.org/10.6073/pasta/ bd8a06d5dab8691912524db28cc24bcd, 2016n.
- **Verdict:** 

### 181. `edi.140.1` cited by `10.15468/dl.pnfodx`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2018, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 182. `edi.140.1` cited by `10.15468/dl.m92snx`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2020, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 183. `edi.140.1` cited by `10.15468/dl.nibxwn`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2020, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 184. `knb-lter-nwt.413.14` cited by `10.1080/15230430.2025.2570526`

- **Dataset:** Air temperature data for Saddle chart recorder, 1981 - 2017. (2023)
- **Paper:** Long-term data suggest a severe decline in recruitment of the American pika on Niwot Ridge, Boulder County, Colorado — *Arctic Antarctic and Alpine Research*, 2025, OA gold; cites 6 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:www.tandfonline.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1080_15230430.2025.2570526.pdf` and re-run
- **Verdict:** 

### 185. `edi.140.1` cited by `10.15468/dl.ua6vii`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 186. `knb-lter-mcr.4.35` cited by `10.1073/pnas.1812412116`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Corals, ongoing since 2005 (2018)
- **Paper:** Experimental support for alternative attractors on coral reefs — *Proceedings of the National Academy of Sciences*, 2019, OA hybrid; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 65,299 chars
- **marker** via ref 81, body [36382–36549]: Details concerning sampling protocols and the data can be viewed at mcr.lternet.edu/data . Data are reported here for lagoon reefs ([80]) and for the fore reef ([81]). ← **query candidate**
- **doi**, reference list [63819–64044]: Edmunds P Moorea Coral Reef LTER 2018 MCR LTER: Coral reef: Long-term population and community dynamics: Corals, ongoing since 2005, Environmental Data Initiative. Available at 10.6073/pasta/263faa48b520b7b2c964f158c184ef96 .
- **title**, reference list [63819–63982]: Edmunds P Moorea Coral Reef LTER 2018 MCR LTER: Coral reef: Long-term population and community dynamics: Corals, ongoing since 2005, Environmental Data Initiative.
- **Verdict:** 

### 187. `knb-lter-gce.267.34` cited by `10.1002/ecy.3278`

- **Dataset:** Fall 2005 plant monitoring survey -- biomass calculated from shoot height and flowering status of plants in permanent plots at GCE sampling sites 1-10 (2015)
- **Paper:** Variation in synchrony of production among species, sites, and intertidal zones in coastal marshes — *Ecology*, 2020, OA closed; cites 38 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 188. `edi.1387.1` cited by `10.1002/lno.12475`

- **Dataset:** Modeled maximum and mean lake depths for the contiguous United States (2023)
- **Paper:** The distribution of depth, volume, and basin shape for lakes in the conterminous United States — *Limnology and Oceanography*, 2023, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 189. `knb-lter-bes.5018.1` cited by `10.1007/s10980-024-01931-y`

- **Dataset:** A Land-use/Land Cover Classification of Baltimore City in 1953 (2022)
- **Paper:** Shaping Baltimore’s urban forests: past insights for present-day ecology — *Landscape Ecology*, 2024, OA hybrid; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s10980-024-01931-y.pdf` and re-run
- **Verdict:** 

### 190. `edi.836.1` cited by `10.1029/2022wr032522`

- **Dataset:** Water Quality Data from Bethel and Stephens Lakes, Columbia, Missouri 2017-2019 (2021)
- **Paper:** Classifying Mixing Regimes in Ponds and Shallow Lakes — *Water Resources Research*, 2022, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2022wr032522.pdf` and re-run
- **Verdict:** 

### 191. `knb-lter-bes.4000.180` cited by `10.1002/fee.2596`

- **Dataset:** BES Household Telephone Survey (2018)
- **Paper:** More green, fewer problems: landcover relates to perception of environmental problems — *Frontiers in Ecology and the Environment*, 2023, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 192. `knb-lter-bnz.501.17` cited by `10.1029/2021jg006376`

- **Dataset:** Eight Mile Lake Research Watershed, Carbon in Permafrost Experimental Heating Research (CiPEHR): Aboveground plant biomass, 2009-2017. (2018)
- **Paper:** Experimental Soil Warming and Permafrost Thaw Increase CH 4 Emissions in an Upland Tundra Ecosystem — *Journal of Geophysical Research Biogeosciences*, 2021, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.osti.gov:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2021jg006376.pdf` and re-run
- **Verdict:** 

### 193. `knb-lter-nwt.112.4` cited by `10.1007/s00027-024-01134-2`

- **Dataset:** Stream water chemistry data for Martinelli basin, 1984 - ongoing. (2021)
- **Paper:** Influence of water source on alpine stream community structure: linking morphological and metabarcoding approaches — *Aquatic Sciences*, 2024, OA green; cites 12 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:escholarship.org:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s00027-024-01134-2.pdf` and re-run
- **Verdict:** 

### 194. `knb-lter-ntl.88.28` cited by `10.1016/j.hal.2021.102100`

- **Dataset:** North Temperate Lakes LTER: Phytoplankton - Madison Lakes Area 1995 - current (2020)
- **Paper:** Development of a sub-seasonal cyanobacteria prediction model by leveraging local and global scale predictors — *Harmful Algae*, 2021, OA closed; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 195. `knb-lter-arc.1644.9` cited by `10.5194/essd-15-2879-2023`

- **Dataset:** Toolik Inlet Discharge Data collected in summer 2005, Arctic LTER, Toolik Research Station, Alaska. (2016)
- **Paper:** GRiMeDB: the Global River Methane Database of concentrations and fluxes — *Earth system science data*, 2023, OA gold; cites 55 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 236,543 chars
- **doi**, reference list [151051–151264]: Kling, G.: Toolik Inlet discharge data collected in summer 2005, Arctic LTER, Toolik Research Station, Alaska, Environmental Data Initiative, https://doi.org/10.6073/pasta/ 9dde811179666deedd0ecf911be39f65, 2016m.
- **Verdict:** 

### 196. `knb-lter-arc.10531.10` cited by `10.1002/lol2.70105`

- **Dataset:** Biogeochemistry data set for Imnavait Creek Weir on the North Slope of Alaska 2002-2022. (2023)
- **Paper:** Limno‐ STOICH : A comprehensive database linking the elemental stoichiometry of organisms with inland aquatic habitats — *Limnology and Oceanography Letters*, 2026, OA gold; cites 47 EDI dataset(s); link source references/crossref
- **Text:** pdf, 121,837 chars
- **doi**, reference list [91459–91616]: “Biogeochemistry Data Set for Imnavait Creek Weir on the North Slope of Alaska 2002 –2022.” https://doi. org/10.6073/PASTA/EB0FC1B37FF66645C62188303FA 4584F.
- **Verdict:** 

### 197. `knb-lter-arc.10488.2` cited by `10.1002/2016jg003377`

- **Dataset:** 2010 thaw depth and soil temperature in LTER moist acidic tundra experimental plots (2016)
- **Paper:** Seasonality of dissolved nitrogen from spring melt to fall freezeup in Alaskan Arctic tundra and mountain streams — *Journal of Geophysical Research Biogeosciences*, 2017, OA bronze; cites 2 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:agupubs.onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_2016jg003377.pdf` and re-run
- **Verdict:** 

### 198. `knb-lter-gce.236.20` cited by `10.1002/ecy.4136`

- **Dataset:** Mollusc population abundance monitoring: Fall 2003 mid-marsh and creekbank infaunal and epifaunal mollusc abundance based on collections from GCE marsh, monitoring sites 1-10 (2014)
- **Paper:** Diversity–stability relationships across organism groups and ecosystem types become decoupled across spatial scales — *Ecology*, 2023, OA bronze; cites 35 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 82,805 chars
- **doi**, reference list [63569–63698]: Monitoring Sites 1-10 Ver 20. ” Environmental Data Initiative. https://doi.org/10.6073/pas ta/81e9040300e43666830c20098c 551310 .
- **title**, reference list [63415–63513]: “Mollusc Population Abundance Monitoring: Fall 2003 Mid-Marsh and Creekbank Infaunal and Epifaunal
- **Verdict:** 

### 199. `knb-lter-vcr.379.1` cited by `10.1111/gcb.17081`

- **Dataset:** Coastal landcover change and the associated biomass trends in the mid-Atlantic sea-level rise hotspot (2022)
- **Paper:** Upland forest retreat lags behind sea‐level rise in the mid‐Atlantic coast — *Global Change Biology*, 2023, OA hybrid; cites 2 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_gcb.17081.pdf` and re-run
- **Verdict:** 

### 200. `knb-lter-ntl.360.1` cited by `10.1002/lno.11913`

- **Dataset:** Cascade Project at North Temperate Lakes LTER High Frequency Sonde Data from Food Web Resilience Experiment 2008 - 2011 (2018)
- **Paper:** Resilience of phytoplankton dynamics to trophic cascades and nutrient enrichment — *Limnology and Oceanography*, 2021, OA green; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lno.11913.pdf` and re-run
- **Verdict:** 

### 201. `knb-lter-cap.629.1` cited by `10.3390/data1010007`

- **Dataset:** Analysis of rooftop surface temperatures in an urban residential environment (2016)
- **Paper:** A MODIS/ASTER Airborne Simulator (MASTER) Imagery for Urban Heat Island Research — *Data*, 2016, OA gold; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.mdpi.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.3390_data1010007.pdf` and re-run
- **Verdict:** 

### 202. `knb-lter-and.4041.11` cited by `10.5194/essd-13-1843-2021`

- **Dataset:** LTER Intersite Fine Litter Decomposition Experiment (LIDET), 1990 to 2002 (2016)
- **Paper:** SoDaH: the SOils DAta Harmonization database, an open-source synthesis of soil data from research networks, version 1.0 — *Earth system science data*, 2021, OA gold; cites 2 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 57,504 chars
- **doi**, reference list [48554–48664]: Forest Science Data Bank, Corvallis, OR, https://doi.org/10.6073/pasta/f35f56bea52d78b6a1ecf1952b4889c5, 2013.
- **Verdict:** 

### 203. `edi.389.7` cited by `10.1029/2023wr036570`

- **Dataset:** Time series of high-frequency meteorological data at Falling Creek Reservoir, Virginia, USA 2015-2022 (2023)
- **Paper:** Using System‐Inspired Metrics to Improve Water Quality Prediction in Stratified Lakes — *Water Resources Research*, 2024, OA gold; cites 5 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2023wr036570.pdf` and re-run
- **Verdict:** 

### 204. `edi.140.1` cited by `10.15468/dl.ffkui8`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2020, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 205. `knb-lter-mcr.6005.2` cited by `10.1002/ecs2.70398`

- **Dataset:** MCR LTER: Coral Reef: 2018 land cover map of Moorea, French Polynesia (2025)
- **Paper:** Long‐term community dynamics are heterogeneous between fringing‐ and fore‐reef habitats on an Indo‐Pacific coral reef — *Ecosphere*, 2025, OA gold; cites 6 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.70398.pdf` and re-run
- **Verdict:** 

### 206. `knb-lter-fce.1239.1` cited by `10.1002/ecy.4427`

- **Dataset:** Decomposition rates of four litter types along coastal gradients in Everglades National Park (FCE LTER), Florida, USA: 2020-2021 (2022)
- **Paper:** Functional effects of subsidies and stressors on benthic microbial communities along freshwater to marine gradients — *Ecology*, 2024, OA hybrid; cites 6 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecy.4427.pdf` and re-run
- **Verdict:** 

### 207. `edi.176.5` cited by `10.1038/sdata.2018.226`

- **Dataset:** The European Multi Lake Survey (EMLS) dataset of physical, chemical, algal pigments and cyanotoxin parameters 2015. (2018)
- **Paper:** A European Multi Lake Survey dataset of environmental variables, phytoplankton pigments and cyanotoxins — *Scientific Data*, 2018, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 29,837 chars
- **doi**, reference list [29715–29837]: Environmental Data Initiative Mantzouki E. et al. 2018 https://doi.org/10.6073/pasta/dabc352040fa58284f78883fa9debe37
- **Verdict:** 

### 208. `knb-lter-sev.203.111849` cited by `10.1002/ecy.1446`

- **Dataset:** Larrea Seedling Monitoring Study at the Sevilleta National Wildlife Refuge, New Mexico (1999- ) (2013)
- **Paper:** Seed‐bank structure and plant‐recruitment conditions regulate the dynamics of a grassland‐shrubland Chihuahuan ecotone — *Ecology*, 2016, OA bronze; cites 1 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecy.1446.pdf` and re-run
- **Verdict:** 

### 209. `edi.494.1` cited by `10.1002/tafs.10028`

- **Dataset:** Interagency Ecological Program: Zooplankton catch and water quality data from the Sacramento River floodplain and tidal slough, collected by the Yolo Bypass Fish Monitoring Program, 1998-2018. (2020)
- **Paper:** Effects of Extreme Hydrologic Regimes on Juvenile Chinook Salmon Prey Resources and Diet Composition in a Large River Floodplain — *Transactions of the American Fisheries Society*, 2017, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:afspubs.onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_tafs.10028.pdf` and re-run
- **Verdict:** 

### 210. `knb-lter-pal.151.7` cited by `10.1002/ecs2.4417`

- **Dataset:** Sea ice duration or the time elapse between day of advance and day of retreat within a given sea ice year for the PAL LTER region West of the Antarctic Peninsula derived from passive microwave satellite, 1979 - 2021. (2022)
- **Paper:** Long‐term patterns in ecosystem phenology near Palmer Station, Antarctica, from the perspective of the Adélie penguin — *Ecosphere*, 2023, OA gold; cites 7 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf; pdf:scholar.colorado.edu:403:not-pdf; pdf:escholarship.org:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4417.pdf` and re-run
- **Verdict:** 

### 211. `knb-lter-hbr.298.3` cited by `10.1111/ele.14498`

- **Dataset:** Tree Seed Data at the Hubbard Brook Experimental Forest, 1993 - ongoing (2024)
- **Paper:** Community Synchrony in Seed Production is Associated With Trait Similarity and Climate Across North America — *Ecology Letters*, 2024, OA hybrid; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1111_ele.14498.pdf` and re-run
- **Verdict:** 

### 212. `knb-lter-hbr.325.1` cited by `10.2737/ne-rp-625`

- **Dataset:** Hubbard Brook Experimental Forest: Watershed 4 Vegetation Inventory (2022)
- **Paper:** Revegetation after strip cutting and block clearcutting in northern hardwoods: a 10-year history — *?*, 1989, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.fs.usda.gov:404:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.2737_ne-rp-625.pdf` and re-run
- **Verdict:** 

### 213. `knb-lter-knz.90.1` cited by `10.1016/j.chemgeo.2018.08.007`

- **Dataset:** AGW03 Konza Prairie Long-term High frequency groundwater level and temperature from wells on N04d (2015)
- **Paper:** Dust, impure calcite, and phytoliths: Modeled alternative sources of chemical weathering solutes in shallow groundwater — *Chemical Geology*, 2018, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 214. `edi.140.1` cited by `10.15468/dl.cs0b0p`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2019, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 215. `knb-lter-knz.188.1` cited by `10.1111/1365-2745.14456`

- **Dataset:** LPT01 Leaf physiological and structural traits of encroaching shrub species at Konza Prairie (2024)
- **Paper:** Divergent resource‐use strategies of encroaching shrubs: Can traits predict encroachment success in tallgrass prairie? — *Journal of Ecology*, 2024, OA closed; cites 3 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 216. `knb-lter-sev.204.154837` cited by `https://www.nature.com/articles/s41467-022-30037-9`

- **Dataset:** Tree Mast Production in Pinyon-Juniper-Oak Forests at the Sevilleta National Wildlife Refuge, New Mexico (2024)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 1 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 217. `knb-lter-mcr.7.28` cited by `10.1126/science.aaw1620`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Other Benthic Invertebrates, ongoing since 2005 (2015)
- **Paper:** The geography of biodiversity change in marine and terrestrial assemblages — *Science*, 2019, OA green; cites 19 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1126_science.aaw1620.pdf` and re-run
- **Verdict:** 

### 218. `knb-lter-nwt.405.3` cited by `10.5194/tc-2021-205`

- **Dataset:** Climate data for saddle data loggers (CR23X and CR1000), 2000 - ongoing, daily. (2019)
- **Paper:** Snow dune growth increases polar heat fluxes — *?*, 2021, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 38,218 chars
- **author_year**, body [6523–6676]: Outlines mark fresh deposits in snow-on-snow photos b and c. are viewable at Kochanski (2018a). Climate records are drawn from Morse and Losleben (2019). ← **query candidate**
- **author_year**, body [12703–13072]: We assume the following conditions, typical of our ﬁeld site: snow grains of diameter (0.1 ± 0.05) mm and density (800 ± 100) kg/m3; air of temperature (−10 ± 2.5)oC (Morse and Losleben, 2019) at 3500 m elevation; surface roughness lengthz0 = (0.24±0.05) mm (Gromke et al., 2011); and threshold wind velocityuc = (4.3±0.9)110 m/s from the ﬁeld results shown in Fig. 2a.
- **doi**, reference list [34609–34821]: F. and Losleben, M.: Climate data for saddle data loggers (CR23X and CR1000) 2000-ongoing, daily, Environmental Data Initiative, https://doi.org/10.6073/pasta/cf8ff4f209a889b4b20a4fb48be6f1d8, 2019.300 Perron, J.
- **Verdict:** 

### 219. `edi.140.1` cited by `10.15468/dl.05tr5e`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2020, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 220. `edi.140.1` cited by `10.15468/dl.hubmrg`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2018, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 221. `knb-lter-hbr.51.14` cited by `10.1002/lno.12741`

- **Dataset:** Hubbard Brook Experimental Forest: Routine Seasonal Phenology Measurements, 1989 - present (2023)
- **Paper:** Stream bryophytes promote “cryptic” productivity in highly oligotrophic headwaters — *Limnology and Oceanography*, 2024, OA closed; cites 8 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 222. `knb-lter-gce.444.2` cited by `10.1016/j.rse.2012.01.018`

- **Dataset:** LIDAR data of the Duplin River and Blackbeard creek salt marshes (2014)
- **Paper:** Accuracy assessment and correction of a LIDAR-derived salt marsh digital elevation model — *Remote Sensing of Environment*, 2012, OA closed; cites 6 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 223. `knb-lter-luq.178.7` cited by `10.1002/essoar.10505524.1`

- **Dataset:** Canopy Trimming Experiment Litterfall Nutrients Data (2018)
- **Paper:** Response and recovery of tropical forests after cyclone disturbance — *?*, 2021, OA gold; cites 7 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_essoar.10505524.1.pdf` and re-run
- **Verdict:** 

### 224. `knb-lter-gce.457.8` cited by `10.1002/ecs2.1487`

- **Dataset:** Fall 2013 plant monitoring survey -- biomass calculated from shoot height and flowering status of plants in permanent plots at GCE sampling sites 1-10 (2015)
- **Paper:** Disturbance in Georgia salt marshes: variation across space and time — *Ecosphere*, 2016, OA gold; cites 32 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:esajournals.onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.1487.pdf` and re-run
- **Verdict:** 

### 225. `knb-lter-knz.94.9` cited by `10.1016/j.soilbio.2023.109145`

- **Dataset:** AET01 Konza prairie grass reference evapotranspiration (2023)
- **Paper:** Thirty years of increased precipitation modifies soil organic matter fractions but not bulk soil carbon and nitrogen in a mesic grassland — *Soil Biology and Biochemistry*, 2023, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 226. `edi.1381.1` cited by `https://ucowr.org/wp-content/uploads/2023/04/177_leung-and-swanner.pdf`

- **Dataset:** Assessment of dissolved iron in Iowa lakes (2023)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 2 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 227. `edi.389.6` cited by `10.1016/j.watres.2023.120084`

- **Dataset:** Time series of high-frequency meteorological data at Falling Creek Reservoir, Virginia, USA 2015-2021 (2022)
- **Paper:** High-frequency sensor data capture short-term variability in Fe and Mn concentrations due to hypolimnetic oxygenation and seasonal dynamics in a drinking water reservoir — *Water Research*, 2023, OA closed; cites 5 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 228. `knb-lter-sbc.13.24` cited by `10.6084/m9.figshare.13543735`

- **Dataset:** SBC LTER: Reef: Bottom Temperature: Continuous water temperature, ongoing since 2000 (2020)
- **Paper:** Additional file 4 of Gene expression patterns of red sea urchins (Mesocentrotus franciscanus) exposed to different combinations of temperature and pCO2 during early development — *Figshare*, 2021, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.6084_m9.figshare.13543735.pdf` and re-run
- **Verdict:** 

### 229. `knb-lter-hbr.13.17` cited by `10.1139/cjfr-2017-0233`

- **Dataset:** Hubbard Brook Experimental Forest: Daily Precipitation Rain Gage Measurements, 1956 - present (2021)
- **Paper:** Long-term decline of sugar maple following forest harvest, Hubbard Brook Experimental Forest, New Hampshire — *Canadian Journal of Forest Research*, 2017, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 61,691 chars
- **Mention:** none found
- **Verdict:** 

### 230. `edi.1106.4` cited by `10.1002/ecs2.4628`

- **Dataset:** Macrosystems EDDIE Module 8: Using Ecological Forecasts to Guide Decision-Making (Instructor Materials) (2023)
- **Paper:** Embedding communication concepts in forecasting training increases students' understanding of ecological uncertainty — *Ecosphere*, 2023, OA gold; cites 2 EDI dataset(s); link source references/crossref
- **Text:** pdf, 105,778 chars
- **doi**, reference list [104382–104485]: Ver 4.” Environmental Data Initiative. https://doi.org/10.6073/ pasta/8bf4a076433f0e9f74f1d764d5bd4c3f.
- **title**, reference list [104264–104323]: Carey. 2023. “Macrosystems EDDIE Module 8: Using Ecological
- **Verdict:** 

### 231. `knb-lter-ntl.31.30` cited by `10.1101/2022.08.04.502871`

- **Dataset:** North Temperate Lakes LTER: Secchi Disk Depth; Other Auxiliary Base Crew Sample Data 1981 - current (2021)
- **Paper:** Species invasions shift microbial phenology in a two-decade freshwater time series — *bioRxiv (Cold Spring Harbor Laboratory)*, 2022, OA green; cites 12 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 63,362 chars
- **package_id**, body [30455–30852]: We combined our measurements with additional water temperature, dissolved oxygen, water clarity, and ice cover datasets made available by the North Temperate Lakes Long-Term Ecological Research program (NTL-LTER) under EDI identifiers 335 knb-lter-ntl.29.29 (41), knb-lter-ntl.130.29 (42), knb-lter-ntl.335.1 (43), knb-lter-ntl.400.2 (44), knb-lter-ntl.31.30 (45), and knb-lter-ntl.33.35 (46). ← **query candidate**
- **package_id**, reference list [50064–50234]: Stanley, North Temperate Lakes LTER: Secchi Disk Depth; Other Auxiliary Base Crew Sample Data 1981 - current. Environmental Data Initiative knb-lter-ntl.31 (2021). 46.
- **title**, reference list [50064–50174]: Stanley, North Temperate Lakes LTER: Secchi Disk Depth; Other Auxiliary Base Crew Sample Data 1981 - current.
- **Verdict:** 

### 232. `knb-lter-bnz.671.3` cited by `10.1007/s10021-019-00384-8`

- **Dataset:** Murphy Dome: Moss (Hylocomium splendens) biomass results from a moss transplant and leaf litter manipulation experiment in three pairs of adjacent black spruce and birchs stands. (2017)
- **Paper:** Broadleaf Litter Controls Feather Moss Growth in Black Spruce and Birch Forests of Interior Alaska — *Ecosystems*, 2019, OA closed; cites 4 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 233. `knb-lter-arc.10123.6` cited by `10.5194/essd-2023-222`

- **Dataset:** Anatuvuk River fire scar thaw depth measurements during the 2008 to 2014 growing season (2016)
- **Paper:** A synthesized field survey database of vegetation and active layer properties for the Alaskan tundra (1972–2020) — *?*, 2023, OA gold; cites 8 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 69,899 chars
- **doi**, reference list [52834–52956]: Environmental Data Initiative. https://doi.org/10.6073/pasta/93121fc86e6fbcf88de4a9350609aed6 Rocha_2020 Rocha, A. 2020.
- **Verdict:** 

### 234. `knb-lter-ntl.336.10` cited by `10.1002/lol2.10045`

- **Dataset:** Chloride and sulfate concentrations in 1918 Marsh, Madison, WI, 2012-2024 (2025)
- **Paper:** Ice formation and the risk of chloride toxicity in shallow wetlands and lakes — *Limnology and Oceanography Letters*, 2017, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:aslopubs.onlinelibrary.wiley.com:403:not-pdf; pdf:digitalcommons.usf.edu:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.10045.pdf` and re-run
- **Verdict:** 

### 235. `edi.140.1` cited by `10.15468/dl.orzgxu`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2020, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 236. `knb-lter-hbr.14.18` cited by `10.1029/2026jg009756`

- **Dataset:** Hubbard Brook Experimental Forest: Total Daily Precipitation by Watershed, 1956 - present (2024)
- **Paper:** Long‐Term Change in the Concentration‐Discharge Relationship Suggests Controls on Watershed Exports of Dissolved Organic Carbon From Forested Headwater Streams — *Journal of Geophysical Research Biogeosciences*, 2026, OA hybrid; cites 7 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2026jg009756.pdf` and re-run
- **Verdict:** 

### 237. `knb-lter-arc.10282.3` cited by `10.1080/20442041.2025.2461419`

- **Dataset:** Time-series of 5 minute water temperatures averages from Lake E5 near Toolik Field Station, Alaska Summer 2004. (2016)
- **Paper:** Prediction of future Alaskan lake methane emissions using a small-lake model coupled to a regional climate model — *Inland Waters*, 2025, OA closed; cites 17 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 238. `knb-lter-nes.6.3` cited by `10.5194/bg-21-1235-2024`

- **Dataset:** Oxygen-argon dissolved gas ratios using Equilibrator Inlet Mass Spectrometry (EIMS) and triple oxygen isotopes (TOI) from NES-LTER Transect cruises, ongoing since 2018 (2024)
- **Paper:** Unusual Hemiaulus bloom influences ocean productivity in Northeastern US Shelf waters — *Biogeosciences*, 2024, OA gold; cites 10 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 111,266 chars
- **package_id**, body [77560–77748]: In particular, the raw gas tracer data used for calculating NCP and GOP are available at https://portal.edirepository.org/nis/mapbrowse? packageid=knb-lter-nes.6.3 (Stanley et al., 2024a). ← **query candidate**
- **title**, reference list [105964–106222]: O.: Oxygen-argon dissolved gas ratios using Equilibrator Inlet Mass Spectrometry (EIMS) and triple oxygen isotopes (TOI) from NES-LTER Transect cruises, ongoing since 2018, Environmental Data Initiative [data set], https://doi.org/10.6073/pasta/97962, 2024a.
- **Verdict:** 

### 239. `edi.563.4` cited by `10.1029/2023wr036513`

- **Dataset:** Marcell Experimental Forest daily precipitation, 1961 - ongoing (2022)
- **Paper:** Methylmercury Export From a Headwater Peatland Catchment Decreased With Cleaner Emissions Despite Opposing Effect of Climate Warming — *Water Resources Research*, 2024, OA gold; cites 4 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2023wr036513.pdf` and re-run
- **Verdict:** 

### 240. `knb-lter-bnz.738.2` cited by `10.1371/journal.pone.0235932`

- **Dataset:** Outplanted seedling survival, height and biomass at Finger Mountain and the Anaktuvuk River Fire. (2020)
- **Paper:** Limited overall impacts of ectomycorrhizal inoculation on recruitment of boreal trees into Arctic tundra following wildfire belie species-specific responses — *PLoS ONE*, 2020, OA gold; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 69,498 chars
- **Mention:** none found
- **Verdict:** 

### 241. `knb-lter-hbr.428.1` cited by `10.1111/gcb.70250`

- **Dataset:** Hubbard Brook Experimental Forest: Litter and soil radiocarbon and selective metal measurements from Bear Brook, 1998–2023 (2025)
- **Paper:** Temporal and Spatial Dynamics of Soil Carbon Cycling and Its Response to Environmental Change in a Northern Hardwood Forest — *Global Change Biology*, 2025, OA hybrid; cites 7 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** europepmc, 93,879 chars
- **doi**, reference list [51297–51648]: Data Availability Statement The data and R code that support the findings of this study are openly available in Zenodo at https://doi.org/10.5281/zenodo.15270746 and Github at https://github.com/SophievF/HubbardBrook_Soil (Dataset 1) and the Environmental Data Initiative at https://doi.org/10.6073/pasta/2455ef85807d390f2b95ec277c6a4af7 (Dataset 2).
- **doi**, reference list [68013–68254]: “Hubbard Brook Experimental Forest: Litter and Soil Radiocarbon and Selective Metal Measurements From Bear Brook, 1998–2023 (Version 2) [Dataset].” Environmental Data Initiative. 10.6073/pasta/2455ef85807d390f2b95ec277c6a4af7. von Fromm, S.
- **doi**, reference list [75696–76047]: Data Availability Statement The data and R code that support the findings of this study are openly available in Zenodo at https://doi.org/10.5281/zenodo.15270746 and Github at https://github.com/SophievF/HubbardBrook_Soil (Dataset 1) and the Environmental Data Initiative at https://doi.org/10.6073/pasta/2455ef85807d390f2b95ec277c6a4af7 (Dataset 2).
- **title**, reference list [92400–92641]: “Hubbard Brook Experimental Forest: Litter and Soil Radiocarbon and Selective Metal Measurements From Bear Brook, 1998–2023 (Version 2) [Dataset].” Environmental Data Initiative. 10.6073/pasta/2455ef85807d390f2b95ec277c6a4af7. von Fromm, S.
- **Verdict:** 

### 242. `edi.552.1` cited by `10.1038/s41597-021-00983-y`

- **Dataset:** Weekly and high frequency temperature profile data and Secchi depth, Mohonk Lake, NY, USA, 1985 to 2017 (2020)
- **Paper:** Global data set of long-term summertime vertical temperature profiles in 153 lakes — *Scientific Data*, 2021, OA gold; cites 7 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 53,132 chars
- **marker** via ref 30, body [17628–17831]: Temperature measurements were measured manually in 1 m increments using Digi-sense Economical Thermistor 400 series (Model #93210-00). Additional weekly temperature profiles are publicly available [30] . ← **query candidate**
- **doi**, reference list [50048–50248]: Mohonk P 2020 Weekly and high frequency temperature profile data and Secchi depth, Mohonk Lake, NY, USA, 1985 to 2017 Environmental Data Initiative 10.6073/pasta/7b67399344129afc63cd57e99e778160 31.
- **Verdict:** 

### 243. `knb-lter-nwt.96.14` cited by `10.5194/hess-23-3765-2019`

- **Dataset:** Snow water equivalent data for Niwot Ridge and Green Lakes Valley, 1993 - ongoing. (2018)
- **Paper:** The sensitivity of modeled snow accumulation and melt to precipitation phase methods across a climatic gradient — *Hydrology and earth system sciences*, 2019, OA gold; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 102,944 chars
- **doi**, reference list [72210–72829]: – Southern Sierra CZO: http://criticalzone.org/sierra/data/ dataset/2529/ (last access: 9 September 2019, Husaker, 2011a) and http://criticalzone.org/sierra/data/dataset/2406/ (last access: 9 September 2019, Husaker, 2011b), – Johnston Draw (Reynolds Creek CZO): https://doi.org/10.15482/USDA.ADC/1402076 (Godsey et al., 2016, 2018), – Yosemite Dana Meadows: http://hdl.handle.net/1773/35957 (Lundquist et al., 2016), – Niwot Ridge LTER: https://doi.org/10.6073/pasta/ 1538ccf520d89c7a11c2c489d973b232 (Jennings et al., 2018a, c) and https://doi.org/10.6073/pasta/ f62b0a3741737c871958cf7e63c089e0 (W
- **doi**, reference list [101429–101626]: Williams, M.: Snow water equivalent data for Niwot Ridge and Green Lakes Valley, 1993–ongoing, Environmental Data Initiative, https://doi.org/10.6073/pasta/ f62b0a3741737c871958cf7e63c089e0, 2016a.
- **Verdict:** 

### 244. `knb-lter-sbc.6003.5` cited by `10.5194/essd-16-219-2024`

- **Dataset:** SBC LTER: Ocean: Time-series: Mid-water SeaFET pH and CO2 system chemistry with surface and bottom Dissolved Oxygen at Mohawk Reef(MKO), 2012 - 2017 (2020)
- **Paper:** A high-resolution synthesis dataset for multistressor analyses along the US West Coast — *Earth system science data*, 2024, OA gold; cites 5 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 125,504 chars
- **doi**, reference list [115496–115823]: Santa Barbara Coastal LTER, Hofmann, G., and Washburn, L.: SBC LTER: Ocean: Time-series: Mid-water SeaFET pH and CO 2 system chemistry with surface and bottom Dissolved Oxygen at Mohawk Reef(MKO), 2012– 2017 ver 5, Environmental Data Initiative [data set], https://doi.org/10.6073/pasta/23b8070eb65bae7aedc82fae8ee38b9f, 2020b.
- **Verdict:** 

### 245. `knb-lter-vcr.268.6` cited by `10.1038/s41598-020-64094-1`

- **Dataset:** Carbon and Nitrogen in Seagrass Tissue from Virginia Coastal Bays, 2010-2021 (2022)
- **Paper:** The greenhouse gas offset potential from seagrass restoration — *Scientific Reports*, 2020, OA gold; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 70,157 chars
- **generic**, reference list [68118–68208]: Environmental Data Initiative. 10.6073/pasta/09a0ce35bb3fc72113b5a16ad5b0d6bd (2017). 77.
- **generic**, reference list [68305–68395]: Environmental Data Initiative. 10.6073/pasta/b4d1f74041d329386591a32e9ea202b2 (2017). 78.
- **generic**, reference list [68876–68966]: Environmental Data Initiative. 10.6073/pasta/5a6ea442cf59cabb3112bb634a968ae5 (2017). 82.
- **Verdict:** 

### 246. `knb-lter-gce.94.43` cited by `10.1007/s10021-013-9732-6`

- **Dataset:** Fall 2002 plant monitoring survey -- biomass calculated from shoot height and flowering status of plants in permanent plots at GCE sampling sites 1-10 (2015)
- **Paper:** Climate Drivers of Spartina alterniflora Saltmarsh Production in Georgia, USA — *Ecosystems*, 2013, OA closed; cites 15 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 247. `knb-lter-nwt.16.6` cited by `10.1029/2023jg007664`

- **Dataset:** Aboveground net primary productivity data for Saddle grid, 1992 - ongoing. (2022)
- **Paper:** Topographic Heterogeneity and Aspect Moderate Exposure to Climate Change Across an Alpine Tundra Hillslope — *Journal of Geophysical Research Biogeosciences*, 2023, OA closed; cites 5 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 248. `edi.854.1` cited by `https://www.proquest.com/docview/2919337560/abstract/651470425ebc48f4pq/1`

- **Dataset:** LAGOS-US LOCUS v1.0: Data module of location, identifiers, and physical characteristics of lakes and their watersheds in the conterminous U.S. (2021)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 2 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 249. `knb-lter-mcm.62.10` cited by `10.1002/lol2.10226`

- **Dataset:** McMurdo Dry Valleys Limnological Chemistry, Ion Concentrations and Silicon (2016)
- **Paper:** Barotropic seiches in a perennially ice‐covered lake, East Antarctica — *Limnology and Oceanography Letters*, 2021, OA gold; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lol2.10226.pdf` and re-run
- **Verdict:** 

### 250. `edi.1710.1` cited by `10.3390/agronomy15020437`

- **Dataset:** Grass Yield Compilation from University of Wisconsin Extension Grass Variety Trials (1983-2016) (2024)
- **Paper:** Simulating Pasture Yield Under Alternative Environments and Grazing Management in Wisconsin, USA — *Agronomy*, 2025, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.mdpi.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.3390_agronomy15020437.pdf` and re-run
- **Verdict:** 

### 251. `edi.2373.1` cited by `10.1007/s10021-026-01084-w`

- **Dataset:** Geochemical analysis of Fraxinus americana and Acer saccharum wood after four years of decomposition in a northern temperate deciduous forest, Corinth, VT USA, 2024 (2026)
- **Paper:** Fungal Community Composition Better Explains Variation in Wood Decomposition than Fungal Biomass in a Northern Temperate Deciduous Forest — *Ecosystems*, 2026, OA hybrid; cites 1 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:link.springer.com:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s10021-026-01084-w.pdf` and re-run
- **Verdict:** 

### 252. `edi.455.6` cited by `10.1029/2022jg007071`

- **Dataset:** Time series of total and soluble iron and manganese concentrations from Falling Creek Reservoir and Beaverdam Reservoir in southwestern Virginia, USA from 2014 through 2021 (2022)
- **Paper:** Effects of Hypoxia on Coupled Carbon and Iron Cycling Differ Between Weekly and Multiannual Timescales in Two Freshwater Reservoirs — *Journal of Geophysical Research Biogeosciences*, 2023, OA hybrid; cites 8 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2022jg007071.pdf` and re-run
- **Verdict:** 

### 253. `knb-lter-sbc.17.28` cited by `10.1126/science.aaw1620`

- **Dataset:** SBC LTER: Reef: Kelp Forest Community Dynamics: Fish abundance (2014)
- **Paper:** The geography of biodiversity change in marine and terrestrial assemblages — *Science*, 2019, OA green; cites 19 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1126_science.aaw1620.pdf` and re-run
- **Verdict:** 

### 254. `edi.1176.1` cited by `10.1002/ecs2.4256`

- **Dataset:** Surveys of coastal foredune topography and vegetation abundance, U.S. North Carolina Outer Banks, 2016-2018 (2022)
- **Paper:** Sand supply and dune grass species density affect foredune shape along the US Central Atlantic Coast — *Ecosphere*, 2022, OA gold; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4256.pdf` and re-run
- **Verdict:** 

### 255. `knb-lter-bnz.679.2` cited by `10.1002/eap.1636`

- **Dataset:** Interior Alaska managed sites:vegetation community composition and ground cover measured one time in either summer 2012 or 2013 (2017)
- **Paper:** Fuel‐reduction management alters plant composition, carbon and nitrogen pools, and soil thaw in Alaskan boreal forest — *Ecological Applications*, 2017, OA closed; cites 6 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 256. `edi.824.1` cited by `10.1371/journal.pone.0262621`

- **Dataset:** Locations of rainforest transformation plots on Palmyra Atoll (2022)
- **Paper:** Transforming Palmyra Atoll to native-tree dominance will increase net carbon storage and reduce dissolved organic carbon reef runoff — *PLoS ONE*, 2022, OA gold; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 81,646 chars
- **doi**, reference list [50505–50894]: Palmyra Atoll dissolved organic carbon sampling locations and values: doi: 10.6073/pasta/1a257081daf08adb5eb665a192cd370a ; Locations of rainforest transformation plots on Palmyra Atoll: doi: 10.6073/pasta/71aaeac403060543f85ca1452665b56e ; Palmyra Atoll soil and/or wood density sampling locations used in the carbon storage analysis: doi: 10.6073/pasta/d30d7d79c4357bf35973b69932151344 .
- **Verdict:** 

### 257. `knb-lter-hbr.8.15` cited by `10.1093/biosci/biz162`

- **Dataset:** Hubbard Brook Experimental Forest: Chemistry of Streamwater – Monthly Volume Weighted Concentrations, Watershed 6, 1963 - present (2019)
- **Paper:** Long-Term Ecological Research and Evolving Frameworks of Disturbance Ecology — *BioScience*, 2019, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 258. `edi.396.1` cited by `10.1038/s43247-023-00958-4`

- **Dataset:** A monthly shortwave radiative forcing kernel for surface albedo change using CERES satellite data (2019)
- **Paper:** Joint optimization of land carbon uptake and albedo can help achieve moderate instantaneous and long-term cooling effects — *Communications Earth & Environment*, 2023, OA gold; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** europepmc, 83,093 chars
- **doi**, reference list [48591–48678]: CACK 1.0 radiative kernels [87] : 10.6073/pasta/d77b84b11be99ed4d5376d77fe0043d8 [94] .
- **doi**, reference list [64917–65079]: A monthly shortwave radiative forcing kernel for surface albedo change using CERES satellite data , <10.6073/pasta/d77b84b11be99ed4d5376d77fe0043d8> (2019). 95.
- **doi**, reference list [66355–66442]: CACK 1.0 radiative kernels [87] : 10.6073/pasta/d77b84b11be99ed4d5376d77fe0043d8 [94] .
- **title**, reference list [82315–82477]: A monthly shortwave radiative forcing kernel for surface albedo change using CERES satellite data , <10.6073/pasta/d77b84b11be99ed4d5376d77fe0043d8> (2019). 95.
- **Verdict:** 

### 259. `knb-lter-arc.10201.5` cited by `10.1038/s41597-024-03139-w`

- **Dataset:** Above ground plant and below ground stem biomass of samples from the severely burned site of the Anaktuvuk River fire, Alaska (2020)
- **Paper:** The Arctic Plant Aboveground Biomass Synthesis Dataset — *Scientific Data*, 2024, OA gold; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 82,053 chars
- **marker** via ref 92, body [11732–11830]: [91] USA 68.95 −150.21 19 2011 Bret-Harte, et al . [92] USA 69.00 −150.29 19 2011 Greaves, et al . ← **query candidate**
- **title**, reference list [57177–57309]: Above ground plant and below ground stem biomass of samples from the severely burned site of the Anaktuvuk River fire, Alaska ver 5.
- **title**, reference list [60932–61064]: Above ground plant and below ground stem biomass of samples from the severely burned site of the Anaktuvuk River fire, Alaska ver 5.
- **title**, reference list [80241–80373]: Above ground plant and below ground stem biomass of samples from the severely burned site of the Anaktuvuk River fire, Alaska ver 5.
- **Verdict:** 

### 260. `knb-lter-knz.5.9` cited by `10.1098/rsbl.2021.0510`

- **Dataset:** APT02 Monthly temperature and precipitation records from Manhattan, KS (2019)
- **Paper:** How and why grasshopper community maturation rates are slowing on a North American tall grass prairie — *Biology Letters*, 2022, OA green; cites 4 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (europepmc:PMC8790374:404)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1098_rsbl.2021.0510.pdf` and re-run
- **Verdict:** 

### 261. `knb-lter-vcr.389.2` cited by `10.1002/lno.12608`

- **Dataset:** Seagrass shoot density and benthic chlorophyll density from the Seagrass Recovery Experiment, South Bay, VA 2020-2022 (2023)
- **Paper:** Seagrass ecosystem recovery: Experimental removal and synthesis of disturbance studies — *Limnology and Oceanography*, 2024, OA hybrid; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lno.12608.pdf` and re-run
- **Verdict:** 

### 262. `knb-lter-pal.42.8` cited by `10.1016/j.rse.2022.113415`

- **Dataset:** Photosynthetic pigments of water column samples and analyzed with High Performance Liquid Chromatography (HPLC), collected aboard Palmer LTER annual cruises off the coast of the Western Antarctica Peninsula, 1991 - 2016. (2018)
- **Paper:** Coupling ecological concepts with an ocean-colour model: Phytoplankton size structure — *Remote Sensing of Environment*, 2022, OA hybrid; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.sciencedirect.com:403:not-pdf; pdf:epic.awi.de:404:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1016_j.rse.2022.113415.pdf` and re-run
- **Verdict:** 

### 263. `knb-lter-hbr.13.23` cited by `10.1007/s11270-005-2831-z`

- **Dataset:** Hubbard Brook Experimental Forest: Daily Precipitation Rain Gage Measurements, 1956 - present (2025)
- **Paper:** Long-Term Nitrate Export Pattern from Hubbard Brook Watershed 6 Driven by Climatic Variation — *Water Air & Soil Pollution*, 2005, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 264. `knb-lter-fce.1077.3` cited by `10.1007/s00267-017-0916-2`

- **Dataset:** Water Quality Data (Grab Samples) from the Taylor Slough, just outside Everglades National Park (FCE), for August 1998 to November 2006 (2015)
- **Paper:** Visioning the Future: Scenarios Modeling of the Florida Coastal Everglades — *Environmental Management*, 2017, OA closed; cites 9 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 265. `knb-lter-nwt.34.13` cited by `10.1029/2023jg007664`

- **Dataset:** Snow depth data for saddle snowfence, 1992 - ongoing. (2022)
- **Paper:** Topographic Heterogeneity and Aspect Moderate Exposure to Climate Change Across an Alpine Tundra Hillslope — *Journal of Geophysical Research Biogeosciences*, 2023, OA closed; cites 5 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 266. `edi.1597.2` cited by `10.1371/journal.pclm.0000517`

- **Dataset:** Temperature logger deployment methods and irradiance-biased temperature data, King Abdullah University of Science and Technology, Red Sea, 2023. (2024)
- **Paper:** Widespread inconsistency in logger deployment methods in coral reef studies may bias perceptions of thermal regimes — *PLOS Climate*, 2024, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 50,647 chars
- **doi**, body [3907–4051]: are available in the Environm ental Data Initiative data repository (DOI: https:// doi.org/10.6073 / pasta/2d529 777840c0c7c a2ff7228b0 61c9e2). ← **query candidate**
- **Verdict:** 

### 267. `edi.1599.1` cited by `10.1002/lno.12666`

- **Dataset:** Metabolism estimates from dissolved oxygen and inorganic carbon in the Upper Clark Fork River, MT, USA. (2024)
- **Paper:** Divergent metabolism estimates from dissolved oxygen and inorganic carbon: Implications for river carbon cycling — *Limnology and Oceanography*, 2024, OA hybrid; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_lno.12666.pdf` and re-run
- **Verdict:** 

### 268. `edi.1057.1` cited by `10.1007/s10750-022-04886-w`

- **Dataset:** Surface and bottom hourly water temperature from the San Francisco Estuary, 2012-2019 (2021)
- **Paper:** Escape from the heat: thermal stratification in a well-mixed estuary and implications for fish species facing a changing climate — *Hydrobiologia*, 2022, OA hybrid; cites 5 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:link.springer.com:200:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1007_s10750-022-04886-w.pdf` and re-run
- **Verdict:** 

### 269. `edi.140.1` cited by `10.15468/dl.twrdk2`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2020, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 270. `knb-lter-sbc.19.20` cited by `https://www.proquest.com/docview/1840890560`

- **Dataset:** SBC LTER: Reef: Kelp Forest Community Dynamics: Invertebrate and algal density (2014)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 3 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 271. `knb-lter-vcr.210.10` cited by `10.1029/2022jf006703`

- **Dataset:** Integrated Topography and Bathymetry for the Eastern Shore of Virginia (2018)
- **Paper:** Vegetation Reconfigures Barrier Coasts and Affects Tidal Basin Infilling Under Sea Level Rise — *Journal of Geophysical Research Earth Surface*, 2023, OA hybrid; cites 1 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2022jf006703.pdf` and re-run
- **Verdict:** 

### 272. `edi.200.11` cited by `10.1111/gcb.16228`

- **Dataset:** Time series of high-frequency profiles of depth, temperature, dissolved oxygen, conductivity, specific conductivity, chlorophyll a, turbidity, pH, oxidation-reduction potential, photosynthetic active radiation, and descent rate for Beaverdam Reservoir, Carvins Cove Reservoir, Falling Creek Reservoir, Gatewood Reservoir, and Spring Hollow Reservoir in Southwestern Virginia, USA 2013-2020 (2021)
- **Paper:** Anoxia decreases the magnitude of the carbon, nitrogen, and phosphorus sink in freshwaters — *Global Change Biology*, 2022, OA hybrid; cites 7 EDI dataset(s); link source references/crossref
- **Text:** europepmc, 96,436 chars
- **doi**, reference list [75850–75952]: Environmental Data Initiative Repository . 10.6073/pasta/5448f9d415fd09e0090a46b9d4020ccc Carey , C.
- **title**, reference list [75450–75849]: Time series of high‐frequency profiles of depth, temperature, dissolved oxygen, conductivity, specific conductivity, chlorophyll a, turbidity, pH, oxidation‐reduction potential, photosynthetic active radiation, and descent rate for Beaverdam Reservoir, Carvins Cove Reservoir, Falling Creek Reservoir, Gatewood Reservoir, and Spring Hollow Reservoir in southwestern Virginia, USA 2013–2020, ver 11 .
- **Verdict:** 

### 273. `edi.498.1` cited by `10.1002/ecs2.4357`

- **Dataset:** High-frequency temperature data from four near-shore sites, Lake Sunapee, NH, USA, 2006-2018 (2020)
- **Paper:** lakeCoSTR : A tool to facilitate use of Landsat Collection 2 to estimate lake surface water temperatures — *Ecosphere*, 2023, OA gold; cites 5 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4357.pdf` and re-run
- **Verdict:** 

### 274. `knb-lter-nwk.3.10` cited by `10.1016/j.ecoinf.2016.08.001`

- **Dataset:** Congruence checks for EML-described datasets in the Long Term Ecological Research (LTER) Network, Checks described as of 2015 (2016)
- **Paper:** Ensuring the quality of data packages in the LTER network data management system — *Ecological Informatics*, 2016, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 275. `knb-lter-mcr.8.28` cited by `10.1016/j.marenvres.2018.08.001`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Benthic Algae and Other Community Components, ongoing since 2005 (2015)
- **Paper:** Epibionts on Turbinaria ornata, a secondary foundational macroalga on coral reefs, provide diverse trophic support to fishes — *Marine Environmental Research*, 2018, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 276. `knb-lter-bnz.654.4` cited by `10.1038/s41561-019-0387-6`

- **Dataset:** Eight Mile Lake Research Watershed, Carbon in Permafrost Experimental Heating Research (CiPEHR): nuclear magnetic resonance spectra of soils, 2009 and 2013 (2017)
- **Paper:** Direct observation of permafrost degradation and rapid soil carbon loss in tundra — *Nature Geoscience*, 2019, OA green; cites 3 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 44,240 chars
- **doi**, reference list [39177–39532]: Ecological Research (LTER) Network Information System Data Portal at https://portal.lternet.edu/nis/home.jsp (https://doi.org/10.6073/pasta/894ec9847bc365347775d3 aaba44a50210.6073/pasta/894ec9847bc365347775d3aaba44a502, https://doi.org/10.6073/pasta/ f502d8fe1a2e1d6c6b035c198af04f3e and https://doi.org/10.6073/pasta/b559d2650efe99ccabb2 a58d9d8819ab).
- **Verdict:** 

### 277. `knb-lter-mcr.6001.4` cited by `https://escholarship.org/uc/item/9zw1t662`

- **Dataset:** MCR LTER: Reference: Fish Taxonomy, Trophic Groups and Morphometry (2014)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 2 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 278. `knb-lter-vcr.25.36` cited by `https://scholarscompass.vcu.edu/etd/6703`

- **Dataset:** Hourly Meteorological Data for the Virginia Coast Reserve LTER 1989-present (2018)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 1 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 279. `knb-lter-mcr.2002.4` cited by `10.1016/j.jembe.2007.05.007`

- **Dataset:** MCR LTER: Coral Reef: Growth and scaling of photosynthetic energy intake in Fungia concinna: Elahi &amp; Edmunds 2007 JEMBE (2019)
- **Paper:** Determinate growth and the scaling of photosynthetic energy intake in the solitary coral Fungia concinna (Verrill) — *Journal of Experimental Marine Biology and Ecology*, 2007, OA bronze; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.sciencedirect.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1016_j.jembe.2007.05.007.pdf` and re-run
- **Verdict:** 

### 280. `knb-lter-mcr.8.36` cited by `10.3354/meps14712`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Benthic Algae and Other Community Components, ongoing since 2005 (2023)
- **Paper:** Coral performance is comparable when transplanted to disparate reef sites despite divergent histories of reef decline and recovery — *Marine Ecology Progress Series*, 2024, OA closed; cites 2 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 281. `knb-lter-gce.422.6` cited by `10.5670/oceanog.2013.44`

- **Dataset:** Climate data from the SINERR/GCE/UGAMI weather station at Marsh Landing on Sapelo Island, Georgia, from 01-Jan-2010 to 31-Dec-2010 (2015)
- **Paper:** The Dynamical Response of Salinity to Freshwater Discharge and Wind Forcing in Adjacent Estuaries on the Georgia Coast — *Oceanography*, 2013, OA gold; cites 48 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 32,888 chars
- **Mention:** none found
- **Verdict:** 

### 282. `knb-lter-hfr.4.28` cited by `10.1029/2018jg004791`

- **Dataset:** Canopy-Atmosphere Exchange of Carbon, Water and Energy at Harvard Forest EMS Tower since 1991 (2018)
- **Paper:** Listening to the Forest: An Artificial Neural Network‐Based Model of Carbon Uptake at Harvard Forest — *Journal of Geophysical Research Biogeosciences*, 2019, OA hybrid; cites 3 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2018jg004791.pdf` and re-run
- **Verdict:** 

### 283. `edi.6.1` cited by `https://espis.boem.gov/final%20reports/boem_2019-064.pdf`

- **Dataset:** Santa Barbara Channel Marine BON: Integrated quad and swath cover (2017)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 4 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 284. `knb-lter-mcr.5028.10` cited by `10.1002/ecy.2511`

- **Dataset:** MCR LTER: Coral Reef: Density-dependence data for Edmunds, et al., Ecology 2018 (2018)
- **Paper:** Density‐dependence mediates coral assemblage structure — *Ecology*, 2018, OA closed; cites 2 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 285. `knb-lter-gce.605.14` cited by `10.1002/ecs2.4821`

- **Dataset:** Long-term Mollusc Population Abundance and Size Data from the Georgia Coastal Ecosystems LTER Fall Marsh Monitoring Program (2022)
- **Paper:** The resistance of Georgia coastal marshes to hurricanes — *Ecosphere*, 2024, OA gold; cites 6 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4821.pdf` and re-run
- **Verdict:** 

### 286. `edi.642.2` cited by `10.1007/s10530-022-02750-5`

- **Dataset:** Invasive buffel grass (Cenchrus ciliaris) increases water stress and reduces growth of native foothills palo verde (Parkinsonia microphylla) seedlings in pot experiments (2020)
- **Paper:** Invasive buffel grass (Cenchrus ciliaris) increases water stress and reduces success of native perennial seedlings in southeastern Arizona — *Biological Invasions*, 2022, OA closed; cites 2 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 287. `knb-lter-ntl.88.30` cited by `10.1038/s41564-024-01876-7`

- **Dataset:** North Temperate Lakes LTER: Phytoplankton - Madison Lakes Area 1995 - current (2022)
- **Paper:** Unravelling viral ecology and evolution over 20 years in a freshwater lake — *Nature Microbiology*, 2025, OA closed; cites 12 EDI dataset(s); link source references/crossref
- **Text:** closed (pdf:www.nature.com:200:not-pdf)
- **Verdict:** 

### 288. `knb-lter-knz.4.19` cited by `https://www.kgs.ku.edu/publications/ofr/2024/ofr2024-6.pdf`

- **Dataset:** APT01 Daily precipitation amounts measured at multiple sites across konza prairie (2023)
- **Paper:** (title unknown) — *?*, ?, OA ?; cites 3 EDI dataset(s); link source is-cited-by/datacite-url
- **Text:** non-doi (no open location)
- **Verdict:** 

### 289. `knb-lter-cdr.662.1` cited by `10.1111/1365-2745.12980`

- **Dataset:** Plot coordinates for the E120 Big Biodiversity Field: Biodiversity II: Effects of Plant Biodiversity on Population and Ecosystem Processes (2018)
- **Paper:** Forbs, grasses, and grassland fire behaviour — *Journal of Ecology*, 2018, OA closed; cites 9 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 290. `knb-lter-mcm.9122.5` cited by `10.1029/2022gb007678`

- **Dataset:** Daily summarized seasonal measurements of discharge, water temperature, and specific conductivity from the Onyx River at Lake Vanda, McMurdo Dry Valleys, Antarctica (1969-2020, ongoing) (2021)
- **Paper:** Long‐Term Changes in Concentration and Yield of Riverine Dissolved Silicon From the Poles to the Tropics — *Global Biogeochemical Cycles*, 2023, OA hybrid; cites 21 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 116,616 chars
- **generic**, reference list [86960–87076]: with compiling data from the Environmental Data Initiative and generating watershed land cover and lithology data.
- **Verdict:** 

### 291. `edi.1080.1` cited by `10.22541/au.166522877.74490863/v1`

- **Dataset:** LAGOS-NE Shallow Lakes: a dataset of lake variables and multi-scaled ecological context variables used to predict and compare trophic status and TP:CHLa relationships between shallow and non-shallow lakes in the Upper Midwest and Northeastern United States. (2022)
- **Paper:** The Environmental Data Initiative: connecting the past to the future through data reuse — *?*, 2022, OA gold; cites 5 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (pdf:www.authorea.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.22541_au.166522877.74490863_v1.pdf` and re-run
- **Verdict:** 

### 292. `knb-lter-ntl.129.27` cited by `10.1002/essoar.10501554.1`

- **Dataset:** North Temperate Lakes LTER: High Frequency Data: Meteorological, Dissolved Oxygen, Chlorophyll, Phycocyanin - Lake Mendota Buoy 2006 - current (2019)
- **Paper:** Resolving space and time variation of lake-atmosphere carbon dioxide fluxes using multiple methods — *?*, 2020, OA gold; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_essoar.10501554.1.pdf` and re-run
- **Verdict:** 

### 293. `edi.140.1` cited by `10.15468/dl.ywgcu2`

- **Dataset:** SBC LTER Darwin Core Archive: Kelp Forest Reef Fish Abundance (2018)
- **Paper:** Occurrence Download — *Global Biodiversity Information Facility*, 2020, OA green; cites 1 EDI dataset(s); link source references/datacite-related
- **Text:** not-a-paper (no open location)
- **Verdict:** 

### 294. `msb-paleon.4.0` cited by `10.1371/journal.pone.0150087`

- **Dataset:** Settlement-Era Tree Composition, Eastern US: Level 1 (2016)
- **Paper:** Statistically-Estimated Tree Composition for the Northeastern United States at Euro-American Settlement — *PLoS ONE*, 2016, OA gold; cites 4 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** europepmc, 60,312 chars
- **doi**, reference list [56668–56767]: Long Term Ecological Research Network ; 2016 10.6073/pasta/e40c1ad172882d5113844296611451f6 19.
- **Verdict:** 

### 295. `knb-lter-vcr.200.11` cited by `10.1007/s10750-026-06205-z`

- **Dataset:** Stable isotopes of M. mercenaria and plant sources on the Virginia Coast (2018)
- **Paper:** Incorporating hydrogen in stable isotope analyses improves the ability to track decomposition in marine macrophytes — *Hydrobiologia*, 2026, OA closed; cites 3 EDI dataset(s); link source references/crossref
- **Text:** closed (no open location)
- **Verdict:** 

### 296. `edi.1127.1` cited by `10.1029/2023wr036570`

- **Dataset:** General Lake Model-Aquatic EcoDynamics model parameter set for Falling Creek Reservoir, Vinton, Virginia, USA 2013-2019 (2022)
- **Paper:** Using System‐Inspired Metrics to Improve Water Quality Prediction in Stratified Lakes — *Water Resources Research*, 2024, OA gold; cites 5 EDI dataset(s); link source references/crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1029_2023wr036570.pdf` and re-run
- **Verdict:** 

### 297. `knb-lter-mcr.6.64` cited by `10.3354/meps15071`

- **Dataset:** MCR LTER: Coral Reef: Long-term Population and Community Dynamics: Fishes, ongoing since 2005 (2025)
- **Paper:** Integrating spatial patterns of herbivorous fish functional diversity to inform coral reef management — *Marine Ecology Progress Series*, 2025, OA hybrid; cites 1 EDI dataset(s); link source references/crossref
- **Text:** walled (no open location)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.3354_meps15071.pdf` and re-run
- **Verdict:** 

### 298. `edi.1216.1` cited by `10.1002/ecs2.4351`

- **Dataset:** FRAME (FoRests Among Managed Ecosystems) – Plant community and seed bank composition in forests, Philadelphia metropolitan area, USA, 2017-2019 (2022)
- **Paper:** Plant community dynamics following non‐native shrub removal depend on invasion intensity and forest site characteristics — *Ecosphere*, 2023, OA gold; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** walled (pdf:onlinelibrary.wiley.com:403:not-pdf)
- **To read it by hand:** save the PDF as `data/evalset/manual/10.1002_ecs2.4351.pdf` and re-run
- **Verdict:** 

### 299. `knb-lter-hfr.1.27` cited by `10.5194/acp-17-4189-2017`

- **Dataset:** Fisher Meteorological Station at Harvard Forest since 2001 (2022)
- **Paper:** Field observations of volatile organic compound (VOC) exchange in red oaks — *Atmospheric chemistry and physics*, 2017, OA gold; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 93,188 chars
- **marker** via ref Boose 2001, body [11359–11462]: Measurements of forest leaf area index are routinely made as well as meteorological data (Boose, 2001). ← **query candidate**
- **package_id**, reference list [60456–60576]: Boose, E.: Fisher Meteorological Station (since 2001) [Data set], Harvard Forest, doi:10.6073/AA/KNB-LTER-HFR.1.2, 2001.
- **Verdict:** 

### 300. `edi.1562.1` cited by `10.1002/ecy.4527`

- **Dataset:** Seed Mass of species from Yasuní National Forest, Ecuador, 2000-2014 (2024)
- **Paper:** Putting seedlings on the map: Trade‐offs in demographic rates between ontogenetic size classes in five tropical forests — *Ecology*, 2025, OA hybrid; cites 6 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** europepmc, 98,873 chars
- **doi**, reference list [51138–52110]: For the Yasuní plot: up to 200 growth observations and up to 1000 survival observations per species and size class dbh > 1 cm (Kambach et al., [2024]) are available in the iDiv data repository at https://doi.org/10.25829/idiv.3565-ws9g97 ; growth and survival rates of seedlings <50 cm tall (Metz, Zambrano, et al., [2023]) are available on the EDI data portal at https://doi.org/10.6073/pasta/2cb969b626c3e276770a4fdc8bb3e375 ; seed trap data (Garwood et al., [2023]) are available on the EDI data portal at https://doi.org/10.6073/pasta/5e6cb3d7ff741fd9d21965c4a904bc1f ; wood density data (Wright,
- **doi**, reference list [57735–57891]: “Seed Mass of Species from Yasuní National Forest, Ecuador, 2000‐2014 ver 1.” Environmental Data Initiative. 10.6073/pasta/95e4095ea61fb3cdc3b29b0cc10fa72e.
- **doi**, reference list [76269–77241]: For the Yasuní plot: up to 200 growth observations and up to 1000 survival observations per species and size class dbh > 1 cm (Kambach et al., [2024]) are available in the iDiv data repository at https://doi.org/10.25829/idiv.3565-ws9g97 ; growth and survival rates of seedlings <50 cm tall (Metz, Zambrano, et al., [2023]) are available on the EDI data portal at https://doi.org/10.6073/pasta/2cb969b626c3e276770a4fdc8bb3e375 ; seed trap data (Garwood et al., [2023]) are available on the EDI data portal at https://doi.org/10.6073/pasta/5e6cb3d7ff741fd9d21965c4a904bc1f ; wood density data (Wright,
- **Verdict:** 
