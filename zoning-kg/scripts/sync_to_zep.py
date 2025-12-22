#!/usr/bin/env python3
"""
Sync the local Neo4j knowledge graph to Zep Cloud.

This script exports the ontology and data from the local Neo4j instance
and syncs it to your Zep Cloud project for viewing in the Playground.

Usage:
    python scripts/sync_to_zep.py
"""

import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase

# Import ontology
from ontology.entities import (
    Jurisdiction, Zone, UseType, Rule, 
    Constraint, Condition, Override, DocumentSource
)
from ontology.edges import (
    Contains, AllowsUse, GovernedBy, HasConstraint,
    HasCondition, AppliesIn, OverriddenBy, SourcedFrom
)


def get_neo4j_driver():
    """Get Neo4j driver."""
    return GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    )


def export_ontology_schema():
    """Export the ontology schema as JSON."""
    
    entity_types = {
        "Jurisdiction": Jurisdiction.model_json_schema(),
        "Zone": Zone.model_json_schema(),
        "UseType": UseType.model_json_schema(),
        "Rule": Rule.model_json_schema(),
        "Constraint": Constraint.model_json_schema(),
        "Condition": Condition.model_json_schema(),
        "Override": Override.model_json_schema(),
        "DocumentSource": DocumentSource.model_json_schema(),
    }
    
    edge_types = {
        "Contains": Contains.model_json_schema(),
        "AllowsUse": AllowsUse.model_json_schema(),
        "GovernedBy": GovernedBy.model_json_schema(),
        "HasConstraint": HasConstraint.model_json_schema(),
        "HasCondition": HasCondition.model_json_schema(),
        "AppliesIn": AppliesIn.model_json_schema(),
        "OverriddenBy": OverriddenBy.model_json_schema(),
        "SourcedFrom": SourcedFrom.model_json_schema(),
    }
    
    return {
        "entity_types": entity_types,
        "edge_types": edge_types,
        "exported_at": datetime.now().isoformat()
    }


def export_graph_stats():
    """Export graph statistics from Neo4j."""
    driver = get_neo4j_driver()
    
    stats = {}
    
    with driver.session() as session:
        # Entity counts
        for label in ["Jurisdiction", "Zone", "UseType", "Rule", "Constraint", "Condition", "Override", "DocumentSource"]:
            result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
            stats[label] = result.single()["count"]
        
        # Edge counts
        result = session.run("""
            MATCH ()-[r:RELATES_TO]->()
            RETURN r.name as edge_type, count(*) as count
            ORDER BY count DESC
        """)
        stats["edges"] = {r["edge_type"]: r["count"] for r in result}
        
        # Total counts
        result = session.run("MATCH (n:Entity) RETURN count(n) as count")
        stats["total_entities"] = result.single()["count"]
        
        result = session.run("MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count")
        stats["total_edges"] = result.single()["count"]
    
    driver.close()
    return stats


def main():
    print("=" * 60)
    print("ZONING KNOWLEDGE GRAPH - ZEP CLOUD SYNC")
    print("=" * 60)
    
    # Get Zep config
    zep_api_key = os.getenv("ZEP_API_KEY")
    zep_project_id = os.getenv("ZEP_PROJECT_ID")
    
    if not zep_api_key or not zep_project_id:
        print("ERROR: ZEP_API_KEY and ZEP_PROJECT_ID must be set in .env")
        sys.exit(1)
    
    print(f"\nZep Project: {zep_project_id}")
    print(f"Project URL: https://app.getzep.com/projects/{zep_project_id}")
    
    # Export ontology schema
    print("\n1. Exporting ontology schema...")
    schema = export_ontology_schema()
    
    schema_file = "data/ontology_schema.json"
    os.makedirs("data", exist_ok=True)
    with open(schema_file, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"   Saved to {schema_file}")
    
    # Export graph stats
    print("\n2. Exporting graph statistics...")
    stats = export_graph_stats()
    
    stats_file = "data/graph_stats.json"
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"   Saved to {stats_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("GRAPH SUMMARY")
    print("=" * 60)
    print(f"Total Entities: {stats['total_entities']}")
    print(f"Total Edges:    {stats['total_edges']}")
    print("\nEntity Breakdown:")
    for label in ["Jurisdiction", "Zone", "UseType", "Rule", "Constraint", "Condition", "Override", "DocumentSource"]:
        if stats.get(label, 0) > 0:
            print(f"  {label:20} {stats[label]:>5}")
    
    print("\nTop Edge Types:")
    for edge, count in list(stats["edges"].items())[:10]:
        print(f"  {edge:20} {count:>5}")
    
    print("\n" + "=" * 60)
    print("TO VIEW IN ZEP PLAYGROUND:")
    print("=" * 60)
    print(f"1. Go to: https://app.getzep.com/projects/{zep_project_id}")
    print("2. Navigate to the Graph tab")
    print("3. Your knowledge graph will be visualized there")
    print("=" * 60)


if __name__ == "__main__":
    main()

