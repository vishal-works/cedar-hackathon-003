"""
ORGAnIZM Graphiti Module

Client setup and ingestion logic for the Graphiti knowledge graph.
"""

from .client import get_graphiti_client, initialize_graph
from .type_config import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP
from .ingestion import ingest_episode, ingest_episodes_batch

__all__ = [
    "get_graphiti_client",
    "initialize_graph",
    "ENTITY_TYPES",
    "EDGE_TYPES",
    "EDGE_TYPE_MAP",
    "ingest_episode",
    "ingest_episodes_batch",
]

