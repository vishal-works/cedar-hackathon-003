"""Tests for the agent pipeline."""

import json
import pytest
from src.agents.schemas import ZoningResponse, Constraint, Override
from src.agents.orchestrator import ZoningQueryPipeline


class TestSchemas:
    """Test Pydantic schema validation."""

    def test_constraint_valid(self):
        """Test valid constraint creation."""

        constraint = Constraint(
            metric="lot_width_min",
            display_name="Minimum Lot Width",
            value=20,
            unit="ft",
            scope="lot",
            source="LDC §25-2-775(B)",
        )
        assert constraint.metric == "lot_width_min"
        assert constraint.value == 20

    def test_override_valid(self):
        """Test valid override creation."""

        override = Override(
            bill="SB-840",
            metric="parking_per_unit",
            local_value=2,
            override_value=1,
            effective_value=1,
            type="ceiling",
            explanation="State caps parking at 1 space per unit",
        )
        assert override.type == "ceiling"
        assert override.effective_value == 1

    def test_zoning_response_minimal(self):
        """Test minimal valid response."""

        response = ZoningResponse(
            query={"original": "Test query", "interpreted": {"jurisdiction": "austin_tx"}},
            permitted=None,
            summary="Test summary",
            confidence="low",
        )
        assert response.permitted is None
        assert response.constraints == []

    def test_zoning_response_full(self):
        """Test full response with all fields."""

        data = {
            "query": {
                "original": "Can I build townhouses in SF-5?",
                "interpreted": {"use_type": "townhouse", "zone": "SF-5", "jurisdiction": "austin_tx"},
            },
            "permitted": True,
            "summary": "Townhouses are permitted in SF-5.",
            "constraints": [
                {
                    "metric": "lot_width_min",
                    "display_name": "Minimum Lot Width",
                    "value": 20,
                    "unit": "ft",
                    "scope": "lot",
                    "source": "LDC §25-2-775",
                }
            ],
            "overrides": [],
            "conditions": [],
            "sources": [{"document": "Austin LDC", "section": "25-2-775", "title": "Townhouses"}],
            "confidence": "high",
            "caveats": [],
        }
        response = ZoningResponse.model_validate(data)
        assert response.permitted is True
        assert len(response.constraints) == 1


class TestPipeline:
    """Integration tests for the pipeline."""

    @pytest.fixture
    def pipeline(self):
        return ZoningQueryPipeline(verbose=False)

    @pytest.mark.skip(reason="Requires OpenAI API key and MCP server")
    def test_simple_query(self, pipeline):
        """Test a simple permissibility query."""

        result = pipeline.query("Can I build townhouses in SF-5?")
        assert result.success or result.raw_response is not None

    @pytest.mark.skip(reason="Requires OpenAI API key and MCP server")
    def test_constraint_query(self, pipeline):
        """Test a constraint lookup query."""

        result = pipeline.query("What's the maximum height in MF-4?")
        assert result.success or result.raw_response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

