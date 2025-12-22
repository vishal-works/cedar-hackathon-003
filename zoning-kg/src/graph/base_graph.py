"""
Build the base graph layer: Jurisdictions, Zones, UseTypes.

This creates the structural foundation before episode ingestion.
"""

from typing import List, Dict
from datetime import datetime

from src.graphiti.client import get_graphiti_client
from src.graphiti.type_config import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP


# Austin zone definitions
AUSTIN_ZONES = {
    # Single-Family
    "SF-1": {"name": "Single-Family Residence (Large Lot)", "family": "single_family"},
    "SF-2": {"name": "Single-Family Residence (Standard Lot)", "family": "single_family"},
    "SF-3": {"name": "Family Residence", "family": "single_family"},
    "SF-4A": {"name": "Urban Family Residence (Moderate-High Density)", "family": "single_family"},
    "SF-4B": {"name": "Urban Family Residence (Moderate-High Density)", "family": "single_family"},
    "SF-5": {"name": "Urban Family Residence", "family": "single_family"},
    "SF-6": {"name": "Townhouse/Condominium Residence", "family": "single_family"},
    
    # Multifamily
    "MF-1": {"name": "Limited Density Multifamily", "family": "multifamily"},
    "MF-2": {"name": "Low Density Multifamily", "family": "multifamily"},
    "MF-3": {"name": "Medium Density Multifamily", "family": "multifamily"},
    "MF-4": {"name": "Moderate-High Density Multifamily", "family": "multifamily"},
    "MF-5": {"name": "High Density Multifamily", "family": "multifamily"},
    "MF-6": {"name": "Highest Density Multifamily", "family": "multifamily"},
    
    # Commercial
    "LR": {"name": "Neighborhood Commercial", "family": "commercial"},
    "GR": {"name": "Community Commercial", "family": "commercial"},
    "CR": {"name": "Commercial Recreation", "family": "commercial"},
    "CS": {"name": "General Commercial Services", "family": "commercial"},
    "CS-1": {"name": "General Commercial Services (Conditional)", "family": "commercial"},
    "CH": {"name": "Commercial Highway", "family": "commercial"},
    "CBD": {"name": "Central Business District", "family": "commercial"},
    
    # Office
    "GO": {"name": "General Office", "family": "office"},
    "LO": {"name": "Limited Office", "family": "office"},
    "NO": {"name": "Neighborhood Office", "family": "office"},
    
    # Industrial
    "IP": {"name": "Industrial Park", "family": "industrial"},
    "MI": {"name": "Major Industry", "family": "industrial"},
    "LI": {"name": "Limited Industrial", "family": "industrial"},
    
    # Mixed Use
    "DMU": {"name": "Downtown Mixed Use", "family": "mixed_use"},
    "MU": {"name": "Mixed Use", "family": "mixed_use"},
    "VMU": {"name": "Vertical Mixed Use", "family": "mixed_use"},
    
    # Planned
    "PUD": {"name": "Planned Unit Development", "family": "planned"},
    "P": {"name": "Public", "family": "planned"},
}


# Use type definitions
USE_TYPES = {
    "single_family": {
        "name": "Single-Family Dwelling",
        "group": "residential",
        "aliases": ["single family", "detached dwelling", "SFR"]
    },
    "townhouse": {
        "name": "Townhouse",
        "group": "residential",
        "aliases": ["townhome", "row house", "attached dwelling"]
    },
    "condominium": {
        "name": "Condominium",
        "group": "residential",
        "aliases": ["condo", "condominium development"]
    },
    "duplex": {
        "name": "Duplex",
        "group": "residential",
        "aliases": ["two-family", "two-unit dwelling"]
    },
    "multifamily": {
        "name": "Multifamily",
        "group": "residential",
        "aliases": ["multi-family", "apartment", "apartment complex"]
    },
    "accessory_dwelling_unit": {
        "name": "Accessory Dwelling Unit",
        "group": "residential",
        "aliases": ["ADU", "granny flat", "secondary dwelling"]
    },
    "mixed_use": {
        "name": "Mixed Use",
        "group": "mixed_use",
        "aliases": ["mixed-use development", "live-work"]
    },
}


# Zone -> allowed use types mapping
ZONE_USE_MAP = {
    "SF-1": ["single_family"],
    "SF-2": ["single_family"],
    "SF-3": ["single_family", "duplex"],
    "SF-4A": ["single_family", "duplex"],
    "SF-4B": ["single_family", "duplex"],
    "SF-5": ["single_family", "duplex", "townhouse", "condominium"],
    "SF-6": ["single_family", "duplex", "townhouse", "condominium", "multifamily"],
    "MF-1": ["single_family", "duplex", "townhouse", "condominium", "multifamily"],
    "MF-2": ["single_family", "duplex", "townhouse", "condominium", "multifamily"],
    "MF-3": ["single_family", "duplex", "townhouse", "condominium", "multifamily"],
    "MF-4": ["single_family", "duplex", "townhouse", "condominium", "multifamily"],
    "MF-5": ["single_family", "duplex", "townhouse", "condominium", "multifamily"],
    "MF-6": ["single_family", "duplex", "townhouse", "condominium", "multifamily"],
    "GR": ["multifamily", "mixed_use"],
    "CR": ["multifamily", "mixed_use"],
    "CS": ["multifamily", "mixed_use"],
    "CH": ["multifamily", "mixed_use"],
    "CBD": ["multifamily", "mixed_use"],
    "DMU": ["multifamily", "mixed_use"],
    "MU": ["multifamily", "mixed_use"],
    "VMU": ["multifamily", "mixed_use"],
}


async def build_base_graph(verbose: bool = False):
    """
    Build the foundational graph structure.
    
    Creates:
    1. Jurisdiction nodes (austin_tx, texas)
    2. Zone nodes with CONTAINS edges
    3. UseType nodes with ALLOWS_USE edges
    """
    client = get_graphiti_client()
    
    print("Building base graph...")
    
    # Create jurisdictions
    jurisdictions_content = """
    City of Austin (austin_tx) is a city jurisdiction in Texas.
    The City of Austin has ID "austin_tx", name "City of Austin", state "TX", and level "city".
    
    State of Texas (texas) is a state jurisdiction.
    The State of Texas has ID "texas", name "State of Texas", state "TX", and level "state".
    
    Austin is contained within Texas for regulatory purposes.
    The texas jurisdiction contains the austin_tx jurisdiction.
    """
    
    await client.add_episode(
        name="Base Jurisdictions",
        episode_body=jurisdictions_content,
        source_description="ORGAnIZM Base Graph",
        reference_time=datetime.now(),
        entity_types=ENTITY_TYPES,
        edge_types=EDGE_TYPES,
        edge_type_map=EDGE_TYPE_MAP
    )
    
    if verbose:
        print("  Created jurisdiction nodes")
    
    # Create zones in batches to reduce API calls
    zone_batch = []
    for zone_code, zone_info in AUSTIN_ZONES.items():
        zone_content = f"""
        Zone {zone_code} ({zone_info['name']}) is a {zone_info['family']} zoning district 
        in the City of Austin (austin_tx). 
        Zone ID: austin_tx:{zone_code}
        Zone code: {zone_code}
        Zone name: {zone_info['name']}
        Zone family: {zone_info['family']}
        Jurisdiction ID: austin_tx
        The jurisdiction austin_tx CONTAINS zone austin_tx:{zone_code}.
        """
        zone_batch.append(zone_content)
    
    # Combine zones into larger episodes for efficiency
    batch_size = 5
    for i in range(0, len(zone_batch), batch_size):
        batch_content = "\n\n---\n\n".join(zone_batch[i:i+batch_size])
        await client.add_episode(
            name=f"Zone Definitions Batch {i//batch_size + 1}",
            episode_body=batch_content,
            source_description="Austin Land Development Code",
            reference_time=datetime.now(),
            entity_types=ENTITY_TYPES,
            edge_types=EDGE_TYPES,
            edge_type_map=EDGE_TYPE_MAP
        )
        if verbose:
            print(f"  Created zone batch {i//batch_size + 1}")
    
    # Create use types
    use_batch = []
    for use_id, use_info in USE_TYPES.items():
        use_content = f"""
        Use type {use_info['name']} (id: {use_id}) is a {use_info['group']} use.
        Use type ID: {use_id}
        Use type name: {use_info['name']}
        Use type group: {use_info['group']}
        Aliases: {', '.join(use_info['aliases'])}
        """
        use_batch.append(use_content)
    
    use_content_all = "\n\n---\n\n".join(use_batch)
    await client.add_episode(
        name="Use Type Definitions",
        episode_body=use_content_all,
        source_description="ORGAnIZM Use Type Definitions",
        reference_time=datetime.now(),
        entity_types=ENTITY_TYPES,
        edge_types=EDGE_TYPES,
        edge_type_map=EDGE_TYPE_MAP
    )
    
    if verbose:
        print("  Created use type nodes")
    
    # Create zone-use relationships in batches
    rel_batch = []
    for zone_code, allowed_uses in ZONE_USE_MAP.items():
        for use_id in allowed_uses:
            rel_content = f"""
            Zone {zone_code} (austin_tx:{zone_code}) allows use type {use_id} by right.
            The zone austin_tx:{zone_code} has an AllowsUse edge to use type {use_id}.
            permitted_by_right: true
            """
            rel_batch.append(rel_content)
    
    for i in range(0, len(rel_batch), 10):
        batch_content = "\n\n".join(rel_batch[i:i+10])
        await client.add_episode(
            name=f"Zone-Use Relationships Batch {i//10 + 1}",
            episode_body=batch_content,
            source_description="Austin LDC Use Regulations",
            reference_time=datetime.now(),
            entity_types=ENTITY_TYPES,
            edge_types=EDGE_TYPES,
            edge_type_map=EDGE_TYPE_MAP
        )
        if verbose:
            print(f"  Created zone-use relationships batch {i//10 + 1}")
    
    print(f"Base graph created: {len(AUSTIN_ZONES)} zones, {len(USE_TYPES)} use types")


async def verify_base_graph():
    """
    Verify that the base graph was created correctly.
    
    Returns summary statistics.
    """
    from neo4j import GraphDatabase
    import os
    
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            RETURN labels(n) as labels, count(n) as count
        """)
        counts = {record["labels"][0]: record["count"] for record in result}
    
    driver.close()
    
    return counts


if __name__ == "__main__":
    import asyncio
    asyncio.run(build_base_graph(verbose=True))

