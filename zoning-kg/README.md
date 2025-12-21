# ORGAnIZM Preprocessing Pipeline

**Ontological Rule Graph and Agentic Inference Zoning Model**

A preprocessing pipeline for building a knowledge graph from the Austin Land Development Code (LDC).

## Overview

This pipeline splits the LDC document into logical sections and runs spaCy NER to tag and normalize zoning entities for Graphiti ingestion.

## Features

- **Section Splitter**: Splits the ~103K line LDC markdown into individual sections based on header patterns (§ 25-X-XXX format)
- **NER Pipeline**: Custom spaCy EntityRuler patterns to recognize zoning-specific entities
- **Entity Normalization**: Canonical forms for zones, measurements, metrics, and references

## Entity Types

| Label | Description | Examples |
|-------|-------------|----------|
| `ZONE` | Zone district codes | SF-5, MF-4, CBD, GR |
| `USE_TYPE` | Use classifications | townhouse, condominium, multifamily |
| `SECTION_REF` | Section references | § 25-2-775, Section 25-2-492 |
| `METRIC` | Metric names | lot width, setback, building coverage |
| `MEASUREMENT` | Values with units | 20 feet, 5750 sqft, 40% |
| `OPERATOR` | Constraint operators | minimum, maximum, not exceed |

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

This creates:
- `data/processed/sections/*.json` - Individual section files
- `data/processed/sections/index.json` - Section index

### 2. Run NER on sections

```bash
# Process all sections
python scripts/02_run_ner.py --summary

# Process a single section (for testing)
python scripts/02_run_ner.py --section 25-1-22 --verbose
```

This creates:
- `data/processed/tagged/*.json` - Tagged section files with entities
- `data/processed/tagged/summary.json` - Entity statistics

### 3. Run tests

```bash
python -m pytest tests/test_preprocessing.py -v
```

## Project Structure

```
zoning-kg/
├── src/
│   ├── __init__.py
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── section_splitter.py    # Section splitting logic
│   │   ├── patterns.py            # EntityRuler patterns
│   │   ├── ner_pipeline.py        # spaCy pipeline
│   │   └── normalizer.py          # Entity normalization
│   └── config.py                  # Configuration settings
├── scripts/
│   ├── 01_split_sections.py       # CLI for section splitting
│   └── 02_run_ner.py              # CLI for NER processing
├── data/
│   ├── raw/
│   │   └── ldc.md                 # Source document (copy here or use --input)
│   └── processed/
│       ├── sections/              # Split sections
│       └── tagged/                # NER-tagged sections
├── tests/
│   └── test_preprocessing.py      # Test suite
└── requirements.txt
```

## Output Format

### Section File (sections/25-2-775.json)

```json
{
  "id": "25-2-775",
  "title": "TOWNHOUSES",
  "level": 2,
  "parent_id": "chapter-25-2",
  "content": "§ 25-2-775 - TOWNHOUSES...",
  "start_line": 45231,
  "end_line": 45389,
  "subsections": ["25-2-775-A", "25-2-775-B"]
}
```

### Tagged Section (tagged/25-2-775.json)

```json
{
  "section_id": "25-2-775",
  "content": "...",
  "entities": [
    {
      "text": "20 feet",
      "label": "MEASUREMENT",
      "start": 45,
      "end": 52,
      "normalized": {"value": 20, "unit": "ft"}
    },
    {
      "text": "lot width",
      "label": "METRIC",
      "start": 33,
      "end": 42,
      "normalized": "lot_width_min"
    }
  ]
}
```

## Normalization Examples

### Zones
- `sf-5` → `{"code": "SF-5"}`
- `urban family residence` → `{"code": "SF-5", "name": "urban family residence"}`

### Measurements
- `20 feet` → `{"value": 20, "unit": "ft"}`
- `40 percent` → `{"value": 40, "unit": "%"}`
- `1:1` → `{"value": "1:1", "unit": "ratio", "numerator": 1, "denominator": 1}`

### Metrics
- `lot width` → `lot_width_min`
- `building coverage` → `building_coverage_max`
- `height` → `height_max`

### Section References
- `§ 25-2-775` → `{"section": "25-2-775"}`
- `§25-2-775(B)` → `{"section": "25-2-775", "subsection": "B"}`

## Requirements

- Python 3.9+
- spaCy 3.7+
- pydantic 2.0+

