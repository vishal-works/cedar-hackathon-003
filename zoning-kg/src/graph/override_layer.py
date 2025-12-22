"""
Add state-level override nodes for Texas bills (SB-840, SB-2835).
"""

from datetime import date, datetime
from typing import List, Dict, Any

from src.graphiti.client import get_graphiti_client
from src.graphiti.type_config import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP


# SB-840 Override Definitions
# Texas Senate Bill 840 - Housing Development in Commercial Areas
SB_840_OVERRIDES = [
    {
        "id": "texas:SB-840:density",
        "bill_id": "SB-840",
        "metric": "density_max",
        "override_type": "floor",
        "value": 36,
        "unit": "units/acre",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["commercial", "office", "mixed_use"],
        "effective_date": date(2025, 9, 1),
        "description": "Municipalities cannot limit density below 36 units/acre for multifamily/mixed-use in commercial zones"
    },
    {
        "id": "texas:SB-840:height",
        "bill_id": "SB-840",
        "metric": "height_max",
        "override_type": "floor",
        "value": 45,
        "unit": "ft",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["commercial", "office", "mixed_use"],
        "effective_date": date(2025, 9, 1),
        "description": "Municipalities cannot limit height below 45 feet"
    },
    {
        "id": "texas:SB-840:setback_front",
        "bill_id": "SB-840",
        "metric": "setback_front_min",
        "override_type": "ceiling",
        "value": 25,
        "unit": "ft",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["commercial", "office", "mixed_use"],
        "effective_date": date(2025, 9, 1),
        "description": "Municipalities cannot require front setbacks greater than 25 feet"
    },
    {
        "id": "texas:SB-840:setback_side",
        "bill_id": "SB-840",
        "metric": "setback_side_min",
        "override_type": "ceiling",
        "value": 10,
        "unit": "ft",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["commercial", "office", "mixed_use"],
        "effective_date": date(2025, 9, 1),
        "description": "Municipalities cannot require side setbacks greater than 10 feet"
    },
    {
        "id": "texas:SB-840:setback_rear",
        "bill_id": "SB-840",
        "metric": "setback_rear_min",
        "override_type": "ceiling",
        "value": 10,
        "unit": "ft",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["commercial", "office", "mixed_use"],
        "effective_date": date(2025, 9, 1),
        "description": "Municipalities cannot require rear setbacks greater than 10 feet"
    },
    {
        "id": "texas:SB-840:parking",
        "bill_id": "SB-840",
        "metric": "parking_spaces_per_unit",
        "override_type": "ceiling",
        "value": 1,
        "unit": "spaces",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["commercial", "office", "mixed_use"],
        "effective_date": date(2025, 9, 1),
        "description": "Municipalities cannot require more than 1 parking space per unit"
    },
    {
        "id": "texas:SB-840:lot_area_per_unit",
        "bill_id": "SB-840",
        "metric": "lot_area_per_unit_min",
        "override_type": "ceiling",
        "value": 1210,
        "unit": "sqft",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["commercial", "office", "mixed_use"],
        "effective_date": date(2025, 9, 1),
        "description": "Municipalities cannot require more than 1,210 sqft of lot area per unit"
    },
]


# SB-2835 Conditions (Housing Development Adjacent to Transit)
SB_2835_CONDITIONS = [
    {
        "id": "texas:SB-2835:transit_density",
        "bill_id": "SB-2835",
        "metric": "density_max",
        "override_type": "floor",
        "value": 50,
        "unit": "units/acre",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["all"],
        "condition": "within 0.5 miles of transit station",
        "effective_date": date(2025, 9, 1),
        "description": "Near transit stations, municipalities cannot limit density below 50 units/acre"
    },
    {
        "id": "texas:SB-2835:transit_height",
        "bill_id": "SB-2835",
        "metric": "height_max",
        "override_type": "floor",
        "value": 65,
        "unit": "ft",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["all"],
        "condition": "within 0.5 miles of transit station",
        "effective_date": date(2025, 9, 1),
        "description": "Near transit stations, municipalities cannot limit height below 65 feet"
    },
    {
        "id": "texas:SB-2835:transit_parking",
        "bill_id": "SB-2835",
        "metric": "parking_spaces_per_unit",
        "override_type": "ceiling",
        "value": 0.5,
        "unit": "spaces",
        "scope_uses": ["multifamily", "mixed_use"],
        "scope_zones": ["all"],
        "condition": "within 0.25 miles of transit station",
        "effective_date": date(2025, 9, 1),
        "description": "Very near transit, parking requirement capped at 0.5 spaces per unit"
    },
]


async def add_override_layer(verbose: bool = False):
    """
    Add Texas state bill overrides to the knowledge graph.
    """
    client = get_graphiti_client()
    
    print("Adding override layer...")
    
    # Add SB-840 overrides
    sb840_content_parts = []
    for override in SB_840_OVERRIDES:
        override_content = f"""
        Texas State Bill SB-840 creates an Override for {override['metric']}.
        Override ID: {override['id']}
        Bill ID: {override['bill_id']}
        Jurisdiction ID: texas
        Override type: {override['override_type']} (localities cannot go {'below' if override['override_type'] == 'floor' else 'above'} this value)
        Metric: {override['metric']}
        Value: {override['value']} {override['unit']}
        Applies to use types: {', '.join(override['scope_uses'])}
        Applies in zone families: {', '.join(override['scope_zones'])}
        Effective date: {override['effective_date'].isoformat()}
        
        {override['description']}
        
        This override is issued by the State of Texas (jurisdiction_id: texas).
        The jurisdiction "texas" CONTAINS this override.
        """
        sb840_content_parts.append(override_content)
        
        if verbose:
            print(f"  Prepared override: {override['id']}")
    
    # Add SB-840 as single episode for efficiency
    await client.add_episode(
        name="Texas SB-840 Overrides",
        episode_body="\n\n---\n\n".join(sb840_content_parts),
        source_description="Texas Senate Bill 840 (89th Legislature)",
        reference_time=datetime.now(),
        entity_types=ENTITY_TYPES,
        edge_types=EDGE_TYPES,
        edge_type_map=EDGE_TYPE_MAP
    )
    
    print(f"  Added {len(SB_840_OVERRIDES)} SB-840 overrides")
    
    # Add SB-2835 conditions
    sb2835_content_parts = []
    for condition in SB_2835_CONDITIONS:
        condition_content = f"""
        Texas State Bill SB-2835 creates a transit-oriented Override for {condition['metric']}.
        Override ID: {condition['id']}
        Bill ID: {condition['bill_id']}
        Jurisdiction ID: texas
        Override type: {condition['override_type']}
        Metric: {condition['metric']}
        Value: {condition['value']} {condition['unit']}
        Condition: {condition.get('condition', 'N/A')}
        Applies to use types: {', '.join(condition['scope_uses'])}
        Effective date: {condition['effective_date'].isoformat()}
        
        {condition['description']}
        
        This is a conditional override that only applies {condition.get('condition', '')}.
        Issued by jurisdiction "texas".
        """
        sb2835_content_parts.append(condition_content)
        
        if verbose:
            print(f"  Prepared condition: {condition['id']}")
    
    await client.add_episode(
        name="Texas SB-2835 Transit-Oriented Overrides",
        episode_body="\n\n---\n\n".join(sb2835_content_parts),
        source_description="Texas Senate Bill 2835 (89th Legislature)",
        reference_time=datetime.now(),
        entity_types=ENTITY_TYPES,
        edge_types=EDGE_TYPES,
        edge_type_map=EDGE_TYPE_MAP
    )
    
    print(f"  Added {len(SB_2835_CONDITIONS)} SB-2835 conditions")
    
    total = len(SB_840_OVERRIDES) + len(SB_2835_CONDITIONS)
    print(f"\nOverride layer complete: {total} total overrides added")


def get_overrides_for_metric(metric: str) -> List[Dict[str, Any]]:
    """
    Get all overrides that apply to a specific metric.
    
    Args:
        metric: Metric slug (e.g., 'density_max', 'height_max')
        
    Returns:
        List of override definitions
    """
    overrides = []
    
    for override in SB_840_OVERRIDES:
        if override["metric"] == metric:
            overrides.append(override)
    
    for condition in SB_2835_CONDITIONS:
        if condition["metric"] == metric:
            overrides.append(condition)
    
    return overrides


def check_override_applies(
    metric: str,
    use_type: str,
    zone_family: str,
    near_transit: bool = False
) -> List[Dict[str, Any]]:
    """
    Check which overrides apply to a specific development context.
    
    Args:
        metric: Metric being checked
        use_type: Type of use (e.g., 'multifamily')
        zone_family: Zone family (e.g., 'commercial')
        near_transit: Whether the site is near transit
        
    Returns:
        List of applicable overrides
    """
    applicable = []
    
    for override in SB_840_OVERRIDES:
        if override["metric"] == metric:
            if use_type in override["scope_uses"]:
                if zone_family in override["scope_zones"]:
                    applicable.append(override)
    
    if near_transit:
        for condition in SB_2835_CONDITIONS:
            if condition["metric"] == metric:
                if use_type in condition["scope_uses"]:
                    applicable.append(condition)
    
    return applicable


if __name__ == "__main__":
    import asyncio
    asyncio.run(add_override_layer(verbose=True))

