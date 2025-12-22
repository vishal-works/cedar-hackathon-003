"""
Edge type definitions for the ORGAnIZM zoning knowledge graph.

These models define the structure of relationships between nodes.
They are passed to Graphiti via the edge_types dict.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class Contains(BaseModel):
    """Jurisdiction contains a zone."""
    source_jurisdiction_id: str
    target_zone_id: str


class AllowsUse(BaseModel):
    """Zone permits a specific use type."""
    source_zone_id: str
    target_use_id: str
    permitted_by_right: bool = True
    requires_conditional_use: bool = False
    requires_special_exception: bool = False


class GovernedBy(BaseModel):
    """Use type is regulated by a rule."""
    source_use_id: str
    target_rule_id: str


class HasConstraint(BaseModel):
    """Rule contains a quantitative constraint."""
    source_rule_id: str
    target_constraint_id: str


class HasCondition(BaseModel):
    """Constraint has conditional application."""
    source_constraint_id: str
    target_condition_id: str
    logic: Literal["AND", "OR"] = "AND"


class AppliesIn(BaseModel):
    """Rule applies in specific zones."""
    source_rule_id: str
    target_zone_id: str


class OverriddenBy(BaseModel):
    """Local constraint is overridden by higher authority."""
    source_constraint_id: str
    target_override_id: str
    resolution: Literal["max", "min"]  # max for floor, min for ceiling


class SourcedFrom(BaseModel):
    """Entity traces back to source document."""
    source_entity_id: str
    target_document_id: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None

