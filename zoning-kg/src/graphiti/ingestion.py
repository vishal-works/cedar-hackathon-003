"""
Episode ingestion logic for Graphiti.

Handles converting tagged sections to episodes and ingesting them.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from .type_config import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP


@dataclass
class EpisodeResult:
    """Result of an episode ingestion."""
    episode_id: str
    section_id: str
    success: bool
    entities_created: int
    edges_created: int
    error: Optional[str] = None


async def ingest_episode(
    client,
    name: str,
    content: str,
    source_description: str = "Austin Land Development Code",
    reference_time: Optional[datetime] = None
) -> EpisodeResult:
    """
    Ingest a single episode into the knowledge graph.
    
    Args:
        client: Graphiti client instance
        name: Episode name (e.g., "LDC: 25-2-775 TOWNHOUSES")
        content: Episode body text (enriched with entity annotations)
        source_description: Source document name
        reference_time: Timestamp for the episode
        
    Returns:
        EpisodeResult with ingestion status
    """
    if reference_time is None:
        reference_time = datetime.now()
    
    try:
        result = await client.add_episode(
            name=name,
            episode_body=content,
            source_description=source_description,
            reference_time=reference_time,
            entity_types=ENTITY_TYPES,
            edge_types=EDGE_TYPES,
            edge_type_map=EDGE_TYPE_MAP
        )
        
        return EpisodeResult(
            episode_id=str(result.episode_id) if hasattr(result, 'episode_id') else name,
            section_id=name,
            success=True,
            entities_created=len(result.nodes) if hasattr(result, 'nodes') else 0,
            edges_created=len(result.edges) if hasattr(result, 'edges') else 0
        )
        
    except Exception as e:
        return EpisodeResult(
            episode_id="",
            section_id=name,
            success=False,
            entities_created=0,
            edges_created=0,
            error=str(e)
        )


async def ingest_episodes_batch(
    client,
    episodes: List[Dict[str, Any]],
    source_description: str = "Austin Land Development Code",
    on_progress: Optional[callable] = None
) -> List[EpisodeResult]:
    """
    Ingest multiple episodes in batch.
    
    Args:
        client: Graphiti client instance
        episodes: List of dicts with 'name' and 'content' keys
        source_description: Source document name
        on_progress: Optional callback(current, total, result)
        
    Returns:
        List of EpisodeResult objects
    """
    results = []
    total = len(episodes)
    
    for i, episode in enumerate(episodes):
        result = await ingest_episode(
            client=client,
            name=episode["name"],
            content=episode["content"],
            source_description=source_description
        )
        results.append(result)
        
        if on_progress:
            on_progress(i + 1, total, result)
    
    return results


def create_episode_content(
    section_id: str,
    title: str,
    content: str,
    entities: List[Dict[str, Any]]
) -> str:
    """
    Create enriched episode content with entity annotations.
    
    This helps Graphiti's LLM better identify and extract entities.
    
    Args:
        section_id: Section identifier
        title: Section title
        content: Raw section content
        entities: List of extracted entities from NER
        
    Returns:
        Enriched content string
    """
    # Build entity summary
    entity_summary = []
    
    zones = [e for e in entities if e.get("label") == "ZONE"]
    if zones:
        zone_codes = list(set(
            e.get("normalized", {}).get("code", e.get("text", ""))
            for e in zones
            if isinstance(e.get("normalized"), dict) or e.get("text")
        ))
        if zone_codes:
            entity_summary.append(f"Zones: {', '.join(filter(None, zone_codes))}")
    
    uses = [e for e in entities if e.get("label") == "USE_TYPE"]
    if uses:
        use_types = list(set(e.get("text", "").lower() for e in uses))
        if use_types:
            entity_summary.append(f"Use types: {', '.join(filter(None, use_types))}")
    
    metrics = [e for e in entities if e.get("label") == "METRIC"]
    if metrics:
        metric_names = list(set(
            e.get("normalized", e.get("text", ""))
            for e in metrics
        ))
        if metric_names:
            entity_summary.append(f"Metrics: {', '.join(filter(None, metric_names))}")
    
    measurements = [e for e in entities if e.get("label") == "MEASUREMENT"]
    if measurements:
        values = []
        for e in measurements[:5]:
            norm = e.get("normalized", {})
            if isinstance(norm, dict) and "value" in norm and "unit" in norm:
                values.append(f"{norm['value']} {norm['unit']}")
        if values:
            entity_summary.append(f"Values: {', '.join(values)}")
    
    section_refs = [e for e in entities if e.get("label") == "SECTION_REF"]
    if section_refs:
        refs = list(set(e.get("text", "") for e in section_refs))[:5]
        if refs:
            entity_summary.append(f"References: {', '.join(filter(None, refs))}")
    
    # Build enriched content
    enriched = f"[SECTION: {section_id}]\n"
    enriched += f"[TITLE: {title}]\n\n"
    
    if entity_summary:
        enriched += "[EXTRACTED ENTITIES]\n"
        enriched += "\n".join(entity_summary)
        enriched += "\n\n"
    
    enriched += "[CONTENT]\n"
    enriched += content
    
    return enriched

