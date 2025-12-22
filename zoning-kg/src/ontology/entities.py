"""
Entity type definitions for the ORGAnIZM zoning knowledge graph.

These Pydantic models define the structure of nodes in the graph.
They are passed to Graphiti via the entity_types dict.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal, Union
from datetime import date


class Jurisdiction(BaseModel):
    """Geographic authority that issues zoning regulations."""
    jurisdiction_id: str = Field(..., description="Composite key, e.g., 'austin_tx' or 'texas'")
    display_name: str = Field(..., description="Full name, e.g., 'City of Austin'")
    state: str = Field(..., description="State abbreviation, e.g., 'TX'")
    level: Literal["city", "county", "state"] = Field(..., description="Hierarchy level")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "jurisdiction_id": "austin_tx",
                "display_name": "City of Austin",
                "state": "TX",
                "level": "city"
            }
        }
    )


class Zone(BaseModel):
    """Zoning district classification within a jurisdiction."""
    zone_id: str = Field(..., description="Composite key: 'austin_tx:SF-5'")
    code: str = Field(..., description="Zone code: 'SF-5'")
    display_name: str = Field(..., description="Full name: 'Urban Family Residence'")
    family: Literal[
        "single_family", "multifamily", "commercial", 
        "office", "industrial", "mixed_use", "planned"
    ]
    jurisdiction_id: str = Field(..., description="Parent jurisdiction reference")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "zone_id": "austin_tx:SF-5",
                "code": "SF-5",
                "display_name": "Urban Family Residence",
                "family": "single_family",
                "jurisdiction_id": "austin_tx"
            }
        }
    )


class UseType(BaseModel):
    """Building or development use type."""
    use_type_id: str = Field(..., description="Canonical ID: 'townhouse'")
    display_name: str = Field(..., description="Display name: 'Townhouse'")
    group: Literal["residential", "commercial", "industrial", "mixed_use"]
    aliases: List[str] = Field(default_factory=list, description="Alternative names")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "use_type_id": "townhouse",
                "display_name": "Townhouse",
                "group": "residential",
                "aliases": ["townhome", "row house", "attached dwelling"]
            }
        }
    )


class Rule(BaseModel):
    """A regulation from a specific document section."""
    rule_id: str = Field(..., description="Composite key: 'austin_tx:LDC:25-2-775'")
    section: str = Field(..., description="Section number: '25-2-775'")
    title: str = Field(..., description="Section title: 'Townhouses'")
    document: str = Field(..., description="Source document name")
    jurisdiction_id: str
    applies_to_uses: List[str] = Field(default_factory=list)
    applies_in_zones: List[str] = Field(default_factory=list)
    text_excerpt: Optional[str] = Field(None, max_length=2000)


class Constraint(BaseModel):
    """Quantitative requirement from a rule."""
    constraint_id: str = Field(..., description="Composite key: 'austin_tx:LDC:25-2-775:B:lot_width_min'")
    rule_id: str
    subsection: Optional[str] = Field(None, description="e.g., 'B', 'H(1)(b)'")
    metric: str = Field(..., description="Standardized metric slug")
    operator: Literal["gte", "gt", "lte", "lt", "eq", "range"]
    constraint_value: float
    value_high: Optional[float] = Field(None, description="For range operator")
    unit: Optional[str] = Field(None, description="e.g., 'ft', 'sqft', '%'")
    applies_to: Literal["lot", "site", "building", "unit"]
    source_text: Optional[str] = Field(None, max_length=500)


class Condition(BaseModel):
    """Context trigger for when a constraint applies."""
    condition_id: str = Field(..., description="Unique condition ID")
    condition_field: str = Field(..., description="e.g., 'parcel.corner_lot', 'parcel.street_class'")
    operator: Literal["eq", "neq", "gt", "gte", "lt", "lte", "in"]
    condition_value: Union[str, float, bool, List[str]]


class Override(BaseModel):
    """Higher-authority law that supersedes local regulations."""
    override_id: str = Field(..., description="e.g., 'texas:SB-840:density'")
    bill_id: str = Field(..., description="e.g., 'SB-840'")
    jurisdiction_id: str = Field(..., description="Issuing authority: 'texas'")
    metric: str = Field(..., description="What's being overridden")
    override_type: Literal["floor", "ceiling"]
    override_value: float
    unit: Optional[str] = None
    scope_uses: List[str] = Field(default_factory=list)
    scope_zones: List[str] = Field(default_factory=list)
    effective_date: date
    exclusions: List[str] = Field(default_factory=list)


class DocumentSource(BaseModel):
    """Citation for traceability."""
    source_id: str = Field(..., description="e.g., 'austin_tx:LDC:25-2-775(B)'")
    document: str
    section: str
    subsection: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    text_excerpt: Optional[str] = Field(None, max_length=1000)

