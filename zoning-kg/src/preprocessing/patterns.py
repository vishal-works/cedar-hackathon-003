"""
EntityRuler patterns for zoning entities.

Defines patterns to recognize:
- ZONE: Zone codes (SF-5, MF-4, GR, CBD, etc.)
- USE_TYPE: Use types (townhouse, condominium, multifamily, duplex)
- SECTION_REF: Section references (§25-2-775, Section 25-2-492)
- METRIC: Metric names (lot width, setback, height, building coverage)
- MEASUREMENT: Measurements with units (20 feet, 5750 sqft, 40%)
- OPERATOR: Constraint operators (minimum, maximum, at least, not exceed)
"""

# ============================================================================
# ZONE PATTERNS
# ============================================================================

# Austin zoning code categories:
# - SF (Single Family): SF-1, SF-2, SF-3, SF-4A, SF-4B, SF-5, SF-6
# - MF (Multifamily): MF-1, MF-2, MF-3, MF-4, MF-5, MF-6
# - MH (Mobile Home)
# - Commercial: NO, LO, GO, CR, LR, GR, CS, CS-1, CH
# - Industrial: IP, MI, LI, R&D
# - Downtown: CBD, DMU
# - Special: LA (Lake Austin), RR (Rural Residence), PUD, DR, AV, AG, P, W/LO, L

ZONE_PATTERNS = [
    # Regex pattern for most zone codes
    {"label": "ZONE", "pattern": [{"TEXT": {"REGEX": r"^(SF|MF|GR|CR|LR|GO|LO|NO|CS|CH|IP|MI|LI|CBD|DMU|PUD|LA|RR|MH|DR|AV|AG)-?\d*[A-Z]?$"}}]},
    
    # Explicit single-family zones
    {"label": "ZONE", "pattern": "SF-1"},
    {"label": "ZONE", "pattern": "SF-2"},
    {"label": "ZONE", "pattern": "SF-3"},
    {"label": "ZONE", "pattern": "SF-4A"},
    {"label": "ZONE", "pattern": "SF-4B"},
    {"label": "ZONE", "pattern": "SF-5"},
    {"label": "ZONE", "pattern": "SF-6"},
    
    # Explicit multifamily zones
    {"label": "ZONE", "pattern": "MF-1"},
    {"label": "ZONE", "pattern": "MF-2"},
    {"label": "ZONE", "pattern": "MF-3"},
    {"label": "ZONE", "pattern": "MF-4"},
    {"label": "ZONE", "pattern": "MF-5"},
    {"label": "ZONE", "pattern": "MF-6"},
    
    # Commercial zones
    {"label": "ZONE", "pattern": "NO"},
    {"label": "ZONE", "pattern": "LO"},
    {"label": "ZONE", "pattern": "GO"},
    {"label": "ZONE", "pattern": "CR"},
    {"label": "ZONE", "pattern": "LR"},
    {"label": "ZONE", "pattern": "GR"},
    {"label": "ZONE", "pattern": "CS"},
    {"label": "ZONE", "pattern": "CS-1"},
    {"label": "ZONE", "pattern": "CH"},
    
    # Industrial zones
    {"label": "ZONE", "pattern": "IP"},
    {"label": "ZONE", "pattern": "MI"},
    {"label": "ZONE", "pattern": "LI"},
    {"label": "ZONE", "pattern": "R&D"},
    
    # Downtown and special zones
    {"label": "ZONE", "pattern": "CBD"},
    {"label": "ZONE", "pattern": "DMU"},
    {"label": "ZONE", "pattern": "PUD"},
    {"label": "ZONE", "pattern": "LA"},
    {"label": "ZONE", "pattern": "RR"},
    {"label": "ZONE", "pattern": "MH"},
    {"label": "ZONE", "pattern": "DR"},
    {"label": "ZONE", "pattern": "AV"},
    {"label": "ZONE", "pattern": "AG"},
    {"label": "ZONE", "pattern": "P"},
    {"label": "ZONE", "pattern": "W/LO"},
    {"label": "ZONE", "pattern": "L"},
    
    # Multi-word zone names (will be merged)
    {"label": "ZONE", "pattern": [{"LOWER": "urban"}, {"LOWER": "family"}, {"LOWER": "residence"}]},
    {"label": "ZONE", "pattern": [{"LOWER": "single"}, {"LOWER": "family"}, {"LOWER": "residence"}]},
    {"label": "ZONE", "pattern": [{"LOWER": "multifamily"}, {"LOWER": "residence"}]},
    {"label": "ZONE", "pattern": [{"LOWER": "rural"}, {"LOWER": "residence"}]},
    {"label": "ZONE", "pattern": [{"LOWER": "lake"}, {"LOWER": "austin"}]},
    {"label": "ZONE", "pattern": [{"LOWER": "central"}, {"LOWER": "business"}, {"LOWER": "district"}]},
    {"label": "ZONE", "pattern": [{"LOWER": "downtown"}, {"LOWER": "mixed"}, {"LOWER": "use"}]},
    {"label": "ZONE", "pattern": [{"LOWER": "planned"}, {"LOWER": "unit"}, {"LOWER": "development"}]},
]

# ============================================================================
# USE TYPE PATTERNS
# ============================================================================

USE_TYPE_PATTERNS = [
    # Single word use types
    {"label": "USE_TYPE", "pattern": "townhouse"},
    {"label": "USE_TYPE", "pattern": "townhouses"},
    {"label": "USE_TYPE", "pattern": "condominium"},
    {"label": "USE_TYPE", "pattern": "condominiums"},
    {"label": "USE_TYPE", "pattern": "duplex"},
    {"label": "USE_TYPE", "pattern": "duplexes"},
    {"label": "USE_TYPE", "pattern": "triplex"},
    {"label": "USE_TYPE", "pattern": "fourplex"},
    {"label": "USE_TYPE", "pattern": "residential"},
    {"label": "USE_TYPE", "pattern": "commercial"},
    {"label": "USE_TYPE", "pattern": "industrial"},
    {"label": "USE_TYPE", "pattern": "retail"},
    {"label": "USE_TYPE", "pattern": "office"},
    {"label": "USE_TYPE", "pattern": "warehouse"},
    {"label": "USE_TYPE", "pattern": "manufacturing"},
    
    # Multi-word use types
    {"label": "USE_TYPE", "pattern": [{"LOWER": "single"}, {"OP": "?", "TEXT": "-"}, {"LOWER": "family"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "two"}, {"OP": "?", "TEXT": "-"}, {"LOWER": "family"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "multi"}, {"OP": "?", "TEXT": "-"}, {"LOWER": "family"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "multifamily"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "group"}, {"LOWER": "residential"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "mobile"}, {"LOWER": "home"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "mobile"}, {"LOWER": "home"}, {"LOWER": "park"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "accessory"}, {"LOWER": "dwelling"}, {"LOWER": "unit"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "adu"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "dwelling"}, {"LOWER": "unit"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "dwelling"}, {"LOWER": "units"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "mixed"}, {"LOWER": "use"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "retirement"}, {"LOWER": "housing"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "affordable"}, {"LOWER": "housing"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "parking"}, {"LOWER": "structure"}]},
    {"label": "USE_TYPE", "pattern": [{"LOWER": "parking"}, {"LOWER": "garage"}]},
]

# ============================================================================
# SECTION REFERENCE PATTERNS
# ============================================================================

# Note: spaCy tokenizes "25-2-775" as ["25", "-", "2", "-", "775"]
# So we need patterns that match this tokenization

SECTION_REF_PATTERNS = [
    # § 25-2-775 format (tokenized as: § 25 - 2 - 775)
    {"label": "SECTION_REF", "pattern": [
        {"TEXT": "§"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"LIKE_NUM": True}
    ]},
    
    # § 25-2-775A format (with letter suffix)
    {"label": "SECTION_REF", "pattern": [
        {"TEXT": "§"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"TEXT": {"REGEX": r"^\d+[A-Z]$"}}
    ]},
    
    # Section 25-2-775 format
    {"label": "SECTION_REF", "pattern": [
        {"LOWER": "section"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"LIKE_NUM": True}
    ]},
    
    # Section 25-2-775A format
    {"label": "SECTION_REF", "pattern": [
        {"LOWER": "section"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"LIKE_NUM": True},
        {"TEXT": "-"},
        {"TEXT": {"REGEX": r"^\d+[A-Z]$"}}
    ]},
    
    # Subsection references like (A), (B), (1)
    {"label": "SECTION_REF", "pattern": [{"LOWER": "subsection"}, {"TEXT": {"REGEX": r"^\([A-Za-z0-9]+\)$"}}]},
    {"label": "SECTION_REF", "pattern": [{"LOWER": "paragraph"}, {"TEXT": {"REGEX": r"^\([A-Za-z0-9]+\)$"}}]},
    
    # Article and Division references
    {"label": "SECTION_REF", "pattern": [{"LOWER": "article"}, {"LIKE_NUM": True}]},
    {"label": "SECTION_REF", "pattern": [{"LOWER": "division"}, {"LIKE_NUM": True}]},
    {"label": "SECTION_REF", "pattern": [{"LOWER": "chapter"}, {"LIKE_NUM": True}, {"TEXT": "-"}, {"LIKE_NUM": True}]},
    {"label": "SECTION_REF", "pattern": [{"LOWER": "subchapter"}, {"TEXT": {"REGEX": r"^[A-Z]$"}}]},
]

# ============================================================================
# METRIC PATTERNS
# ============================================================================

METRIC_PATTERNS = [
    # Lot dimensions
    {"label": "METRIC", "pattern": [{"LOWER": "lot"}, {"LOWER": "width"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "lot"}, {"LOWER": "size"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "lot"}, {"LOWER": "area"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "lot"}, {"LOWER": "depth"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "corner"}, {"LOWER": "lot"}, {"LOWER": "width"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "corner"}, {"LOWER": "lot"}, {"LOWER": "area"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "site"}, {"LOWER": "area"}]},
    
    # Setbacks
    {"label": "METRIC", "pattern": [{"LOWER": "setback"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "setbacks"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "front"}, {"LOWER": "yard"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "rear"}, {"LOWER": "yard"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "side"}, {"LOWER": "yard"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "front"}, {"LOWER": "setback"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "rear"}, {"LOWER": "setback"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "side"}, {"LOWER": "setback"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "street"}, {"LOWER": "side"}, {"LOWER": "yard"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "interior"}, {"LOWER": "side"}, {"LOWER": "yard"}]},
    
    # Height
    {"label": "METRIC", "pattern": [{"LOWER": "height"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "building"}, {"LOWER": "height"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "maximum"}, {"LOWER": "height"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "structure"}, {"LOWER": "height"}]},
    
    # Coverage and density
    {"label": "METRIC", "pattern": [{"LOWER": "building"}, {"LOWER": "coverage"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "impervious"}, {"LOWER": "cover"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "impervious"}, {"LOWER": "coverage"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "floor"}, {"LOWER": "area"}, {"LOWER": "ratio"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "far"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "density"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "dwelling"}, {"LOWER": "units"}, {"LOWER": "per"}, {"LOWER": "acre"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "units"}, {"LOWER": "per"}, {"LOWER": "acre"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "dwelling"}, {"LOWER": "units"}, {"LOWER": "per"}, {"LOWER": "lot"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "units"}, {"LOWER": "per"}, {"LOWER": "lot"}]},
    
    # Parking
    {"label": "METRIC", "pattern": [{"LOWER": "parking"}, {"LOWER": "spaces"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "parking"}, {"LOWER": "requirement"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "parking"}, {"LOWER": "requirements"}]},
    
    # Other
    {"label": "METRIC", "pattern": [{"LOWER": "open"}, {"LOWER": "space"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "landscaping"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "buffer"}]},
    {"label": "METRIC", "pattern": [{"LOWER": "screening"}]},
]

# ============================================================================
# MEASUREMENT PATTERNS
# ============================================================================

MEASUREMENT_PATTERNS = [
    # Feet measurements
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "feet"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "foot"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "ft"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "ft."}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"TEXT": "'"}]},
    
    # Square feet measurements
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "square"}, {"LOWER": "feet"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "sq"}, {"LOWER": "ft"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "sq."}, {"LOWER": "ft."}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "sqft"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "sf"}]},
    
    # Acres
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "acre"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "acres"}]},
    
    # Percentages
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"TEXT": "%"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "percent"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "percentage"}]},
    
    # Stories
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "stories"}]},
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "story"}]},
    
    # Units per acre (for density)
    {"label": "MEASUREMENT", "pattern": [{"LIKE_NUM": True}, {"LOWER": "units"}, {"LOWER": "per"}, {"LOWER": "acre"}]},
    
    # Ratio patterns (like 1:1, 8:1)
    {"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": r"^\d+:\d+$"}}]},
    
    # Comma-separated numbers with units
    {"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": r"^\d{1,3}(,\d{3})*$"}}, {"LOWER": "square"}, {"LOWER": "feet"}]},
    {"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": r"^\d{1,3}(,\d{3})*$"}}, {"LOWER": "feet"}]},
    {"label": "MEASUREMENT", "pattern": [{"TEXT": {"REGEX": r"^\d{1,3}(,\d{3})*$"}}, {"LOWER": "sqft"}]},
]

# ============================================================================
# OPERATOR PATTERNS
# ============================================================================

OPERATOR_PATTERNS = [
    # Minimum/Maximum
    {"label": "OPERATOR", "pattern": "minimum"},
    {"label": "OPERATOR", "pattern": "maximum"},
    {"label": "OPERATOR", "pattern": "min"},
    {"label": "OPERATOR", "pattern": "max"},
    
    # At least / at most
    {"label": "OPERATOR", "pattern": [{"LOWER": "at"}, {"LOWER": "least"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "at"}, {"LOWER": "most"}]},
    
    # Not exceed / not less than
    {"label": "OPERATOR", "pattern": [{"LOWER": "not"}, {"LOWER": "exceed"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "not"}, {"LOWER": "exceeding"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "not"}, {"LOWER": "less"}, {"LOWER": "than"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "not"}, {"LOWER": "more"}, {"LOWER": "than"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "no"}, {"LOWER": "more"}, {"LOWER": "than"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "no"}, {"LOWER": "less"}, {"LOWER": "than"}]},
    
    # Greater/less than
    {"label": "OPERATOR", "pattern": [{"LOWER": "greater"}, {"LOWER": "than"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "less"}, {"LOWER": "than"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "more"}, {"LOWER": "than"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "fewer"}, {"LOWER": "than"}]},
    
    # Up to
    {"label": "OPERATOR", "pattern": [{"LOWER": "up"}, {"LOWER": "to"}]},
    
    # Required/permitted
    {"label": "OPERATOR", "pattern": "required"},
    {"label": "OPERATOR", "pattern": "permitted"},
    {"label": "OPERATOR", "pattern": "prohibited"},
    {"label": "OPERATOR", "pattern": "allowed"},
    {"label": "OPERATOR", "pattern": "restricted"},
    {"label": "OPERATOR", "pattern": "limited"},
    
    # Equal to
    {"label": "OPERATOR", "pattern": [{"LOWER": "equal"}, {"LOWER": "to"}]},
    {"label": "OPERATOR", "pattern": [{"LOWER": "equals"}]},
]

# ============================================================================
# COMBINED PATTERNS
# ============================================================================

ALL_PATTERNS = (
    ZONE_PATTERNS +
    USE_TYPE_PATTERNS +
    SECTION_REF_PATTERNS +
    METRIC_PATTERNS +
    MEASUREMENT_PATTERNS +
    OPERATOR_PATTERNS
)

# Pattern label to category mapping
LABEL_CATEGORIES = {
    "ZONE": "zoning",
    "USE_TYPE": "use",
    "SECTION_REF": "reference",
    "METRIC": "metric",
    "MEASUREMENT": "measurement",
    "OPERATOR": "operator"
}

