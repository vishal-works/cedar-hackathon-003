"""
Graphiti type configuration for ORGAnIZM.

This module defines the entity_types, edge_types, and edge_type_map
that are passed to Graphiti's add_episode() method.
"""

from src.ontology.entities import (
    Jurisdiction, Zone, UseType, Rule, 
    Constraint, Condition, Override, DocumentSource
)
from src.ontology.edges import (
    Contains, AllowsUse, GovernedBy, HasConstraint,
    HasCondition, AppliesIn, OverriddenBy, SourcedFrom
)


# Entity types dict: maps type names to Pydantic models
ENTITY_TYPES = {
    "Jurisdiction": Jurisdiction,
    "Zone": Zone,
    "UseType": UseType,
    "Rule": Rule,
    "Constraint": Constraint,
    "Condition": Condition,
    "Override": Override,
    "DocumentSource": DocumentSource,
}


# Edge types dict: maps edge names to Pydantic models
EDGE_TYPES = {
    "Contains": Contains,
    "AllowsUse": AllowsUse,
    "GovernedBy": GovernedBy,
    "HasConstraint": HasConstraint,
    "HasCondition": HasCondition,
    "AppliesIn": AppliesIn,
    "OverriddenBy": OverriddenBy,
    "SourcedFrom": SourcedFrom,
}


# Edge type map: defines which edges can connect which entity types
# Format: (source_type, target_type) -> [allowed_edge_types]
EDGE_TYPE_MAP = {
    # Jurisdiction relationships
    ("Jurisdiction", "Zone"): ["Contains"],
    ("Jurisdiction", "Override"): ["Contains"],
    
    # Zone relationships
    ("Zone", "UseType"): ["AllowsUse"],
    
    # UseType relationships
    ("UseType", "Rule"): ["GovernedBy"],
    
    # Rule relationships
    ("Rule", "Constraint"): ["HasConstraint"],
    ("Rule", "Zone"): ["AppliesIn"],
    ("Rule", "DocumentSource"): ["SourcedFrom"],
    
    # Constraint relationships
    ("Constraint", "Condition"): ["HasCondition"],
    ("Constraint", "Override"): ["OverriddenBy"],
    ("Constraint", "DocumentSource"): ["SourcedFrom"],
    
    # Override relationships
    ("Override", "DocumentSource"): ["SourcedFrom"],
}

