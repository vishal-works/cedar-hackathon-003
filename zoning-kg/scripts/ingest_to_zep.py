#!/usr/bin/env python3
"""
Ingest tagged episodes to Zep Cloud knowledge graph.

This script loads the tagged sections from the preprocessing stage
and ingests them into Zep Cloud using our custom ontology.

Usage:
    python scripts/ingest_to_zep.py [--limit N]
"""

import os
import sys
import json
import argparse
import uuid
from pathlib import Path
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

from zep_cloud.client import Zep
from zep_cloud.types import Message

# Configuration
ZEP_API_KEY = os.getenv("ZEP_API_KEY")
TAGGED_DIR = Path("data/tagged")
USER_ID = "austin-zoning-kg"


def load_tagged_sections(limit: int = None):
    """Load tagged section files."""
    sections = []
    
    tagged_files = sorted(TAGGED_DIR.glob("*.json"))
    if limit:
        tagged_files = tagged_files[:limit]
    
    for f in tagged_files:
        with open(f) as fp:
            data = json.load(fp)
            sections.append(data)
    
    return sections


def format_section_for_zep(section: dict) -> str:
    """
    Format a tagged section as content for Zep ingestion.
    
    We enrich the content with explicit entity mentions to help
    Zep's extraction align with our ontology.
    """
    content_parts = []
    
    # Add section metadata
    section_id = section.get("section_id", "unknown")
    title = section.get("title", "")
    
    content_parts.append(f"Document Section: {section_id}")
    if title:
        content_parts.append(f"Title: {title}")
    
    # Add jurisdiction context
    content_parts.append("Jurisdiction: City of Austin, Texas (austin_tx)")
    
    # Add the main content
    text = section.get("text", "")
    if text:
        content_parts.append(f"\nContent:\n{text}")
    
    # Add entity annotations from NER
    entities = section.get("entities", [])
    if entities:
        content_parts.append("\nExtracted Entities:")
        for ent in entities:
            label = ent.get("label", "")
            text_val = ent.get("text", "")
            
            # Map NER labels to our ontology types
            type_map = {
                "ZONE": "Zone",
                "USE_TYPE": "UseType", 
                "MEASUREMENT": "Constraint",
                "SECTION_REF": "DocumentSource",
                "ORG": "Jurisdiction",
            }
            
            onto_type = type_map.get(label, label)
            content_parts.append(f"  - [{onto_type}] {text_val}")
    
    return "\n".join(content_parts)


def ingest_to_zep(sections: list, batch_size: int = 10):
    """Ingest sections to Zep Cloud."""
    
    client = Zep(api_key=ZEP_API_KEY)
    
    # Create a thread for ingestion
    thread_id = f"zoning-ingest-{uuid.uuid4().hex[:8]}"
    
    try:
        client.thread.create(
            thread_id=thread_id,
            user_id=USER_ID
        )
        print(f"Created thread: {thread_id}")
    except Exception as e:
        print(f"Thread creation note: {e}")
    
    # Ingest in batches
    success_count = 0
    error_count = 0
    
    for i, section in enumerate(tqdm(sections, desc="Ingesting")):
        content = format_section_for_zep(section)
        
        try:
            # Add as a message to the thread
            client.thread.add_messages(
                thread_id=thread_id,
                messages=[
                    Message(
                        role="user",
                        name="ZoningCodeLoader",
                        content=content
                    )
                ],
                ignore_roles=["assistant"]  # We're not adding assistant responses
            )
            success_count += 1
            
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # Only show first 5 errors
                print(f"\nError on section {i}: {e}")
    
    return success_count, error_count, thread_id


def main():
    parser = argparse.ArgumentParser(description="Ingest tagged sections to Zep Cloud")
    parser.add_argument("--limit", type=int, help="Limit number of sections to ingest")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for ingestion")
    args = parser.parse_args()
    
    print("=" * 60)
    print("ZEP CLOUD INGESTION")
    print("=" * 60)
    
    if not ZEP_API_KEY:
        print("ERROR: ZEP_API_KEY not found in .env")
        sys.exit(1)
    
    # Check for tagged sections
    if not TAGGED_DIR.exists():
        print(f"ERROR: Tagged directory not found: {TAGGED_DIR}")
        sys.exit(1)
    
    # Load sections
    print("\n1. Loading tagged sections...")
    sections = load_tagged_sections(args.limit)
    print(f"   Loaded {len(sections)} sections")
    
    # Ingest to Zep
    print("\n2. Ingesting to Zep Cloud...")
    success, errors, thread_id = ingest_to_zep(sections, args.batch_size)
    
    # Summary
    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)
    print(f"Successful: {success}")
    print(f"Errors:     {errors}")
    print(f"Thread ID:  {thread_id}")
    print(f"\nView in Zep Playground:")
    print(f"https://app.getzep.com/")
    print("=" * 60)


if __name__ == "__main__":
    main()

