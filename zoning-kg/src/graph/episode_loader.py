"""
Load tagged sections from preprocessing and convert to Graphiti episodes.
"""

import json
from pathlib import Path
from typing import List, Dict, Iterator, Optional
from dataclasses import dataclass


@dataclass
class TaggedEpisode:
    """A preprocessed section ready for Graphiti ingestion."""
    section_id: str
    title: str
    content: str
    entities: List[Dict]
    source_file: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None


def load_tagged_sections(
    tagged_dir: str = "data/processed/tagged"
) -> Iterator[TaggedEpisode]:
    """
    Load all tagged section files and yield TaggedEpisode objects.
    
    Yields:
        TaggedEpisode objects ready for Graphiti ingestion
    """
    tagged_path = Path(tagged_dir)
    
    if not tagged_path.exists():
        raise FileNotFoundError(f"Tagged sections directory not found: {tagged_dir}")
    
    for json_file in sorted(tagged_path.glob("*.json")):
        if json_file.name in ("summary.json", "index.json"):
            continue
            
        with open(json_file) as f:
            data = json.load(f)
        
        yield TaggedEpisode(
            section_id=data.get("section_id", json_file.stem),
            title=data.get("title", data.get("section_id", json_file.stem)),
            content=data.get("content", ""),
            entities=data.get("entities", []),
            source_file=str(json_file),
            start_line=data.get("start_line"),
            end_line=data.get("end_line")
        )


def enrich_content_with_entities(episode: TaggedEpisode) -> str:
    """
    Enrich episode content with explicit entity annotations.
    
    This helps Graphiti's LLM better identify and extract entities.
    """
    # Build entity summary
    entity_summary = []
    
    zones = [e for e in episode.entities if e.get("label") == "ZONE"]
    if zones:
        zone_codes = list(set(
            e.get("normalized", {}).get("code", e.get("text", "")) 
            if isinstance(e.get("normalized"), dict) else e.get("text", "")
            for e in zones
        ))
        zone_codes = [z for z in zone_codes if z]
        if zone_codes:
            entity_summary.append(f"Zones mentioned: {', '.join(zone_codes)}")
    
    uses = [e for e in episode.entities if e.get("label") == "USE_TYPE"]
    if uses:
        use_types = list(set(e.get("text", "").lower() for e in uses))
        use_types = [u for u in use_types if u]
        if use_types:
            entity_summary.append(f"Use types mentioned: {', '.join(use_types)}")
    
    metrics = [e for e in episode.entities if e.get("label") == "METRIC"]
    if metrics:
        metric_names = list(set(
            e.get("normalized", "") if isinstance(e.get("normalized"), str) 
            else e.get("text", "")
            for e in metrics
        ))
        metric_names = [m for m in metric_names if m]
        if metric_names:
            entity_summary.append(f"Metrics: {', '.join(metric_names)}")
    
    measurements = [e for e in episode.entities if e.get("label") == "MEASUREMENT"]
    if measurements:
        values = []
        for e in measurements[:5]:
            norm = e.get("normalized", {})
            if isinstance(norm, dict) and "value" in norm and "unit" in norm:
                values.append(f"{norm['value']} {norm['unit']}")
        if values:
            entity_summary.append(f"Values: {', '.join(values)}")
    
    operators = [e for e in episode.entities if e.get("label") == "OPERATOR"]
    if operators:
        ops = list(set(e.get("text", "").lower() for e in operators))
        ops = [o for o in ops if o]
        if ops:
            entity_summary.append(f"Constraints: {', '.join(ops[:5])}")
    
    section_refs = [e for e in episode.entities if e.get("label") == "SECTION_REF"]
    if section_refs:
        refs = list(set(e.get("text", "") for e in section_refs))[:5]
        refs = [r for r in refs if r]
        if refs:
            entity_summary.append(f"References: {', '.join(refs)}")
    
    # Prepend entity summary to content
    enriched = f"[SECTION ID: {episode.section_id}]\n"
    enriched += f"[TITLE: {episode.title}]\n"
    
    if entity_summary:
        enriched += "\n[EXTRACTED ENTITIES]\n" + "\n".join(entity_summary) + "\n"
    
    enriched += f"\n[SECTION CONTENT]\n{episode.content}"
    
    return enriched


def get_episode_count(tagged_dir: str = "data/processed/tagged") -> int:
    """Return the total number of tagged episodes."""
    tagged_path = Path(tagged_dir)
    
    if not tagged_path.exists():
        return 0
    
    count = 0
    for json_file in tagged_path.glob("*.json"):
        if json_file.name not in ("summary.json", "index.json"):
            count += 1
    
    return count


def load_sections_index(sections_dir: str = "data/processed/sections") -> Dict:
    """Load the sections index for metadata lookup."""
    index_path = Path(sections_dir) / "index.json"
    
    if not index_path.exists():
        return {"sections": []}
    
    with open(index_path) as f:
        return json.load(f)


def get_section_metadata(section_id: str, sections_dir: str = "data/processed/sections") -> Optional[Dict]:
    """Get metadata for a specific section from the index."""
    index = load_sections_index(sections_dir)
    
    for section in index.get("sections", []):
        if section.get("id") == section_id:
            return section
    
    return None


def filter_episodes_by_entity_type(
    tagged_dir: str = "data/processed/tagged",
    entity_type: str = "ZONE"
) -> Iterator[TaggedEpisode]:
    """
    Filter episodes to only those containing a specific entity type.
    
    Args:
        tagged_dir: Path to tagged sections
        entity_type: Entity label to filter by (ZONE, USE_TYPE, etc.)
        
    Yields:
        TaggedEpisode objects containing the specified entity type
    """
    for episode in load_tagged_sections(tagged_dir):
        if any(e.get("label") == entity_type for e in episode.entities):
            yield episode


def get_episodes_summary(tagged_dir: str = "data/processed/tagged") -> Dict:
    """
    Get summary statistics for all tagged episodes.
    
    Returns:
        Dict with counts and distributions
    """
    summary_path = Path(tagged_dir) / "summary.json"
    
    if summary_path.exists():
        with open(summary_path) as f:
            return json.load(f)
    
    # Calculate if summary doesn't exist
    total_entities = 0
    entities_by_label = {}
    
    for episode in load_tagged_sections(tagged_dir):
        total_entities += len(episode.entities)
        for entity in episode.entities:
            label = entity.get("label", "UNKNOWN")
            entities_by_label[label] = entities_by_label.get(label, 0) + 1
    
    return {
        "total_sections": get_episode_count(tagged_dir),
        "total_entities": total_entities,
        "entities_by_label": entities_by_label
    }

