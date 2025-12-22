# ORGAnIZM Preprocessing & Knowledge Graph Pipeline

**Ontological Rule Graph and Agentic Inference Zoning Model**

A complete pipeline for building a knowledge graph from the Austin Land Development Code (LDC). This system:

1. **Preprocesses** the LDC document into structured sections
2. **Extracts** zoning entities using spaCy NER
3. **Ingests** into a Graphiti/Neo4j knowledge graph
4. **Applies** Texas state bill overrides for regulatory hierarchy

---

## Pipeline Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   ldc.md        │────▶│ Section Splitter │────▶│ sections/*.json │
│ (103K lines)    │     │ (01_split)       │     │ (298 files)     │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                        ┌──────────────────┐              │
                        │   NER Pipeline   │◀─────────────┘
                        │ (02_run_ner)     │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ tagged/*.json   │
                        │ (27,516 entities)│
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Base Graph    │     │ Episode Ingestion│     │ Override Layer   │
│ (03_build)    │     │ (04_ingest)      │     │ (05_add)         │
│               │     │                  │     │                  │
│ Jurisdictions │     │ Rules, Constr-   │     │ TX SB-840,       │
│ Zones, Uses   │     │ aints, Refs      │     │ SB-2835          │
└───────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Neo4j Graph   │
                        │                 │
                        │ Jurisdiction    │
                        │   ├─ Zone       │
                        │   │  └─ UseType │
                        │   │     └─ Rule │
                        │   │        └─ Constraint
                        │   └─ Override   │
                        └─────────────────┘
```

---

## Pipeline Metrics

### Stage 1: Preprocessing

| Metric | Value |
|--------|-------|
| **Source Document** | Austin LDC (~103,756 lines, 3.35M chars) |
| **TOC Entries** | 688 sections |
| **Structural Blocks Extracted** | 298 |
| **Content Coverage** | **100%** of regulatory content |
| **Total Entities Tagged** | **27,516** |

### Entity Distribution

| Label | Count | Description |
|-------|-------|-------------|
| `OPERATOR` | 6,706 | Constraint operators (minimum, maximum) |
| `MEASUREMENT` | 5,163 | Values with units (20 feet, 40%) |
| `SECTION_REF` | 4,657 | Section references (§ 25-2-775) |
| `USE_TYPE` | 4,260 | Use classifications (townhouse) |
| `ZONE` | 3,640 | Zone district codes (SF-5, MF-4) |
| `METRIC` | 3,090 | Metric names (lot width, setback) |

### Stage 2: Knowledge Graph

| Metric | Value |
|--------|-------|
| **Jurisdictions** | 2 (Austin, Texas) |
| **Zone Districts** | 31 |
| **Use Types** | 7 |
| **State Overrides** | 10 (SB-840 + SB-2835) |

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

### Environment Setup

```bash
# Copy example environment file
cp env.example .env

# Edit .env with your credentials
# Required: NEO4J_PASSWORD, OPENAI_API_KEY
```

### Start Neo4j

```bash
# Start Neo4j container
docker-compose up -d

# Wait for Neo4j to be ready (~30 seconds)
# Access browser at http://localhost:7474
# Login: neo4j / organism_password
```

---

## Usage

### Full Pipeline

```bash
# 1. Split LDC into sections
python scripts/01_split_sections.py --input ../TX/source_documents/ldc.md --verbose

# 2. Run NER on all sections
python scripts/02_run_ner.py --summary

# 3. Build base graph (jurisdictions, zones, use types)
python scripts/03_build_base_graph.py --verbose

# 4. Ingest all tagged episodes
python scripts/04_ingest_episodes.py --verbose

# 5. Add Texas state bill overrides
python scripts/05_add_overrides.py --verbose
```

### Testing Individual Sections

```bash
# Test NER on a single section
python scripts/02_run_ner.py --section chapter-25-2 --verbose

# Test episode ingestion
python scripts/04_ingest_episodes.py --section chapter-25-2 --verbose

# Ingest first 10 episodes only
python scripts/04_ingest_episodes.py --limit 10
```

### Run Tests

```bash
# All tests
python -m pytest tests/ -v

# Ontology tests only
python -m pytest tests/test_ontology.py -v

# Preprocessing tests only
python -m pytest tests/test_preprocessing.py -v
```

---

## Project Structure

```
zoning-kg/
├── src/
│   ├── __init__.py
│   ├── config.py                   # Path configuration
│   ├── preprocessing/              # Stage 1: NLP Pipeline
│   │   ├── section_splitter.py     # Split LDC into sections
│   │   ├── patterns.py             # 200+ EntityRuler patterns
│   │   ├── ner_pipeline.py         # spaCy pipeline setup
│   │   └── normalizer.py           # Entity normalization
│   ├── ontology/                   # Pydantic models
│   │   ├── entities.py             # Node types (Zone, Rule, Constraint)
│   │   ├── edges.py                # Edge types (Contains, AllowsUse)
│   │   └── metrics.py              # Standardized metric catalog
│   ├── graphiti/                   # Graphiti integration
│   │   ├── client.py               # Neo4j/Graphiti client
│   │   ├── type_config.py          # Entity/edge type maps
│   │   └── ingestion.py            # Episode ingestion logic
│   └── graph/                      # Graph builders
│       ├── base_graph.py           # Jurisdictions, zones, uses
│       ├── episode_loader.py       # Load tagged sections
│       └── override_layer.py       # State bill overrides
├── scripts/
│   ├── 01_split_sections.py        # Split LDC document
│   ├── 02_run_ner.py               # Run NER pipeline
│   ├── 03_build_base_graph.py      # Create base graph
│   ├── 04_ingest_episodes.py       # Ingest episodes
│   └── 05_add_overrides.py         # Add overrides
├── data/
│   ├── raw/                        # Source documents
│   ├── processed/
│   │   ├── sections/               # Split sections (298 JSON)
│   │   └── tagged/                 # NER-tagged sections (298 JSON)
│   └── state_bills/                # Override definitions
│       ├── sb840.json              # SB-840 overrides
│       └── sb2835.json             # SB-2835 conditions
├── tests/
│   ├── test_preprocessing.py       # NLP tests (35 tests)
│   └── test_ontology.py            # Ontology tests
├── docker-compose.yml              # Neo4j container
├── env.example                     # Environment template
└── requirements.txt
```

---

## Ontology Model

### Entity Types

| Entity | Description | Example ID |
|--------|-------------|------------|
| `Jurisdiction` | Geographic authority | `austin_tx`, `texas` |
| `Zone` | Zoning district | `austin_tx:SF-5` |
| `UseType` | Building use | `townhouse` |
| `Rule` | Regulation section | `austin_tx:LDC:25-2-775` |
| `Constraint` | Quantitative limit | `austin_tx:LDC:25-2-775:B:lot_width_min` |
| `Condition` | Contextual trigger | `cond_corner_lot` |
| `Override` | State preemption | `texas:SB-840:density` |
| `DocumentSource` | Citation | `austin_tx:LDC:25-2-775(B)` |

### Edge Types

| Edge | From → To | Description |
|------|-----------|-------------|
| `Contains` | Jurisdiction → Zone | District in jurisdiction |
| `AllowsUse` | Zone → UseType | Permitted use |
| `GovernedBy` | UseType → Rule | Applicable regulation |
| `HasConstraint` | Rule → Constraint | Quantitative requirement |
| `HasCondition` | Constraint → Condition | Conditional application |
| `AppliesIn` | Rule → Zone | Zone scope |
| `OverriddenBy` | Constraint → Override | State preemption |
| `SourcedFrom` | * → DocumentSource | Traceability |

### Metrics Catalog

```python
# Lot-level metrics
lot_area_min, lot_width_min, lot_depth_min
setback_front_min, setback_side_min, setback_rear_min

# Site-level metrics  
site_area_min, density_max, far_max, impervious_cover_max

# Building-level metrics
height_max, stories_max, building_coverage_max

# Unit-level metrics
unit_area_min, parking_spaces_per_unit
```

---

## Override Layer

### SB-840: Housing in Commercial Areas

| Override | Type | Value | Applies To |
|----------|------|-------|------------|
| `density_max` | floor | 36 units/acre | MF, mixed-use in commercial |
| `height_max` | floor | 45 ft | MF, mixed-use in commercial |
| `setback_front_min` | ceiling | 25 ft | MF, mixed-use in commercial |
| `setback_side_min` | ceiling | 10 ft | MF, mixed-use in commercial |
| `parking_per_unit` | ceiling | 1 space | MF, mixed-use in commercial |

### SB-2835: Transit-Oriented Development

| Override | Type | Value | Condition |
|----------|------|-------|-----------|
| `density_max` | floor | 50 units/acre | Within 0.5mi of transit |
| `height_max` | floor | 65 ft | Within 0.5mi of transit |
| `parking_per_unit` | ceiling | 0.5 spaces | Within 0.25mi of transit |

**Override Types:**
- `floor`: Localities cannot set limits BELOW this value
- `ceiling`: Localities cannot require values ABOVE this limit

---

## Neo4j Queries

### View All Zones

```cypher
MATCH (j:Jurisdiction)-[:Contains]->(z:Zone)
RETURN j.name, z.code, z.family
ORDER BY z.code
```

### Find Rules for a Use Type

```cypher
MATCH (u:UseType {id: 'townhouse'})-[:GovernedBy]->(r:Rule)
RETURN r.section, r.title
```

### Get Constraints with Overrides

```cypher
MATCH (c:Constraint)-[:OverriddenBy]->(o:Override)
RETURN c.metric, c.value, c.unit, 
       o.override_type, o.value AS override_value
```

### Trace a Constraint to Source

```cypher
MATCH (c:Constraint)-[:SourcedFrom]->(d:DocumentSource)
WHERE c.id = 'austin_tx:LDC:25-2-775:B:lot_width_min'
RETURN c.metric, c.value, d.section, d.subsection, d.text_excerpt
```

---

## Validation

### Verify Neo4j Connection

```bash
python -c "from src.graphiti.client import check_neo4j_connection; print(check_neo4j_connection())"
```

### Check Episode Summary

```bash
python scripts/04_ingest_episodes.py --summary
```

### List Overrides

```bash
python scripts/05_add_overrides.py --list
```

### Run Full Test Suite

```bash
python -m pytest tests/ -v --tb=short
```

---

## Requirements

- Python 3.9+
- Docker (for Neo4j)
- spaCy 3.7+
- graphiti-core 0.5+
- pydantic 2.0+
- OpenAI API key (for Graphiti LLM extraction)

---

## License

This pipeline is part of the ORGAnIZM project for zoning regulation knowledge graphs.
