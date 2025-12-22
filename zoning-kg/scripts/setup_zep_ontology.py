#!/usr/bin/env python3
"""
Set up custom ontology in Zep Cloud for the ORGAnIZM Zoning Knowledge Graph.

Based on: https://help.getzep.com/customizing-graph-structure

This script defines custom entity and edge types that match our ontology,
so when episodes are ingested, Zep will classify nodes/edges correctly.

Usage:
    python scripts/setup_zep_ontology.py
"""

import os
import sys
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

from zep_cloud.client import Zep
from zep_cloud.external_clients.ontology import (
    EntityModel, 
    EdgeModel, 
    EntityBaseText, 
    EntityBaseBoolean,
)

# Get Zep API key
ZEP_API_KEY = os.getenv("ZEP_API_KEY")

if not ZEP_API_KEY:
    print("ERROR: ZEP_API_KEY not found in .env")
    sys.exit(1)


# =============================================================================
# CUSTOM ENTITY TYPES (max 10, each with up to 10 fields)
# Note: Cannot use reserved names: uuid, name, graph_id, name_embedding, summary, created_at
# =============================================================================

class Jurisdiction(EntityModel):
    """Geographic authority that issues zoning regulations (city, county, or state)."""
    
    jurisdiction_id: Annotated[str, EntityBaseText(
        description="Composite key, e.g., 'austin_tx' or 'texas'"
    )]
    state: Annotated[str, EntityBaseText(
        description="State abbreviation, e.g., 'TX'"
    )]
    level: Annotated[str, EntityBaseText(
        description="Hierarchy level: 'city', 'county', or 'state'"
    )]


class Zone(EntityModel):
    """Zoning district classification within a jurisdiction."""
    
    zone_code: Annotated[str, EntityBaseText(
        description="Zone code, e.g., 'SF-5', 'MF-4', 'GR'"
    )]
    zone_family: Annotated[str, EntityBaseText(
        description="Zone family: single_family, multifamily, commercial, office, industrial, mixed_use, planned"
    )]
    jurisdiction_id: Annotated[str, EntityBaseText(
        description="Parent jurisdiction reference, e.g., 'austin_tx'"
    )]


class UseType(EntityModel):
    """Building or development use type (e.g., Townhouse, Single Family, Retail)."""
    
    use_group: Annotated[str, EntityBaseText(
        description="Use group: residential, commercial, industrial, or mixed_use"
    )]
    aliases: Annotated[str, EntityBaseText(
        description="Comma-separated alternative names for this use type"
    )]


class Rule(EntityModel):
    """A regulation from a specific document section."""
    
    section: Annotated[str, EntityBaseText(
        description="Section number, e.g., '25-2-775'"
    )]
    document: Annotated[str, EntityBaseText(
        description="Source document name, e.g., 'Land Development Code'"
    )]
    jurisdiction_id: Annotated[str, EntityBaseText(
        description="Jurisdiction this rule belongs to"
    )]


class Constraint(EntityModel):
    """Quantitative requirement from a rule (e.g., minimum lot width, max height)."""
    
    metric: Annotated[str, EntityBaseText(
        description="Standardized metric slug, e.g., 'lot_width_min', 'height_max', 'far_max'"
    )]
    operator: Annotated[str, EntityBaseText(
        description="Comparison operator: gte, gt, lte, lt, eq, range"
    )]
    value: Annotated[str, EntityBaseText(
        description="Numeric value as string, e.g., '25'"
    )]
    unit: Annotated[str, EntityBaseText(
        description="Unit of measurement, e.g., 'ft', 'sqft', '%'"
    )]


class Condition(EntityModel):
    """Context trigger for when a constraint applies (e.g., corner lot, arterial street)."""
    
    field: Annotated[str, EntityBaseText(
        description="Field being evaluated, e.g., 'parcel.corner_lot', 'parcel.street_class'"
    )]
    operator: Annotated[str, EntityBaseText(
        description="Comparison operator: eq, neq, gt, gte, lt, lte, in"
    )]
    condition_value: Annotated[str, EntityBaseText(
        description="Value to compare against"
    )]


class Override(EntityModel):
    """Higher-authority law that supersedes local regulations (e.g., Texas state bills)."""
    
    bill_id: Annotated[str, EntityBaseText(
        description="Bill identifier, e.g., 'SB-840', 'SB-2835'"
    )]
    override_type: Annotated[str, EntityBaseText(
        description="Type of override: 'floor' (minimum) or 'ceiling' (maximum)"
    )]
    metric: Annotated[str, EntityBaseText(
        description="What's being overridden, e.g., 'density_max', 'parking_min'"
    )]
    effective_date: Annotated[str, EntityBaseText(
        description="When the override takes effect, e.g., '2024-01-01'"
    )]


class DocumentSource(EntityModel):
    """Citation for traceability back to source documents."""
    
    document: Annotated[str, EntityBaseText(
        description="Document name, e.g., 'Land Development Code'"
    )]
    section: Annotated[str, EntityBaseText(
        description="Section reference, e.g., '25-2-775(B)'"
    )]
    subsection: Annotated[str, EntityBaseText(
        description="Subsection reference if applicable"
    )]


# =============================================================================
# CUSTOM EDGE TYPES (max 10, each with up to 10 fields)
# =============================================================================

class CONTAINS(EdgeModel):
    """Jurisdiction contains a zone or zone contains a use type."""
    
    relationship_type: Annotated[str, EntityBaseText(
        description="Type of containment: 'jurisdiction_zone' or 'zone_use'"
    )]


class ALLOWS_USE(EdgeModel):
    """Zone permits a specific use type."""
    
    permitted_by_right: Annotated[bool, EntityBaseBoolean(
        description="True if use is permitted by right without special approval"
    )]
    requires_conditional_use: Annotated[bool, EntityBaseBoolean(
        description="True if conditional use permit is required"
    )]


class GOVERNED_BY(EdgeModel):
    """Use type is regulated by a rule."""
    
    applicability: Annotated[str, EntityBaseText(
        description="How the rule applies: 'primary', 'conditional', 'exception'"
    )]


class HAS_CONSTRAINT(EdgeModel):
    """Rule contains a quantitative constraint."""
    
    constraint_type: Annotated[str, EntityBaseText(
        description="Type of constraint: 'dimensional', 'density', 'parking', 'design'"
    )]


class HAS_CONDITION(EdgeModel):
    """Constraint has conditional application."""
    
    logic: Annotated[str, EntityBaseText(
        description="Logical operator for combining conditions: 'AND' or 'OR'"
    )]


class APPLIES_IN(EdgeModel):
    """Rule or constraint applies in specific zones."""
    
    scope: Annotated[str, EntityBaseText(
        description="Scope of application: 'all', 'specific', 'except'"
    )]


class OVERRIDDEN_BY(EdgeModel):
    """Local constraint is overridden by higher authority."""
    
    resolution: Annotated[str, EntityBaseText(
        description="How conflict is resolved: 'max' for floor, 'min' for ceiling"
    )]


class SOURCED_FROM(EdgeModel):
    """Entity traces back to source document."""
    
    citation: Annotated[str, EntityBaseText(
        description="Full citation reference"
    )]


# =============================================================================
# MAIN SETUP FUNCTION
# =============================================================================

def setup_zep_ontology():
    """Set up custom ontology in Zep Cloud."""
    
    print("=" * 60)
    print("SETTING UP ZEP CLOUD CUSTOM ONTOLOGY")
    print("=" * 60)
    
    # Initialize Zep client
    client = Zep(api_key=ZEP_API_KEY)
    
    # Define entity types as dict (name -> class)
    entity_types = {
        "Jurisdiction": Jurisdiction,
        "Zone": Zone,
        "UseType": UseType,
        "Rule": Rule,
        "Constraint": Constraint,
        "Condition": Condition,
        "Override": Override,
        "DocumentSource": DocumentSource,
    }
    
    # Define edge types as dict (name -> class)
    edge_types = {
        "CONTAINS": CONTAINS,
        "ALLOWS_USE": ALLOWS_USE,
        "GOVERNED_BY": GOVERNED_BY,
        "HAS_CONSTRAINT": HAS_CONSTRAINT,
        "HAS_CONDITION": HAS_CONDITION,
        "APPLIES_IN": APPLIES_IN,
        "OVERRIDDEN_BY": OVERRIDDEN_BY,
        "SOURCED_FROM": SOURCED_FROM,
    }
    
    print(f"\nEntity Types ({len(entity_types)}):")
    for name in entity_types:
        print(f"  - {name}")
    
    print(f"\nEdge Types ({len(edge_types)}):")
    for name in edge_types:
        print(f"  - {name}")
    
    # Set ontology project-wide
    print("\nSetting ontology project-wide...")
    
    try:
        client.graph.set_ontology(
            entities=entity_types,
            edges=edge_types
        )
        print("✅ Ontology set successfully!")
    except Exception as e:
        print(f"❌ Error setting ontology: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("""
1. Create a user with default ontology disabled:
   
   client.user.add(
       user_id="austin-zoning",
       disable_default_ontology=True
   )

2. Add episodes/messages to build the graph:
   
   client.thread.add_messages(
       thread_id=thread_id,
       messages=[Message(
           role="user",
           content="Zone SF-5 (Urban Family Residence) allows Townhouses..."
       )]
   )

3. View graph in Zep Playground:
   https://app.getzep.com/
""")
    
    return True


def create_zoning_user():
    """Create a user for the zoning knowledge graph with custom ontology only."""
    
    client = Zep(api_key=ZEP_API_KEY)
    
    user_id = "austin-zoning-kg"
    
    try:
        # Create user with default ontology disabled
        user = client.user.add(
            user_id=user_id,
            first_name="Austin",
            last_name="Zoning KG",
            email="zoning@organism.ai",
            disable_default_ontology=True  # Only use our custom types
        )
        print(f"✅ Created user: {user_id}")
        print("   Default ontology disabled - only custom types will be used")
        return user_id
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"User {user_id} already exists, updating...")
            client.user.update(
                user_id=user_id,
                disable_default_ontology=True
            )
            return user_id
        else:
            print(f"❌ Error creating user: {e}")
            return None


if __name__ == "__main__":
    # Set up ontology
    success = setup_zep_ontology()
    
    if success:
        print("\n" + "-" * 60)
        print("Creating zoning user...")
        print("-" * 60)
        create_zoning_user()

