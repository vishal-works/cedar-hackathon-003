#!/usr/bin/env python3
"""
Ingest tagged episodes into the Graphiti knowledge graph.

Usage:
    python scripts/04_ingest_episodes.py [--limit N] [--verbose] [--section SECTION_ID]
"""

import argparse
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphiti.client import get_graphiti_client, check_neo4j_connection
from src.graphiti.type_config import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP
from src.graph.episode_loader import (
    load_tagged_sections, 
    enrich_content_with_entities,
    get_episode_count,
    get_episodes_summary
)


async def ingest_single_section(section_id: str, tagged_dir: str, verbose: bool = False):
    """Ingest a single section for testing."""
    client = get_graphiti_client()
    
    # Find the section
    found = None
    for episode in load_tagged_sections(tagged_dir):
        if episode.section_id == section_id:
            found = episode
            break
    
    if not found:
        print(f"Error: Section '{section_id}' not found in {tagged_dir}")
        return
    
    print(f"Processing section: {found.section_id}")
    print(f"  Title: {found.title}")
    print(f"  Entities: {len(found.entities)}")
    
    if verbose:
        print("\n  Entity breakdown:")
        entity_counts = {}
        for e in found.entities:
            label = e.get("label", "UNKNOWN")
            entity_counts[label] = entity_counts.get(label, 0) + 1
        for label, count in sorted(entity_counts.items()):
            print(f"    {label}: {count}")
    
    # Enrich content
    enriched_content = enrich_content_with_entities(found)
    
    if verbose:
        print("\n  Enriched content preview:")
        preview = enriched_content[:500]
        print(f"    {preview}...")
    
    # Ingest
    print("\n  Ingesting into Graphiti...")
    try:
        result = await client.add_episode(
            name=f"LDC: {found.section_id} - {found.title}",
            episode_body=enriched_content,
            source_description="Austin Land Development Code",
            reference_time=datetime.now(),
            entity_types=ENTITY_TYPES,
            edge_types=EDGE_TYPES,
            edge_type_map=EDGE_TYPE_MAP
        )
        
        print(f"  ✅ Ingested successfully")
        if hasattr(result, 'nodes'):
            print(f"     Nodes created: {len(result.nodes)}")
        if hasattr(result, 'edges'):
            print(f"     Edges created: {len(result.edges)}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")


async def ingest_all_episodes(tagged_dir: str, limit: int = None, verbose: bool = False):
    """Ingest all tagged episodes."""
    client = get_graphiti_client()
    
    total = get_episode_count(tagged_dir)
    if limit:
        total = min(total, limit)
    
    print(f"Ingesting {total} episodes into knowledge graph...")
    
    # Get summary for progress reporting
    summary = get_episodes_summary(tagged_dir)
    print(f"  Total entities to process: {summary.get('total_entities', 'unknown')}")
    print()
    
    success_count = 0
    error_count = 0
    total_nodes = 0
    total_edges = 0
    
    for i, episode in enumerate(load_tagged_sections(tagged_dir)):
        if limit and i >= limit:
            break
        
        # Enrich content
        enriched_content = enrich_content_with_entities(episode)
        
        try:
            result = await client.add_episode(
                name=f"LDC: {episode.section_id}",
                episode_body=enriched_content,
                source_description="Austin Land Development Code",
                reference_time=datetime.now(),
                entity_types=ENTITY_TYPES,
                edge_types=EDGE_TYPES,
                edge_type_map=EDGE_TYPE_MAP
            )
            
            success_count += 1
            if hasattr(result, 'nodes'):
                total_nodes += len(result.nodes)
            if hasattr(result, 'edges'):
                total_edges += len(result.edges)
            
            if verbose:
                nodes = len(result.nodes) if hasattr(result, 'nodes') else 0
                edges = len(result.edges) if hasattr(result, 'edges') else 0
                print(f"  [{i+1}/{total}] {episode.section_id}: {nodes} nodes, {edges} edges")
            else:
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"  Progress: {i+1}/{total} episodes ({100*(i+1)//total}%)")
                    
        except Exception as e:
            error_count += 1
            if verbose:
                print(f"  [{i+1}/{total}] {episode.section_id}: ERROR - {e}")
            else:
                print(f"  Error on {episode.section_id}: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print("Ingestion Complete!")
    print(f"  Successful: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total nodes created: {total_nodes}")
    print(f"  Total edges created: {total_edges}")


async def main():
    parser = argparse.ArgumentParser(description="Ingest tagged episodes into Graphiti")
    parser.add_argument("--input", "-i", default="data/processed/tagged", 
                        help="Input directory for tagged sections")
    parser.add_argument("--limit", "-l", type=int, help="Max episodes to ingest")
    parser.add_argument("--section", "-s", help="Process single section by ID")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--summary", action="store_true", help="Show summary and exit")
    
    args = parser.parse_args()
    
    # Check tagged directory
    tagged_path = Path(args.input)
    if not tagged_path.exists():
        print(f"Error: Tagged sections directory not found: {args.input}")
        print("Run scripts/02_run_ner.py first to create tagged sections.")
        sys.exit(1)
    
    # Summary only mode
    if args.summary:
        summary = get_episodes_summary(args.input)
        print("Episode Summary:")
        print(f"  Total sections: {summary.get('total_sections', 0)}")
        print(f"  Total entities: {summary.get('total_entities', 0)}")
        print("\n  Entities by label:")
        for label, count in summary.get('entities_by_label', {}).items():
            print(f"    {label}: {count}")
        return
    
    # Check Neo4j connection
    print("Checking Neo4j connection...")
    if not check_neo4j_connection():
        print("Error: Cannot connect to Neo4j. Please ensure:")
        print("  1. Neo4j is running (docker-compose up -d)")
        print("  2. Environment variables are set")
        sys.exit(1)
    print("  Neo4j connection OK\n")
    
    # Single section mode
    if args.section:
        await ingest_single_section(args.section, args.input, args.verbose)
        return
    
    # Full ingestion
    await ingest_all_episodes(args.input, args.limit, args.verbose)
    
    print("\n✅ Episode ingestion complete!")


if __name__ == "__main__":
    asyncio.run(main())

