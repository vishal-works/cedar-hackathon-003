# ORGAnIZM Zoning Knowledge Graph - Complete Documentation

**Comprehensive Graph Documentation for LLM Context**

This document provides complete information about the Austin Zoning Knowledge Graph,
including all entity types, their properties, sample values, relationships, and query patterns.
Use this as context to understand and query the graph.

*Generated: 2025-12-21 21:39:04*

---

## 1. Graph Overview

This knowledge graph represents the **Austin, Texas Land Development Code (LDC)**
and **Texas state housing bills (SB-840, SB-2835)** as a structured graph database.

### Statistics

| Metric | Value |
|--------|-------|
| Total Nodes | 1,211 |
| Total Relationships | 9,772 |
| Episodes Ingested | 306 |

---

## 2. Node Types (Labels)

| Label | Count | Description |
|-------|-------|-------------|
| Episodic | 306 | Ingested text episodes (source content) |
| Entity | 192 | Generic/untyped entities extracted by LLM |
| Rule | 159 | Regulation section from the Land Development Code |
| DocumentSource | 154 | Citation/source reference for traceability |
| Zone | 135 | Zoning district classification (SF-1, MF-4, CBD, etc.) |
| UseType | 112 | Building/development use category (residential, commercial, etc.) |
| Jurisdiction | 65 | Geographic authority (city, county, state) that issues regulations |
| Constraint | 64 | Quantitative requirement (min/max values for setbacks, height, etc.) |
| Override | 15 | State law that supersedes local regulations |
| Condition | 9 | Contextual trigger for when constraints apply |

---

## 3. Entity Type Schemas

Detailed schema for each ontology entity type including properties and sample values.

### 3.1. Jurisdiction

**Count:** 65 nodes

**Description:** Geographic authority (city, county, state) that issues regulations

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `display_name` | City of Austin, State of Texas, Texas |
| `jurisdiction_id` | austin_tx, texas, county |
| `level` | city, state, county |
| `name` | City of Austin (austin_tx), State of Texas (texas), Austin |
| `state` | TX, , NA |
| `summary` | City of Austin governs subdivision and right-of-wa, State of Texas overrides SB-840 for density, heigh, Austin regulates Lake Austin District regulations  |

**Sample Entities:**

1. **City of Austin (austin_tx)**
   - City of Austin governs subdivision and right-of-way processes, including preliminary plan approvals, staff reviews, required notices, dedication of right-of-way, waivers, and council/county actions un...
2. **State of Texas (texas)**
   - State of Texas overrides SB-840 for density, height, setbacks, parking, and lot area per unit in multifamily/mixed-use in commercial/office/mixed-use zones, effective 2025-09-01; prohibits lowering de...
3. **Austin**
   - Austin regulates Lake Austin District regulations (Chapter 25-2) including minimum lot sizes, widths, setbacks, height, impervious cover, and floor area ratios for SF-3, SF-4, SF-6, LA, MF, W/LO, IP, ...
4. **board or commission**
   - City of Austin board or commission hearings: appeals, notices, and procedures handled by the office; public hearings scheduled, notices issued, standing, and appeal procedures governed by City Code an...
5. **the commissioners court**
   - Texas commissioners court (state-level) reviews subdivision plans and final plats, ensures compliance with city/county sections, maintains official records, and ensures public access to staff reports,...


### 3.2. Zone

**Count:** 135 nodes

**Description:** Zoning district classification (SF-1, MF-4, CBD, etc.)

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `code` | SF-1, SF-2, SF-3 |
| `display_name` | Single-Family Residence (Large Lot), Single-Family Residence (Standard Lot), Family Residence |
| `family` | single_family, multifamily, commercial |
| `jurisdiction_id` | austin_tx, city_code, unknown |
| `name` | Zone SF-1 (Single-Family Residence (Large Lot)), austin_tx:SF-1, SF-1 |
| `summary` | Zone SF-1 (Single-Family Residence Large Lot) is a, SF-1 (Single-Family Residence Large Lot) is a resi, SF-1: Single-Family Residence (Large Lot) in Lake  |
| `zone_id` | austin_tx:SF-1, austin_tx:SF-2, austin_tx:SF-3 |

**Sample Entities:**

1. **Zone SF-1 (Single-Family Residence (Large Lot))**
   - Zone SF-1 (Single-Family Residence Large Lot) is a residential district with minimum lot area 10,000 sq ft (up to 1 acre), front setback ~40 ft, and height/open-space rules tied to SF-1 and Lake Austi...
2. **austin_tx:SF-1**
   - SF-1 (Single-Family Residence Large Lot) is a residential zone in Austin, TX. It designates a single-family district with large lot characteristics under City of Austin regulations....
3. **SF-1**
   - SF-1: Single-Family Residence (Large Lot) in Lake Austin (LA) overlay. Lake Austin District regulations apply; minimum lot size 43,560 sq ft; height/front setbacks governed by LA rules; references inc...
4. **Single-Family Residence (Large Lot)**
   - SF-1 is a single-family residential district in Austin, designated SF-1 for large lots (minimum lot size 10,000 sq ft)....
5. **single_family (zone family)**
   - Austin SF-1 (Single-Family Residence Large Lot) is a residential district; SF-2, SF-3, SF-4A, SF-4B (Urban Family Residence variants) represent additional single-family and moderate/high density optio...


### 3.3. UseType

**Count:** 112 nodes

**Description:** Building/development use category (residential, commercial, etc.)

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `aliases` | [], ['General Commercial Services (Conditional)'], ['Commercial Highway', 'Commercial Highway Zone',  |
| `display_name` | Commercial Recreation, General Commercial Services (Conditional), Commercial Highway |
| `group` | commercial, residential, mixed_use |
| `name` | Commercial Recreation, General Commercial Services (Conditional), Commercial Highway |
| `summary` | Commercial Recreation (CR) is a permitted commerci, General Commercial Services (Conditional) (CS-1) u, Commercial Highway use (commercial) referenced in  |
| `use_type_id` | commercial_recreation, CS-1, commercial |

**Sample Entities:**

1. **Commercial Recreation**
   - Commercial Recreation (CR) is a permitted commercial use in CBD/DMU districts, aimed at supporting a mix of residential, commercial, and civic uses within downtown and mixed-use areas....
2. **General Commercial Services (Conditional)**
   - General Commercial Services (Conditional) (CS-1) use in Austin, TX; treated as CS-1 district use with conditional approvals per Downtown/Conditional Use provisions....
3. **Commercial Highway**
   - Commercial Highway use (commercial) referenced in Austin mixed-use provisions; tied to CBD/DMU/PUD zones with density/parcel guidelines in the Austin Code....
4. **Single-Family Dwelling (use type ID: single_family)**
   - Single-Family Dwelling (single_family) is a permitted residential use in SF districts, including SF-3 site development regulations, setbacks, and open-space requirements for single-family residences....
5. **Townhouse (use type ID: townhouse)**
   - Townhouse (use type ID: townhouse) in SF-5 district is a residential use permitted by right....


### 3.4. Rule

**Count:** 159 nodes

**Description:** Regulation section from the Land Development Code

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `applies_in_zones` | ['SF-1', 'SF-2', 'SF-3', 'SF-4A', 'SF-4B', 'SF-5',, ['SF-1', 'SF-2', 'SF-3', 'SF-4A', 'SF-5', 'SF-6', , ['SF-1', 'SF-2', 'SF-3', 'SF-4A', 'SF-4B', 'SF-5', |
| `applies_to_uses` | ['single_family', 'townhouse', 'duplex', 'condomin, ['Single-Family Dwelling', 'Townhouse', 'Condomini, ['Single-Family Dwelling', 'Townhouse', 'Condomini |
| `document` | City of Austin Zoning Rules, Austin Zoning, City Code Section 25-2-775 |
| `jurisdiction_id` | austin_tx, Austin, City of Austin |
| `name` | 25-1-1010 - RECOMMENDATION CRITERIA, Section 25-1-132(A) (Notice of Public Hearing), Section 25-1-132(B) (Notice of Public Hearing) |
| `rule_id` | austin_tx:LDC:25-2-775, austin_tx:LDC:25-1-131, austin_tx:LDC:25-1-133 |
| `section` | 25-2-775, 25-1-188, 25-1-131 |
| `summary` | Townhouses (MF and traditional housing) are allowe, Notice of Public Hearing requirements under Sectio, Notice of Public Hearing (Section 25-1-132(B)) is  |
| `text_excerpt` | Zone SF-1 (austin_tx:SF-1) allows use type single_, Referenced sections and use allowances for various, Section 25-2-775 |
| `title` | Townhouses, Notice by single office of interested party, 25-1-188 |

**Sample Entities:**

1. **25-1-1010 - RECOMMENDATION CRITERIA**
   - Townhouses (MF and traditional housing) are allowed by-right in multiple Austin zones (SF-1 to SF-4, MF-1 to MF-6, CBD, DMU, MU, VMU, PUD). Uses include single family, duplex, condominium, townhouse a...
2. **Section 25-1-132(A) (Notice of Public Hearing)**
   - Notice of Public Hearing requirements under Section 25-1-132(A) govern appeals to boards/commissions within the Austin zoning framework; references to Townhouses and various residential uses, with rel...
3. **Section 25-1-132(B) (Notice of Public Hearing)**
   - Notice of Public Hearing (Section 25-1-132(B)) is given by the responsible director under Section 25-1-132(A) for appeals, with exceptions in (C) aligning to Chapter 25-12 and applicable state law....
4. **certificate of compliance**
   - Certificate of compliance (City of Austin) issued prior to occupancy, tied to final acceptance and site/subdivision readiness; issued after subdivision/site plan completion and compliance with applica...
5. **final acceptance letter**
   - Final acceptance letter issued after subdivision work is completed and all requirements are satisfied, including construction summary, engineer concurrence, reproducible as-built plans, required bonds...


### 3.5. Constraint

**Count:** 64 nodes

**Description:** Quantitative requirement (min/max values for setbacks, height, etc.)

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `applies_to` | site, lot, building |
| `constraint_id` | austin_tx:LDC:25-2-775:B:lot_width_min, austin_tx:LDC:25-2-775:B:median_family_income, austin_tx:LDC:25-2-775:B:BUFFER ZONE |
| `constraint_value` | 0, 775, 500 |
| `metric` | fee_constraint, lot_width_min, impervious_cover_max |
| `name` | fees, fiscal security, cash deposit |
| `operator` | gte, lte, range |
| `rule_id` | update_entity, update_entity_attributes, update_from_messages |
| `source_text` | [MESSAGES], [SECTION ID: 25-1-article-2]\n[TITLE: 25-1-article, The messages do not provide any information about  |
| `subsection` | B, null, C |
| `summary` | Fees: The office collects and assesses fees before, Fiscal security may be posted as cash, a performan, Cash deposits serve as fiscal security for project |
| `unit` | $, ft, % |

**Sample Entities:**

1. **fees**
   - Fees: The office collects and assesses fees before filing; may require fiscal security or other payment (cash, performance bond, or letter of credit); security may be returned or drawn if obligations ...
2. **fiscal security**
   - Fiscal security may be posted as cash, a performance bond, or a letter of credit to secure subdivision improvements; may be drawn if obligations are breached....
3. **cash deposit**
   - Cash deposits serve as fiscal security for project obligations, used alongside performance bonds or letters of credit....
4. **performance bond**
   - The performance bond is an allowed form of fiscal security that an applicant may post, or that may be drawn on by the director to cover obligations, with return of any balance when fulfilled....
5. **letter of credit**
   - No information about a letter of credit requirement or lot width minimum is provided in the messages....


### 3.6. Condition

**Count:** 9 nodes

**Description:** Contextual trigger for when constraints apply

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `condition_field` | Entity, exceptions to the minutes, sale of beer or wine locations |
| `condition_id` | cond_01, 25-1-284_exceptions_to_minutes, C1 |
| `condition_value` | first available meeting for which notice of the he, The minutes of the preconstruction conference; con, Locations for the sale of beer or wine, if any, mu |
| `name` | first available meeting for which notice of the he, exceptions to the minutes, sale of beer or wine locations |
| `operator` | eq |
| `summary` | A public hearing on an appeal shall be scheduled f, Before construction begins, the owner's consulting, Locations for the sale of beer or wine must be ide |

**All Condition Entities:**

- **critical water quality zone**
- **exceptions to the minutes**
- **first available meeting for which notice of the hearing can be timely provided**
- **lot and dwelling residential character**
- **postponement of the public hearing on a neighborhood plan amendment application**
- **sale of beer or wine locations**
- **secondary setback area**
- **shoreline setback area**
- **triggering property**


### 3.7. Override

**Count:** 15 nodes

**Description:** State law that supersedes local regulations

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `bill_id` | SB-840, SB-2835, 25-1-251 |
| `effective_date` | 2025-09-01, 2024-01-01, 2025-12-21 |
| `exclusions` | [], ['none'], ['International Dark Sky standards'] |
| `jurisdiction_id` | texas, city-code |
| `metric` | density_max, height_max, setback_front_min |
| `name` | texas:SB-840:density, texas:SB-840:height, texas:SB-840:setback_front |
| `override_id` | texas:SB-840:density, texas:SB-840:height, texas:SB-840:setback_front |
| `override_type` | floor, ceiling |
| `override_value` | 36, 45, 25 |
| `scope_uses` | ['multifamily', 'mixed_use'], ['adjustment-application-process', 'water-quality-, ['zoning', 'variance', 'land-use planning'] |
| `scope_zones` | ['commercial', 'office', 'mixed_use'], [], ['city of interest'] |
| `summary` | Texas SB-840 density override increases density_ma, SB-840 height override sets height_max to 45 ft fo, texas:SB-840 setback front overrides set front set |
| `unit` | units/acre, ft, spaces |

**All Override Entities:**

- **International Dark Sky standards**
- **Texas Constitution**
- **Texas Local Government Code Chapter 212 Subchapter A (Regulation of Subdivisions)**
- **Texas Local Government Code Chapter 232 Subchapter A (Subdivision Platting Requirements in General)**
- **United States Constitution**
- **applicable state law**
- **federal statute**
- **texas:SB-2835:transit_density**
- **texas:SB-840:density**
- **texas:SB-840:height**
- **texas:SB-840:lot_area_per_unit**
- **texas:SB-840:parking**
- **texas:SB-840:setback_front**
- **texas:SB-840:setback_rear**
- **texas:SB-840:setback_side**


### 3.8. DocumentSource

**Count:** 154 nodes

**Description:** Citation/source reference for traceability

**Properties:**

| Property | Sample Values |
|----------|---------------|
| `document` | CHAPTER 25-2. - ZONING., CHAPTER 25-1. - GENERAL REQUIREMENTS AND PROCEDURE, CHAPTER 25-3. - TRADITIONAL NEIGHBORHOOD DISTRICT. |
| `name` | [SECTION ID: 25-1-1010], CHAPTER 25-2 - ZONING, CHAPTER 25-3 - TRADITIONAL NEIGHBORHOOD DISTRICT |
| `section` | CHAPTER 25-2. - ZONING., CHAPTER 25-2. - ZONING, CHAPTER 25-3. - TRADITIONAL NEIGHBORHOOD DISTRICT. |
| `source_id` | 25-1-1010, 25-1-1010|25-1-131|25-1-132|25-1-132(C), Source: Section 13-1-253(b); Ord. 990225-70; Ord.  |
| `subsection` | § 25-1-1010 - RECOMMENDATION CRITERIA., null, (C) |
| `summary` | Recommendation criteria for Chapter 25-2 (Zoning) , CHAPTER 25-2 - ZONING governs mixed-use districts , TN District (CHAPTER 25-3) is described within the |
| `text_excerpt` | [SECTION CONTENT]
## CHAPTER 25-2. - ZONING.

§ 25, CHAPTER 25-2. - ZONING, § 25-1-1010 - RECOMMENDATION CRITERIA.
CHAPTER 25- |

**Sample Entities:**

1. **[SECTION ID: 25-1-1010]**
   - Recommendation criteria for Chapter 25-2 (Zoning) outlined in § 25-1-1010, referencing Chapter 25-3 (Traditional Neighborhood District)....
2. **CHAPTER 25-2 - ZONING**
   - CHAPTER 25-2 - ZONING governs mixed-use districts (CBD, DMU, LO/NO/GO ranges, LR, CR, MF, IP/MI/LI, LA, DMU, DR, PDA) in Austin, with Traditional Neighborhood overlays and ETOD considerations; referen...
3. **CHAPTER 25-3 - TRADITIONAL NEIGHBORHOOD DISTRICT**
   - TN District (CHAPTER 25-3) is described within the City’s zoning framework, linked to base districts in CHAPTER 25-2 and guided by recommendation criteria in § 25-1-1010....
4. **Chapter 25-12 (Technical Codes)**
   - Chapter 25-12 (Technical Codes): The responsible director must give notice under Chapter 25-12 (Technical Codes) and state law of a public hearing on an appeal to a board or commission created by Chap...
5. **Source: Section 13-1-253(b); Ord. 990225-70; Ord. 010329-18; Ord. 031211-11**
   - Source: Section 13-1-253(b); Ord. 990225-70; Ord. 010329-18; Ord. 031211-11; RECOMMENDATION CRITERIA (25-1-1010) within ZONING Chapter 25-2....


---

## 4. Relationship Types

### 4.1. Neo4j Relationship Types

| Type | Count | Description |
|------|-------|-------------|
| `MENTIONS` | 5,656 | Episode mentions entity |
| `RELATES_TO` | 4,116 | Semantic relationship with name property |

### 4.2. Semantic Edge Types

The `RELATES_TO` relationships have a `name` property indicating semantic meaning.

| Edge Type | Count | Description |
|-----------|-------|-------------|
| `APPLIES_IN` | 587 | Rule/Constraint applies in a specific zone |
| `CONTAINS` | 363 | Jurisdiction contains zone; Zone contains subzone |
| `SOURCED_FROM` | 294 | Entity traced back to source document |
| `GOVERNED_BY` | 242 | Use type is governed by a rule |
| `ALLOWS_USE` | 231 | Zone permits a use type |
| `HAS_CONSTRAINT` | 194 | Rule has a quantitative constraint |
| `REQUIRES` | 77 | Conditional requirement |
| `APPLIES_TO` | 68 |  |
| `DEFINES` | 65 | Definition relationship |
| `INCLUDES` | 51 | Inclusion relationship |
| `REFERENCES` | 50 | Cross-reference to another section |
| `HAS_CONDITION` | 32 | Constraint has a conditional trigger |
| `GOVERNS_ZONE` | 22 |  |
| `GOVERNS` | 18 |  |
| `SUPERSEDES` | 15 |  |
| `GOVERNES_METRIC` | 14 |  |
| `SUPERSEDED_BY` | 13 |  |
| `PERMITS_TEMPORARY_USE` | 13 |  |
| `SOURCE_DOCUMENT` | 12 |  |
| `MUST_COMPLY_WITH` | 12 |  |
| `NOTIFIES` | 12 |  |
| `DEFINED_AS` | 12 |  |
| `PROHIBITS` | 11 |  |
| `OVERRIDDEN_BY` | 10 | Local rule overridden by state law |
| `DISCUSSSES_TOPIC_WITH` | 9 |  |
| ... | ... | *(1171 more edge types)* |

### 4.3. Common Relationship Patterns

| From Type | Edge | To Type | Count |
|-----------|------|---------|-------|
| Rule | `APPLIES_IN` | Zone | 317 |
| Rule | `SOURCED_FROM` | DocumentSource | 153 |
| Zone | `ALLOWS_USE` | UseType | 90 |
| DocumentSource | `CONTAINS` | Zone | 76 |
| Rule | `HAS_CONSTRAINT` | Constraint | 67 |
| DocumentSource | `SOURCED_FROM` | DocumentSource | 51 |
| Jurisdiction | `CONTAINS` | Zone | 46 |
| UseType | `GOVERNED_BY` | Rule | 44 |
| DocumentSource | `CONTAINS` | Rule | 25 |
| Rule | `CONTAINS` | Rule | 24 |
| Rule | `APPLIES_IN` | Entity | 23 |
| Rule | `APPLIES_IN` | Jurisdiction | 21 |
| Rule | `CONTAINS` | Zone | 20 |
| Constraint | `APPLIES_IN` | Zone | 20 |
| Rule | `GOVERNED_BY` | Rule | 20 |
| Rule | `APPLIES_IN` | Rule | 19 |
| Zone | `ALLOWS_USE` | Zone | 19 |
| Entity | `GOVERNED_BY` | Entity | 19 |
| DocumentSource | `CONTAINS` | DocumentSource | 18 |
| Zone | `CONTAINS` | Zone | 18 |
| UseType | `ALLOWS_USE` | UseType | 18 |
| Rule | `GOVERNS_ZONE` | Zone | 17 |
| Zone | `ALLOWS_USE` | Rule | 16 |
| Rule | `DEFINES` | Entity | 15 |
| Entity | `DEFINES` | Entity | 15 |

---

## 5. Query Examples

### 5.1. Find all zones in Austin
```cypher
MATCH (j:Jurisdiction)-[r:RELATES_TO]->(z:Zone)
WHERE r.name = 'CONTAINS' AND j.name CONTAINS 'Austin'
RETURN z.name, z.code, z.family
ORDER BY z.name
```

### 5.2. Find zones that allow townhouses
```cypher
MATCH (z:Zone)-[r:RELATES_TO]->(u:UseType)
WHERE r.name = 'ALLOWS_USE' AND u.name CONTAINS 'Townhouse'
RETURN z.name, u.name
```

### 5.3. Get constraints for a specific zone
```cypher
MATCH (z:Zone)-[:RELATES_TO]-(r:Rule)-[rel:RELATES_TO]->(c:Constraint)
WHERE z.name CONTAINS 'SF-5' AND rel.name = 'HAS_CONSTRAINT'
RETURN z.name, r.name, c.name, c.summary
```

### 5.4. Find all state overrides
```cypher
MATCH (o:Override)
RETURN o.name, o.bill_id, o.metric, o.override_value, o.summary
```

### 5.5. Trace a rule to its source document
```cypher
MATCH (r:Rule)-[rel:RELATES_TO]->(d:DocumentSource)
WHERE rel.name = 'SOURCED_FROM'
RETURN r.name, r.section, d.document, d.section
LIMIT 10
```

### 5.6. Find rules that apply in multiple zones
```cypher
MATCH (r:Rule)-[rel:RELATES_TO]->(z:Zone)
WHERE rel.name = 'APPLIES_IN'
WITH r, count(z) as zone_count
WHERE zone_count > 3
RETURN r.name, zone_count
ORDER BY zone_count DESC
```

### 5.7. Full graph visualization query
```cypher
MATCH path = (j:Jurisdiction)-[:RELATES_TO*1..3]->(n)
WHERE j.name CONTAINS 'Austin'
RETURN path
LIMIT 100
```

---

## 6. Ontology Summary

### Entity Hierarchy
```
Jurisdiction (city, county, state)
├── Zone (zoning districts)
│   └── UseType (permitted uses)
│       └── Rule (regulations)
│           └── Constraint (quantitative limits)
│               └── Condition (when constraint applies)
└── Override (state preemptions)
    └── applies to local Constraints
```

### Key Relationships
```
Jurisdiction --[CONTAINS]--> Zone
Zone --[ALLOWS_USE]--> UseType
UseType --[GOVERNED_BY]--> Rule
Rule --[APPLIES_IN]--> Zone
Rule --[HAS_CONSTRAINT]--> Constraint
Constraint --[HAS_CONDITION]--> Condition
Constraint --[OVERRIDDEN_BY]--> Override
* --[SOURCED_FROM]--> DocumentSource
```

---

## 7. Data Sources

| Source | Description |
|--------|-------------|
| Austin LDC | Land Development Code (~103,756 lines) |
| Texas SB-840 | Housing in commercial areas bill |
| Texas SB-2835 | Transit-oriented development bill |

---

*End of Knowledge Graph Documentation*