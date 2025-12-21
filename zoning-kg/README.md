# ORGAnIZM Preprocessing Pipeline

**Ontological Rule Graph and Agentic Inference Zoning Model**

A preprocessing pipeline for building a knowledge graph from the Austin Land Development Code (LDC). This pipeline splits the LDC document into logical sections and runs spaCy NER to tag and normalize zoning entities for Graphiti ingestion.

---

## Pipeline Metrics

| Metric | Value |
|--------|-------|
| **Source Document** | Austin LDC (~103,756 lines, 3.35M chars) |
| **TOC Entries** | 688 sections |
| **Structural Blocks Extracted** | 298 (chapters, articles, sections) |
| **Content Coverage** | **100%** of regulatory content |
| **Total Entities Tagged** | **27,516** |
| **Test Coverage** | 35 tests passing |

### Entity Distribution

| Label | Count | Description | Examples |
|-------|-------|-------------|----------|
| `OPERATOR` | 6,706 | Constraint operators | minimum, maximum, not exceed |
| `MEASUREMENT` | 5,163 | Values with units | 20 feet, 5750 sqft, 40% |
| `SECTION_REF` | 4,657 | Section references | § 25-2-775, Section 25-2-492 |
| `USE_TYPE` | 4,260 | Use classifications | townhouse, condominium, multifamily |
| `ZONE` | 3,640 | Zone district codes | SF-5, MF-4, CBD, GR |
| `METRIC` | 3,090 | Metric names | lot width, setback, building coverage |

---

## Pipeline Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   ldc.md        │────▶│ Section Splitter │────▶│ sections/*.json │
│ (103K lines)    │     │                  │     │ (298 files)     │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │   NER Pipeline   │◀────│ Load sections   │
                        │ + EntityRuler    │     └─────────────────┘
                        │ + Normalizer     │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ tagged/*.json   │
                        │ (27,516 entities)│
                        └─────────────────┘
```

---

## Step 1: Section Splitter (`section_splitter.py`)

### Purpose
Split the monolithic LDC markdown document into manageable, logically-grouped sections while preserving hierarchical relationships.

### Document Structure Analysis

The Austin LDC has a complex, nested structure:

```
Document Layout:
├── Preamble (lines 1-150): Metadata, council members, copyright
├── TOC Blocks (lines starting with "*"): Section listings
│   └── Example: "* § 25-2-775 - TOWNHOUSES."
├── Content Blocks: Actual regulatory text
│   ├── ### Headers: Chapter/Article/Division markers
│   ├── Regulatory text: The actual rules
│   └── Source: citations: End-of-section markers
└── Tables: Zoning requirement matrices
```

### Splitting Algorithm

The splitter uses a **three-strategy approach**:

#### Strategy 1: Structural Boundary Detection
Finds markdown headers that define hierarchical units:

```python
# Patterns matched:
### CHAPTER 25-2. - ZONING.
### ARTICLE 1. - USE CLASSIFICATIONS.
### Division 1. - General Provisions.
### Subchapter A. - GENERAL PROVISIONS.
```

**Result**: 56 structural boundaries identified

#### Strategy 2: Source Citation Blocks
Uses `Source:` lines as section delimiters (common pattern in legal documents):

```
(A) The minimum lot width is 20 feet.
(B) The minimum lot area is 2,500 square feet.

Source: Ord. 990225-70; Ord. 031211-11.  ← Section ends here
```

**Result**: 1,835 content blocks identified

#### Strategy 3: TOC-Based Section Search
For TOC entries without explicit content markers, searches for inline references:

```python
# Searches for patterns like:
"Section 25-2-775"
"§ 25-2-775"
```

### Why Structural Blocks (Not Individual TOC Entries)?

The LDC doesn't have clean per-section boundaries:

| Approach | Files | Coverage |
|----------|-------|----------|
| Individual TOC entries | Would need 688 | Gaps in content |
| Structural blocks | 298 | **100% content** |

The document flows continuously within structural units. Extracting by structure ensures **zero missed regulatory content**.

---

## Step 2: Coverage Analysis

### How We Verified Complete Coverage

```python
# Document composition:
Total lines:     103,756
Empty lines:      35,948 (34.6%)
TOC lines:         1,273 (1.2%)
Table lines:      10,800 (10.4%)
Content lines:    55,734 (53.7%)

# Our sections captured:
Content lines in sections: 73,767
Coverage: 132.4% (overlapping blocks)
```

### Critical Verification

We checked for any missed zoning-relevant content:

```python
# Search for uncovered lines containing zoning keywords:
keywords = ['setback', 'lot width', 'building coverage', 
            'height limit', 'minimum', 'maximum', 'SF-', 'MF-']
            
# Result: 0 uncovered lines with zoning keywords
```

**Conclusion**: All regulatory content is captured, with some intentional overlap between hierarchical blocks.

---

## Step 3: NER Pipeline (`ner_pipeline.py`)

### Purpose
Recognize and extract zoning-specific entities using spaCy with custom EntityRuler patterns.

### Pipeline Architecture

```python
nlp = spacy.load("en_core_web_sm")

# Add EntityRuler BEFORE default NER (higher priority)
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns(ALL_PATTERNS)  # 200+ custom patterns
```

### Entity Types and Patterns (`patterns.py`)

#### ZONE Patterns
```python
# Regex for zone codes
{"label": "ZONE", "pattern": [{"TEXT": {"REGEX": r"^(SF|MF|GR|CR|LR|GO|LO|NO|CS|CH|IP|MI|LI|CBD|DMU|PUD)-?\d*[A-Z]?$"}}]}

# Explicit patterns
{"label": "ZONE", "pattern": "SF-5"}
{"label": "ZONE", "pattern": "MF-4"}

# Multi-word zone names
{"label": "ZONE", "pattern": [{"LOWER": "urban"}, {"LOWER": "family"}, {"LOWER": "residence"}]}
```

#### MEASUREMENT Patterns
```python
# Feet measurements
{"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "feet"}]}

# Square feet
{"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "square"}, {"LOWER": "feet"}]}

# Percentages
{"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"TEXT": "%"}]}

# Ratios (FAR)
{"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": r"^\d+:\d+$"}}]}
```

#### SECTION_REF Patterns
```python
# Note: spaCy tokenizes "25-2-775" as ["25", "-", "2", "-", "775"]
{"label": "SECTION_REF", "pattern": [
    {"TEXT": "§"},
    {"LIKE_NUM": True},
    {"TEXT": "-"},
    {"LIKE_NUM": True},
    {"TEXT": "-"},
    {"LIKE_NUM": True}
]}
```

#### METRIC Patterns
```python
{"label": "METRIC", "pattern": [{"LOWER": "lot"}, {"LOWER": "width"}]}
{"label": "METRIC", "pattern": [{"LOWER": "building"}, {"LOWER": "coverage"}]}
{"label": "METRIC", "pattern": [{"LOWER": "front"}, {"LOWER": "setback"}]}
```

#### OPERATOR Patterns
```python
{"label": "OPERATOR", "pattern": "minimum"}
{"label": "OPERATOR", "pattern": "maximum"}
{"label": "OPERATOR", "pattern": [{"LOWER": "not"}, {"LOWER": "exceed"}]}
{"label": "OPERATOR", "pattern": [{"LOWER": "at"}, {"LOWER": "least"}]}
```

#### USE_TYPE Patterns
```python
{"label": "USE_TYPE", "pattern": "townhouse"}
{"label": "USE_TYPE", "pattern": [{"LOWER": "single"}, {"OP": "?"}, {"TEXT": "-"}, {"LOWER": "family"}]}
{"label": "USE_TYPE", "pattern": [{"LOWER": "accessory"}, {"LOWER": "dwelling"}, {"LOWER": "unit"}]}
```

---

## Step 4: Entity Normalizer (`normalizer.py`)

### Purpose
Convert recognized entities to canonical forms for consistent knowledge graph representation.

### Normalization Rules

#### ZONE Normalization
```python
normalize_zone("sf-5")     → {"code": "SF-5"}
normalize_zone("SF5")      → {"code": "SF-5"}
normalize_zone("SF 5")     → {"code": "SF-5"}
normalize_zone("urban family residence") → {"code": "SF-5", "name": "urban family residence"}
```

#### MEASUREMENT Normalization
```python
normalize_measurement("20 feet")        → {"value": 20, "unit": "ft"}
normalize_measurement("5,750 sqft")     → {"value": 5750, "unit": "sqft"}
normalize_measurement("40%")            → {"value": 40, "unit": "%"}
normalize_measurement("40 percent")     → {"value": 40, "unit": "%"}
normalize_measurement("1:1")            → {"value": "1:1", "unit": "ratio", "numerator": 1, "denominator": 1}
normalize_measurement("17 units per acre") → {"value": 17, "unit": "units/acre"}
```

#### METRIC Normalization
```python
normalize_metric("lot width")           → "lot_width_min"
normalize_metric("minimum lot width")   → "lot_width_min"
normalize_metric("building coverage")   → "building_coverage_max"
normalize_metric("height")              → "height_max"
normalize_metric("front setback")       → "front_setback_min"
```

#### SECTION_REF Normalization
```python
normalize_section_ref("§ 25-2-775")     → {"section": "25-2-775", "subsection": None}
normalize_section_ref("§25-2-775(B)")   → {"section": "25-2-775", "subsection": "B"}
normalize_section_ref("Article 7")      → {"type": "article", "number": 7}
normalize_section_ref("Chapter 25-2")   → {"type": "chapter", "number": "25-2"}
```

#### OPERATOR Normalization
```python
normalize_operator("minimum")     → "min"
normalize_operator("maximum")     → "max"
normalize_operator("at least")    → "gte"
normalize_operator("not exceed")  → "lte"
normalize_operator("required")    → "required"
```

---

## Installation

```bash
cd zoning-kg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Usage

### 1. Split the LDC into sections

```bash
python scripts/01_split_sections.py --input ../TX/source_documents/ldc.md --verbose
```

**Output**:
- `data/processed/sections/*.json` - 298 section files
- `data/processed/sections/index.json` - Section index with metadata

### 2. Run NER on all sections

```bash
python scripts/02_run_ner.py --summary
```

**Output**:
- `data/processed/tagged/*.json` - 298 tagged section files
- `data/processed/tagged/summary.json` - Aggregate entity statistics

### 3. Process a single section (for testing)

```bash
python scripts/02_run_ner.py --section chapter-25-2 --verbose
```

### 4. Run tests

```bash
python -m pytest tests/test_preprocessing.py -v
```

---

## Project Structure

```
zoning-kg/
├── src/
│   ├── __init__.py
│   └── preprocessing/
│       ├── __init__.py
│       ├── section_splitter.py  # Document splitting logic
│       ├── patterns.py          # 200+ EntityRuler patterns
│       ├── ner_pipeline.py      # spaCy pipeline setup
│       └── normalizer.py        # Entity normalization
├── scripts/
│   ├── 01_split_sections.py     # CLI: Split document
│   └── 02_run_ner.py            # CLI: Run NER pipeline
├── data/
│   ├── raw/                     # Source documents (input)
│   └── processed/
│       ├── sections/            # Split sections (298 JSON files)
│       └── tagged/              # NER-tagged sections (298 JSON files)
├── tests/
│   └── test_preprocessing.py    # 35 test cases
└── requirements.txt
```

### Data Directory Purpose

| Directory | Purpose |
|-----------|---------|
| `data/raw/` | Input location for source documents. Copy/symlink `ldc.md` here, or use `--input` flag. |
| `data/processed/sections/` | Split section JSON files + `index.json` metadata. |
| `data/processed/tagged/` | NER-tagged sections + `summary.json` statistics. |

---

## Output Formats

### Section File (`sections/chapter-25-2.json`)

```json
{
  "id": "chapter-25-2",
  "title": "ZONING",
  "level": 1,
  "parent_id": null,
  "content": "### CHAPTER 25-2. - ZONING...",
  "start_line": 10423,
  "end_line": 14620,
  "subsections": ["chapter-25-2-A", "chapter-25-2-B"]
}
```

### Tagged Section (`tagged/chapter-25-2.json`)

```json
{
  "section_id": "chapter-25-2",
  "content": "...",
  "entities": [
    {
      "text": "SF-5",
      "label": "ZONE",
      "start": 156,
      "end": 160,
      "normalized": {"code": "SF-5"}
    },
    {
      "text": "5,750 square feet",
      "label": "MEASUREMENT",
      "start": 892,
      "end": 909,
      "normalized": {"value": 5750, "unit": "sqft"}
    }
  ]
}
```

### Summary File (`tagged/summary.json`)

```json
{
  "total_sections": 298,
  "total_entities": 27516,
  "entities_by_label": {
    "OPERATOR": 6706,
    "MEASUREMENT": 5163,
    "SECTION_REF": 4657,
    "USE_TYPE": 4260,
    "ZONE": 3640,
    "METRIC": 3090
  }
}
```

---

## Top Sections by Entity Count

| Section | Entities | Description |
|---------|----------|-------------|
| chapter-25-12 | 2,687 | Building codes |
| 25-2-article-3 | 2,470 | Use regulations |
| 25-2-article-2 | 1,605 | Zoning districts |
| 25-2-article-4 | 1,354 | Development standards |
| chapter-25-8 | 1,155 | Environment |
| 25-2-subchapter-D | 1,094 | Neighborhood plans |
| chapter-30-5 | 1,013 | Subdivision (Travis County) |
| 25-2-subchapter-E | 972 | Design standards |

---

## Verification Commands

### Check content coverage
```bash
python3 -c "
from pathlib import Path
import json

content = ''
for f in Path('data/processed/sections').glob('*.json'):
    if f.name != 'index.json':
        content += json.load(open(f))['content']

terms = ['SF-5', 'MF-4', 'setback', 'lot width', 'building coverage']
for term in terms:
    print(f'{term}: {content.lower().count(term.lower())} occurrences')
"
```

### View entity summary
```bash
cat data/processed/tagged/summary.json | python -m json.tool
```

### Sample entities from a section
```bash
python3 -c "
import json
with open('data/processed/tagged/chapter-25-2.json') as f:
    data = json.load(f)
for e in data['entities'][:10]:
    print(f\"{e['label']}: {e['text']} → {e['normalized']}\")
"
```

---

## Requirements

- Python 3.9+
- spaCy 3.7+
- pydantic 2.0+

## License

This preprocessing pipeline is part of the ORGAnIZM project for zoning regulation knowledge graphs.
