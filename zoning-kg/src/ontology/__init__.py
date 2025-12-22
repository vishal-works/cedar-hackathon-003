"""
ORGAnIZM Ontology Module

Entity and edge type definitions for the zoning knowledge graph.
"""

from .entities import (
    Jurisdiction,
    Zone,
    UseType,
    Rule,
    Constraint,
    Condition,
    Override,
    DocumentSource,
)

from .edges import (
    Contains,
    AllowsUse,
    GovernedBy,
    HasConstraint,
    HasCondition,
    AppliesIn,
    OverriddenBy,
    SourcedFrom,
)

from .metrics import METRICS_CATALOG, MetricScope, validate_metric_slug, get_metric_scope

__all__ = [
    # Entities
    "Jurisdiction",
    "Zone",
    "UseType",
    "Rule",
    "Constraint",
    "Condition",
    "Override",
    "DocumentSource",
    # Edges
    "Contains",
    "AllowsUse",
    "GovernedBy",
    "HasConstraint",
    "HasCondition",
    "AppliesIn",
    "OverriddenBy",
    "SourcedFrom",
    # Metrics
    "METRICS_CATALOG",
    "MetricScope",
    "validate_metric_slug",
    "get_metric_scope",
]

