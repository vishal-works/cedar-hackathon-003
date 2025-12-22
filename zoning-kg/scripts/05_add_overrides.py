#!/usr/bin/env python3
"""
Add Texas state bill overrides to the knowledge graph.

This adds the override layer that supersedes local regulations.

Usage:
    python scripts/05_add_overrides.py [--verbose] [--list]
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphiti.client import check_neo4j_connection
from src.graph.override_layer import (
    add_override_layer, 
    SB_840_OVERRIDES, 
    SB_2835_CONDITIONS,
    get_overrides_for_metric
)


def list_overrides():
    """List all defined overrides."""
    print("=" * 60)
    print("SB-840 OVERRIDES (Housing in Commercial Zones)")
    print("=" * 60)
    
    for override in SB_840_OVERRIDES:
        print(f"\n{override['id']}")
        print(f"  Metric: {override['metric']}")
        print(f"  Type: {override['override_type']} ({override['value']} {override['unit']})")
        print(f"  Uses: {', '.join(override['scope_uses'])}")
        print(f"  Zones: {', '.join(override['scope_zones'])}")
        print(f"  Effective: {override['effective_date']}")
    
    print("\n" + "=" * 60)
    print("SB-2835 CONDITIONS (Transit-Oriented Development)")
    print("=" * 60)
    
    for condition in SB_2835_CONDITIONS:
        print(f"\n{condition['id']}")
        print(f"  Metric: {condition['metric']}")
        print(f"  Type: {condition['override_type']} ({condition['value']} {condition['unit']})")
        print(f"  Condition: {condition.get('condition', 'N/A')}")
        print(f"  Effective: {condition['effective_date']}")
    
    print("\n" + "=" * 60)
    total = len(SB_840_OVERRIDES) + len(SB_2835_CONDITIONS)
    print(f"Total overrides: {total}")


async def main():
    parser = argparse.ArgumentParser(description="Add Texas state bill overrides")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--list", "-l", action="store_true", help="List overrides and exit")
    parser.add_argument("--metric", "-m", help="Show overrides for specific metric")
    
    args = parser.parse_args()
    
    # List mode
    if args.list:
        list_overrides()
        return
    
    # Query specific metric
    if args.metric:
        overrides = get_overrides_for_metric(args.metric)
        if not overrides:
            print(f"No overrides found for metric: {args.metric}")
        else:
            print(f"Overrides for metric '{args.metric}':")
            for o in overrides:
                print(f"  {o['id']}: {o['override_type']} {o['value']} {o['unit']}")
        return
    
    # Check Neo4j connection
    print("Checking Neo4j connection...")
    if not check_neo4j_connection():
        print("Error: Cannot connect to Neo4j. Please ensure:")
        print("  1. Neo4j is running (docker-compose up -d)")
        print("  2. Environment variables are set")
        sys.exit(1)
    print("  Neo4j connection OK\n")
    
    # Add overrides
    print("Adding Texas state bill overrides...")
    print(f"  SB-840 overrides: {len(SB_840_OVERRIDES)}")
    print(f"  SB-2835 conditions: {len(SB_2835_CONDITIONS)}")
    print()
    
    try:
        await add_override_layer(verbose=args.verbose)
    except Exception as e:
        print(f"\nError adding overrides: {e}")
        sys.exit(1)
    
    print("\n✅ Override layer added successfully!")
    print("\nTo verify in Neo4j Browser (http://localhost:7474):")
    print("  MATCH (o:Override) RETURN o.id, o.override_type, o.value, o.metric")


if __name__ == "__main__":
    asyncio.run(main())

