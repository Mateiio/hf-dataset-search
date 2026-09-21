<!-- Generated from fields-and-search.html by tools/html2md.py; edit the HTML, then regenerate. The HTML version has the styling. -->

<sub>Harvard Forest data archive · hf-dataset-search</sub>

# Fields and Search at Harvard Forest

*The structure of a Harvard Forest dataset description, the fields consulted by the archive's own search and by the new search engine, and the rank-fusion step that combines the new engine's two result lists.*

## 1. Where a dataset's description lives

Every Harvard Forest dataset — take `hf206`, *Microclimate at Harvard Forest HEM, LPH and EMS Towers since 2005* — exists in three places, with the same content in each:

1. **The landing page** on the Harvard Forest website (`showData.html?id=hf206`). This is what a person sees: a title, an abstract, who made it, where, when, and a "Detailed Metadata" section listing every data file and every column in it.
2. **The EML file.** It is linked from the landing page: the row labelled **EML file:** points to `data/eml/hf206.xml`. EML (Ecological Metadata Language) is an XML format: the same information as the landing page, but as tagged text a program can read. The landing page is *generated from* this file.
3. **Copies at EDI and DataONE.** Harvard Forest publishes each dataset to the Environmental Data Initiative, which gives it a package id (`knb-lter-hfr.206.30`) and a DOI. Both links are on the landing page too. The EML there is byte-for-byte the same file.
The actual data — the CSV files with the measurements — is separate. The EML *describes* the CSVs (what each column means, its unit) but does not contain them. Search engines index the description, not the numbers.

### What the EML file contains

Counting across all 459 Harvard Forest EML files, these elements appear. "459" means every dataset has it.

| Group | EML element | What it holds | Datasets with it |
|---|---|---|---|
| What | `title` | One line | 459 |
| `abstract` | A paragraph or two | 459 |  |
| `keywordSet` | Three lists: LTER controlled vocabulary, LTER core area, and a default set (Harvard Forest, HFR, LTER, USA) | 459 |  |
| `methods` | How the data was collected, in prose | 459 |  |
| Who | `creator` | Investigators (name, organisation) | 459 |
| `contact` | Who to ask | 459 |  |
| `associatedParty` | Other people involved | 320 |  |
| Where / when | `geographicCoverage` | Place name plus a bounding box of coordinates | 459 |
| `temporalCoverage` | Start and end dates | 450 |  |
| `taxonomicCoverage` | Species studied, Latin and common names | 282 |  |
| The files | `dataTable` | One per CSV: filename, a one-line description, and every column as an `attribute` with a name, a definition sentence, and a unit | 413 |
| `otherEntity` | Non-table files: shapefiles, images, zips | 167 |  |
| `unit` | Units on columns (celsius, micromolePerMeterSquaredPerSecond…) | 400 |  |
| Admin | `project`, `funding` | "Harvard Forest Long-Term Ecological Research", NSF grant numbers | 459 |
| `intellectualRights`, `licensed` | CC0, plus the "please keep the creators informed" text | 459 |  |
| `pubDate`, `maintenance` | Release date; "ongoing" or "completed" | 459 |  |
| `alternateIdentifier` | The DOI | 458 |  |
| Custom | `additionalMetadata` | Harvard Forest's own tags: `studyType` and `researchTopic` | 459 |

The 46 datasets with no `dataTable` are ones whose files are not tables — GIS layers, photos — described as `otherEntity` instead. `hf206` alone has 5 tables and 344 columns.

## 2. Landing page vs. EML file: the overlap

**The landing page is the EML file, rendered.** Of the 31 labelled fields on `hf206`'s page, 30 come straight from the XML. The only thing the website adds is **Related links** (pointers to other Harvard Forest datasets), which comes from the site's own database.

| Landing-page label | Where it comes from in the EML |
|---|---|
| Lead, Investigators, Contact, Organization | `creator`, `associatedParty`, `contact` |
| Start date, End date | `temporalCoverage` |
| Status | `maintenance` ("ongoing") |
| Location, Latitude, Longitude, Elevation, Datum | `geographicCoverage` |
| Taxa | `taxonomicCoverage` |
| Release date, Language | `pubDate`, `language` |
| EML file, DOI, EDI, DataONE | The file itself; `alternateIdentifier`; the package id |
| Study type, Research topic | `additionalMetadata` (Harvard Forest's custom tags; the page expands "plot" to "large experiments and permanent plot studies") |
| LTER core area, Keywords | The three `keywordSet`s |
| Abstract, Methods | `abstract`, `methods` |
| Project, Funding, Use, License, Citation | `project`, `funding`, `intellectualRights`, `licensed`; the citation is assembled from creator + title + year |
| Detailed Metadata (each file, each column) | `dataTable` → `attribute`: name, definition, unit, missing-value code |
| **Related links** | **Not in the EML.** Added by the website |

So for search purposes there is one source of truth: the EML. Anything a search engine could know about a dataset, it can get from that file — and the new engine reads exactly that file (the same one, fetched from EDI).

## 3. Which fields each search uses

### Harvard Forest's own search

The archive offers six search pages. The main one, "Search Datasets by Multiple Fields", says in its own words which fields it reads:

> "Search datasets by ID number, title, abstract, methods, keyword, location, investigator, and contact. Displays datasets where the submitted string is contained in one or more of these fields."

Two things follow from "contained in". First, it is a **substring match**: your text has to appear literally. Second, there is **no ranking** — results come back alphabetically by title, so the best match is not first. The other five pages (keyword, investigator, taxon, year range, ID) each require an *exact* match on one field.

Tested live on 19 September 2026:

| Typed into "search all" | Results | Is `hf206` among them? | Why |
|---|---|---|---|
| microclimate | 18 | yes | The word is in its title. Alphabetical, so it appears 12th. |
| understory | 56 | yes | Common word; long unranked list. |
| understory PAR | 1 | yes | That exact phrase is in its methods. |
| `par1_ave` | 0 | no | A column name. **Column names and definitions are not searched.** |
| walk-up tower | 2 | **no** | hf206's text writes "walkup tower". A hyphen breaks a substring match. |
| walkup tower | 2 | yes | Same query without the hyphen. |
| sunlight | 4 | no | hf206 says "photosynthetically active radiation", never "sunlight". |
| light below the canopy | 0 | no | No dataset contains that phrase. Meaning is not considered. |

### The new engine

The new engine builds **three separate indexes** from the EML, each fed different fields, and combines two of them at search time. The next section explains each; this table is the summary. Dots mark which fields go where.

● Harvard Forest search ● new: dataset index (TF-IDF) ● new: column index (TF-IDF) ● new: semantic index (bge-m3)

| Field (from the EML) | Harvard Forest | Dataset index | Column index | Semantic |
|---|---|---|---|---|
| Title | ● | ● ×4 | – | ● |
| Keywords | ● | ● ×3 | – | ● |
| Abstract | ● | ● ×2 | – | ● |
| Methods | ● | – | – | – |
| Investigators, contact | ● | – | – | – |
| Location (place name) | ● | – | – | – |
| ID number | ● | – | – | – |
| Taxa, years | ● (separate pages, exact match) | – | – | – |
| Table description (one line per CSV) | – | ● ×1 | – | – |
| Table filename (`hf069-01-lai-plot.csv` → "lai plot") | – | ● | – | – |
| Column names (`par1_ave`) | – | ● | ● | – |
| Column definitions ("understory photosynthetically active radiation 1…") | – | – | ● | ● |
| Column units | – | – | ● | – |
| Coordinates, dates, project, funding, license, study type | – | – | – | – |

### The totals

| | |
|---|---|
| **On the landing page** | 31 labelled fields |
| **Harvard Forest search reads** | 8 fields (plus taxa and years on their own pages) |
| **New engine reads** | 9 distinct fields, spread over three indexes |
| **Both read** | **3**: title, keywords, abstract |
| **Only Harvard Forest reads** | methods, investigators, contact, location, ID, taxa, years |
| **Only the new engine reads** | table descriptions, table filenames, column names, column definitions, column units |

> **Fields not indexed.** The new engine does not index **methods** or **people**; the Harvard Forest search does. A search for an investigator's name, or for a technique mentioned only in the methods text, works on the Harvard Forest site and not in the new engine. The parser already extracts both, so adding them is small — but it has not been tested, and adding text to a TF-IDF index can hurt as well as help (folding column definitions into the dataset index was tried and dropped recall from 0.90 to 0.80).

## 4. What feeds the new engine's three indexes

### **dataset index** one document per dataset, TF-IDF

TF-IDF is word matching with weights: a word scores higher the more it appears in a dataset and the fewer other datasets use it, so "understory" is worth more than "forest". Each dataset becomes one document built from: title (repeated 4×), keywords (3×), abstract (2×), and for every CSV its one-line description (1×), its filename with the dashes turned into spaces, and its column names. Repeating a field is how you tell TF-IDF that a match in the title matters more than one in a column name. It indexes single words and two-word phrases ("understory par"), and hyphenated words are added a second time without the hyphen — which is why "walk-up tower" finds hf206 here and not on the Harvard Forest site.

Column *definitions* are deliberately left out of this index: hf206 has 344 of them covering soil moisture, wind, and temperature, and stuffing all of that into one document dilutes the signal.

### **column index** one document per distinct column definition, TF-IDF

Instead, definitions get their own index at column granularity: 15,395 tiny documents, each "`par1_ave` (micromolePerMeterSquaredPerSecond): understory photosynthetically active radiation 1, measured by the HK2 datalogger". Duplicates are removed (hf206's six PAR sensors share one sentence). A dataset's *single best* column is its score here. This is how "understory light sensors" finds a dataset whose title says only "Microclimate": the title never mentions light, but a column does. Datasets found this way are injected into the lexical results in reserved slots (up to a quarter of the list), ranked below the ordinary matches — but they do get in.

### **semantic index** one vector per dataset, bge-m3

No word matching at all. The bge-m3 model reads a text and produces a **vector**: a list of 1,024 numbers that captures what the text is about, such that texts with similar meaning get vectors pointing in similar directions. Each dataset is turned into one vector from its title, keywords, abstract, *and* all its distinct column definitions (up to 20,000 characters). At search time your query is turned into a vector the same way, and every dataset is scored by the **cosine** between the two — 1.0 for identical direction, ~0.3 for unrelated. Here the definitions help (tested: 0.14 → 0.43 on paraphrased queries), which is the opposite of what they did to TF-IDF. That is why the two indexes are built from different text.

This is the engine that answers "how much sunlight reaches the forest floor" with a PAR dataset. Its weakness is the mirror image: it is fuzzy about exact names and sites, so on the full 10,639-package EDI corpus, where a dozen sites have tower microclimate data, it loses more than word matching does.

## 5. How hybrid combines two ranked lists

The scores from the two engines are not comparable — a cosine of 0.62 and a TF-IDF score of 0.09 mean nothing next to each other. So hybrid ignores scores and uses **ranks**. The method is called reciprocal rank fusion.

1. **Semantic** scores *all 458* datasets and ranks them 1 to 458.
2. **Lexical** returns its top **60**: 45 from the dataset index, up to 15 injected from the column index.
3. Each dataset gets a fused score, one term per list it appears in:
```
score = 1 / (20 + rank in semantic list) + 1 / (20 + rank in lexical list)
```

The constant 20 keeps a #1 from being worth infinitely more than a #2 (the textbook value is 60; this code uses 20, which makes the top of each list count a bit more). Since every dataset has a semantic rank, a dataset that lexical never saw simply gets only its semantic term — half the formula. The top **10** by fused score are shown.

---

### Worked example, real numbers

Query: *understory light sensors at the walk-up tower*, from the trace on 19 September 2026.

| Dataset | Semantic rank | 1/(20+r) | Lexical rank | 1/(20+r) | Fused | Final |
|---|---|---|---|---|---|---|
| `hf282` Microclimate at the walk-up tower | 1 | 0.0500 | 2 | 0.0476 | **0.0976** | 1 |
| `hf183` Canopy phenology & microclimate | 5 | 0.0417 | 1 | 0.0500 | **0.0917** | 2 |
| `hf249` Radiometric measurements | 3 | 0.0455 | 4 | 0.0435 | **0.0889** | 3 |
| `hf206` Microclimate at HEM, LPH, EMS towers | 2 | 0.0476 | 15 | 0.0294 | **0.0770** | 5 |
| `hf237` Snowpack | 34 | 0.0189 | 3 | 0.0455 | **0.0643** | 8 |
| *any dataset outside lexical's top 60* | 7 | 0.0370 | – | 0 | **0.0370** | below 10 |

The two engines *disagreed* about first place — semantic said hf282, lexical said hf183. Neither wins outright; hf282 edges ahead because its lexical rank (2) is closer to the top than hf183's semantic rank (5). hf206, semantic's #2, drops to 5th because lexical ranked it only 15th. And hf237 shows what a lopsided result looks like: lexical loved it (the word "tower" appears in its text), semantic did not (34th), so it lands 8th.

That is the entire mechanism: two engines with complementary failure modes — one insensitive to synonyms, one imprecise about names — vote by rank, and a dataset ranked well by both outranks one ranked well by only one.

---

* Sources: the `hf206` landing page and EML file; element counts over the 459 EML files harvested from EDI on 14 September 2026; Harvard Forest's search pages, probed live 19 September 2026; `hf_search/corpus.py`, `lexical.py`, `semantic.py`, `hybrid.py`; and one traced hybrid query. Written for the `hf-dataset-search` project. *
