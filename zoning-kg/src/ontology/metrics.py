"""
Standardized metric slugs for constraint normalization.

All constraints must use these slugs to enable consistent querying.
"""

from enum import Enum
from typing import Dict, Any


class MetricScope(str, Enum):
    LOT = "lot"
    SITE = "site"
    BUILDING = "building"
    UNIT = "unit"


# Metric definitions: slug -> {display_name, unit, scope, description}
METRICS_CATALOG: Dict[str, Dict[str, Any]] = {
    # Lot-level metrics
    "lot_area_min": {
        "display_name": "Minimum Lot Area",
        "unit": "sqft",
        "scope": MetricScope.LOT,
        "description": "Minimum area per individual lot"
    },
    "lot_width_min": {
        "display_name": "Minimum Lot Width",
        "unit": "ft",
        "scope": MetricScope.LOT,
        "description": "Minimum width at building line"
    },
    "lot_depth_min": {
        "display_name": "Minimum Lot Depth",
        "unit": "ft",
        "scope": MetricScope.LOT,
        "description": "Front-to-rear dimension"
    },
    "setback_front_min": {
        "display_name": "Front Setback",
        "unit": "ft",
        "scope": MetricScope.LOT,
        "description": "Distance from front property line"
    },
    "setback_side_min": {
        "display_name": "Side Setback",
        "unit": "ft",
        "scope": MetricScope.LOT,
        "description": "Distance from side property line"
    },
    "setback_rear_min": {
        "display_name": "Rear Setback",
        "unit": "ft",
        "scope": MetricScope.LOT,
        "description": "Distance from rear property line"
    },
    "setback_street_side_min": {
        "display_name": "Street Side Setback",
        "unit": "ft",
        "scope": MetricScope.LOT,
        "description": "Corner lot street-facing side"
    },
    "setback_min": {
        "display_name": "General Setback",
        "unit": "ft",
        "scope": MetricScope.LOT,
        "description": "Generic setback requirement"
    },
    
    # Site-level metrics
    "site_area_min": {
        "display_name": "Minimum Site Area",
        "unit": "sqft",
        "scope": MetricScope.SITE,
        "description": "Total development parcel"
    },
    "lot_area_per_unit_min": {
        "display_name": "Lot Area per Unit",
        "unit": "sqft",
        "scope": MetricScope.SITE,
        "description": "Site area ÷ unit count"
    },
    "impervious_cover_max": {
        "display_name": "Impervious Cover",
        "unit": "%",
        "scope": MetricScope.SITE,
        "description": "Maximum impervious surface"
    },
    "density_max": {
        "display_name": "Maximum Density",
        "unit": "units/acre",
        "scope": MetricScope.SITE,
        "description": "Dwelling units per acre"
    },
    "far_max": {
        "display_name": "Floor Area Ratio",
        "unit": "ratio",
        "scope": MetricScope.SITE,
        "description": "Floor area ÷ lot area"
    },
    "units_per_group_max": {
        "display_name": "Units per Group",
        "unit": "units",
        "scope": MetricScope.SITE,
        "description": "Max attached units (townhouse)"
    },
    "group_spacing_min": {
        "display_name": "Group Spacing",
        "unit": "ft",
        "scope": MetricScope.SITE,
        "description": "Distance between unit groups"
    },
    "open_space_min": {
        "display_name": "Minimum Open Space",
        "unit": "sqft",
        "scope": MetricScope.SITE,
        "description": "Required open space area"
    },
    
    # Building-level metrics
    "height_max": {
        "display_name": "Maximum Height",
        "unit": "ft",
        "scope": MetricScope.BUILDING,
        "description": "Building height limit"
    },
    "stories_max": {
        "display_name": "Maximum Stories",
        "unit": "stories",
        "scope": MetricScope.BUILDING,
        "description": "Number of floors"
    },
    "building_coverage_max": {
        "display_name": "Building Coverage",
        "unit": "%",
        "scope": MetricScope.BUILDING,
        "description": "Lot area under buildings"
    },
    
    # Unit-level metrics
    "unit_area_min": {
        "display_name": "Minimum Unit Area",
        "unit": "sqft",
        "scope": MetricScope.UNIT,
        "description": "Dwelling unit size"
    },
    "open_space_private_min": {
        "display_name": "Private Open Space",
        "unit": "sqft",
        "scope": MetricScope.UNIT,
        "description": "Outdoor space per unit"
    },
    "parking_spaces_per_unit": {
        "display_name": "Parking per Unit",
        "unit": "spaces",
        "scope": MetricScope.UNIT,
        "description": "Required parking"
    },
    "units_per_lot_max": {
        "display_name": "Units per Lot",
        "unit": "units",
        "scope": MetricScope.LOT,
        "description": "Maximum dwelling units per lot"
    },
}


def get_metric_scope(metric_slug: str) -> MetricScope:
    """Get the scope for a metric slug."""
    if metric_slug in METRICS_CATALOG:
        return METRICS_CATALOG[metric_slug]["scope"]
    raise ValueError(f"Unknown metric: {metric_slug}")


def validate_metric_slug(slug: str) -> bool:
    """Check if a metric slug is valid."""
    return slug in METRICS_CATALOG


def get_metric_info(slug: str) -> Dict[str, Any]:
    """Get full metadata for a metric."""
    if slug in METRICS_CATALOG:
        return METRICS_CATALOG[slug]
    raise ValueError(f"Unknown metric: {slug}")

