# ORGAnIZM Zoning Knowledge Graph - Complete Documentation

**Comprehensive Graph Documentation for LLM Context**

This document provides complete information about the Austin Zoning Knowledge Graph,
including all entity types, properties, relationships, orphan nodes, and query patterns.

*Generated: 2025-12-21 21:46:55*

---

## 1. Graph Overview

| Metric | Value |
|--------|-------|
| **Total Nodes** | 1,211 |
| **Total Relationships** | 9,772 |
| **Episodes Ingested** | 306 |

---

## 2. Node Labels

| Label | Count | Description |
|-------|-------|-------------|
| `Episodic` | 306 | Ingested text episodes |
| `Entity` | 192 | Generic/untyped entities from LLM |
| `Rule` | 159 | Regulation section from LDC |
| `DocumentSource` | 154 | Citation/source reference |
| `Zone` | 135 | Zoning district classification (SF-1, MF-4, CBD) |
| `UseType` | 112 | Building/development use category |
| `Jurisdiction` | 65 | Geographic authority (city, county, state) |
| `Constraint` | 64 | Quantitative requirement (min/max values) |
| `Override` | 15 | State law superseding local regulations |
| `Condition` | 9 | Contextual trigger for constraints |

---

## 3. Entity Type Schemas

### 3.1. Jurisdiction

**Count:** 65 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `created_at` | DateTime | 2025-12-21T20:08:17.820089000+00:00, 2025-12-21T20:08:17.820099000+00:00, 2025-12-21T20:08:17.820105000+00:00 |
| `display_name` | str | City of Austin, State of Texas, Texas |
| `jurisdiction_id` | str | austin_tx, texas, county |
| `level` | str | city, state, county |
| `name` | str | City of Austin (austin_tx), State of Texas (texas), Austin |
| `orphan_candidate` | bool | True |
| `state` | str | TX, , NA |
| `summary` | str | City of Austin governs subdivision and r, State of Texas overrides SB-840 for dens, Austin regulates Lake Austin District re |

**Sample Entities (showing 10 of 65):**

1. **City of Austin (austin_tx)**
   - City of Austin governs subdivision and right-of-way processes, including preliminary plan approvals, staff reviews, required notices, dedication of ri...
2. **State of Texas (texas)**
   - State of Texas overrides SB-840 for density, height, setbacks, parking, and lot area per unit in multifamily/mixed-use in commercial/office/mixed-use ...
3. **Austin**
   - Austin regulates Lake Austin District regulations (Chapter 25-2) including minimum lot sizes, widths, setbacks, height, impervious cover, and floor ar...
4. **board or commission**
   - City of Austin board or commission hearings: appeals, notices, and procedures handled by the office; public hearings scheduled, notices issued, standi...
5. **the commissioners court**
   - Texas commissioners court (state-level) reviews subdivision plans and final plats, ensures compliance with city/county sections, maintains official re...
6. **transit station**
   - Transit station: density max 50 units/acre; height max 65 ft within 0.5 miles; parking up to 0.5 per unit. Density/height/parking boosts under SB-2835...
7. **county**
   - County notices for public hearings and owner notices; appeal timelines; fiscal security duties; approvals/denials timelines; fast-track/permitting con...
8. **newspaper of general circulation in the city**
   - Published notice for city actions is effective when published in a newspaper of general circulation in the city (TX)....
9. **Planning and Development Review Department**
   - Planning and Development Review Department (city-level): implements land development regulations, including zoning, subdivision approvals, preliminary...
10. **the same or a substantially the same site**
   - If a variance is denied or revoked, an applicant may not file a similar variance on the same or a substantially the same site for one year from the de...


### 3.2. Zone

**Count:** 135 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `code` | str | SF-1, SF-2, SF-3 |
| `created_at` | DateTime | 2025-12-21T20:08:48.110821000+00:00, 2025-12-21T20:08:48.110944000+00:00, 2025-12-21T20:08:48.110974000+00:00 |
| `display_name` | str | Single-Family Residence (Large Lot), Single-Family Residence (Standard Lot), Family Residence |
| `duplicate_candidate` | bool | True |
| `duplicate_group` | str | single_family (zone family), Urban Family Residence (Moderate-High De, Zone family single_family |
| `family` | str | single_family, multifamily, commercial |
| `jurisdiction_id` | str | austin_tx, city_code, unknown |
| `name` | str | Zone SF-1 (Single-Family Residence (Larg, austin_tx:SF-1, SF-1 |
| `orphan_candidate` | bool | True |
| `summary` | str | Zone SF-1 (Single-Family Residence Large, SF-1 (Single-Family Residence Large Lot), SF-1: Single-Family Residence (Large Lot |
| `zone_id` | str | austin_tx:SF-1, austin_tx:SF-2, austin_tx:SF-3 |

**Sample Entities (showing 10 of 135):**

1. **Zone SF-1 (Single-Family Residence (Large Lot))**
   - Zone SF-1 (Single-Family Residence Large Lot) is a residential district with minimum lot area 10,000 sq ft (up to 1 acre), front setback ~40 ft, and h...
2. **austin_tx:SF-1**
   - SF-1 (Single-Family Residence Large Lot) is a residential zone in Austin, TX. It designates a single-family district with large lot characteristics un...
3. **SF-1**
   - SF-1: Single-Family Residence (Large Lot) in Lake Austin (LA) overlay. Lake Austin District regulations apply; minimum lot size 43,560 sq ft; height/f...
4. **Single-Family Residence (Large Lot)**
   - SF-1 is a single-family residential district in Austin, designated SF-1 for large lots (minimum lot size 10,000 sq ft)....
5. **single_family (zone family)**
   - Austin SF-1 (Single-Family Residence Large Lot) is a residential district; SF-2, SF-3, SF-4A, SF-4B (Urban Family Residence variants) represent additi...
6. **Zone SF-2 (Single-Family Residence (Standard Lot))**
   - Zone SF-2 (Single-Family Residence, Standard Lot) in Austin, TX. Primary residential use with SF-2 minimums; located in Lake Austin area. SF-2 provisi...
7. **austin_tx:SF-2**
   - austin_tx:SF-2 is a Single-Family Residence (Standard Lot) zoning district (zone code SF-2) in City of Austin; Zone ID austin_tx:SF-2; Jurisdiction au...
8. **SF-2**
   - SF-2 is a Lake Austin overlay zone for Single-Family Residence (Standard Lot). Requires minimum lot size 10,000 sq ft, max height 35 ft, and dwelling ...
9. **Single-Family Residence (Standard Lot)**
   - SF-2 (Single-Family Residence, Standard Lot) in Austin: residential base district SF-2 with minimum lot size 5,750 sq ft; supports moderate-density si...
10. **Zone SF-3 (Family Residence)**
   - SF-3 (Family Residence) is a single-family zoning district in Austin, TX with setback, lot size, and dwelling-unit requirements defined in Article 2, ...


### 3.3. UseType

**Count:** 112 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `aliases` | list | [], ['General Commercial Services (Condition, ['Commercial Highway', 'Commercial Highw |
| `created_at` | DateTime | 2025-12-21T20:10:56.108413000+00:00, 2025-12-21T20:10:56.108461000+00:00, 2025-12-21T20:10:56.108485000+00:00 |
| `display_name` | str | Commercial Recreation, General Commercial Services (Conditional, Commercial Highway |
| `group` | str | commercial, residential, mixed_use |
| `name` | str | Commercial Recreation, General Commercial Services (Conditional, Commercial Highway |
| `orphan_candidate` | bool | True |
| `summary` | str | Commercial Recreation (CR) is a permitte, General Commercial Services (Conditional, Commercial Highway use (commercial) refe |
| `use_type_id` | str | commercial_recreation, CS-1, commercial |

**Sample Entities (showing 10 of 112):**

1. **Commercial Recreation**
   - Commercial Recreation (CR) is a permitted commercial use in CBD/DMU districts, aimed at supporting a mix of residential, commercial, and civic uses wi...
2. **General Commercial Services (Conditional)**
   - General Commercial Services (Conditional) (CS-1) use in Austin, TX; treated as CS-1 district use with conditional approvals per Downtown/Conditional U...
3. **Commercial Highway**
   - Commercial Highway use (commercial) referenced in Austin mixed-use provisions; tied to CBD/DMU/PUD zones with density/parcel guidelines in the Austin ...
4. **Single-Family Dwelling (use type ID: single_family)**
   - Single-Family Dwelling (single_family) is a permitted residential use in SF districts, including SF-3 site development regulations, setbacks, and open...
5. **Townhouse (use type ID: townhouse)**
   - Townhouse (use type ID: townhouse) in SF-5 district is a residential use permitted by right....
6. **Condominium (use type ID: condominium)**
   - Condominium (use type: condominium) is a residential use. Aliases: condo, condominium development....
7. **Duplex (use type ID: duplex)**
   - Duplex (use_type_id: duplex) is a residential use type; aliases include two-family and two-unit dwelling....
8. **Accessory Dwelling Unit (use type ID: accessory_dwelling_uni**
   - Accessory Dwelling Unit (ADU) is a residential use that may be a separate dwelling on the same lot as a primary residence; aliases include ADU, granny...
9. **Use type multifamily (id: multifamily)**
   - Multifamily use (Use Type: multifamily) is a residential use allowed in MF zones; may be subject to parkland dedication and vesting rights requirement...
10. **proposed neighborhood plan amendment**
   - Proposed neighborhood plan amendment introduces a mixed-use framework (MU) across Austin districts (CBD/DMU/DMU, etc.), outlining notice, planning, an...


### 3.4. Rule

**Count:** 159 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `applies_in_zones` | list | ['SF-1', 'SF-2', 'SF-3', 'SF-4A', 'SF-4B, ['SF-1', 'SF-2', 'SF-3', 'SF-4A', 'SF-5', ['SF-1', 'SF-2', 'SF-3', 'SF-4A', 'SF-4B |
| `applies_to_uses` | list | ['single_family', 'townhouse', 'duplex',, ['Single-Family Dwelling', 'Townhouse', , ['Single-Family Dwelling', 'Townhouse',  |
| `created_at` | DateTime | 2025-12-21T20:18:31.590389000+00:00, 2025-12-21T20:20:11.936336000+00:00, 2025-12-21T20:20:11.936343000+00:00 |
| `document` | str | City of Austin Zoning Rules, Austin Zoning, City Code Section 25-2-775 |
| `jurisdiction_id` | str | austin_tx, Austin, City of Austin |
| `name` | str | 25-1-1010 - RECOMMENDATION CRITERIA, Section 25-1-132(A) (Notice of Public He, Section 25-1-132(B) (Notice of Public He |
| `orphan_candidate` | bool | True |
| `rule_id` | str | austin_tx:LDC:25-2-775, austin_tx:LDC:25-1-131, austin_tx:LDC:25-1-133 |
| `section` | str | 25-2-775, 25-1-188, 25-1-131 |
| `summary` | str | Townhouses (MF and traditional housing) , Notice of Public Hearing requirements un, Notice of Public Hearing (Section 25-1-1 |
| `text_excerpt` | str | Zone SF-1 (austin_tx:SF-1) allows use ty, Referenced sections and use allowances f, Section 25-2-775 |
| `title` | str | Townhouses, Notice by single office of interested pa, 25-1-188 |

**Sample Entities (showing 10 of 159):**

1. **25-1-1010 - RECOMMENDATION CRITERIA**
   - Townhouses (MF and traditional housing) are allowed by-right in multiple Austin zones (SF-1 to SF-4, MF-1 to MF-6, CBD, DMU, MU, VMU, PUD). Uses inclu...
2. **Section 25-1-132(A) (Notice of Public Hearing)**
   - Notice of Public Hearing requirements under Section 25-1-132(A) govern appeals to boards/commissions within the Austin zoning framework; references to...
3. **Section 25-1-132(B) (Notice of Public Hearing)**
   - Notice of Public Hearing (Section 25-1-132(B)) is given by the responsible director under Section 25-1-132(A) for appeals, with exceptions in (C) alig...
4. **certificate of compliance**
   - Certificate of compliance (City of Austin) issued prior to occupancy, tied to final acceptance and site/subdivision readiness; issued after subdivisio...
5. **final acceptance letter**
   - Final acceptance letter issued after subdivision work is completed and all requirements are satisfied, including construction summary, engineer concur...
6. **administrative site plan**
   - Administrative site plan may substitute for a zoning site plan if replacement complies with current rules, traffic analyses are valid or mitigated, im...
7. **zoning site plan**
   - Replacement zoning site plan may substitute for a zoning site plan if it complies with current regulations, keeps impervious/building coverage within ...
8. **traffic impact analysis**
   - Traffic Impact Analysis (TIA) is required to support zoning/site plan approvals. For replacement site plans, a valid TIA must be supported by an adden...
9. **restrictive covenant**
   - Restrictive covenant: a formal clause restricting property use or development, often tied to zoning or site plan approval (City Code 25-2-775; Townhou...
10. **25-1-184**
   - Notice by single office of interested party: The single office shall notify an applicant in writing if there is an interested party to an administrati...


### 3.5. Constraint

**Count:** 64 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `applies_to` | str | site, lot, building |
| `constraint_id` | str | austin_tx:LDC:25-2-775:B:lot_width_min, austin_tx:LDC:25-2-775:B:median_family_i, austin_tx:LDC:25-2-775:B:BUFFER ZONE |
| `constraint_value` | int | 0, 775, 500 |
| `created_at` | DateTime | 2025-12-21T20:21:18.366803000+00:00, 2025-12-21T20:21:18.366812000+00:00, 2025-12-21T20:21:18.366845000+00:00 |
| `metric` | str | fee_constraint, lot_width_min, impervious_cover_max |
| `name` | str | fees, fiscal security, cash deposit |
| `operator` | str | gte, lte, range |
| `orphan_candidate` | bool | True |
| `rule_id` | str | update_entity, update_entity_attributes, update_from_messages |
| `source_text` | str | [MESSAGES], [SECTION ID: 25-1-article-2]\n[TITLE: 25, The messages do not provide any informat |
| `subsection` | str | B, null, C |
| `summary` | str | Fees: The office collects and assesses f, Fiscal security may be posted as cash, a, Cash deposits serve as fiscal security f |
| `unit` | str | $, ft, % |
| `value_high` | int | 6, 0, 9 |

**Sample Entities (showing 10 of 64):**

1. **fees**
   - Fees: The office collects and assesses fees before filing; may require fiscal security or other payment (cash, performance bond, or letter of credit);...
2. **fiscal security**
   - Fiscal security may be posted as cash, a performance bond, or a letter of credit to secure subdivision improvements; may be drawn if obligations are b...
3. **cash deposit**
   - Cash deposits serve as fiscal security for project obligations, used alongside performance bonds or letters of credit....
4. **performance bond**
   - The performance bond is an allowed form of fiscal security that an applicant may post, or that may be drawn on by the director to cover obligations, w...
5. **letter of credit**
   - No information about a letter of credit requirement or lot width minimum is provided in the messages....
6. **500 ft**
   - Neighborhood notice radius is 500 ft....
7. **impervious cover**
   - Replacement site plans may not exceed the impervious_cover_max approved for the zoning site plan....
8. **building coverage**
   - Building coverage and impervious limits follow zoning guidelines; maximum building coverage is established by the zoning site plan (25-2-775). Height ...
9. **building height**
   - Replacement site plan building height must not exceed the approved zoning site plan height by more than 6 ft....
10. **list of determinations**
   - The director maintains use determinations and notifies filings and dispositions under 25-1-197....


### 3.6. Condition

**Count:** 9 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `condition_field` | str | Entity, exceptions to the minutes, sale of beer or wine locations |
| `condition_id` | str | cond_01, 25-1-284_exceptions_to_minutes, C1 |
| `condition_value` | str | first available meeting for which notice, The minutes of the preconstruction confe, Locations for the sale of beer or wine,  |
| `created_at` | DateTime | 2025-12-21T20:29:51.363352000+00:00, 2025-12-21T21:00:52.247664000+00:00, 2025-12-21T22:03:19.238665000+00:00 |
| `name` | str | first available meeting for which notice, exceptions to the minutes, sale of beer or wine locations |
| `operator` | str | eq |
| `summary` | str | A public hearing on an appeal shall be s, Before construction begins, the owner's , Locations for the sale of beer or wine m |

**All Condition Entities (9):**

- critical water quality zone
- exceptions to the minutes
- first available meeting for which notice of the hearing can be timely provided
- lot and dwelling residential character
- postponement of the public hearing on a neighborhood plan amendment application
- sale of beer or wine locations
- secondary setback area
- shoreline setback area
- triggering property


### 3.7. Override

**Count:** 15 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `bill_id` | str | SB-840, SB-2835, 25-1-251 |
| `created_at` | DateTime | 2025-12-21T20:32:29.678995000+00:00, 2025-12-21T20:32:29.679000000+00:00, 2025-12-21T20:32:29.679004000+00:00 |
| `effective_date` | str | 2025-09-01, 2024-01-01, 2025-12-21 |
| `exclusions` | list | [], ['none'], ['International Dark Sky standards'] |
| `jurisdiction_id` | str | texas, city-code |
| `metric` | str | density_max, height_max, setback_front_min |
| `name` | str | texas:SB-840:density, texas:SB-840:height, texas:SB-840:setback_front |
| `override_id` | str | texas:SB-840:density, texas:SB-840:height, texas:SB-840:setback_front |
| `override_type` | str | floor, ceiling |
| `override_value` | int | 36, 45, 25 |
| `scope_uses` | list | ['multifamily', 'mixed_use'], ['adjustment-application-process', 'wate, ['zoning', 'variance', 'land-use plannin |
| `scope_zones` | list | ['commercial', 'office', 'mixed_use'], [], ['city of interest'] |
| `summary` | str | Texas SB-840 density override increases , SB-840 height override sets height_max t, texas:SB-840 setback front overrides set |
| `unit` | str | units/acre, ft, spaces |

**All Override Entities (15):**

- International Dark Sky standards
- Texas Constitution
- Texas Local Government Code Chapter 212 Subchapter A (Regulation of Subdivisions)
- Texas Local Government Code Chapter 232 Subchapter A (Subdivision Platting Requirements in General)
- United States Constitution
- applicable state law
- federal statute
- texas:SB-2835:transit_density
- texas:SB-840:density
- texas:SB-840:height
- texas:SB-840:lot_area_per_unit
- texas:SB-840:parking
- texas:SB-840:setback_front
- texas:SB-840:setback_rear
- texas:SB-840:setback_side


### 3.8. DocumentSource

**Count:** 154 nodes

**Properties:**

| Property | Type | Sample Values |
|----------|------|---------------|
| `created_at` | DateTime | 2025-12-21T20:18:31.590335000+00:00, 2025-12-21T20:18:31.590398000+00:00, 2025-12-21T20:18:31.590405000+00:00 |
| `document` | str | CHAPTER 25-2. - ZONING., CHAPTER 25-1. - GENERAL REQUIREMENTS AND, CHAPTER 25-3. - TRADITIONAL NEIGHBORHOOD |
| `line_end` | int | 999, 1, 1010 |
| `line_start` | int | 1, 25, 9999 |
| `name` | str | [SECTION ID: 25-1-1010], CHAPTER 25-2 - ZONING, CHAPTER 25-3 - TRADITIONAL NEIGHBORHOOD  |
| `orphan_candidate` | bool | True |
| `section` | str | CHAPTER 25-2. - ZONING., CHAPTER 25-2. - ZONING, CHAPTER 25-3. - TRADITIONAL NEIGHBORHOOD |
| `source_id` | str | 25-1-1010, 25-1-1010|25-1-131|25-1-132|25-1-132(C), Source: Section 13-1-253(b); Ord. 990225 |
| `subsection` | str | § 25-1-1010 - RECOMMENDATION CRITERIA., null, (C) |
| `summary` | str | Recommendation criteria for Chapter 25-2, CHAPTER 25-2 - ZONING governs mixed-use , TN District (CHAPTER 25-3) is described  |
| `text_excerpt` | str | [SECTION CONTENT]
## CHAPTER 25-2. - ZON, CHAPTER 25-2. - ZONING, § 25-1-1010 - RECOMMENDATION CRITERIA.
C |

**Sample Entities (showing 10 of 154):**

1. **[SECTION ID: 25-1-1010]**
   - Recommendation criteria for Chapter 25-2 (Zoning) outlined in § 25-1-1010, referencing Chapter 25-3 (Traditional Neighborhood District)....
2. **CHAPTER 25-2 - ZONING**
   - CHAPTER 25-2 - ZONING governs mixed-use districts (CBD, DMU, LO/NO/GO ranges, LR, CR, MF, IP/MI/LI, LA, DMU, DR, PDA) in Austin, with Traditional Neig...
3. **CHAPTER 25-3 - TRADITIONAL NEIGHBORHOOD DISTRICT**
   - TN District (CHAPTER 25-3) is described within the City’s zoning framework, linked to base districts in CHAPTER 25-2 and guided by recommendation crit...
4. **Chapter 25-12 (Technical Codes)**
   - Chapter 25-12 (Technical Codes): The responsible director must give notice under Chapter 25-12 (Technical Codes) and state law of a public hearing on ...
5. **Source: Section 13-1-253(b); Ord. 990225-70; Ord. 010329-18;**
   - Source: Section 13-1-253(b); Ord. 990225-70; Ord. 010329-18; Ord. 031211-11; RECOMMENDATION CRITERIA (25-1-1010) within ZONING Chapter 25-2....
6. **Sign notifying the public of the change of location**
   - Sign notifying the public of relocation: include original hearing location, identify the hearing, state new time and location, and explain relocation ...
7. **[SECTION ID: 25-1-154]**
   - Public hearings must be recorded (audio/video) and the official record includes the recording, staff reports, and documentary evidence; records are ac...
8. **City Code Section 25-1-185**
   - City Code Section 25-1-185: On receipt of a notice of appeal or amendment, the single office must promptly notify the presiding officer of the appeal ...
9. **[SECTION ID: 25-1-186]**
   - The single office shall schedule a meeting to discuss and attempt to resolve issues raised by an appeal; all interested parties must be notified and m...
10. **[TITLE: 25-1-186]**
   - Meeting to discuss and resolve issues raised by an appeal of an administrative decision upon request by an interested party; all interested parties ma...


---

## 4. Relationship Types

### 4.1. Neo4j Relationship Types

| Type | Count |
|------|-------|
| `MENTIONS` | 5,656 |
| `RELATES_TO` | 4,116 |

### 4.2. ALL Semantic Edge Types (RELATES_TO.name)

**Total Unique Edge Types: 1196**

| Edge Type | Count |
|-----------|-------|
| `APPLIES_IN` | 587 |
| `CONTAINS` | 363 |
| `SOURCED_FROM` | 294 |
| `GOVERNED_BY` | 242 |
| `ALLOWS_USE` | 231 |
| `HAS_CONSTRAINT` | 194 |
| `REQUIRES` | 77 |
| `APPLIES_TO` | 68 |
| `DEFINES` | 65 |
| `INCLUDES` | 51 |
| `REFERENCES` | 50 |
| `HAS_CONDITION` | 32 |
| `GOVERNS_ZONE` | 22 |
| `GOVERNS` | 18 |
| `SUPERSEDES` | 15 |
| `GOVERNES_METRIC` | 14 |
| `SUPERSEDED_BY` | 13 |
| `PERMITS_TEMPORARY_USE` | 13 |
| `SOURCE_DOCUMENT` | 12 |
| `MUST_COMPLY_WITH` | 12 |
| `NOTIFIES` | 12 |
| `DEFINED_AS` | 12 |
| `PROHIBITS` | 11 |
| `OVERRIDDEN_BY` | 10 |
| `DISCUSSSES_TOPIC_WITH` | 9 |
| `Defaults` | 8 |
| `SENT_TO` | 8 |
| `LIMITS` | 8 |
| `REQUIRES_APPROVAL_IN_ORDER` | 8 |
| `MAY_FILE_APPLICATION_FOR` | 8 |
| `AUTHORIZES` | 8 |
| `ALLOWS_MIXED_USE_IN` | 8 |
| `EXEMPTS` | 8 |
| `BOUNDS` | 8 |
| `ESTABLISHED_BY` | 7 |
| `MUST_NOTIFY` | 7 |
| `REQUIRES_COMPLIANCE_WITH` | 7 |
| `ENCOURAGES_ASSESSMENT_FOR` | 7 |
| `IDENTIFIES_POTENTIAL_ISSUE` | 7 |
| `DEFINED_BY` | 7 |
| `APPLIES_TO_ZONE` | 7 |
| `DESCRIBES` | 6 |
| `REQUIRES_INFORMATION_FROM` | 6 |
| `REQUIRES_NOTICE_TO` | 6 |
| `REQUIRES_SUBMISSION_OF` | 6 |
| `MAINTAINS_COPY` | 6 |
| `HAS_ATTRIBUTE` | 5 |
| `HAS_CODE` | 5 |
| `HAS_NAME` | 5 |
| `INCLUDES_INFORMATION` | 5 |
| `APPEALABLE_TO` | 5 |
| `REVIEWS` | 5 |
| `NOT_TREATED_AS_SINGLE_APPLICATION_FOR` | 5 |
| `EXCLUDES` | 5 |
| `ADOPTS` | 5 |
| `HAS_CRITERION` | 5 |
| `HAS_PURPOSE` | 5 |
| `ALLOWED_BY` | 5 |
| `DETERMINES_NUMBER_OF_SPACES_FOR` | 5 |
| `CAN_CONVERT_TO` | 5 |
| `SOURCE_CITES` | 5 |
| `FINAL_APPROVAL_EXERCISED_BY` | 5 |
| `GIVES_NOTICE_UNDER` | 4 |
| `GIVES_NOTICE_FOR` | 4 |
| `MAY_CHARGE_CONDITIONED_ON` | 4 |
| `INVITES_TO_MEETING` | 4 |
| `MUST_ALLOW_ENTRY_FOR_INSPECTION` | 4 |
| `MAY_SUSPEND` | 4 |
| `CONSIDERS` | 4 |
| `APPLIES_FOR_PURPOSES_OF` | 4 |
| `DERIVED_FROM` | 4 |
| `WAIVER_LEVEL` | 4 |
| `REGULATES` | 4 |
| `RESPONSIBLE_FOR` | 4 |
| `PROMOTES` | 4 |
| `CONSTRAINS` | 4 |
| `PROVIDES_FOR` | 4 |
| `PROHIBITED_BY` | 4 |
| `PERMITS` | 4 |
| `ENFORCED_BY` | 4 |
| `PERMITS_AS_ACCESSORY` | 4 |
| `CLASSIFIED_BY` | 4 |
| `CLASSIFIED_AS` | 4 |
| `INCLUDES_DISTRICT` | 4 |
| `CITES_SOURCE` | 4 |
| `REQUIRES_FINAL_APPROVAL_FROM` | 4 |
| `TAKES_INTO_ACCOUNT` | 3 |
| `MAY_POST_AS` | 3 |
| `MAY_DRAW_ON` | 3 |
| `LIABLE_FOR_EXCESS_COSTS` | 3 |
| `DEFINED_IN` | 3 |
| `INCLUDES_IN_OFFICIAL_RECORD` | 3 |
| `SUSPENDS_ON_APPEAL` | 3 |
| `OVERRIDE_GOVERNS_CONSTRAINT` | 3 |
| `APPLIES_IN_ZONE_CONDITION` | 3 |
| `REQUIRES_APPROVAL_BY` | 3 |
| `FORWARDS_RECOMMENDATION_TO` | 3 |
| `PRESENTS_TO` | 3 |
| `REQUIRES_REVIEW_BY` | 3 |
| `MAY_CONFLICT_WITH` | 3 |
| `ISSUES` | 3 |
| `SUSPENSION_EFFECTIVE_UNTIL_COMPLIANCE` | 3 |
| `MAY_SUSPEND_VARIANCE_OR_EXCEPTION` | 3 |
| `HOLDS_PUBLIC_HEARING` | 3 |
| `GUIDELINES_AID_REVIEW_OF` | 3 |
| `GUIDELINES_APPLY_TO_SECTION` | 3 |
| `ALLOWS_CREDIT_TOWARD` | 3 |
| `AUTHORIZED_TO_ADOPT_RULES` | 3 |
| `TRANSFERS_WITH` | 3 |
| `HAS_NUMERIC_REQUIREMENT` | 3 |
| `REPEALED_BY` | 3 |
| `MAY_INVOLVE` | 3 |
| `MAY_INITIATE_AMENDMENT_FOR_PROPERTY` | 3 |
| `INCLUDES_REPRESENTATIVES_FROM` | 3 |
| `APPOINTED_BY` | 3 |
| `REQUIRES_APPROVAL_ORDER` | 3 |
| `TOLLS_EXPIRATION_IF_DISCRETIONARY_REVIEW_REQUIRED` | 3 |
| `MUST_RECEIVE_NOTICE_FROM` | 3 |
| `INCLUDES_IN_RECOMMENDATION` | 3 |
| `VARIANCE_FROM_RULE` | 3 |
| `MAY_REQUEST_VARIANCE_FROM` | 3 |
| `PROHIBITED_IN` | 3 |
| `WAIVER_RELATES_TO_DOCUMENT` | 3 |
| `WAIVER_APPLIES_TO_DOCUMENTS` | 3 |
| `REPLACEMENT_ALLOWED_AS_PER` | 3 |
| `MUST_NOT_BE_LOCATED_WITHIN_DISTANCE_OF` | 3 |
| `HEIGHT_LIMIT_SPECIFIED` | 3 |
| `HEIGHT_LIMIT_CONDITIONAL` | 3 |
| `PERMITTED_BY` | 3 |
| `COMBINING_DISTRICT_INCLUDES` | 3 |
| `INITIATED_BY` | 3 |
| `MAY_CONSIDER_APPLICATIONS` | 3 |
| `REQUIRES_CONSTRUCTION_OF` | 3 |
| `APPEALS_TO` | 3 |
| `REQUIRES_REGISTRATION_WITH` | 3 |
| `DEPICTS` | 3 |
| `IS_A` | 2 |
| `GIVES_NOTICE_FOR_PUBLIC_HEARING_ON_APPEAL_TO` | 2 |
| `MUST_GIVE_NOTICE_UNDER` | 2 |
| `REFERENCES_DOCUMENT` | 2 |
| `CALCULATES_FEES` | 2 |
| `REQUIRES_POSTING` | 2 |
| `DETERMINES_PAYABLE_TO` | 2 |
| `AMOUNTOF_EQUALS_ESTIMATED_COST` | 2 |
| `REQUIRES_ESTIMATE_FROM` | 2 |
| `RETURNS_IF` | 2 |
| `HOLDS_PUBLIC_HEARING_ON` | 2 |
| `PUBLISHED_NOTICE_EFFECTIVE_IN` | 2 |
| `NOTICE_REQUIRED_IF_NO_DATE_SPECIFIED` | 2 |
| `SIGN_MUST_STATE_TIME_DATE_AND_NEW_LOCATION` | 2 |
| `MAY_ESTABLISH_RULES_FOR_REVIEW` | 2 |
| `HAS_STANDING_IF` | 2 |
| `DETERMINES_STANDING` | 2 |
| `REPLACES` | 2 |
| `MUST_NOT_EXCEED` | 2 |
| `TRIGGEREDEVENT` | 2 |
| `MUST_ESTABLISH` | 2 |
| `ESTABLISHES_FEES_BY` | 2 |
| `SHALL_CALCULATE_FEES` | 2 |
| `PREPARES` | 2 |
| `RELATED_TO` | 2 |
| `CITED_IN` | 2 |
| `CLASSIFICATION_REFERENCE_TO_ZONE` | 2 |
| `DETERMINES_BASED_ON_CHARACTERISTICS_SIMILARITIES` | 2 |
| `NOTIFIES_OF_FILING_WITHIN_30_DAYS` | 2 |
| `NOTIFIES_OF_DISPOSITION_WITHIN_30_DAYS` | 2 |
| `REQUIRES_DISTANCE` | 2 |
| `HAS_MAX_WIDTH` | 2 |
| `VARIANCE_GRANTED_BY` | 2 |
| `CONSIDERS_RECOMMENDATION_FROM` | 2 |
| `EXPIRES_ON` | 2 |
| `DETERMINES` | 2 |
| `GRANTS` | 2 |
| `APPLIES_WITHIN` | 2 |
| `DISTRIBUTES_EXCEPTIONS_TO` | 2 |
| `CONTAINS_OVERRIDE` | 2 |
| `CONTROLS_IF_CONFLICT` | 2 |
| `INVITES` | 2 |
| `REQUIRES_CONTRACT_CONDITIONS_SATISFIED` | 2 |
| `REQUIRES_COMPLETION_OF` | 2 |
| `REQUIRES_CERTIFICATE_FROM` | 2 |
| `INSPECTORS_CAN_ENTER_TO_INVESTIGATE_OR_ENFORCE` | 2 |
| `MUST_PRESENT_CREDENTIALS_IF_OCCUPIED` | 2 |
| `MUST_ATTEMPT_TO_CONTACT_RESPONSIBLE_PERSON_IF UNOCCUPIED` | 2 |
| `SUSPENSION_REASON` | 2 |
| `MAY_REVOKE_OR_TAKE_ACTION` | 2 |
| `MAY_REVOKE` | 2 |
| `REFERENCES_RULE` | 2 |
| `AUTHORIZED_BY` | 2 |
| `PRESERVES` | 2 |
| `BASED_ON` | 2 |
| `CANNOT_REQUIRE_VARIANCE_UNLESS` | 2 |
| `REQUIRES_FISCAL_SURETY_PRIOR_TO` | 2 |
| `OPERATING_PROCEDURES_ESTABLISH` | 2 |
| `CAN_CONCURRENTLY_FILE` | 2 |
| `AUTHORIZES_CONCURRENT_APPLICATIONS` | 2 |
| `RECOMMENDATION_VALID_FOR` | 2 |
| `MUST_COMPLY_WITH_TIMELINES_ADOPTED_UNDER` | 2 |
| `REQUIRED_TO_POST_SIGN` | 2 |
| `MEANS` | 2 |
| `HAS_REQUIREMENT` | 2 |
| `REVIEW_AND_DETERMINE` | 2 |
| `PART_OF` | 2 |
| `TREATED_AS_SINGLE_APPLICATION_FOR` | 2 |
| `REFERS_TO` | 2 |
| `NOT_APPLICABLE_TO` | 2 |
| `REFERENCES_SOURCE` | 2 |
| `AUTHORIZED_TO_PERMIT_OMISSION` | 2 |
| `MAY_REJECT_AS_INCOMPLETE` | 2 |
| `MAY_NOT_ACCEPT_UNLESS_COMPLETE` | 2 |
| `MUST_KEEP_AND_PRODUCE` | 2 |
| `MAY_SUSPEND_IF_ISSUED_IN_ERROR` | 2 |
| `MAY_RECOMMEND_AMENDMENTS_TO` | 2 |
| `MAY_APPEAL_TO` | 2 |
| `MAKES_RECOMMENDATION_TO` | 2 |
| `DESIGNATES` | 2 |
| `LABELS` | 2 |
| `ACTS_AS` | 2 |
| `CAN_BE_FORMS_OF` | 2 |
| `ENCOURAGES` | 2 |
| `HIERARCHY_INCLUDES` | 2 |
| `ADOPTED_BY` | 2 |
| `USED_BY` | 2 |
| `FIGURE_1_2_AMENDMENTS_REFLECTED_IN` | 2 |
| `WAIVES_FEE_FOR` | 2 |
| `REFUNDS_FEES_FOR` | 2 |
| `REQUIRES_DETERMINATION_BY` | 2 |
| `EXCLUDES_FEES_FOR` | 2 |
| `REMAINDER_RULE_FOR` | 2 |
| `MAY_EXCEED` | 2 |
| `CONSTRAINED_BY` | 2 |
| `APPLICANT_MAY_APPEAL_TO` | 2 |
| `NO_REQUIREMENT_FOR` | 2 |
| `CAN_CONVERT_TO_LIMITED` | 2 |
| `EXCEPTS_MAX_SETBACK_ON` | 2 |
| `ALLOWS_MAX_SETBACK_FOR` | 2 |
| `NO_MAX_SETBACK_FOR` | 2 |
| `PROTECTS_ENTITY` | 2 |
| `REQUIRES_MIN_DISTANCE_FROM` | 2 |
| `EXCLUDES_ZONE` | 2 |
| `DOES_NOT_APPLY` | 2 |
| `DOES_NOT_APPLY_INSTEAD_OF` | 2 |
| `MAY_SUBMIT_WAIVER_APPLICATION` | 2 |
| `DIRECTOR_GIVES_NOTICE_OF` | 2 |
| `OVERRIDES` | 2 |
| `MUST_NOTIFY_DIRECTOR_OF_CESSATION` | 2 |
| `MUST_REMOVE_TOWER_IF_UNUSED_FOR_ONE_YEAR` | 2 |
| `DISTANCE_REQUIREMENT_FROM` | 2 |
| `CONSTRAINT_ON` | 2 |
| `PROHIBITED` | 2 |
| `REQUIRES_APPROVAL_FROM` | 2 |
| `ALLOWS_SALE_FROM` | 2 |
| `MAINTAINS` | 2 |
| `PROHIBITS_ACTIVITY` | 2 |
| `APPLIES_FOR` | 2 |
| `MAY_FILE_APPLICATION_WITH` | 2 |
| `APPLICATION_MUST_INCLUDE` | 2 |
| `EXCLUDES_USE` | 2 |
| `MAY_BE_PART_OF` | 2 |
| `LISTS_AS_PERMITTED_ACCESSORY` | 2 |
| `GOVERNS_USE_ON_SUBSTANDARD_LOT` | 2 |
| `APPLIES_IN_ZONE` | 2 |
| `APPEAL_TO` | 2 |
| `INCLUDES_USE_TYPE` | 2 |
| `MAY_REQUEST_RECOMMENDATION` | 2 |
| `PROVIDES_OPTION` | 2 |
| `SETS_MAX` | 2 |
| `CATEGORIZES_AS` | 2 |
| `APPLIES_TIME_PERIOD_FOR` | 2 |
| `PROVIDES_NOTICE_UNDER` | 2 |
| `DISCRETIONARY_REVIEW_BY` | 2 |
| `DISCRETIONARY_REVIEW_EXCLUDES` | 2 |
| `SECTION_REFERENCES` | 2 |
| `MUST_RELATE_CONDITION_TO` | 2 |
| `NOTICE_REQUIRED_BY` | 2 |
| `PROTECTS` | 2 |
| `ALLOWS_APPEAL_TO` | 2 |
| `DEFINITION_OF` | 2 |
| `EQUIVALENT_TO` | 2 |
| `REQUIRES_AUTHORITY_CITATION` | 2 |
| `APPEAL_TARGET` | 2 |
| `PROHIBITS_ERECTING_OR_IMPROVING` | 2 |
| `MUST_ACT` | 2 |
| `COORDINATES_WITH` | 2 |
| `ASSIGNS_AUTHORITY` | 2 |
| `REQUIRES_ENFORCEMENT_BY` | 2 |
| `REQUIRES_COORDINATION_WITH` | 2 |
| `ASSOCIATED_WITH` | 2 |
| `SOURCE_DOCUMENT_FOR_SECTION` | 1 |
| `COLLECTS_FEES` | 1 |
| `APPROVAL_REQUIRED_FROM` | 1 |
| `USES_IN` | 1 |
| `MAY_APPROVE_PLAT_ONLY_IF` | 1 |
| `MAY_REQUIRE_CONSTRUCTION_OF` | 1 |
| `MAY_PROVIDE_FISCAL_SECURITY` | 1 |
| `MAY_USE_FISCAL_SECURITY_TO_CONSTRUCT` | 1 |
| `GIVES_NOTICE_TO` | 1 |
| `APPLIES_WITH_OVERRIDE` | 1 |
| `GIVES_NOTICE_OF_FILING` | 1 |
| `CONDUCTS_COMMUNITY_MEETING_FOR` | 1 |
| `RESPONSIBLE_FOR_COST_OF_NOTICE` | 1 |
| `CITY_RESPONSIBLE_FOR_COST_FOR_CONTACT_TEAM` | 1 |
| `GIVES_NOTICE_TO_PROPERTY_OWNERS_WITHIN_BOUNDARIES` | 1 |
| `GIVES_NOTICE_TO_CITY_UTILITY_ADDRESSES_WITHIN_BOUNDARIES` | 1 |
| `GIVES_NOTICE_TO_NEIGHBORHOOD_ORGS_WITHIN_AND_WITHIN_500FT` | 1 |
| `APPLIES_WITHIN_DISTANCE` | 1 |
| `MAILED_NOTICE_EFFECTIVE_VIA` | 1 |
| `MAILED_TO_APPLICANT` | 1 |
| `MAILED_TO_PROPERTY_OWNER` | 1 |
| `MAILED_TO_AGENT` | 1 |
| `SENT_BY_MAIL_TO_RECORD_OWNER` | 1 |
| `MAILED_TO_NEIGHBORHOOD_ORGANIZATION` | 1 |
| `CERTIFIED_MAIL_REQUIRED_IF` | 1 |
| `HAND_DELIVERY_SUBSTITUTION_FOR` | 1 |
| `SINGLE_OFFICE_PREPARES_LIST_OF` | 1 |
| `APPLICANT_PROVIDES_LIST_IF_TAX_DB_INACCESSIBLE` | 1 |
| `SINGLE_OFFICE_NOTIFIES_NEIGHBORHOOD_ORGANIZATION_OF_APPLICATION` | 1 |
| `SINGLE_OFFICE_NOTIFIES_NEIGHBORHOOD_ORGANIZATION_OF_AMENDMENT` | 1 |
| `SECTION_SOURCED_FROM` | 1 |
| `DIVISION_APPLIES_TO` | 1 |
| `DIVISION_APPLIES_TO_COUNCIL` | 1 |
| `MUST_REGISTER_TO_SPEAK_WITH` | 1 |
| `REGISTERS_TO_SPEAK_FOR_HEARING_CONDUCTED_BY` | 1 |
| `SPEAKER_REGISTRATION_IDENTIFIES` | 1 |
| `SPEAKER_REGISTRATION_IDENTIFIES_MATTER` | 1 |
| `SPEAKER_MUST_STATE_NAME_TO` | 1 |
| `HEARING_PROCEDURE_INCLUDES_REPORT_BY` | 1 |
| `HEARING_PROCEDURE_INCLUDES_PRESENTATION_BY` | 1 |
| `HEARING_PROCEDURE_INCLUDES_SUPPORTING_PARTY_PRESENTATION` | 1 |
| `HEARING_PROCEDURE_INCLUDES_OPPOSING_PARTY_PRESENTATION` | 1 |
| `APPLICANT_HAS_REBUTTAL_RIGHT_IN` | 1 |
| `MEMBER_MAY_ASK_QUESTIONS_OF` | 1 |
| `PERSON_MAY_ASK_QUESTION_OF_WITH_APPROVAL_OF` | 1 |
| `BODY_MAY_LIMIT_SPEAKER_TIME` | 1 |
| `PRESIDING_OFFICER_MAY_REQUEST_REMOVE_REPETITIOUS_TESTIMONY_FROM` | 1 |
| `BODY_MAY_POSTPONE_HEARING_BY_ANNOUNCING_ON` | 1 |
| `BODY_MAY_CONTINUE_HEARING_TO_LATER_DATE_BY_ANNOUNCING_AFTER_BEGINNING` | 1 |
| `CONTINUANCE_ANNOUNCEMENT_WITHIN_60_DAYS_IS_ADEQUATE_NOTICE` | 1 |
| `NEXT_HEARING_USUALLY_HELD_AT_SAME_LOCATION_AS_ORIGINAL` | 1 |
| `MAY_POSTPONE_HEARING` | 1 |
| `MAY_CONTINUE_HEARING` | 1 |
| `MAY_CHANGE_LOCATION_FOR_GOOD_CAUSE` | 1 |
| `MUST_POST_SIGN_NOTIFYING_PUBLIC` | 1 |
| `MUST_PROVIDE_REASONABLE_TRAVEL_TIME` | 1 |
| `SHALL_POST_SIGN_NOTIFYING_PUBLIC_OF_CHANGE` | 1 |
| `SIGN_MUST_BE_DISPLAYED_AT_ORIGINAL_LOCATION_AT_TIME_OF_HEARING` | 1 |
| `SIGN_MUST_IDENTIFY_HEARING_BEING_RELOCATED` | 1 |
| `SIGN_MUST_PROVIDE_EXPLANATION_FOR_RELOCATION` | 1 |
| `MAY_REVIEW_OFFICIAL_RECORD` | 1 |
| `RECORDS` | 1 |
| `MAY_REVIEW` | 1 |
| `FILES_APPEAL_WITH` | 1 |
| `APPEAL_DEADLINE_AFTER_DECISION_OF` | 1 |
| `APPEAL_DEADLINE_AFTER` | 1 |
| `APPEAL_DEADLINE_AS_SPECIFIED_BY` | 1 |
| `MAY_APPROVE` | 1 |
| `REQUIRES_REVIEW_OF` | 1 |
| `MAY_SUBMIT_ADDENDUM` | 1 |
| `MUST_NOT_EXCEED_BY_MORE_THAN` | 1 |
| `MUST_NOT_BE_LESS_THAN_UNLESS_APPROVED_BY` | 1 |
| `MUST_NOT_BE_MORE_INTENSE_THAN` | 1 |
| `MUST_NOT_CHANGE_CONDITION_OF_APPROVAL` | 1 |
| `MAY_APPEAL_DETERMINATION_TO` | 1 |
| `MAY_APPEAL_DECISION_TO` | 1 |
| `REQUIRES_FORM` | 1 |
| `NOTIFIES_WHEN_THERE_IS` | 1 |
| `RELATION` | 1 |
| `SCHEDULE_MEETING_FOR_APPEAL_IF_REQUESTED` | 1 |
| `NOTIFY_INTERESTED_PARTIES_OF_MEETING` | 1 |
| `ALL_MAY_ATTEND_MEETING` | 1 |
| `SUSPENDS_ON_TIMELY_APPEAL` | 1 |
| `DEVELOPMENT_PROHIBITED_PENDING_APPEAL_DECISION` | 1 |
| `DEVELOPMENT_MAY_NOT_OCCUR_PENDING_APPEAL` | 1 |
| `PUBLIC_HEARING_SCHEDULED_FOR_FIRST_AVAILABLE_MEETING` | 1 |
| `COLLECTS_FEES_FOR` | 1 |
| `PERMITTED_FORMS` | 1 |
| `DESCRIBED_BY` | 1 |
| `DOCUMENTED_AS` | 1 |
| `GIVES_NOTICE_UNDER_SOURCE_FOR_BOARD_HEARING` | 1 |
| `GIVES_NOTICE_OF_MEETING_UNDER` | 1 |
| `CITY_PAYS_COST_OF_NOTICE_FOR_CONTACT_TEAM` | 1 |
| `DIRECTOR_GIVES_NOTICE_TO_NRO_AND_CONTACT_TEAMS_WITHIN_500FT` | 1 |
| `DISTANCE_CONSTRAINT_APPLIES_TO` | 1 |
| `ALLOWS_SUBSTITUTION` | 1 |
| `REQUIRES_PROVISION_FROM` | 1 |
| `REGISTERS_WITH` | 1 |
| `MAY_SPEAK_WITH_PERMISSION` | 1 |
| `REGISTRATION_IDENTIFIES` | 1 |
| `HEARING_PROCEDURE_INCLUDES` | 1 |
| `MAY_ASK_QUESTIONS_OF` | 1 |
| `PERSON_MAY_ASK_WITH_APPROVAL` | 1 |
| `MAY_POSTPONE` | 1 |
| `MAY_CONTINUE` | 1 |
| `MAY_CHANGE_LOCATION` | 1 |
| `SIGN_IDENTIFIES_HEARING_AND_NEW_LOCATION` | 1 |
| `CHANGE_REQUIRES_REASON` | 1 |
| `NEXT_HEARING_AT_SAME_LOCATION_UNLESS_CHANGED` | 1 |
| `MAY_CHANGE_LOCATION_OF` | 1 |
| `SIGN_MUST_BE_DISPLAYED_AT_ORIGINAL_LOCATION` | 1 |
| `SIGN_MUST_IDENTIFY_HEARING` | 1 |
| `SIGN_MUST_PROVIDE_EXPLANATION` | 1 |
| `HEARING_SHALL_BE_POSTPONED_TO_ALLOW_TRAVEL` | 1 |
| `MUST_RECORD_HEARING` | 1 |
| `PERSON_MAY_REVIEW_RECORD` | 1 |
| `ALLOWS_REVIEW_BY` | 1 |
| `HAS_STANDING_TO_APPEAL_IF` | 1 |
| `FILE_APPEAL_WITH` | 1 |
| `INCLUDES_ENTITY` | 1 |
| `MAY_APPROVE_REPLACEMENT_SITE_PLAN` | 1 |
| `REQUIRES_MINIMUM_TREE_CALIPER_UNLESS_APPROVED_BY` | 1 |
| `MUST_NOT_CHANGE_CONDITION_OF_APPROVAL_OF` | 1 |
| `MAY_APPEAL_DIRECTOR_DETERMINATION_TO` | 1 |
| `MAY_APPEAL_LAND_USE_COMMISSION_DECISION_TO` | 1 |
| `LIMITS_CONTENT_OF_APPELLANT_STATEMENT` | 1 |
| `REQUIRES_TRAFFIC_IMPACT_ANALYSIS_VALIDITY_OR_ADDENDUM` | 1 |
| `MAY_ATTEND_MEETING` | 1 |
| `DEVELOPMENT_HALTED_BY` | 1 |
| `SUSPENDED_ON` | 1 |
| `DEVELOPMENT_PROHIBITED_PENDING` | 1 |
| `SCHEDULED_FOR` | 1 |
| `REQUIRES_NOTICE_FOR_SCHEDULING` | 1 |
| `CONTRARY_TO` | 1 |
| `DECIDES_WHETHER_TO_POSTPONE_OR_CONTINUE_HEARING_FOR` | 1 |
| `HEARING_ORDER_INCLUDES_COMMENT_BY_SUPPORTERS` | 1 |
| `HEARING_ORDER_INCLUDES_COMMENT_BY_OPPONENTS` | 1 |
| `HEARING_ORDER_INCLUDES_REBUTTAL_BY` | 1 |
| `EXERCISES_POWER_OF` | 1 |
| `MAY_UPHOLD_MODIFY_OR_REVERSE_DECISION_OF` | 1 |
| `MAY_EXERCISE_POWER_OF` | 1 |
| `MAY_EXERCISE_POWER_IN_ACCORDANCE_WITH` | 1 |
| `SOURCE_DOCUMENT_FOR` | 1 |
| `DETERMINES_USE_CLASSIFICATION_FOR` | 1 |
| `WORKS_IN_DEPARTMENT` | 1 |
| `MAY_REQUEST_USE_DETERMINATION` | 1 |
| `MAINTAINS_LIST_OF` | 1 |
| `CAN_BE_ATTACHED_BY` | 1 |
| `EXEMPTION_CONDITION` | 1 |
| `LIMITS_EXEMPTION_PER_SITE` | 1 |
| `ALLOWS_ADDITIONAL_EXEMPTION` | 1 |
| `EXCLUDES_IF_NOT_ACCESSIBLE_BY_AUTOMOBILE` | 1 |
| `EXCLUDES_IF_BELOW_GRADE_AND_WITHIN_FOOTPRINT` | 1 |
| `EXCLUDES_IF_ATTIC_CONDITIONS_MET` | 1 |
| `MEASURES_AREA_ON` | 1 |
| `MEASURES_HEIGHT_TO` | 1 |
| `COUNTS_TWICE` | 1 |
| `ALLOWS_USE_APPLICATION_FOR_VARIANCE` | 1 |
| `MAY_REQUEST_VARIANCES_FROM_REGULATIONS_APPLICABLE_TO_SITE` | 1 |
| `MAY_REQUEST_VARIANCES_ON_ADJACENT_PARCELS` | 1 |
| `SHALL_PREPARE_REPORT_FOR` | 1 |
| `CONSIDERED_BY` | 1 |
| `REQUIRES_APPROVAL_BEFORE` | 1 |
| `VARIANCE_REQUIRED_FOR` | 1 |
| `APPROVAL_BY` | 1 |
| `EXEMPTS_LAND_USE_COMMISSION_TIMELINE` | 1 |
| `RELATES_TO_DOCUMENT` | 1 |
| `PROHIBITS_FILING_FOR_PERIOD` | 1 |
| `PROHIBITS_FILING_SAME_OR_SIMILAR_VARIANCE` | 1 |
| `PROHIBITS_FILING_ON_SAME_SITE` | 1 |
| `APPLIES_TO_VARIANCE` | 1 |
| `REQUIRES_VOTE` | 1 |
| `ADVISES` | 1 |
| `REQUIRES_VOTE_THRESHOLD` | 1 |
| `IF_NOT_AFFIRMATIVE_THEN` | 1 |
| `DETERMINES_MINIMUM_ADJUSTMENT` | 1 |
| `CAN_APPROVE` | 1 |
| `REQUIRES_CERTIFICATION` | 1 |
| `REQUIRES_ELIGIBLE_RESPONSIBLE_PERSON` | 1 |
| `REQUIRES_CERTIFICATE_OF_OCCUPANCY` | 1 |
| `MUST_INCLUDE_CONDITIONS` | 1 |
| `MUST_NOTE_PRECONSTRUCTION_CONFERENCE` | 1 |
| `AUTHORIZES_CITY_TO_DRAW_ON_SURETY` | 1 |
| `REQUIRES_OTHER_APPROVALS` | 1 |
| `EXPIRES_IF_SITE_PLAN_DENIED` | 1 |
| `MAY_REVOKE_IF_NONCOMPLIANT` | 1 |
| `DISTRIBUTES_TO` | 1 |
| `EXCHANGES_CONTACT_INFO_WITH` | 1 |
| `DISCUSS_TOPICS_WITH` | 1 |
| `PREPARES_AND_DISTRIBUTES` | 1 |
| `MAY_FILE_EXCEPTIONS_TO` | 1 |
| `INCLUDES_IN` | 1 |
| `PREPARES_AND_DISTRIBUTES_MINUTES_FOR` | 1 |
| `DELIVERS` | 1 |
| `COORDINATES_CONTACT_BETWEEN` | 1 |
| `REQUESTS_INSPECTION_FROM` | 1 |
| `REQUIRES_REQUEST_TIME` | 1 |
| `MAINTAINS_RECORDS_FOR` | 1 |
| `MUST_POST_BEFORE_BEGINNING_WORK` | 1 |
| `MUST_POST_IN_LOCATION` | 1 |
| `NOTES_INSPECTION_ON` | 1 |
| `MUST_KEEP_POSTED_UNTIL` | 1 |
| `INDICATES_COMPLETION_FOR` | 1 |
| `REQUIRES_REQUEST_FOR_INSPECTION` | 1 |
| `SCHEDULES_INSPECTION` | 1 |
| `PRESENTS_PLAN_TO` | 1 |
| `MAY_MODIFY_WITH_NOTICE` | 1 |
| `MAY_MAKE_MINOR_CHANGES_TO` | 1 |
| `MAY_CHARGE_REINSPECTION_FEE_IF` | 1 |
| `EXEMPTS_FROM_REINSPECTION_FEE` | 1 |
| `PROHIBITS_INSPECTIONS_UNTIL_FEE_PAID` | 1 |
| `MAY_REINSPECT_WITHOUT_FEE` | 1 |
| `MUST_SUBMIT_REPORT` | 1 |
| `RELATES_TO_ZONE` | 1 |
| `TEXT_OVERRIDES_ILLUSTRATION` | 1 |
| `DELIVERS_ENTITY` | 1 |
| `SUBMITS` | 1 |
| `REPORTS_REQUIRE_FINAL_ACCEPTANCE_FROM` | 1 |
| `SUMMARY_REPORT_DOCUMENTS` | 1 |
| `FINAL_ACCEPTANCE_ISSUED_BY` | 1 |
| `REQUIRED_TO_REVIEW` | 1 |
| `REQUIRED_TO_SCHEDULE_MEETING` | 1 |
| `MAY_NOT_ISSUE_UNTIL` | 1 |
| `REQUIRES_IF_REQUIRED` | 1 |
| `REQUIRES_IF_APPLICABLE` | 1 |
| `ISSUES_TO` | 1 |
| `ISSUES_LIST_IF_NOT_SATISFIED` | 1 |
| `PROHIBITS_USE_UNTIL` | 1 |
| `APPLIES_AT_SITE` | 1 |
| `REQUIRES_PASSED_INSPECTIONS` | 1 |
| `REQUIRES_COMPLETION_IN_ACCORDANCE_WITH` | 1 |
| `REQUIRES_FINAL_ACCEPTANCE_OR_DEVELOPER_AGREEMENT` | 1 |
| `ACCOUNTABLE_OFFICIAL_SIGNATURE_REQUIRED_FOR` | 1 |
| `OWNER_MUST_SATISFY_FOR` | 1 |
| `SHALL_HOLD_HEARING` | 1 |
| `HEARING_DEADLINE_REFERENCES` | 1 |
| `REVOCATION_EFFECTIVE_IMMEDIATELY` | 1 |
| `REQUIRES_HEARING` | 1 |
| `SHALL_HOLD_HEARING_WITHIN_DAYS` | 1 |
| `REVOKE_EFFECTIVE_IMMEDIATELY` | 1 |
| `MAY_IMMEDIATELY_REVOKE_PLAN` | 1 |
| `NOTICE_SPECIFIES_TIME_FOR_COMPLIANCE` | 1 |
| `NOTICE_LIMITS_SUSPEND_OR_REVOKE_BEFORE_EXPIRATION` | 1 |
| `MAY_GIVE_NOTICE_TO` | 1 |
| `MAY_SUSPEND_OR_REVOKE_BEFORE_TIME_FOR_COMPLIANCE_PROHIBITED` | 1 |
| `SHALL_GIVE_NOTICE_BY_CERTIFIED_MAIL_UNDER` | 1 |
| `IS_LINKED_TO_RULE` | 1 |
| `SHALL_HOLD_PUBLIC_HEARING_BY` | 1 |
| `SHALL_GIVE_NOTICE_UNDER` | 1 |
| `PROHIBITS_INSPECTION_DURING_STOP_WORK` | 1 |
| `PROHIBITS_UTILITY_CONNECTION_DURING_STOP_WORK` | 1 |
| `REQUIRES_REINSPECTION_AFTER_FAILED_INSPECTION` | 1 |
| `REQUIRES_DIRECTOR_CLEARANCE_FOR_HAZARD` | 1 |
| `POSTS_AND_MAILS_STOP_WORK_ORDER` | 1 |
| `APPEAL_RIGHT_AGAINST_STOP_WORK` | 1 |
| `HEARS_APPEAL` | 1 |
| `ALLOWS_TESTIMONY_IN_APPEAL` | 1 |
| `ALLOWS_DEPARTMENT_TESTIMONY_IN_APPEAL` | 1 |
| `DECIDES_APPEAL_WITHIN_TWO_WORKING_DAYS` | 1 |
| `MAINTAINS_STOP_WORK_DURING_APPEAL` | 1 |
| `MENTIONS` | 1 |
| `ALLOWS_INITIATION_ON_BEHALF_OF` | 1 |
| `EXCLUSIVE_INITIATION_FOR_COUNTY` | 1 |
| `MAY_AMEND_AFTER_HEARING` | 1 |
| `REQUIRES_RECOMMENDATION_FROM` | 1 |
| `EXCEPTION_REFERENCES` | 1 |
| `CAUSES` | 1 |
| `REQUIRED_TO_REVIEW_WITHIN` | 1 |
| `REVIEWS_UNDER` | 1 |
| `MAY_APPROVE_AS` | 1 |
| `MAY_DENY` | 1 |
| `MAY_APPROVE_IN_PART` | 1 |
| `DETERMINATION_FINAL_FOR_RECONSIDERATION` | 1 |
| `DOES_NOT_AFFECT_AVAILABILITY_OF` | 1 |
| `SHALL_MAKE_AVAILABLE_ON` | 1 |
| `RELATES_TO` | 1 |
| `REFERENCES_EXPIRATION_RULES_IN` | 1 |
| `MAY_ADOPT` | 1 |
| `GUIDELINES_ADDRESS_QUESTIONS_ABOUT` | 1 |
| `GUIDELINES_HELP_DETERMINE` | 1 |
| `GUIDELINES_POSTED_ON` | 1 |
| `CONDITIONAL_ON` | 1 |
| `PROVIDES_MECHANISM_FOR` | 1 |
| `MUST_EXCLUDE_JURISDICTION` | 1 |
| `MAY_BE_SUBMITTED_AFTER_FIRST_PERMIT_BUT_NO_LATER_THAN` | 1 |
| `MUST_COMPLY_WITH_REGULATIONS_OR_PROVIDE_BENEFITS` | 1 |
| `DIRECTOR_SHALL_SCHEDULE_HEARING_AND_NOTIFY_UNDER` | 1 |
| `DIRECTOR_SHALL_CONSIDER_RECOMMENDATION_FROM` | 1 |
| `MAY_ESTABLISH_EXPIRATION_PERIOD_FOR` | 1 |
| `TREATS_PROJECT_AS_VESTED_TO` | 1 |
| `APPLIES_TO_USE_TYPE` | 1 |
| `MUST_NOT_IMPEDE` | 1 |
| `GUIDELINES_NOT_REQUIRED_TO_BE_ADOPTED_BY_RULE` | 1 |
| `OVERWRITES` | 1 |
| `REQUIRES_DEDICATION` | 1 |
| `REQUIRES_FEE` | 1 |
| `REQUIRES_DEDICATION_AND_REDUCED_FEE` | 1 |
| `CONSIDERS_CONNECTIVITY` | 1 |
| `USES_FORMULA_TO_DETERMINE` | 1 |
| `FORMULA_INCLUDES` | 1 |
| `PRORATES_FOR` | 1 |
| `AUTHORIZED_TO` | 1 |
| `EXCLUDES_FEATURES_FROM_COUNTING_AS` | 1 |
| `ALLOWS_PRIVATE_PARKLAND_OUTSIDE_CITY_IF_MEETS_STANDARDS` | 1 |
| `REQUIRES_RECORDING_OF` | 1 |
| `STANDARDS_REFERENCED` | 1 |
| `REQUIRED_TO_ADOPT_BY_RULE_UNDER` | 1 |
| `PARKLAND_MAP_ILLUSTRATES_SHORTAGES` | 1 |
| `OPERATING_PROCEDURES_DETERMINE_METHODOLOGY_FOR` | 1 |
| `MUST_PRESENT_TO_FOR_RECOMMENDATION` | 1 |
| `BASED_ON_INFORMATION_FROM` | 1 |
| `BASED_ON_REQUIREMENTS_AT_TIME_OF` | 1 |
| `INCLUDES_EXPLANATION_OF` | 1 |
| `INCLUDES_ESTIMATE_OF` | 1 |
| `MAY_REQUEST_ASSESSMENT` | 1 |
| `ASSESSMENT_BASED_ON` | 1 |
| `INCLUDES_PROCEDURE_INFO` | 1 |
| `INCLUDES_FEE_ESTIMATE` | 1 |
| `CHECKS_COMPREHENSIVE_PLAN_CONFORMITY` | 1 |
| `DEFINES_SUBDIVISION_AS` | 1 |
| `PROJECT_ASSESSMENT_BASED_ON` | 1 |
| `PROJECT_ASSESSMENT_INCLUDES_PROCEDURES` | 1 |
| `PROJECT_ASSESSMENT_IDENTIFIES_ISSUES` | 1 |
| `DELIVERY_TIMEFRAME_SET_BY` | 1 |
| `MAY_UPDATE_AND_RESUBMIT` | 1 |
| `MAY_PROVIDE_REPORT` | 1 |
| `MAY_RECEIVE_REPORT` | 1 |
| `CANNOT_BE_UPDATED_AFTER_EXPIRATION` | 1 |
| `SIGN_DESCRIBES_APPLICATION_AND_POTENTIAL_RELOCATION` | 1 |
| `SIGN_PLACED_AT_MAIN_ENTRANCE` | 1 |
| `DIRECTOR_APPROVES_SIGN_FORM` | 1 |
| `SIGN_MUST_REMAIN_UNTIL_MULTI_FAMILY_REDEVELOPMENT_STARTS` | 1 |
| `SIGN_MUST_REMAIN_UNTIL_MOBILE_HOME_PARK_CONDITION` | 1 |
| `LANDOWNER_MUST_NOTIFY_NEW_TENANT` | 1 |
| `QUALIFIES_AS` | 1 |
| `IS_ELIGIBLE_FOR` | 1 |
| `MAY_NOT_DISCRIMINATE_ON_BASIS_OF` | 1 |
| `LOCATED_NEAR` | 1 |
| `REQUIRES_ACTION_TOWARD` | 1 |
| `MUST_PROVIDE_RELOCATION_BENEFITS_UNDER` | 1 |
| `MUST_OFFER` | 1 |
| `HAS_AUTHORITY_OVER` | 1 |
| `DEFINES_ROLE` | 1 |
| `DEFINES_TERM` | 1 |
| `INVOLVES` | 1 |
| `MAY_FILE_UPDATE` | 1 |
| `UNTIL_EXPIRED_UNDER` | 1 |
| `REQUIRES_DILIGENT_ACTION` | 1 |
| `MAY_EXTEND_REVIEW_PERIOD_FOR` | 1 |
| `REQUIRES_REQUEST_FROM` | 1 |
| `MUST_DECIDE_WITHIN_EXTENDED_PERIOD` | 1 |
| `MUST_APPROVE_WITHIN_30_DAYS` | 1 |
| `EXTENSION_REFERENCES` | 1 |
| `CONDITION_MUST_RELY_ON` | 1 |
| `CONDITION_MUST_CITE` | 1 |
| `REQUIRES_PAYMENT_AND_INFORMATION` | 1 |
| `CERTIFICATION_VALIDITY` | 1 |
| `REJECTION_CONDITION_MULTI_FAMILY` | 1 |
| `REJECTION_CONDITION_MOBILE_HOME_PARK` | 1 |
| `SUBJECT_TO_NOTIFICATION_REQUIREMENTS` | 1 |
| `TIMELINE_CONSISTENCY_REQUIRED` | 1 |
| `REQUIRES_PUBLIC_HEARING_WITHIN_DAYS` | 1 |
| `REQUIRES_NOTICE_BY_DIRECTOR` | 1 |
| `NOTICE_METHOD_FOR_SITE_SPECIFIC_AGREEMENT` | 1 |
| `NOTICE_METHOD_FOR_MASTER_PLAN_AGREEMENT` | 1 |
| `MAY_AUTHORIZE_EXECUTION` | 1 |
| `MAY_AUTHORIZE_EXECUTE_MODIFIED_AGREEMENT` | 1 |
| `MAY_AUTHORIZE_NEGOTIATION_SUBJECT_TO_REVIEW` | 1 |
| `MAY_AUTHORIZE_REJECTION_AND_DISCONTINUATION` | 1 |
| `REFERENCES_NOTICE_RULE` | 1 |
| `REFERENCES_MAILING_RULE` | 1 |
| `REFERENCES_NOTICE_RULE_FOR_MASTER_PLAN` | 1 |
| `CONFLICT_RULES` | 1 |
| `ENTRY_MUST_BE_REASONABLE_TIME` | 1 |
| `PRESENT_CREDENTIALS_IF_OCCUPIED` | 1 |
| `ATTEMPT_CONTACT_IF_UNOCCUPIED` | 1 |
| `FAILURE_TO_PRODUCE_EVIDENCE` | 1 |
| `MUST_IDENTIFY_CONTACT` | 1 |
| `FAILURE_TO_PRODUCE_PERMIT_EVIDENCE` | 1 |
| `MAY_SUSPEND_RIGHT_OF_WAY_PERMIT` | 1 |
| `MAY_REQUEST_REVIEW` | 1 |
| `MAY_REQUIRE_INVESTIGATION_FEE` | 1 |
| `NOTICE_OF_HEARING_BY_DIRECTOR` | 1 |
| `MAY_REVOKE_IMMEDIATELY_AFTER_SUSPENSION` | 1 |
| `NOTICE_MAY_SPECIFY_COMPLIANCE_TIME` | 1 |
| `NOTICE_BY_CERTIFIED_MAIL` | 1 |
| `MAY_ORDER_STOP_WORK` | 1 |
| `STOP_WORK_PROHIBITS_INSPECTION_AND_WORK` | 1 |
| `STOP_WORK_PROHIBITS_UTILITY_CONNECTION` | 1 |
| `STOP_WORK_FOR_FAILED_INSPECTION` | 1 |
| `STOP_WORK_FOR_HEALTH_SAFETY_HAZARD` | 1 |
| `RIGHT_OF_WAY_STOP_WORK_REQUIREMENTS` | 1 |
| `RIGHT_OF_WAY_STOP_WORK_REMEDIES` | 1 |
| `STOP_WORK_ORDER_POSTED_AND_MAILED` | 1 |
| `MAY_ORDER_REMOVE_OR_RESTORE_EQUIPMENT` | 1 |
| `REMOVE_OR_RESTORE_ORDER_REQUIREMENTS` | 1 |
| `PROHIBITS_USE_AFTER_ORDER` | 1 |
| `APPEAL_DEADLINE_FOR_ORDERS` | 1 |
| `APPEAL_HEARING_TIMELINE` | 1 |
| `FURTHER_APPEAL_TO_COMMISSION_OR_BOARD` | 1 |
| `COMMISSION_HEARING_SCHEDULE_AND_AUTO_GRANT` | 1 |
| `ORDINAL_OFFENSE_PER_DAY` | 1 |
| `MISDEMEANOR_PENALTY` | 1 |
| `TECHNICAL_CODES_PENALTIES` | 1 |
| `ONLY_ENTITY_OTHER_THAN_CITY_COUNCIL_MAY_INITIATE_AMENDMENT` | 1 |
| `AMENDMENT_TO_ZONING_MAP_INITIATED_IN_ACCORDANCE_WITH` | 1 |
| `PLANNING_COMMISSION_REVIEW_REQUIRED_FOR_PROPOSED_AMENDMENT_UNLESS` | 1 |
| `TECHNICAL_CODE_REVIEW_BY_APPROPRIATE_TECHNICAL_BOARD_REQUIRED` | 1 |
| `HISTORIC_ZONING_REVIEW_BY_HISTORIC_LANDMARK_COMMISSION_REQUIRED_BEFORE_PLANNING_COMMISSION` | 1 |
| `HISTORIC_LANDMARK_COMMISSION_FORWARDS_RECOMMENDATION_TO` | 1 |
| `ADMINISTERS` | 1 |
| `WAIVES_FEES_ELIGIBILITY` | 1 |
| `REQUIRES_AFFORDABILITY_PERIOD_FOR_OWNER_OCCUPIED` | 1 |
| `REQUIRES_AFFORDABILITY_PERIOD_FOR_RENTAL` | 1 |
| `MAY_ADOPT_GUIDELINES` | 1 |
| `MAY_WAIVE_TRANSIT_REQUIREMENT` | 1 |
| `MUST_ADOPT_PROGRAM` | 1 |
| `DEPOSITS_TO` | 1 |
| `ADMINISTERS_FUND` | 1 |
| `MAY_USE_FUND_FOR` | 1 |
| `MUST_INCLUDE_LEASE_PROVISIONS` | 1 |
| `CERTIFIES` | 1 |
| `REQUIRES_AGREEMENT` | 1 |
| `IS_COMPOSED_OF` | 1 |
| `QUALIFIES_AS_INTERESTED_PARTY` | 1 |
| `MAY_WAIVE_FEES_FOR` | 1 |
| `SHALL_FORM` | 1 |
| `MAY_SUBMIT_RECOMMENDATION_TO` | 1 |
| `MAY_FORWARD_APPLICATION_TO` | 1 |
| `SHALL_HOLD_PUBLIC_HEARING_NOT_LATER_THAN` | 1 |
| `MUST_MEET_CRITERIA_TO_RECOMMEND` | 1 |
| `MAY_REMOVE_RECOGNITION_OF` | 1 |
| `REGISTERS_IN` | 1 |
| `SCHEDULES_HEARING` | 1 |
| `HOLDS_PUBLIC_HEARING_FOR` | 1 |
| `RECOMMENDS_AMENDMENTS_TO` | 1 |
| `INITIATES_AMENDMENT_PROCESS` | 1 |
| `IS_USED_FOR` | 1 |
| `IS_AUTHORITY_FOR` | 1 |
| `SEPARATES` | 1 |
| `MARKS` | 1 |
| `SHELTERS` | 1 |
| `CHANGES` | 1 |
| `COLLECTS_TRAFFIC_FOR` | 1 |
| `COMBINES_WITH` | 1 |
| `IS_CONDITIONALLY_ALLOWED` | 1 |
| `EMPLOYS` | 1 |
| `LOCATED_AT` | 1 |
| `IS_HELD_BY` | 1 |
| `IS_MEASURE_OF` | 1 |
| `IS_AREA_OF` | 1 |
| `MEASURES` | 1 |
| `IS_INCLUDED_IN` | 1 |
| `IDENTIFIES` | 1 |
| `IS_PART_OF` | 1 |
| `IS_MEASURED_BY` | 1 |
| `ADJACENT_TO` | 1 |
| `IS_REQUIRED_FOR` | 1 |
| `IS_DEFINED_AS` | 1 |
| `IS_GROUP_OF` | 1 |
| `PROVIDES_SERVICES` | 1 |
| `MANAGES_DEPARTMENT` | 1 |
| `ENSURES_COMPLIANCE` | 1 |
| `ADVISES_AND_DIRECTS` | 1 |
| `REPORTS_TO` | 1 |
| `DETERMINES_WHICH_ACTS_AS` | 1 |
| `HAS_LIAISON_COMMITTEE_WITH` | 1 |
| `AUTHORIZES_CONCURRENT_REVIEW` | 1 |
| `IDENTIFIES_ISSUES_WITH` | 1 |
| `INCLUDES_CHECK_FOR` | 1 |
| `ASSESSMENT_REQUIRES` | 1 |
| `RECOMMENDATION_NOT_FINAL` | 1 |
| `MUST_DECIDE_WITHIN_STATE_TIMEFRAME` | 1 |
| `MAY_REQUIRE_CERTIFICATION` | 1 |
| `APPLICATION_EXPIRES_AFTER` | 1 |
| `MAY_REQUIRE_CMSWL_CERTIFICATION` | 1 |
| `DEFINES_LANDFILL_AREA_RADIUS` | 1 |
| `MAY_ESTABLISH_CYCLES` | 1 |
| `MAY_EXTEND_REVIEW_PERIOD` | 1 |
| `ESTIMATE_PROVIDED_BY` | 1 |
| `RETURNED_IF` | 1 |
| `NOT_REQUIRED_TO_POST` | 1 |
| `FEES_ESTABLISHED_BY` | 1 |
| `COMMUNICATES_INTEREST_TO` | 1 |
| `NOTICE_SENT_TO` | 1 |
| `MUST_POST_SIGN` | 1 |
| `SIGN_MUST_IDENTIFY` | 1 |
| `HEARING_RECORDS_MAINTAINED_BY` | 1 |
| `HEARING_RECORD_INCLUDES` | 1 |
| `APPEAL_DESCRIBED_IN_NOTICE_MUST` | 1 |
| `MUST_FILE_APPEAL_WITHIN` | 1 |
| `MUST_FILE_APPEAL_WITH` | 1 |
| `MUST_INCLUDE_IN_APPEAL` | 1 |
| `SUSPENDS_PLAN_ON_APPEAL` | 1 |
| `SCHEDULES_PUBLIC_HEARING` | 1 |
| `REQUIRES_APPELLANT_TO_PROVE_LEGAL_ERROR` | 1 |
| `QUESTIONS_STANDING` | 1 |
| `EXERCISES_POWERS_OF_DECISION_MAKER` | 1 |
| `REQUESTS_USE_DETERMINATION_FROM` | 1 |
| `MUST_USE_DETERMINATION_FOR_PROJECT_FROM` | 1 |
| `MAY_APPEAL_USE_DETERMINATION_TO` | 1 |
| `FOLLOWS_USE_DETERMINATION_UNLESS_REVERSED_BY` | 1 |
| `PREPARES_REPORT_FOR_BOARD` | 1 |
| `WAIVES_FEE_IF_SUPPORTED_BY_NOTICE_OWNERS` | 1 |
| `FORWARDS_VARIANCE_RECOMMENDATION_FROM` | 1 |
| `CONSIDERS_ENV_BOARD_RECOMMENDATION` | 1 |
| `LAW_DEPARTMENT_REVIEWS_ADJUSTMENT` | 1 |
| `CITY_MANAGER_PRESENTS_ADJUSTMENT_TO` | 1 |
| `WATERSHED_REVIEWS_AFTER_COUNCIL_DETERMINATION` | 1 |
| `COUNCIL_GRANTS_ADJUSTMENT_AFTER_HEARING` | 1 |
| `REQUIRES_PRECONSTRUCTION_CONFERENCE` | 1 |
| `MAY_REQUEST_PRECONSTRUCTION_CONFERENCE` | 1 |
| `MAY_WAIVE_PRECONFERENCE_REQUIREMENT` | 1 |
| `MUST_DISTRIBUTE_PLANS` | 1 |
| `SHARE_CONTACTS` | 1 |
| `DISCUSS_SEQUENCING` | 1 |
| `DISCUSS_TRAFFIC_CONTROL` | 1 |
| `FILE_EXCEPTIONS` | 1 |
| `COORDINATES_CONTACT` | 1 |
| `RECEIVES_INSPECTION_REQUESTS` | 1 |
| `MAY_REQUIRE_REQUEST_LEAD_TIME` | 1 |
| `MAINTAINS_REQUESTS` | 1 |
| `INSPECTOR_NOTES_ON_CARD` | 1 |
| `OWNER_REQUESTS_INSPECTION_OF_CONTROLS` | 1 |
| `ACCOUNTABLE_OFFICIAL_SCHEDULES_INSPECTION` | 1 |
| `OWNER_MUST_DEMONSTRATE_COMPLIANCE` | 1 |
| `INSPECTOR_MAY_MODIFY_PLANS` | 1 |
| `INSPECTOR_MAY_MAKE_MINOR_CHANGES` | 1 |
| `PROHIBITS_START_BEFORE_CONTROLS_OK` | 1 |
| `PERMITS_START_IF_NO_INSPECTION` | 1 |
| `CHARGES_REINSPECTION_FEE_IF` | 1 |
| `EXEMPTS_FIRST_FAILURE_FROM_REINSPECTION_FEE` | 1 |
| `DELIVERS_PLANS_TO_ACCOUNTABLE_OFFICIAL` | 1 |
| `OWNER_NOTIFIES_SUBSTANTIAL_COMPLETION` | 1 |
| `CONSULTING_ENGINEER_SUBMITS_SUMMARY` | 1 |
| `ACCOUNTABLE_OFFICIAL_REVIEWS_AND_REPORTS` | 1 |
| `SCHEDULES_FINAL_ACCEPTANCE_MEETING` | 1 |
| `REQUIRES_DOCUMENTS_FOR_FINAL_ACCEPTANCE` | 1 |
| `FORWARDS_SITE_PLAN_TO_BUILDING_OFFICIAL` | 1 |
| `OWNER_MUST_KEEP_PLANS_ON_SITE` | 1 |
| `INSPECTS_GRADING_AND_DRAINAGE` | 1 |
| `DESIGN_ENGINEER_CERTIFIES_COMPLIANCE` | 1 |
| `FINAL_INSPECTION_AFTER_CERTIFICATION` | 1 |
| `CONDITIONAL_CERTIFICATE_OF_OCCUPANCY` | 1 |
| `CITY_UTILITIES_PROVIDED_IF` | 1 |
| `CITY_UTILITIES_PROVIDED_IF_OCCUPANCY` | 1 |
| `TEMPORARY_ELECTRICAL_IF_CONTROLS_DONE` | 1 |
| `APPEARS_IN` | 1 |
| `ENCOURAGES_PEDESTRIAN_CONNECTIONS` | 1 |
| `DEFINES_BUILDING_TYPE` | 1 |
| `REQUIRES_USES_ALLOWED` | 1 |
| ` DEFAULT` | 1 |
| `HAS_BOUNDARIES_IN` | 1 |
| `DOCUMENTS_SECTION` | 1 |
| `APPLIES_TO_DETERMINATION` | 1 |
| `MAY_REQUEST_DETERMINATION` | 1 |
| `MUST_INCLUDE_INFORMATION` | 1 |
| `SITE_PLAN_REVIEW_TRIGGER` | 1 |
| `MUST_REQUEST_PROJECT_DETERMINATION` | 1 |
| `DIRECTOR_ISSUES_DETERMINATION_WITHIN_14_DAYS` | 1 |
| `NOTICE_CAN_BE_APPEALED_TO` | 1 |
| `NON_PROJECT_REQUESTABLE_BY` | 1 |
| `NON_PROJECT_NOTICE_TO_ORGS` | 1 |
| `NON_PROJECT_NOTICE_TO_PARTIES` | 1 |
| `APPEAL_PERIOD_TO_BOARD` | 1 |
| `DIRECTOR_CANNOT_DECIDE_WHILE_APPEAL_PENDANT` | 1 |
| `APPEAL_TO_DISTRICT_COURT_STAYS_DECISION` | 1 |
| `DIRECTOR_FOLLOWS_PRIOR_DETERMINATION` | 1 |
| `DETERMINATION_MUST_INCLUDE_NOTICE_INFO` | 1 |
| `DETERMINATION_MUST_STATE_CLASSIFICATION` | 1 |
| `DETERMINATION_MUST_EXPLAIN_FACTORS` | 1 |
| `DETERMINATION_MUST_DESCRIBE_LIMITATIONS` | 1 |
| `DETERMINATION_NOT_FOR_SITE_REGULATION_INTERPRETATION` | 1 |
| `REQUIRED_TO_HOLD_HEARING_BY` | 1 |
| `FORWARDS_APPLICATION_TO` | 1 |
| `ALLOW_APPLICANT_TO_REQUEST_HEARING_FROM` | 1 |
| `REPORTS_RECOMMENDATION_TO` | 1 |
| `REQUIRED_TO_HOLD_PUBLIC_HEARING_WITHIN_DAYS_AFTER` | 1 |
| `HIERARCHY_BEGINS_WITH` | 1 |
| `COMBINING_DISTRICT_CLASSIFIED_BY` | 1 |
| `SPECIAL_PURPOSE_EXCLUDED_FROM_HIERARCHY` | 1 |
| `CONSIDERS_CRITERIA` | 1 |
| `RECOMMENDS_DESIGNATION_TO` | 1 |
| `ADOPTED_IN_ACCORDANCE_WITH` | 1 |
| `PARALLEL_TO` | 1 |
| `REQUIRES_RECOMMENDATIONS_FROM` | 1 |
| `CONSIDERS_CRITERIA_ESTABLISHED_IN` | 1 |
| `REVIEWS_APPLICATION_FOR_DESIGNATION_OF` | 1 |
| `FOLLOWS` | 1 |
| `PRESCRIBES_SITE_DEVELOPMENT_REGULATIONS` | 1 |
| `SUPERSEDES_OTHER_TITLE_PROVISIONS` | 1 |
| `LIMITS_BOARD_OF_ADJUSTMENT_VARIANCE_AUTHORITY` | 1 |
| `AMENDMENTS_SUBJECT_TO_PROCEDURE` | 1 |
| `FIGURE_1_2_AMENDMENTS_SUBJECT_TO` | 1 |
| `CONDITION_COMPLIES_WITH` | 1 |
| `APPLIES_ONLY_TO` | 1 |
| `MAY_RECEIVE` | 1 |
| `CAN_BE_GRANTED_BY` | 1 |
| `REFUNDS_FEES_COLLECTED_AFTER` | 1 |
| `REGULATED_BY` | 1 |
| `LOCATED_WITHIN_DISTANCE` | 1 |
| `ALLOWED_LOCATION` | 1 |
| `DISTANCE_COMPARISON` | 1 |
| `CAN_BE_OVERRIDDEN_BY` | 1 |
| `DOES_NOT_CAUSE_NONCOMPLIANCE` | 1 |
| `CONFLICT_RULE` | 1 |
| `REPEALED` | 1 |
| `PROVIDES_EXCEPTION_TO` | 1 |
| `HEIGHT_LIMITED_BY` | 1 |
| `MAY_EXCEED_WITH_APPROVAL` | 1 |
| `MAY_BE` | 1 |
| `REQUIRES_LOCATION` | 1 |
| `REQUIRES_USE` | 1 |
| `MAY_EXCEED_DUE_TO` | 1 |
| `PROVIDED_TO_OBTAIN` | 1 |
| `ELIGIBLE_FOR` | 1 |
| `RESOLVED_BY` | 1 |
| `PRIORITY_OVER` | 1 |
| `CONSISTENT_WITH` | 1 |
| `MUST_BE_CONSISTENT_WITH` | 1 |
| `EXCEEDS_REQUIREMENT` | 1 |
| `SUBJECT_TO` | 1 |
| `MAY_ENABLE` | 1 |
| `MUST_INCLUDE_MINIMUM_AREA` | 1 |
| `MAY_REQUEST_VARIANCE_TO` | 1 |
| `CANNOT_GRANT_VARIANCE_FROM` | 1 |
| `MAY_RECOMMEND_APPROVAL` | 1 |
| `EVALUATES_CONSISTENCY_WITH` | 1 |
| `GRANT_OR_DENY_BASED_ON` | 1 |
| `COUNCIL_DECIDES_BASED_ON` | 1 |
| `REQUIRES_PROPORTIONAL_INCREASE` | 1 |
| `LOCATION_REQUIREMENT` | 1 |
| `ALTERNATE_LOCATION_OPTIONS` | 1 |
| `PROXIMITY_REQUIREMENT` | 1 |
| `APPLIES_ALSO_TO` | 1 |
| `MAY_WAIVE_OR_APPROVE_ALTERNATE` | 1 |
| `REQUIRES_SHOWERS_IF_OPTION_SELECTED_IN` | 1 |
| `SPECIFIES_QUANTITY_FOR_SMALL_BUILDINGS` | 1 |
| `SPECIFIES_QUANTITY_FOR_LARGE_BUILDINGS` | 1 |
| `PROVIDES_RECOMMENDATION_TO` | 1 |
| `REVIEWS_FOR` | 1 |
| `PROVIDES_COPIES_TO` | 1 |
| `REVIEWS_VARIANCES_FOR` | 1 |
| `IS_DEFINED_IN` | 1 |
| `HOLDS_PUBLIC_HEARING_ON_APPLICATION` | 1 |
| `GIVES_NOTICE_OF_PUBLIC_HEARING` | 1 |
| `REQUESTS_RECOMMENDATION_FROM` | 1 |
| `MAY_ACT_WITHOUT_RECOMMENDATION_IF_BOARD_FAILS` | 1 |
| `MAY_FILE_HEARING_REQUEST_WITH` | 1 |
| `REVIEWS_VARIANCE_REQUESTS_FROM` | 1 |
| `MAY_RECOMMEND_APPROVAL_TO` | 1 |
| `EVALUATES_AGAINST` | 1 |
| `GRANTS_OR_DENIES_VARIANCE` | 1 |
| `REQUIRES_MINIMUM_SETBACK_ALONG` | 1 |
| `HAS_MAXIMUM_SETBACK` | 1 |
| `GRANTS_MODIFICATION_AUTHORITY` | 1 |
| `HAS_NO_MINIMUM_SETBACK` | 1 |
| `HAS_NO_MAXIMUM_SETBACK` | 1 |
| `REQUIRES_WALL_BETWEEN` | 1 |
| `CONVERTS_TO` | 1 |
| `EXEMPTS_FROM` | 1 |
| `SUPERSEDES_TO_EXTENT_OF_CONFLICT` | 1 |
| `GOVERNS_USE_TYPE` | 1 |
| `SHALL_GIVE_NOTICE_OF_WAIVER_APPLICATION` | 1 |
| `CONSIDERS_WAIVER_APPLICATION` | 1 |
| `GRANTS_WAIVER_IF_NO_HARM` | 1 |
| `IF_PROTEST_APPLICATION_CONSIDERED_BY` | 1 |
| `REVIEWED_IN_ACCORDANCE_WITH` | 1 |
| `DIRECTOR_CONSIDERS` | 1 |
| `DIRECTOR_GRANTS_IF_NO_HARM` | 1 |
| `PROTEST_TRIGGERS_REVIEW_BY` | 1 |
| `LAND_USE_COMMISSION_REVIEWS_IN_ACCORDANCE_WITH` | 1 |
| `WAIVER_APPLIES_TO` | 1 |
| `WAIVER_APPLIES_TO_NUMBER_OF_ROOMS` | 1 |
| `WAIVER_APPLIES_TO_PARKING_REQUIREMENTS` | 1 |
| `ELIGIBLE_TO_SUBMIT_WAIVER` | 1 |
| `DIRECTOR_REVIEWS_WAIVER` | 1 |
| `PROTEST_TRIGGER_REVIEW_BY` | 1 |
| `PROTEST_CAUSES` | 1 |
| `NOTICE_PROCEDURE_REFERENCES` | 1 |
| `REFERENCES_DEFINITION` | 1 |
| `REQUIRES_SIGN_POSTING` | 1 |
| `REQUIRES_SIGN_INFORMATION` | 1 |
| `REQUIRES_SIGN_FOR_CONDITIONAL_USE` | 1 |
| `USES_DOCUMENT` | 1 |
| `CONFLICTS_WITH` | 1 |
| `OVERIDDEN_BY` | 1 |
| `REQUIRES_ACCOMPANIED_BY` | 1 |
| `AFFIDAVIT_INCLUDES_DESCRIPTION_OF_SEARCH_AREA` | 1 |
| `AFFIDAVIT_INCLUDES_ELEVATION_REQUIRED` | 1 |
| `AFFIDAVIT_INCLUDES_REASONS_CANNOT_LOCATE_ON_EXISTING` | 1 |
| `APPLICANT_MUST_RECORD_CONTACTS` | 1 |
| `APPLICANT_MAY_DISCLOSE_RECORDED_INFORMATION_TO` | 1 |
| `DIRECTOR_MAINTAINS` | 1 |
| `EXEMPT_FROM` | 1 |
| `MAY_EXCEED_COMPATIBILITY_STANDARDS` | 1 |
| `HEIGHT_LIMIT_RELATIVE` | 1 |
| `MUST_NOT_OBSTRUCT` | 1 |
| `MUST_RESEMBLE` | 1 |
| `MUST_NOT_BE_LOCATED_WITHIN` | 1 |
| `REQUIRES_DESIGN` | 1 |
| `ANTENNA_ARRAY_LIMIT` | 1 |
| `REQUIRES_SECURITY_FENCING` | 1 |
| `REQUIRES_LANDSCAPING_SCREEN` | 1 |
| `REQUIRES_IDENTIFICATION_SIGN` | 1 |
| `PERMITTED_IN` | 1 |
| `DIRECTOR_MAY_WAIVE_REQUIREMENT` | 1 |
| `CONDITIONAL_USE_IN` | 1 |
| `DISTANCE_REQUIREMENT_CONDITIONAL` | 1 |
| `LAND_USE_COMMISSION_MAY_SET_HEIGHT` | 1 |
| `LAND_USE_COMMISSION_MAY_WAIVE_REQUIREMENT` | 1 |
| `DISTANCE_MEASUREMENT_RULE` | 1 |
| `EXCLUSION_LIST_APPLIES` | 1 |
| `WAIVES_INCONSISTENT_REGULATIONS` | 1 |
| `ALLOWED_IN` | 1 |
| `DISTANCE_CONSTRAINT` | 1 |
| `LIMITED_PERMIT` | 1 |
| `EMPLOYEE_LIMIT` | 1 |
| `EXEMPTS_FROM_PERMIT` | 1 |
| `MAY_MODIFY_OR_MAINTAIN` | 1 |
| `REQUIRES_LIMIT_ON_DEMOLITION` | 1 |
| `PERMITS_REPLACEMENT_FOR_SAFETY` | 1 |
| `LIMITS_FOUNDATION_ELEVATION_CHANGE` | 1 |
| `LIMITS_IMPROVEMENT_COST_IF_NONCOMPLYING` | 1 |
| `LOSES_NONCOMPLYING_STATUS_IF_DEMOLISHED` | 1 |
| `RESTRICTS_LOCATION_AND_FOOTPRINT` | 1 |
| `REQUIRES_SURVEY_FOR_APPLICATION` | 1 |
| `ALLOWS_ALTERATION_WITHOUT_REDUCING_FOOTPRINT` | 1 |
| `PROHIBITS_INCREASES` | 1 |
| `REQUIRES_EVIDENCE_OF_PRIOR_PERMIT` | 1 |
| `PROHIBITS_POST_1984_UNPERMITTED_ADDITIONS` | 1 |
| `ALLOWS_HEIGHT_INCREASE_SUBJECT_TO_LIMITS` | 1 |
| `ALLOWS_YARD_SETBACK_MODIFICATION_SUBJECT_TO_LIMITS` | 1 |
| `APPLIES_TO_EACH_YARD_SETBACK` | 1 |
| `LIMITS_NUMBER_OF_MODIFICATIONS` | 1 |
| `OVERriddenBY` | 1 |
| `PERMITS_AS_ACCESSORY_USE` | 1 |
| `REQUIRES_REPORTING_TO` | 1 |
| `LIMITS_PARTICIPATION_DAYS_PER_YEAR` | 1 |
| `LIMITS_PROPERTY_PARTICIPATION_DAYS_PER_YEAR` | 1 |
| `LIMITS_PROPERTY_TOURS_PER_YEAR` | 1 |
| `LIMITS_PROPERTY_DAYS_PER_WEEK` | 1 |
| `LIMITS_GUEST_ARTISTS` | 1 |
| `REQUIRES_PERMIT` | 1 |
| `PERMITS_USE` | 1 |
| `APPLICATION_MUST_BE_FILED_AT_LEAST_DAYS_BEFORE` | 1 |
| `BUILDING_OFFICIAL_MAKES_DETERMINATION_UNDER` | 1 |
| `BUILDING_OFFICIAL_ACTION_DEADLINE_AFTER_APPLICATION` | 1 |
| `CONDITIONAL_APPROVAL_REFERENCES` | 1 |
| `BUILDING_OFFICIAL_ISSUES_TEMPORARY_USE_PERMIT` | 1 |
| `BUILDING_OFFICIAL_MAY_RENEW_AUTHORIZATION_FOR` | 1 |
| `TEMPORARY_USE_DURATION_LIMITED_BY` | 1 |
| `APPLICANT_MUST_FILE_NEW_APPLICATION_TO_CONTINUE` | 1 |
| `BUILDING_OFFICIAL_ISSUES` | 1 |
| `APPLICATION_FILING_DEADLINE` | 1 |
| `MAY_ADOPT_GUIDELINES_FOR_INTERPRETATION` | 1 |
| `HEAR_AND_DECIDE_REQUESTS_FOR_VARIANCE` | 1 |
| `MAY_GRANT_VARIANCE_FOR_PROPERTY` | 1 |
| `MAY_GRANT_VARIANCE_FROM_PARKING_REQUIREMENTS` | 1 |
| `VARIANCE_FOR_PARKING_NOT_RUN_WITH_LAND` | 1 |
| `MAY_NOT_APPLY_TO_BICYCLE_PARKING` | 1 |
| `MAY_SEEK_WAIVER_PER_CODE_SECTION` | 1 |
| `MAY_APPEAL_BUILDING_OFFICIAL_DECISIONS` | 1 |
| `SHALL_PROVIDE_DOCUMENTS_TO_BOARD_AFTER_APPEAL` | 1 |
| `SHALL_GRANT_SPECIAL_EXCEPTION_FOR_RESIDENTIAL_SETBACK_VIOLATION` | 1 |
| `SPECIAL_EXCEPTION_APPLIES_TO_EXISTING_RESIDENTIAL_STRUCTURE` | 1 |
| `SPECIAL_EXCEPTION_RESTRICTED_IN_SF3` | 1 |
| `SPECIAL_EXCEPTION_CONDITION_SHARED_LOT_LIMIT` | 1 |
| `SPECIAL_EXCEPTION_TIME_CONDITION` | 1 |
| `SPECIAL_EXCEPTION_DOES_NOT_RUN_WITH_LAND` | 1 |
| `STRUCTURE_TREATED_AS_NONCOMPLYING_AFTER_SPECIAL_EXCEPTION` | 1 |
| `CAN_BE_SCREENED_BY` | 1 |
| `MAINTAINS_FILE_ON` | 1 |
| `HAS_AUTHORITY` | 1 |
| `REQUIRES_INSPECTION_REPORT_FROM` | 1 |
| `REQUIRES_LIGHTING` | 1 |
| `EQUIVALENCE` | 1 |
| `SETBACK_REQUIREMENT` | 1 |
| `MUST_APPROVE` | 1 |
| `MUST_BE_SCREENED_FROM` | 1 |
| `PROHIBITS_CONSTRUCTION` | 1 |
| `LICENSE_NOT_REQUIRED_FOR` | 1 |
| `MAY_ABATE` | 1 |
| `REQUIRES_TAG` | 1 |
| `REQUIRES_LICENSE_FROM` | 1 |
| `REQUIRES_FIRE_CHIEF_APPROVAL` | 1 |
| `LICENSE_VOID_IF_SITEPLAN_EXPIRED` | 1 |
| `MUST_ACT_ON_TRANSFER_REQUEST` | 1 |
| `LICENSE_EXPIRES_AFTER` | 1 |
| `APPEAL_DENIAL_TO` | 1 |
| `MUST_PROVIDE_PARKING_ON` | 1 |
| `MUST_BE_SEPARATED_FROM` | 1 |
| `REQUIRES_BARRIER_ALONG_BOUNDARY` | 1 |
| `MUST_COMPLY_SITE_REGULATIONS_OF` | 1 |
| `OCCUPANT_MUST_SECURE` | 1 |
| `OWNER_MUST_NOTIFY_VIOLATIONS_TO` | 1 |
| `MUST_SUPPLY_TAX_INFO_TO` | 1 |
| `MUST_MAINTAIN_REGISTER_FOR_INSPECTION_BY` | 1 |
| `MUST_PROVIDE_ACCESS_FOR_REPAIRS_TO` | 1 |
| `BUILDING_OFFICIAL_MAY_DENY_PERMIT_FOR` | 1 |
| `OWNER_MUST_MAINTAIN_INTERNAL_STREETS` | 1 |
| `MAY_ISSUE_CITATION_AND_IMPOUND` | 1 |
| `MUST_APPROVE_INTERNAL_STREET_DESIGN` | 1 |
| `MUST_PROVIDE_STREET_LIGHTING_ALONG` | 1 |
| `MUST_HANDLE_LPG_IN_COMPLIANCE_WITH` | 1 |
| `MUST_PROVIDE_FIRE_HYDRANTS_WITHIN` | 1 |
| `MUST_PROVIDE_WATER_SUPPLY_APPROVED_BY` | 1 |
| `SEWER_SYSTEM_MUST_COMPLY_WITH` | 1 |
| `FACILITIES_MUST_COMPLY_WITH_CODES` | 1 |
| `SPECIFIES` | 1 |
| `CONDITIONALLY_ALLOWS` | 1 |
| `SETS_LIMIT` | 1 |
| `SETS_REQUIREMENT` | 1 |
| `REQUESTS_REVIEW` | 1 |
| `REQUIRES_REVIEW` | 1 |
| `ALLOWS_AS_ACCESSORY` | 1 |
| `LIMITS_STORAGE` | 1 |
| `ALLOWS_OFFSITE` | 1 |
| `RESTRICTS_APPURTENANCES` | 1 |
| `ALLOWS_CHILD_CARE_AS_ACCESSORY` | 1 |
| `LIMITS_OCCUPANCY` | 1 |
| `LIMITS_TRAFFIC` | 1 |
| `HAS_EXPIRATION_CONDITION` | 1 |
| `PERMITS_TEMPORARY_RETAIL` | 1 |
| `REQUIRES_APPLICATION_WINDOW` | 1 |
| `REQUIRES_DOCUMENTATION` | 1 |
| `MAY_RENEW_AUTHORIZATION` | 1 |
| `MAKES_DETERMINATION` | 1 |
| `REQUIRES_CONDITIONS` | 1 |
| `REQUIRES_CLEANUP` | 1 |
| `REQUIRES_DETERMINATION_BEFORE_REPAIR` | 1 |
| `TERMINATES_IF_DISCONTINUED` | 1 |
| `DEFINITION` | 1 |
| `ACCESSORY_USE_REQUIREMENT` | 1 |
| `REQUIRES_DOCUMENTATION_FROM` | 1 |
| `APPROVES_ALTERNATIVES` | 1 |
| `REQUIRES_REPLACEMENT` | 1 |
| `COUNTS_TOWARD` | 1 |
| `REQUIRES_SCREENING` | 1 |
| `REQUIRES_IRRIGATION` | 1 |
| `INSPECTS_FINAL` | 1 |
| `GOVERNS_USE_CLASSIFICATION` | 1 |
| `MAP_MAINTAINED_BY` | 1 |
| `MAP_KEPT_BY` | 1 |
| `MAY_COMBINE_WITH` | 1 |
| `MAY_MODIFY` | 1 |
| `IS_SUPERSEDED_BY` | 1 |
| `MAY_REFERENCE` | 1 |
| `INTERACTS_WITH` | 1 |
| `SUPERCEDES` | 1 |
| `DEFINES_BY` | 1 |
| `ESTABLISHES` | 1 |
| `AUTHORIZES_EXCEPTION` | 1 |
| `MODIFIED_BY` | 1 |
| `MAKES_USE_DETERMINATION_UNDER` | 1 |
| `MAY_REQUIRE_FOR` | 1 |
| `ENTITLED_TO_APPEAL_TO` | 1 |
| `MUST_INCLUDE_IN_NOTICE` | 1 |
| `MAY_BE_APPEALED_TO` | 1 |
| `SINGLE_OFFICE_IDENTIFIES_DISCRETIONARY_REVIEW` | 1 |
| `APPLICATION_MAY_REMAIN_PENDING_WHILE_SURETY_OUTSTANDING` | 1 |
| `MUST_CITE_AUTHORITY` | 1 |
| `AUTOMATIC_APPROVAL_IF_TIMEOUT` | 1 |
| `REQUIRES_POSTING_OF_FISCAL_SECURITY` | 1 |
| `MAY_ACCEPT_FISCAL_SECURITY_FROM` | 1 |
| `REQUIRES_POSTING_BY` | 1 |
| `IS_SECTION_OF` | 1 |
| `SHALL_HOLD_PUBLIC_HEARING_BY_SPECIFIED_DEADLINE` | 1 |
| `GOVERNED_BY_PROCEDURE` | 1 |
| `REVIEW_REQUIRED_OF` | 1 |
| `NOTICE_PROVIDED_IN_ACCORDANCE_WITH` | 1 |
| `IMPLEMENTED_BY` | 1 |
| `DEFINES_REMOVAL_ACTIONS` | 1 |
| `GIVES_NOTICE_UNDER_SECTION_30_1_153_A` | 1 |
| `SUPERSEDES_PROVISION` | 1 |
| `ALLOWS_EXTENSION_OF` | 1 |
| `RESTRICTS_EXTENSION_TO_ONE_TIME` | 1 |
| `REQUIRES_APPROVAL_ACTION_BY_DEADLINE` | 1 |
| `MAY_REQUEST_EXTENSION` | 1 |
| `PREPARES_REPORT_FOR` | 1 |
| `AUTHORITY_BOUND_BY` | 1 |
| `EXEMPTION_DEFINED_BY` | 1 |
| `REQUIRES_DEDICATION_LIMIT_150FT` | 1 |
| `REQUIRES_DEDICATION_LIMIT_50_PERCENT` | 1 |
| `MAY_REQUIRE_GREATER_DEDICATION_WHEN_NOT_COMPLIANT` | 1 |
| `MAY_REQUIRE_GREATER_DEDICATION_FOR_TRAFFIC` | 1 |
| `MAY_DEFER_DEDICATION_TO_LATER_STAGE` | 1 |
| `MAY_REQUIRE_CONSTRUCTION_OR_FEE` | 1 |
| `RIGHT_OF_WAY_RESERVED_SUBJECT_TO_SECTION_30_3_22` | 1 |
| `CAN_REQUIRE_GREATER_DEDICATION` | 1 |
| `RESERVATION_SUBJECT` | 1 |
| `CAN_GRANT_VARIANCE` | 1 |
| `VARIANCE_GROUNDS_INCLUDE` | 1 |
| `EXCEPTED_BY` | 1 |
| `DENIES_IF` | 1 |
| `AFFECTED_BY` | 1 |
| `REVIEWED_BY` | 1 |
| `ADOPTED` | 1 |
| `AMENDS` | 1 |
| `ADOPTS_WITH_DELETIONS` | 1 |
| `GIVES_AUTHORITY_TO` | 1 |
| `REQUIRES_SUBMISSION_TO` | 1 |
| `REQUIRES_COPY_HELD_BY` | 1 |
| `ADMINISTERED_BY` | 1 |
| `HEARS_APPEALS` | 1 |
| `MAINTAINS_MAP` | 1 |
| `ALIASES` | 1 |
| `REQUIRES_DOCUMENT_FROM` | 1 |

---

## 5. Relationship Patterns

Common patterns showing (FromType)--[EDGE]-->(ToType)

| From | Edge | To | Count |
|------|------|----|-------|
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
| Entity | `GOVERNED_BY` | Entity | 19 |
| Rule | `APPLIES_IN` | Rule | 19 |
| Zone | `ALLOWS_USE` | Zone | 19 |
| DocumentSource | `CONTAINS` | DocumentSource | 18 |
| Zone | `CONTAINS` | Zone | 18 |
| UseType | `ALLOWS_USE` | UseType | 18 |
| Rule | `GOVERNS_ZONE` | Zone | 17 |
| Zone | `ALLOWS_USE` | Rule | 16 |
| Entity | `DEFINES` | Entity | 15 |
| Rule | `DEFINES` | Entity | 15 |
| DocumentSource | `APPLIES_IN` | Jurisdiction | 15 |
| Entity | `CONTAINS` | Entity | 15 |
| Override | `APPLIES_IN` | Zone | 14 |
| Entity | `SOURCED_FROM` | DocumentSource | 14 |
| Entity | `INCLUDES` | Entity | 14 |
| Entity | `APPLIES_IN` | Entity | 13 |
| Entity | `PERMITS_TEMPORARY_USE` | UseType | 13 |
| Entity | `HAS_CONSTRAINT` | Constraint | 13 |
| Jurisdiction | `CONTAINS` | Rule | 13 |
| UseType | `CONTAINS` | DocumentSource | 12 |
| Zone | `APPLIES_IN` | Zone | 12 |
| Entity | `APPLIES_IN` | Zone | 12 |
| Rule | `ALLOWS_USE` | UseType | 12 |
| Rule | `GOVERNED_BY` | Entity | 12 |
| DocumentSource | `REFERENCES` | DocumentSource | 12 |
| Entity | `GOVERNED_BY` | DocumentSource | 11 |
| UseType | `HAS_CONDITION` | Entity | 11 |
| Override | `SOURCED_FROM` | DocumentSource | 11 |
| DocumentSource | `GOVERNES_METRIC` | Constraint | 11 |
| DocumentSource | `REFERENCES` | Rule | 11 |
| UseType | `APPLIES_IN` | Zone | 11 |
| Zone | `HAS_CONSTRAINT` | UseType | 11 |
| DocumentSource | `APPLIES_IN` | Zone | 10 |
| UseType | `GOVERNED_BY` | Zone | 10 |
| Jurisdiction | `CONTAINS` | Override | 10 |
| Zone | `REQUIRES` | Entity | 10 |
| UseType | `GOVERNED_BY` | Constraint | 10 |
| Entity | `NOTIFIES` | Entity | 10 |
| Entity | `GOVERNED_BY` | Rule | 9 |
| Entity | `CONTAINS` | Zone | 9 |
| UseType | `HAS_CONSTRAINT` | Constraint | 9 |
| DocumentSource | `GOVERNED_BY` | DocumentSource | 9 |
| Entity | `INCLUDES` | Jurisdiction | 9 |
| Jurisdiction | `CONTAINS` | Jurisdiction | 9 |
| DocumentSource | `ALLOWS_USE` | Entity | 9 |
| Constraint | `APPLIES_IN` | Rule | 8 |
| Rule | `DISCUSSSES_TOPIC_WITH` | Entity | 8 |
| DocumentSource | `APPLIES_IN` | Rule | 8 |
| Zone | `GOVERNED_BY` | Zone | 8 |
| Rule | `APPLIES_IN` | DocumentSource | 8 |
| Entity | `MAY_FILE_APPLICATION_FOR` | Entity | 8 |
| UseType | `GOVERNED_BY` | DocumentSource | 8 |
| Entity | `REQUIRES` | Rule | 8 |
| Zone | `Defaults` | UseType | 8 |
| Rule | `SOURCED_FROM` | Zone | 8 |
| Entity | `ALLOWS_USE` | UseType | 8 |
| Entity | `SENT_TO` | Entity | 8 |
| UseType | `DEFINED_AS` | UseType | 7 |
| Override | `ALLOWS_USE` | Zone | 7 |
| Override | `ALLOWS_USE` | UseType | 7 |
| Rule | `APPLIES_TO` | UseType | 7 |
| Override | `APPLIES_IN` | UseType | 7 |
| Rule | `HAS_CONSTRAINT` | Rule | 7 |
| Rule | `APPLIES_IN` | UseType | 7 |
| Rule | `DEFINES` | UseType | 7 |
| DocumentSource | `REQUIRES` | Entity | 7 |
| Rule | `SOURCED_FROM` | Entity | 6 |
| DocumentSource | `APPLIES_TO` | UseType | 6 |
| Entity | `REQUIRES_NOTICE_TO` | Entity | 6 |
| Entity | `REQUIRES` | Entity | 6 |
| Rule | `CONTAINS` | UseType | 6 |
| UseType | `APPLIES_IN` | Jurisdiction | 6 |
| DocumentSource | `GOVERNED_BY` | Entity | 6 |
| UseType | `GOVERNED_BY` | Entity | 6 |
| DocumentSource | `GOVERNED_BY` | Jurisdiction | 6 |
| Entity | `BOUNDS` | Jurisdiction | 6 |
| DocumentSource | `SOURCED_FROM` | Rule | 6 |
| Rule | `CONTAINS` | Jurisdiction | 6 |
| Entity | `SUPERSEDES` | DocumentSource | 6 |
| DocumentSource | `ALLOWS_USE` | UseType | 6 |
| Rule | `DEFINES` | Rule | 6 |
| DocumentSource | `APPLIES_IN` | DocumentSource | 6 |
| Jurisdiction | `GOVERNED_BY` | Entity | 6 |
| Entity | `REFERENCES` | DocumentSource | 5 |
| Entity | `MUST_NOTIFY` | Entity | 5 |

---

## 6. Orphan Nodes (No RELATES_TO connections)

**Total Orphan Nodes: 56**

### Constraint (4 orphans)

- 10 acre
- 2 story
- corner_lot_area_min
- minimum corner lot width

### DocumentSource (10 orphans)

- 25-2-subchapter-A
- TITLE: 30-3-22
- [SECTION ID: 25-2-563]
- [SECTION ID: 25-2-581]
- [SECTION ID: 25-2-779]
- [SECTION ID: 30-1-93]
- [SECTION ID: 30-3-25]
- [SECTION ID: 30-3-26]
- [SECTION ID: 30-3-42]
- [TITLE: 25-1-186]

### Entity (15 orphans)

- 25-2-146
- 25-2-163
- COMMON SIDE LOT LINE
- DOMINANT SIDE YARD
- DRIPLINE
- DRIVEWAY APPROACH
- FLAG LOT
- MIRRORED GLASS
- Metrics
- Supplemental Zone
- automated data base
- bus or transit line
- office approved plans distribution
- office conference
- top chord of the roof truss

### Jurisdiction (10 orphans)

- Anderson Mill Road
- Bierce Street
- Blunn Creek
- Dawson Road
- Highland Hills Drive
- Level 3 street
- Level 4 street
- River Street
- SH 71
- Zones

### Rule (4 orphans)

- 25-1-502
- 25-1-805
- 25-2-772
- Section 4.3

### UseType (6 orphans)

- THREE-UNIT RESIDENTIAL
- aquatic foods
- multi-lot master planned subdivision
- multi-tenant center sign
- on-premise sign
- projecting sign

### Zone (7 orphans)

- Limited Office
- Private Streets
- Zone ID: austin_tx:DMU
- Zone ID: austin_tx:LI
- Zone SF-4B (Urban Family Residence (Moderate-High Density))
- Zone code: VMU
- Zone name: Vertical Mixed Use

---

## 7. Data Quality Metrics

### Nodes with NULL names

None

### Duplicate Entity Names (Top 30)

None

---

## 8. Query Examples

### Find all zones in Austin
```cypher
MATCH (j:Jurisdiction)-[r:RELATES_TO]->(z:Zone)
WHERE r.name = 'CONTAINS' AND j.name CONTAINS 'Austin'
RETURN z.name, z.code, z.family
ORDER BY z.name
```

### Find zones that allow townhouses
```cypher
MATCH (z:Zone)-[r:RELATES_TO]->(u:UseType)
WHERE r.name = 'ALLOWS_USE' AND u.name CONTAINS 'Townhouse'
RETURN z.name, u.name
```

### Get constraints for a zone
```cypher
MATCH (z:Zone)-[:RELATES_TO]-(r:Rule)-[rel:RELATES_TO]->(c:Constraint)
WHERE z.name CONTAINS 'SF-5' AND rel.name = 'HAS_CONSTRAINT'
RETURN z.name, r.name, c.name, c.summary
```

### Find all state overrides
```cypher
MATCH (o:Override)
RETURN o.name, o.bill_id, o.metric, o.override_value, o.summary
```

### Trace rule to source document
```cypher
MATCH (r:Rule)-[rel:RELATES_TO]->(d:DocumentSource)
WHERE rel.name = 'SOURCED_FROM'
RETURN r.name, r.section, d.document, d.section
LIMIT 10
```

### Find orphan nodes
```cypher
MATCH (n)
WHERE NOT (n)-[:RELATES_TO]-() AND NOT (n)<-[:RELATES_TO]-()
  AND NOT n:Episodic
RETURN labels(n) as type, n.name as name
```

### Get all edge types
```cypher
MATCH ()-[r:RELATES_TO]->()
RETURN DISTINCT r.name as edge_type, count(*) as count
ORDER BY count DESC
```

### Full hierarchy visualization
```cypher
MATCH path = (j:Jurisdiction)-[:RELATES_TO*1..4]->(n)
WHERE j.name CONTAINS 'Austin'
RETURN path
LIMIT 200
```

---

## 9. Ontology Summary

### Entity Hierarchy
```
Jurisdiction (city, county, state)
├── Zone (zoning districts: SF-1 to SF-6, MF-1 to MF-6, CBD, etc.)
│   └── UseType (permitted uses: residential, commercial, mixed)
│       └── Rule (LDC regulations)
│           └── Constraint (quantitative limits)
│               └── Condition (contextual triggers)
└── Override (state preemptions: SB-840, SB-2835)
    └── supersedes local Constraints

DocumentSource: Citations linked to all entity types via SOURCED_FROM
Entity: Untyped entities extracted by LLM (need classification)
Episodic: Source text episodes (306 ingested)
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
* --[MENTIONS]--> * (Episodic connections)
```

---

## 10. Data Sources

| Source | Description |
|--------|-------------|
| Austin LDC | Land Development Code (~103,756 lines, 3.35M chars) |
| Texas SB-840 | Housing in commercial areas (density, height, setbacks) |
| Texas SB-2835 | Transit-oriented development (density, parking) |

---

*End of Knowledge Graph Documentation*