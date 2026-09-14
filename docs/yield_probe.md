# Yield probe: citation links to candidate query sentences

Run 2026-09-14 by `python -m edisearch.evalset.yield_probe`, n = 50, seed 0, sampled uniformly from 6,871 distinct (dataset, paper) pairs in DataCite. Mechanical yield only: whether the paper could be read and whether it names the dataset. **Whether a sentence describes what the dataset contains is a human call and the column for it is empty below.**

## Funnel

| Stage | Pairs | Share |
|---|---:|---:|
| Sampled | 50 | 100% |
| Full text read by the script | 12 | 24% |
| ... via Europe PMC XML | 2 | |
| ... via open PDF | 10 | |
| ... via a PDF saved by hand | 0 | |
| Dataset named unambiguously (DOI, package id or title) | 9 | 18% |
| ... with a query candidate in the body text | 10 | 20% |
| ...... of which found by resolving a reference-list marker | 1 | |
| ... hits only in the reference list (body sentence still to be resolved) | 1 | 2% |
| Only a weak pointer (author-year or a generic EDI mention) | 2 | 4% |
| Read, but no mention of the dataset found | 1 | 2% |
| Open in a browser, bot-walled for a script (recoverable by hand) | 25 | 50% |
| Closed | 10 | 20% |
| Not a paper, or not a DOI (theses, GBIF downloads) | 3 | 6% |

The walled row matters: those papers are open access, only the download is refused to a script. At the sizes this project needs (tens to low hundreds of pairs) a person can save them from a browser, so the reachable share for the evaluation set is up to 74%, not 24%.

By link source (a pair can be in both): `is-cited-by` none 23, doi 8, author_year 2, marker 1; `references` none 19, doi 2, marker 1

29 of 50 citing papers cite more than one EDI dataset, which is where attribution can go wrong; those rows say how many.

## Every pair, for reading

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
- **marker** via ref 51, body [26425–26628]: Dataset and regulatory information Data from weather stations C1 and D1, including the daily maximum and minimum temperatures, were provided by the Niwot Ridge Long-Term Ecological Research site [49–52].
- **doi**, reference list [64763–64851]: Available from: https://doi.or g/10. 6073/pas ta/edd9e457f d22a703a587 cc8608d54 bde 52.
- **Verdict:** 

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
- **doi**, body [57459–57608]: Environmental Data Initiative. https://doi.org/10.6073/pasta/a5a4d4154e0a8181a5523b4d9c49ed99 364 https://doi.org/10.5194/essd-2023-222 Preprint. ← **query candidate**
- **title**, body [57321–57457]: Measurements of Leaf area, foliar C and N for 14 sites along a transect down the Kuparuk River basin, summer 1997, North Slope, Alaska.
- **Verdict:** 

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
- **author_year**, body [12637–12928]: Allen: Seasonal partitioning of precipitation 2 Proof-of-concept application 2.1 Field site and data As a proof-of-concept demonstration, here we apply endmember splitting analysis to Campbell and Green’s (2019) measurements of δ18O and δ2H at Hubbard Brook Experimental Forest, Watershed 3. ← **query candidate**
- **author_year**, body [12929–13235]: Campbell and Green (2019) measuredδ18O andδ2H in time-integrated bulk precipitation samples, and instantaneous streamwater grab samples, taken at Watershed 3 approximately every 2 weeks between October 2006 and June 2010 (Fig. 2); the isotope sampling and analysis procedures are documented in Green et al.
- **author_year**, body [18892–19102]: (a) Time series of daily water ﬂuxes and biweekly deuterium values in streamwater (dark blue) and precipitation (light blue) at Watershed 3, Hubbard Brook Experimental Forest (data of Campbell and Green, 2019).
- **doi**, reference list [109701–109862]: B.: Water isotope samples from Watershed 3 at Hubbard Brook Experimental Forest, 2006–2010, https://doi.org/10.6073/pasta/f5740876b68ec42b695c39d8ad790cee, 2019.
- **Verdict:** 

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
- **Verdict:** 

### 32. `edi.1811.1` cited by `10.1073/pnas.2502289122`

- **Dataset:** Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024 (2024)
- **Paper:** Chlorophyll trends are negative for lakes but positive for estuarine–coastal waters — *Proceedings of the National Academy of Sciences*, 2025, OA hybrid; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** europepmc, 47,534 chars
- **doi**, body [29261–29443]: Those data sources are listed and acknowledged in file Metadata- Sampling Locations.csv included in our data package: https://doi.org/10.6073/pasta/dd706bbd8bae2386517d3bf20be02396 . ← **query candidate**
- **doi**, body [30728–30957]: Data, Materials, and Software Availability All chlorophyll a time series data used in this study have been deposited at the Environmental Data Initiative ( https://doi.org/10.6073/pasta/dd706bbd8bae2386517d3bf20be02396 ) ([37]).
- **doi**, body [37791–37998]: Cloern J., Jassby A., “Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024”. Environmental Data Initiative. 10.6073/pasta/dd706bbd8bae2386517d3bf20be02396.
- **title**, body [37791–37919]: Cloern J., Jassby A., “Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024”.
- **marker** via ref 37, body [25323–25464]: The data are available at the Environmental Data Initiative ([37]), including a full description of each site and its associated data source.
- **marker** via ref 37, body [39121–39410]: Associated Data Supplementary Materials Appendix 01 (PDF) Code S01 (R) Data Availability Statement All chlorophyll a time series data used in this study have been deposited at the Environmental Data Initiative ( https://doi.org/10.6073/pasta/dd706bbd8bae2386517d3bf20be02396 ) ([37]).
- **title**, reference list [46207–46335]: Cloern J., Jassby A., “Multidecadal Time Series of Measured Chlorophyll-a in Lakes and Estuarine-Coastal Ecosystems, 1966-2024”.
- **Verdict:** 

### 33. `edi.911.1` cited by `10.21203/rs.3.rs-859794/v1`

- **Dataset:** First-order vertebrated mortality due the 2020 wildfires in the Pantanal wetland, Brazil (2021)
- **Paper:** Counting the Dead: 17 Million Vertebrates Directly Killed by the 2020’s Wildfires in the Pantanal Wetland, Brazil — *Research Square*, 2021, OA green; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** pdf, 40,709 chars
- **doi**, body [26861–27044]: Page 11/16 Declarations Data availability - the data used to conduct the analysis is available at https://doi.org/10.6073/pasta/1688bdf9c001c89972d2cb53d242c4ef (Accessed 2021-08-02). ← **query candidate**
- **Verdict:** 

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
- **doi**, body [72018–72829]: Andrews LTER: https://doi.org/10.6073/pasta/ c96875918bb9c86d330a457bf4295cd9 (McKee, 2015) and http://andlter.forestry.oregonstate.edu/data/ (last access: 16 July 2019) (for sub-daily data), – Southern Sierra CZO: http://criticalzone.org/sierra/data/ dataset/2529/ (last access: 9 September 2019, Husaker, 2011a) and http://criticalzone.org/sierra/data/dataset/2406/ (last access: 9 September 2019, Husaker, 2011b), – Johnston Draw (Reynolds Creek CZO): https://doi.org/10.15482/USDA.ADC/1402076 (Godsey et al., 2016, 2018), – Yosemite Dana Meadows: http://hdl.handle.net/1773/35957 (Lundquist et al ← **query candidate**
- **doi**, reference list [91664–91866]: A.: Meteorological data from benchmark stations at the Andrews Experimental Forest, 1957 to present, Environmental Data Initiative, https://doi.org/10.6073/pasta/ c96875918bb9c86d330a457bf4295cd9, 2015.
- **Verdict:** 

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
- **doi**, body [41986–42356]: Hession, W., Lehmann, L., Wind, L., and Lofton, M.: High-frequency time series of stage height, stream discharge, and water quality (speciﬁc conductivity, dissolved oxygen, pH, temperature, turbidity) for Stroubles Creek in Blacksburg, Virginia, USA 2013-2018 ver 1,365 Environmental Data Initiative, https://doi.org/10.6073/pasta/42727d38837cb4bdf04ce4e0d158ea92, 2020. ← **query candidate**
- **Verdict:** 

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
- **Verdict:** 

### 49. `edi.306.2` cited by `10.1002/ecs2.4208`

- **Dataset:** American Residential Macrosystems - Soil chemistry data within residential yards in six major metropolitan areas, 2012-2013 (2019)
- **Paper:** Ecological homogenization of soil properties in the American residential macrosystem — *Ecosphere*, 2022, OA gold; cites 1 EDI dataset(s); link source references/crossref, is-cited-by/datacite-crossref
- **Text:** pdf, 73,697 chars
- **doi**, body [51787–51924]: DATA AVAILABILITY STATEMENT Data are available from the EDI Data Portal: https://doi. org/10.6073/pasta/5683662180499904732e654e3869f3e6. ← **query candidate**
- **author_year**, body [18960–19105]: Statistical analysis The data used in this paper are publicly available via the Environmental Data Initiative (EDI) Data Portal (Groffman, 2019).
- **doi**, reference list [56473–56705]: “American Residential Macrosystems — Soil Chemistry Data within Residential Yards in Six Major Metropolitan Areas, 2012–2013 Version 2.” Environmental Data Initiative. https://doi.org/10.6073/pasta/5683662180499904732e65 4e3869f3e6.
- **Verdict:** 

### 50. `knb-lter-hbr.406.1` cited by `10.1007/s10021-025-00965-w`

- **Dataset:** Hubbard Brook Experimental Forest and Adirondack Mountains: In-stream large wood and riparian forest structure, 2002-2019 (2025)
- **Paper:** An Emerging Carbon Sink in Headwater Streams and the Role of Large Wood and Riparian Forest Structure — *Ecosystems*, 2025, OA closed; cites 1 EDI dataset(s); link source is-cited-by/datacite-crossref
- **Text:** closed (no open location)
- **Verdict:** 
