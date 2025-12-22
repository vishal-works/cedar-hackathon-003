"""Pydantic models for zoning query responses."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class InterpretedQuery(BaseModel):
    """Extracted entities from user query."""

    use_type: Optional[str] = Field(None, description="Extracted use type (townhouse, multifamily, etc.)")
    zone: Optional[str] = Field(None, description="Extracted zone code (SF-5, MF-4, etc.)")
    jurisdiction: str = Field(default="austin_tx", description="Jurisdiction ID")
    metric: Optional[str] = Field(None, description="Specific metric if queried (height_max, etc.)")


class QueryInfo(BaseModel):
    """Query metadata."""

    original: str = Field(..., description="Original user query")
    interpreted: InterpretedQuery


class Constraint(BaseModel):
    """A quantitative zoning constraint."""

    metric: str = Field(..., description="Standardized metric slug (lot_width_min, height_max, etc.)")
    display_name: str = Field(..., description="Human-readable name")
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit of measurement (ft, sqft, %, units/acre)")
    scope: Literal["lot", "site", "building", "unit"] = Field(..., description="What level this applies to")
    source: str = Field(..., description="Source citation (e.g., 'LDC §25-2-775(B)')")


class Override(BaseModel):
    """A state-level override of local constraints."""

    bill: str = Field(..., description="State bill ID (SB-840, SB-2835)")
    metric: str = Field(..., description="Metric being overridden")
    local_value: float = Field(..., description="Original local value")
    override_value: float = Field(..., description="State override value")
    effective_value: float = Field(..., description="Resolved effective value")
    type: Literal["floor", "ceiling"] = Field(..., description="Override type")
    explanation: str = Field(..., description="Plain English explanation of the override")


class Condition(BaseModel):
    """A parcel-specific condition that modifies constraints."""

    field: str = Field(..., description="Condition field (e.g., 'parcel.corner_lot')")
    affects: str = Field(..., description="What constraint this condition affects")
    description: str = Field(..., description="Plain English explanation")


class Source(BaseModel):
    """Document source citation."""

    document: str = Field(..., description="Document name (Austin LDC, SB-840, etc.)")
    section: str = Field(..., description="Section number")
    title: Optional[str] = Field(None, description="Section title if available")


class ZoningResponse(BaseModel):
    """Complete structured response for a zoning query."""

    query: QueryInfo
    permitted: Optional[bool] = Field(..., description="Whether use is permitted (null if unknown)")
    summary: str = Field(..., description="1-2 sentence plain English summary")
    constraints: list[Constraint] = Field(default_factory=list, description="Applicable constraints")
    overrides: list[Override] = Field(default_factory=list, description="State overrides if applicable")
    conditions: list[Condition] = Field(default_factory=list, description="Conditional requirements")
    sources: list[Source] = Field(default_factory=list, description="Source citations")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Confidence in response")
    caveats: list[str] = Field(default_factory=list, description="Important notes or limitations")

    class Config:
        json_schema_extra = {
            "example": {
                "query": {
                    "original": "Can I build townhouses in SF-5?",
                    "interpreted": {"use_type": "townhouse", "zone": "SF-5", "jurisdiction": "austin_tx"},
                },
                "permitted": True,
                "summary": "Townhouses are permitted by right in SF-5 zone.",
                "constraints": [
                    {
                        "metric": "lot_width_min",
                        "display_name": "Minimum Lot Width",
                        "value": 20,
                        "unit": "ft",
                        "scope": "lot",
                        "source": "LDC §25-2-775(B)",
                    }
                ],
                "overrides": [],
                "conditions": [],
                "sources": [{"document": "Austin LDC", "section": "25-2-775", "title": "Townhouses"}],
                "confidence": "high",
                "caveats": [],
            }
        }

