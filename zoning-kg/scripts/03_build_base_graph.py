#!/usr/bin/env python3
"""
Build the base knowledge graph with jurisdictions, zones, and use types.

This creates the foundational structure before episode ingestion.

Usage:
    python scripts/03_build_base_graph.py [--verbose]
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphiti.client import check_neo4j_connection
from src.graph.base_graph import build_base_graph, verify_base_graph, AUSTIN_ZONES, USE_TYPES


async def main():
    parser = argparse.ArgumentParser(description="Build base knowledge graph")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--verify-only", action="store_true", help="Only verify existing graph")
    
    args = parser.parse_args()
    
    # Check Neo4j connection
    print("Checking Neo4j connection...")
    if not check_neo4j_connection():
        print("Error: Cannot connect to Neo4j. Please ensure:")
        print("  1. Neo4j is running (docker-compose up -d)")
        print("  2. Environment variables are set (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)")
        sys.exit(1)
    print("  Neo4j connection OK\n")
    
    if args.verify_only:
        print("Verifying existing graph...")
        try:
            counts = await verify_base_graph()
            print("\nGraph node counts:")
            for label, count in counts.items():
                print(f"  {label}: {count}")
        except Exception as e:
            print(f"Error verifying graph: {e}")
            sys.exit(1)
        return
    
    # Build base graph
    print("Building base knowledge graph...")
    print(f"  Zones to create: {len(AUSTIN_ZONES)}")
    print(f"  Use types to create: {len(USE_TYPES)}")
    print()
    
    try:
        await build_base_graph(verbose=args.verbose)
    except Exception as e:
        print(f"\nError building graph: {e}")
        sys.exit(1)
    
    # Verify
    print("\nVerifying graph...")
    try:
        counts = await verify_base_graph()
        print("\nGraph node counts:")
        for label, count in counts.items():
            print(f"  {label}: {count}")
    except Exception as e:
        print(f"Verification error: {e}")
    
    print("\n✅ Base graph build complete!")


if __name__ == "__main__":
    asyncio.run(main())

