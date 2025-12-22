#!/usr/bin/env python3
"""
Ingest ALL content to Zep Cloud with custom ontology.

This script:
1. Ensures custom ontology is set
2. Disables default ontology for the user
3. Ingests ALL tagged LDC sections
4. Ingests ALL state bill overrides
5. Tracks progress and ensures nothing is missed

Usage:
    python scripts/ingest_all_to_zep.py
"""

import os
import sys
import json
import uuid
import time
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

from zep_cloud.client import Zep
from zep_cloud.types import Message

# Configuration
ZEP_API_KEY = os.getenv("ZEP_API_KEY")
TAGGED_DIR = Path("data/processed/tagged")
STATE_BILLS_DIR = Path("data/state_bills")
USER_ID = "austin-zoning-kg"

if not ZEP_API_KEY:
    print("ERROR: ZEP_API_KEY not found in .env")
    sys.exit(1)

client = Zep(api_key=ZEP_API_KEY)


def ensure_user_exists():
    """Ensure user exists with default ontology disabled."""
    try:
        user = client.user.get(user_id=USER_ID)
        print(f"✓ User exists: {USER_ID}")
        # Update to ensure default ontology is disabled
        client.user.update(user_id=USER_ID, disable_default_ontology=True)
        print("✓ Default ontology disabled")
    except Exception as e:
        if "not found" in str(e).lower():
            client.user.add(
                user_id=USER_ID,
                first_name="Austin",
                last_name="Zoning KG",
                disable_default_ontology=True
            )
            print(f"✓ Created user: {USER_ID}")
        else:
            print(f"User check error: {e}")


def format_ldc_section(section: dict) -> str:
    """
    Format an LDC section for Zep ingestion.
    
    We structure the content to help Zep extract entities according to our ontology:
    - Jurisdiction, Zone, UseType, Rule, Constraint, Condition, Override, DocumentSource
    - CONTAINS, ALLOWS_USE, GOVERNED_BY, HAS_CONSTRAINT, HAS_CONDITION, APPLIES_IN, OVERRIDDEN_BY, SOURCED_FROM
    """
    parts = []
    
    section_id = section.get("section_id", "unknown")
    title = section.get("title", "")
    text = section.get("text", "")
    entities = section.get("entities", [])
    
    # Header with jurisdiction context
    parts.append("=== AUSTIN LAND DEVELOPMENT CODE SECTION ===")
    parts.append(f"Jurisdiction: City of Austin, Texas (jurisdiction_id: austin_tx, state: TX, level: city)")
    parts.append(f"Document: Land Development Code")
    parts.append(f"Section: {section_id}")
    if title:
        parts.append(f"Title: {title}")
    parts.append("")
    
    # Main content
    parts.append("CONTENT:")
    parts.append(text)
    parts.append("")
    
    # Extracted entities with type hints for Zep
    if entities:
        parts.append("EXTRACTED ENTITIES:")
        for ent in entities:
            label = ent.get("label", "")
            ent_text = ent.get("text", "")
            
            # Map to our ontology types
            if label == "ZONE":
                parts.append(f"  [Zone] {ent_text} (zone_code: {ent_text}, jurisdiction_id: austin_tx)")
            elif label == "USE_TYPE":
                parts.append(f"  [UseType] {ent_text} (use_group: residential)")
            elif label == "MEASUREMENT":
                parts.append(f"  [Constraint] {ent_text} (metric: dimensional, value: extracted from text)")
            elif label == "SECTION_REF":
                parts.append(f"  [DocumentSource] {ent_text} (document: Land Development Code, section: {ent_text})")
            else:
                parts.append(f"  [{label}] {ent_text}")
    
    # Add rule context
    parts.append("")
    parts.append(f"This section defines a Rule with section: {section_id}, document: Land Development Code, jurisdiction_id: austin_tx")
    parts.append(f"The Rule is SOURCED_FROM DocumentSource with document: Land Development Code, section: {section_id}")
    parts.append(f"The Rule APPLIES_IN zones within jurisdiction austin_tx")
    
    return "\n".join(parts)


def format_state_bill(bill_data: dict, bill_file: str) -> str:
    """Format a state bill override for Zep ingestion."""
    parts = []
    
    bill_id = bill_data.get("bill_id", bill_file.replace(".json", "").upper())
    
    parts.append("=== TEXAS STATE BILL OVERRIDE ===")
    parts.append(f"Jurisdiction: State of Texas (jurisdiction_id: texas, state: TX, level: state)")
    parts.append(f"Bill: {bill_id}")
    parts.append("")
    
    # Process overrides
    overrides = bill_data.get("overrides", [])
    for override in overrides:
        metric = override.get("metric", "")
        override_type = override.get("override_type", "")
        value = override.get("value", "")
        unit = override.get("unit", "")
        effective_date = override.get("effective_date", "")
        
        parts.append(f"[Override] {bill_id}:{metric}")
        parts.append(f"  bill_id: {bill_id}")
        parts.append(f"  override_type: {override_type}")
        parts.append(f"  metric: {metric}")
        parts.append(f"  value: {value} {unit}")
        parts.append(f"  effective_date: {effective_date}")
        parts.append("")
        
        # Add relationship context
        parts.append(f"This Override OVERRIDDEN_BY relationship affects local Constraints")
        parts.append(f"Resolution: {'max' if override_type == 'floor' else 'min'}")
        parts.append("")
    
    # Process conditions
    conditions = bill_data.get("conditions", [])
    for condition in conditions:
        field = condition.get("field", "")
        operator = condition.get("operator", "")
        value = condition.get("value", "")
        
        parts.append(f"[Condition] {field} {operator} {value}")
        parts.append(f"  field: {field}")
        parts.append(f"  operator: {operator}")
        parts.append(f"  condition_value: {value}")
        parts.append("")
    
    return "\n".join(parts)


def load_all_content():
    """Load all LDC sections and state bills."""
    content = []
    
    # Load tagged LDC sections
    print("Loading LDC sections...")
    tagged_files = sorted(TAGGED_DIR.glob("*.json"))
    for f in tagged_files:
        with open(f) as fp:
            data = json.load(fp)
            content.append({
                "type": "ldc_section",
                "file": f.name,
                "data": data,
                "formatted": format_ldc_section(data)
            })
    print(f"  Loaded {len(tagged_files)} LDC sections")
    
    # Load state bills
    print("Loading state bills...")
    if STATE_BILLS_DIR.exists():
        bill_files = list(STATE_BILLS_DIR.glob("*.json"))
        for f in bill_files:
            with open(f) as fp:
                data = json.load(fp)
                content.append({
                    "type": "state_bill",
                    "file": f.name,
                    "data": data,
                    "formatted": format_state_bill(data, f.name)
                })
        print(f"  Loaded {len(bill_files)} state bills")
    else:
        print("  No state bills directory found")
    
    return content


def chunk_content(content: str, max_size: int = 9000) -> list:
    """Split content into chunks of max_size characters."""
    if len(content) <= max_size:
        return [content]
    
    chunks = []
    lines = content.split('\n')
    current_chunk = []
    current_size = 0
    
    for line in lines:
        line_size = len(line) + 1  # +1 for newline
        if current_size + line_size > max_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks


def ingest_with_retry(func, max_retries=3):
    """Execute function with retry on rate limit."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                wait_time = 15 * (attempt + 1)  # 15, 30, 45 seconds
                print(f"    Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded")


def ingest_to_zep(content: list):
    """Ingest all content to Zep Cloud with rate limiting."""
    
    # Wait for rate limit to reset from previous runs
    print("Waiting 60s for rate limit reset...")
    time.sleep(60)
    
    # Create a dedicated thread for this ingestion
    thread_id = f"zoning-full-ingest-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    try:
        client.thread.create(thread_id=thread_id, user_id=USER_ID)
        print(f"✓ Created thread: {thread_id}")
    except Exception as e:
        print(f"Thread creation: {e}")
    
    success = 0
    errors = 0
    error_files = []
    chunks_sent = 0
    
    # FREE plan: 5 requests/minute = 1 request per 12 seconds (use 15s to be safe)
    REQUEST_DELAY = 15  # seconds between requests
    
    print(f"\nIngesting {len(content)} items (rate limited to ~4 req/min)...")
    print(f"Estimated time: ~{len(content) * REQUEST_DELAY / 60:.0f} minutes")
    print("-" * 60)
    
    for i, item in enumerate(content):
        formatted_content = item["formatted"]
        
        try:
            # Chunk large content
            chunks = chunk_content(formatted_content, max_size=9000)
            
            for chunk_idx, chunk in enumerate(chunks):
                # Add header for continuation chunks
                if chunk_idx > 0:
                    chunk = f"=== CONTINUATION (Part {chunk_idx + 1}) - {item['file']} ===\n\n{chunk}"
                
                # Use graph.add for all content (more reliable)
                def send_chunk():
                    client.graph.add(
                        user_id=USER_ID,
                        type="text",
                        data=chunk,
                        source_description=f"LDC Section: {item['file']}" + (f" (Part {chunk_idx + 1})" if chunk_idx > 0 else "")
                    )
                
                ingest_with_retry(send_chunk)
                chunks_sent += 1
                
                # Rate limiting delay
                time.sleep(REQUEST_DELAY)
            
            success += 1
            
            # Progress update
            if (i + 1) % 10 == 0 or (i + 1) == len(content):
                pct = (i + 1) / len(content) * 100
                elapsed = (i + 1) * REQUEST_DELAY / 60
                remaining = (len(content) - i - 1) * REQUEST_DELAY / 60
                print(f"  [{i+1}/{len(content)}] {pct:.1f}% | Success: {success} | Errors: {errors} | ~{remaining:.0f}min left")
                
        except Exception as e:
            errors += 1
            error_files.append(item["file"])
            if errors <= 5:
                print(f"  Error on {item['file']}: {e}")
            time.sleep(REQUEST_DELAY)  # Still wait to respect rate limit
    
    return success, errors, error_files, thread_id


def main():
    print("=" * 65)
    print("   ZEP CLOUD FULL INGESTION - AUSTIN ZONING KNOWLEDGE GRAPH")
    print("=" * 65)
    print()
    
    # Step 1: Ensure user exists
    print("1. Checking user setup...")
    ensure_user_exists()
    print()
    
    # Step 2: Load all content
    print("2. Loading all content...")
    content = load_all_content()
    print(f"   Total items to ingest: {len(content)}")
    print()
    
    # Step 3: Ingest to Zep
    print("3. Ingesting to Zep Cloud...")
    start_time = time.time()
    success, errors, error_files, thread_id = ingest_to_zep(content)
    elapsed = time.time() - start_time
    
    # Summary
    print()
    print("=" * 65)
    print("   INGESTION COMPLETE")
    print("=" * 65)
    print(f"Total Items:    {len(content)}")
    print(f"Successful:     {success}")
    print(f"Errors:         {errors}")
    print(f"Time Elapsed:   {elapsed:.1f} seconds")
    print(f"Thread ID:      {thread_id}")
    print()
    
    if error_files:
        print("Failed files:")
        for f in error_files[:10]:
            print(f"  - {f}")
        if len(error_files) > 10:
            print(f"  ... and {len(error_files) - 10} more")
    
    print()
    print("=" * 65)
    print("   VIEW YOUR GRAPH")
    print("=" * 65)
    print("Zep Playground: https://app.getzep.com/")
    print("User ID:        austin-zoning-kg")
    print("Thread ID:      " + thread_id)
    print()
    print("The graph may take a few minutes to fully process.")
    print("Refresh the playground to see new entities appear.")
    print("=" * 65)


if __name__ == "__main__":
    main()

