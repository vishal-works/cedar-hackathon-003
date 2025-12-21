"""
Entity normalization functions for zoning entities.

Normalizes recognized entities to canonical forms for consistent
representation in the knowledge graph.
"""
import re
from typing import Union, Dict, Optional, Any


# ============================================================================
# ZONE NORMALIZATION
# ============================================================================

# Zone code normalization patterns
ZONE_VARIANT_MAP = {
    # Handle common variants without hyphens
    "SF1": "SF-1",
    "SF2": "SF-2",
    "SF3": "SF-3",
    "SF4A": "SF-4A",
    "SF4B": "SF-4B",
    "SF5": "SF-5",
    "SF6": "SF-6",
    "MF1": "MF-1",
    "MF2": "MF-2",
    "MF3": "MF-3",
    "MF4": "MF-4",
    "MF5": "MF-5",
    "MF6": "MF-6",
    "CS1": "CS-1",
}

# Zone name to code mapping
ZONE_NAME_TO_CODE = {
    "urban family residence": "SF-5",
    "single family residence": "SF-3",
    "single family residence large lot": "SF-1",
    "single family residence standard lot": "SF-2",
    "family residence": "SF-3",
    "single family residence small lot": "SF-4A",
    "single family residence condominium site": "SF-4B",
    "townhouse and condominium residence": "SF-6",
    "multifamily residence limited density": "MF-1",
    "multifamily residence low density": "MF-2",
    "multifamily residence medium density": "MF-3",
    "multifamily residence moderate high density": "MF-4",
    "multifamily residence moderate - high density": "MF-4",
    "multifamily residence high density": "MF-5",
    "multifamily residence highest density": "MF-6",
    "mobile home residence": "MH",
    "lake austin": "LA",
    "rural residence": "RR",
    "central business district": "CBD",
    "downtown mixed use": "DMU",
    "planned unit development": "PUD",
    "neighborhood office": "NO",
    "limited office": "LO",
    "general office": "GO",
    "community commercial": "CR",
    "limited retail": "LR",
    "general retail": "GR",
    "commercial services": "CS",
    "commercial highway": "CH",
    "industrial park": "IP",
    "major industry": "MI",
    "limited industrial": "LI",
    "research and development": "R&D",
    "aviation services": "AV",
    "agricultural": "AG",
    "public": "P",
    "warehouse limited office": "W/LO",
}


def normalize_zone(text: str) -> Dict[str, Any]:
    """
    Normalize zone codes to canonical form.
    
    Args:
        text: The zone text to normalize
        
    Returns:
        Dictionary with normalized zone information
    """
    original = text
    
    # Uppercase and strip
    text = text.upper().strip()
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Check variant map first
    if text.replace(' ', '') in ZONE_VARIANT_MAP:
        text = ZONE_VARIANT_MAP[text.replace(' ', '')]
    
    # Handle "SF 5" -> "SF-5" pattern
    match = re.match(r'^([A-Z]+)\s*(\d+[A-Z]?)$', text)
    if match:
        text = f"{match.group(1)}-{match.group(2)}"
    
    # Check name mapping for full names
    text_lower = original.lower().strip()
    if text_lower in ZONE_NAME_TO_CODE:
        code = ZONE_NAME_TO_CODE[text_lower]
        return {
            "code": code,
            "name": text_lower,
            "original": original
        }
    
    return {
        "code": text,
        "original": original
    }


# ============================================================================
# MEASUREMENT NORMALIZATION
# ============================================================================

# Unit normalization mapping
UNIT_NORMALIZATION = {
    "feet": "ft",
    "foot": "ft",
    "ft.": "ft",
    "'": "ft",
    "square feet": "sqft",
    "sq ft": "sqft",
    "sq. ft.": "sqft",
    "sq. ft": "sqft",
    "sf": "sqft",
    "acre": "acre",
    "acres": "acre",
    "percent": "%",
    "percentage": "%",
    "stories": "story",
    "story": "story",
}


def normalize_measurement(text: str) -> Dict[str, Any]:
    """
    Normalize measurement values.
    
    Extracts numeric value and normalizes unit.
    
    Args:
        text: The measurement text (e.g., "20 feet", "40%")
        
    Returns:
        Dictionary with value, unit, and original text
    """
    original = text.lower().strip()
    
    # Handle ratio patterns (e.g., "1:1", "8:1")
    ratio_match = re.match(r'^(\d+):(\d+)$', text.strip())
    if ratio_match:
        return {
            "value": f"{ratio_match.group(1)}:{ratio_match.group(2)}",
            "unit": "ratio",
            "numerator": int(ratio_match.group(1)),
            "denominator": int(ratio_match.group(2)),
            "original": text
        }
    
    # Handle percentage pattern
    percent_match = re.match(r'^([\d,]+(?:\.\d+)?)\s*(%|percent|percentage)$', text.strip(), re.IGNORECASE)
    if percent_match:
        value_str = percent_match.group(1).replace(',', '')
        return {
            "value": float(value_str),
            "unit": "%",
            "original": text
        }
    
    # Handle units per acre (density)
    density_match = re.match(r'^([\d,]+(?:\.\d+)?)\s*units?\s*per\s*acre$', text.strip(), re.IGNORECASE)
    if density_match:
        value_str = density_match.group(1).replace(',', '')
        return {
            "value": float(value_str),
            "unit": "units/acre",
            "original": text
        }
    
    # General pattern: number + unit
    pattern = re.match(r'^([\d,]+(?:\.\d+)?)\s*(.+)$', text.strip())
    if pattern:
        value_str = pattern.group(1).replace(',', '')
        try:
            value = float(value_str)
            if value == int(value):
                value = int(value)
        except ValueError:
            value = value_str
            
        unit_text = pattern.group(2).strip().lower()
        
        # Normalize unit
        unit = unit_text
        for variant, normalized in UNIT_NORMALIZATION.items():
            if unit_text == variant or unit_text.startswith(variant):
                unit = normalized
                break
        
        # Handle "square feet" specifically
        if "square" in unit_text and "feet" in unit_text:
            unit = "sqft"
        elif "sq" in unit_text and "ft" in unit_text:
            unit = "sqft"
        
        return {
            "value": value,
            "unit": unit,
            "original": text
        }
    
    # Fallback: return as-is
    return {
        "value": text,
        "unit": None,
        "original": text
    }


# ============================================================================
# METRIC NORMALIZATION
# ============================================================================

# Metric slug mapping
METRIC_SLUG_MAP = {
    # Lot dimensions
    "lot width": "lot_width_min",
    "minimum lot width": "lot_width_min",
    "lot size": "lot_size_min",
    "minimum lot size": "lot_size_min",
    "lot area": "lot_area_min",
    "minimum lot area": "lot_area_min",
    "lot depth": "lot_depth_min",
    "corner lot width": "corner_lot_width_min",
    "corner lot area": "corner_lot_area_min",
    "site area": "site_area_min",
    "minimum site area": "site_area_min",
    
    # Setbacks
    "setback": "setback_min",
    "setbacks": "setback_min",
    "front yard": "front_yard_setback_min",
    "rear yard": "rear_yard_setback_min",
    "side yard": "side_yard_setback_min",
    "front setback": "front_setback_min",
    "rear setback": "rear_setback_min",
    "side setback": "side_setback_min",
    "street side yard": "street_side_yard_min",
    "interior side yard": "interior_side_yard_min",
    
    # Height
    "height": "height_max",
    "building height": "height_max",
    "maximum height": "height_max",
    "structure height": "height_max",
    
    # Coverage
    "building coverage": "building_coverage_max",
    "maximum building coverage": "building_coverage_max",
    "impervious cover": "impervious_cover_max",
    "impervious coverage": "impervious_cover_max",
    "maximum impervious cover": "impervious_cover_max",
    
    # Density and FAR
    "floor area ratio": "floor_area_ratio_max",
    "far": "floor_area_ratio_max",
    "maximum floor area ratio": "floor_area_ratio_max",
    "density": "density_max",
    "dwelling units per acre": "dwelling_units_per_acre_max",
    "units per acre": "dwelling_units_per_acre_max",
    "dwelling units per lot": "dwelling_units_per_lot_max",
    "units per lot": "dwelling_units_per_lot_max",
    
    # Parking
    "parking spaces": "parking_spaces_min",
    "parking requirement": "parking_spaces_min",
    "parking requirements": "parking_spaces_min",
    
    # Other
    "open space": "open_space_min",
    "landscaping": "landscaping_min",
    "buffer": "buffer_min",
    "screening": "screening_required",
}


def normalize_metric(text: str) -> str:
    """
    Normalize metric names to standardized slugs.
    
    Args:
        text: The metric text (e.g., "lot width", "minimum lot width")
        
    Returns:
        Normalized slug string
    """
    text_lower = text.lower().strip()
    
    # Check direct mapping
    if text_lower in METRIC_SLUG_MAP:
        return METRIC_SLUG_MAP[text_lower]
    
    # Try without "minimum" or "maximum" prefix
    for prefix in ["minimum ", "maximum ", "min ", "max "]:
        if text_lower.startswith(prefix):
            stripped = text_lower[len(prefix):]
            if stripped in METRIC_SLUG_MAP:
                return METRIC_SLUG_MAP[stripped]
    
    # Fallback: convert to slug format
    slug = re.sub(r'\s+', '_', text_lower)
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    return slug


# ============================================================================
# SECTION REFERENCE NORMALIZATION
# ============================================================================

def normalize_section_ref(text: str) -> Dict[str, Any]:
    """
    Normalize section references.
    
    Args:
        text: The section reference text (e.g., "§ 25-2-775", "Section 25-2-775(B)")
        
    Returns:
        Dictionary with section number and optional subsection
    """
    # Remove § symbol and "Section" prefix
    text = text.replace('§', '').strip()
    text = re.sub(r'^section\s*', '', text, flags=re.IGNORECASE)
    text = text.strip()
    
    # Check for subsection in parentheses
    subsection_match = re.match(r'^([\d-]+[A-Z]?)\(([A-Za-z0-9]+)\)$', text)
    if subsection_match:
        return {
            "section": subsection_match.group(1),
            "subsection": subsection_match.group(2),
            "full_reference": f"{subsection_match.group(1)}({subsection_match.group(2)})"
        }
    
    # Simple section reference
    section_match = re.match(r'^([\d-]+[A-Z]?)$', text)
    if section_match:
        return {
            "section": section_match.group(1),
            "subsection": None,
            "full_reference": section_match.group(1)
        }
    
    # Handle article/division/chapter references
    article_match = re.match(r'^article\s*(\d+)$', text, re.IGNORECASE)
    if article_match:
        return {
            "type": "article",
            "number": int(article_match.group(1)),
            "full_reference": f"Article {article_match.group(1)}"
        }
    
    division_match = re.match(r'^division\s*(\d+)$', text, re.IGNORECASE)
    if division_match:
        return {
            "type": "division",
            "number": int(division_match.group(1)),
            "full_reference": f"Division {division_match.group(1)}"
        }
    
    chapter_match = re.match(r'^chapter\s*([\d-]+)$', text, re.IGNORECASE)
    if chapter_match:
        return {
            "type": "chapter",
            "number": chapter_match.group(1),
            "full_reference": f"Chapter {chapter_match.group(1)}"
        }
    
    subchapter_match = re.match(r'^subchapter\s*([A-Z])$', text, re.IGNORECASE)
    if subchapter_match:
        return {
            "type": "subchapter",
            "letter": subchapter_match.group(1).upper(),
            "full_reference": f"Subchapter {subchapter_match.group(1).upper()}"
        }
    
    # Fallback
    return {
        "section": text,
        "subsection": None,
        "full_reference": text
    }


# ============================================================================
# USE TYPE NORMALIZATION
# ============================================================================

# Use type normalization mapping
USE_TYPE_NORMALIZATION = {
    "townhouses": "townhouse",
    "condominiums": "condominium",
    "duplexes": "duplex",
    "single-family": "single_family",
    "single family": "single_family",
    "two-family": "two_family",
    "two family": "two_family",
    "multi-family": "multifamily",
    "multi family": "multifamily",
    "mobile home": "mobile_home",
    "mobile home park": "mobile_home_park",
    "accessory dwelling unit": "adu",
    "dwelling unit": "dwelling_unit",
    "dwelling units": "dwelling_unit",
    "group residential": "group_residential",
    "mixed use": "mixed_use",
    "retirement housing": "retirement_housing",
    "affordable housing": "affordable_housing",
    "parking structure": "parking_structure",
    "parking garage": "parking_garage",
}


def normalize_use_type(text: str) -> str:
    """
    Normalize use type to canonical form.
    
    Args:
        text: The use type text
        
    Returns:
        Normalized use type string
    """
    text_lower = text.lower().strip()
    
    if text_lower in USE_TYPE_NORMALIZATION:
        return USE_TYPE_NORMALIZATION[text_lower]
    
    # Default: lowercase and replace spaces with underscores
    return re.sub(r'\s+', '_', text_lower)


# ============================================================================
# OPERATOR NORMALIZATION
# ============================================================================

# Operator normalization mapping
OPERATOR_NORMALIZATION = {
    "minimum": "min",
    "maximum": "max",
    "at least": "gte",
    "at most": "lte",
    "not exceed": "lte",
    "not exceeding": "lte",
    "not less than": "gte",
    "not more than": "lte",
    "no more than": "lte",
    "no less than": "gte",
    "greater than": "gt",
    "less than": "lt",
    "more than": "gt",
    "fewer than": "lt",
    "up to": "lte",
    "equal to": "eq",
    "equals": "eq",
    "required": "required",
    "permitted": "permitted",
    "prohibited": "prohibited",
    "allowed": "permitted",
    "restricted": "restricted",
    "limited": "limited",
}


def normalize_operator(text: str) -> str:
    """
    Normalize operator to canonical form.
    
    Args:
        text: The operator text
        
    Returns:
        Normalized operator string
    """
    text_lower = text.lower().strip()
    
    if text_lower in OPERATOR_NORMALIZATION:
        return OPERATOR_NORMALIZATION[text_lower]
    
    return text_lower


# ============================================================================
# UNIFIED NORMALIZATION FUNCTION
# ============================================================================

def normalize_entity(text: str, label: str) -> Union[str, Dict[str, Any]]:
    """
    Normalize an entity based on its label.
    
    Args:
        text: The entity text
        label: The entity label (ZONE, MEASUREMENT, METRIC, etc.)
        
    Returns:
        Normalized form - either a string or dictionary depending on entity type
    """
    if label == "ZONE":
        return normalize_zone(text)
    elif label == "MEASUREMENT":
        return normalize_measurement(text)
    elif label == "METRIC":
        return normalize_metric(text)
    elif label == "SECTION_REF":
        return normalize_section_ref(text)
    elif label == "USE_TYPE":
        return normalize_use_type(text)
    elif label == "OPERATOR":
        return normalize_operator(text)
    else:
        return text


if __name__ == "__main__":
    # Test normalization functions
    print("Zone normalization tests:")
    print(f"  'sf-5' -> {normalize_zone('sf-5')}")
    print(f"  'SF5' -> {normalize_zone('SF5')}")
    print(f"  'SF 5' -> {normalize_zone('SF 5')}")
    print(f"  'urban family residence' -> {normalize_zone('urban family residence')}")
    
    print("\nMeasurement normalization tests:")
    print(f"  '20 feet' -> {normalize_measurement('20 feet')}")
    print(f"  '5750 sqft' -> {normalize_measurement('5750 sqft')}")
    print(f"  '40%' -> {normalize_measurement('40%')}")
    print(f"  '40 percent' -> {normalize_measurement('40 percent')}")
    print(f"  '1:1' -> {normalize_measurement('1:1')}")
    print(f"  '17 units per acre' -> {normalize_measurement('17 units per acre')}")
    
    print("\nMetric normalization tests:")
    print(f"  'lot width' -> {normalize_metric('lot width')}")
    print(f"  'minimum lot width' -> {normalize_metric('minimum lot width')}")
    print(f"  'setback' -> {normalize_metric('setback')}")
    print(f"  'height' -> {normalize_metric('height')}")
    print(f"  'building coverage' -> {normalize_metric('building coverage')}")
    
    print("\nSection reference normalization tests:")
    print(f"  '§ 25-2-775' -> {normalize_section_ref('§ 25-2-775')}")
    print(f"  'Section 25-2-492' -> {normalize_section_ref('Section 25-2-492')}")
    print(f"  '§25-2-775(B)' -> {normalize_section_ref('§25-2-775(B)')}")

