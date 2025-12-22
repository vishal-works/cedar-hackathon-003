"""Tests for ontology models and Graphiti configuration."""

import pytest
from datetime import date
from pydantic import ValidationError

from src.ontology.entities import (
    Jurisdiction, Zone, UseType, Rule, 
    Constraint, Condition, Override, DocumentSource
)
from src.ontology.edges import (
    AllowsUse, OverriddenBy, Contains, 
    GovernedBy, HasConstraint, AppliesIn
)
from src.ontology.metrics import (
    METRICS_CATALOG, MetricScope,
    validate_metric_slug, get_metric_scope, get_metric_info
)
from src.graphiti.type_config import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP


class TestJurisdiction:
    def test_valid_city_jurisdiction(self):
        j = Jurisdiction(
            id="austin_tx",
            name="City of Austin",
            state="TX",
            level="city"
        )
        assert j.id == "austin_tx"
        assert j.level == "city"
    
    def test_valid_state_jurisdiction(self):
        j = Jurisdiction(
            id="texas",
            name="State of Texas",
            state="TX",
            level="state"
        )
        assert j.id == "texas"
        assert j.level == "state"
    
    def test_invalid_level(self):
        with pytest.raises(ValidationError):
            Jurisdiction(
                id="test",
                name="Test",
                state="TX",
                level="invalid"
            )


class TestZone:
    def test_valid_zone(self):
        z = Zone(
            id="austin_tx:SF-5",
            code="SF-5",
            name="Urban Family Residence",
            family="single_family",
            jurisdiction_id="austin_tx"
        )
        assert z.code == "SF-5"
        assert z.family == "single_family"
    
    def test_multifamily_zone(self):
        z = Zone(
            id="austin_tx:MF-4",
            code="MF-4",
            name="Moderate-High Density Multifamily",
            family="multifamily",
            jurisdiction_id="austin_tx"
        )
        assert z.family == "multifamily"
    
    def test_invalid_family(self):
        with pytest.raises(ValidationError):
            Zone(
                id="test",
                code="XX-1",
                name="Invalid Zone",
                family="invalid_family",
                jurisdiction_id="austin_tx"
            )


class TestUseType:
    def test_valid_use_type(self):
        u = UseType(
            id="townhouse",
            name="Townhouse",
            group="residential",
            aliases=["townhome", "row house"]
        )
        assert u.id == "townhouse"
        assert "townhome" in u.aliases
    
    def test_use_type_default_aliases(self):
        u = UseType(
            id="multifamily",
            name="Multifamily",
            group="residential"
        )
        assert u.aliases == []


class TestRule:
    def test_valid_rule(self):
        r = Rule(
            id="austin_tx:LDC:25-2-775",
            section="25-2-775",
            title="Townhouses",
            document="Austin Land Development Code",
            jurisdiction_id="austin_tx",
            applies_to_uses=["townhouse"],
            applies_in_zones=["SF-5", "SF-6"]
        )
        assert r.section == "25-2-775"
        assert "townhouse" in r.applies_to_uses


class TestConstraint:
    def test_valid_constraint(self):
        c = Constraint(
            id="austin_tx:LDC:25-2-775:B:lot_width_min",
            rule_id="austin_tx:LDC:25-2-775",
            subsection="B",
            metric="lot_width_min",
            operator="gte",
            value=20,
            unit="ft",
            applies_to="lot"
        )
        assert c.value == 20
        assert c.operator == "gte"
    
    def test_range_constraint(self):
        c = Constraint(
            id="austin_tx:LDC:25-2-775:C:density",
            rule_id="austin_tx:LDC:25-2-775",
            metric="density_max",
            operator="range",
            value=10,
            value_high=25,
            unit="units/acre",
            applies_to="site"
        )
        assert c.value == 10
        assert c.value_high == 25


class TestCondition:
    def test_valid_condition(self):
        c = Condition(
            id="cond_corner_lot",
            field="parcel.corner_lot",
            operator="eq",
            value=True
        )
        assert c.field == "parcel.corner_lot"
        assert c.value is True
    
    def test_list_condition(self):
        c = Condition(
            id="cond_street_class",
            field="parcel.street_class",
            operator="in",
            value=["arterial", "collector"]
        )
        assert isinstance(c.value, list)


class TestOverride:
    def test_valid_override(self):
        o = Override(
            id="texas:SB-840:density",
            bill_id="SB-840",
            jurisdiction_id="texas",
            metric="density_max",
            override_type="floor",
            value=36,
            unit="units/acre",
            scope_uses=["multifamily", "mixed_use"],
            scope_zones=["commercial"],
            effective_date=date(2025, 9, 1)
        )
        assert o.override_type == "floor"
        assert o.value == 36
    
    def test_ceiling_override(self):
        o = Override(
            id="texas:SB-840:parking",
            bill_id="SB-840",
            jurisdiction_id="texas",
            metric="parking_spaces_per_unit",
            override_type="ceiling",
            value=1,
            unit="spaces",
            effective_date=date(2025, 9, 1)
        )
        assert o.override_type == "ceiling"


class TestDocumentSource:
    def test_valid_source(self):
        d = DocumentSource(
            id="austin_tx:LDC:25-2-775(B)",
            document="Austin Land Development Code",
            section="25-2-775",
            subsection="B",
            line_start=45231,
            line_end=45245,
            text_excerpt="The minimum lot width is 20 feet."
        )
        assert d.section == "25-2-775"
        assert d.line_start == 45231


class TestEdgeModels:
    def test_contains_edge(self):
        edge = Contains(
            source_jurisdiction_id="austin_tx",
            target_zone_id="austin_tx:SF-5"
        )
        assert edge.source_jurisdiction_id == "austin_tx"
    
    def test_allows_use(self):
        edge = AllowsUse(
            source_zone_id="austin_tx:SF-5",
            target_use_id="townhouse",
            permitted_by_right=True,
            requires_conditional_use=False
        )
        assert edge.permitted_by_right is True
    
    def test_overridden_by(self):
        edge = OverriddenBy(
            source_constraint_id="austin_tx:LDC:25-2-492:height_max",
            target_override_id="texas:SB-840:height",
            resolution="max"
        )
        assert edge.resolution == "max"
    
    def test_governed_by(self):
        edge = GovernedBy(
            source_use_id="townhouse",
            target_rule_id="austin_tx:LDC:25-2-775"
        )
        assert edge.target_rule_id == "austin_tx:LDC:25-2-775"
    
    def test_has_constraint(self):
        edge = HasConstraint(
            source_rule_id="austin_tx:LDC:25-2-775",
            target_constraint_id="austin_tx:LDC:25-2-775:B:lot_width_min"
        )
        assert edge.source_rule_id == "austin_tx:LDC:25-2-775"
    
    def test_applies_in(self):
        edge = AppliesIn(
            source_rule_id="austin_tx:LDC:25-2-775",
            target_zone_id="austin_tx:SF-5"
        )
        assert edge.target_zone_id == "austin_tx:SF-5"


class TestMetricsCatalog:
    def test_all_metrics_have_required_fields(self):
        required_fields = ["display_name", "unit", "scope", "description"]
        for slug, info in METRICS_CATALOG.items():
            for field in required_fields:
                assert field in info, f"Metric {slug} missing {field}"
    
    def test_all_metrics_have_valid_scope(self):
        for slug, info in METRICS_CATALOG.items():
            assert isinstance(info["scope"], MetricScope), f"Metric {slug} has invalid scope"
    
    def test_validate_known_metric(self):
        assert validate_metric_slug("lot_width_min") is True
        assert validate_metric_slug("height_max") is True
        assert validate_metric_slug("density_max") is True
    
    def test_validate_unknown_metric(self):
        assert validate_metric_slug("unknown_metric") is False
        assert validate_metric_slug("") is False
    
    def test_get_metric_scope(self):
        assert get_metric_scope("lot_width_min") == MetricScope.LOT
        assert get_metric_scope("height_max") == MetricScope.BUILDING
        assert get_metric_scope("density_max") == MetricScope.SITE
    
    def test_get_metric_scope_unknown(self):
        with pytest.raises(ValueError):
            get_metric_scope("unknown_metric")
    
    def test_get_metric_info(self):
        info = get_metric_info("lot_width_min")
        assert info["unit"] == "ft"
        assert info["scope"] == MetricScope.LOT
    
    def test_lot_metrics_exist(self):
        lot_metrics = ["lot_area_min", "lot_width_min", "lot_depth_min", 
                       "setback_front_min", "setback_side_min", "setback_rear_min"]
        for metric in lot_metrics:
            assert validate_metric_slug(metric), f"Missing lot metric: {metric}"
    
    def test_building_metrics_exist(self):
        building_metrics = ["height_max", "stories_max", "building_coverage_max"]
        for metric in building_metrics:
            assert validate_metric_slug(metric), f"Missing building metric: {metric}"


class TestTypeConfig:
    def test_all_entity_types_present(self):
        required = ["Jurisdiction", "Zone", "UseType", "Rule", 
                    "Constraint", "Condition", "Override", "DocumentSource"]
        for entity in required:
            assert entity in ENTITY_TYPES, f"Missing entity type: {entity}"
    
    def test_all_edge_types_present(self):
        required = ["Contains", "AllowsUse", "GovernedBy", "HasConstraint",
                    "HasCondition", "AppliesIn", "OverriddenBy", "SourcedFrom"]
        for edge in required:
            assert edge in EDGE_TYPES, f"Missing edge type: {edge}"
    
    def test_entity_types_are_classes(self):
        for name, cls in ENTITY_TYPES.items():
            assert hasattr(cls, 'model_validate'), f"{name} is not a Pydantic model"
    
    def test_edge_types_are_classes(self):
        for name, cls in EDGE_TYPES.items():
            assert hasattr(cls, 'model_validate'), f"{name} is not a Pydantic model"
    
    def test_edge_type_map_valid_edges(self):
        """Every edge in map should exist in EDGE_TYPES."""
        for (src, tgt), edges in EDGE_TYPE_MAP.items():
            for edge in edges:
                assert edge in EDGE_TYPES, f"Edge {edge} not in EDGE_TYPES"
    
    def test_edge_type_map_valid_entities(self):
        """Every entity in map should exist in ENTITY_TYPES."""
        entities_in_map = set()
        for (src, tgt) in EDGE_TYPE_MAP.keys():
            entities_in_map.add(src)
            entities_in_map.add(tgt)
        
        for entity in entities_in_map:
            assert entity in ENTITY_TYPES, f"Entity {entity} not in ENTITY_TYPES"
    
    def test_jurisdiction_zone_edge_exists(self):
        assert ("Jurisdiction", "Zone") in EDGE_TYPE_MAP
        assert "Contains" in EDGE_TYPE_MAP[("Jurisdiction", "Zone")]
    
    def test_zone_use_edge_exists(self):
        assert ("Zone", "UseType") in EDGE_TYPE_MAP
        assert "AllowsUse" in EDGE_TYPE_MAP[("Zone", "UseType")]
    
    def test_rule_constraint_edge_exists(self):
        assert ("Rule", "Constraint") in EDGE_TYPE_MAP
        assert "HasConstraint" in EDGE_TYPE_MAP[("Rule", "Constraint")]


class TestIntegration:
    def test_full_constraint_chain(self):
        """Test creating a complete constraint chain."""
        # Jurisdiction
        jurisdiction = Jurisdiction(
            id="austin_tx",
            name="City of Austin",
            state="TX",
            level="city"
        )
        
        # Zone
        zone = Zone(
            id="austin_tx:SF-5",
            code="SF-5",
            name="Urban Family Residence",
            family="single_family",
            jurisdiction_id=jurisdiction.id
        )
        
        # Use type
        use_type = UseType(
            id="townhouse",
            name="Townhouse",
            group="residential"
        )
        
        # Rule
        rule = Rule(
            id="austin_tx:LDC:25-2-775",
            section="25-2-775",
            title="Townhouses",
            document="Austin Land Development Code",
            jurisdiction_id=jurisdiction.id,
            applies_to_uses=[use_type.id],
            applies_in_zones=[zone.code]
        )
        
        # Constraint
        constraint = Constraint(
            id="austin_tx:LDC:25-2-775:B:lot_width_min",
            rule_id=rule.id,
            subsection="B",
            metric="lot_width_min",
            operator="gte",
            value=20,
            unit="ft",
            applies_to="lot"
        )
        
        # Source
        source = DocumentSource(
            id="austin_tx:LDC:25-2-775(B)",
            document="Austin Land Development Code",
            section="25-2-775",
            subsection="B"
        )
        
        # Verify all relationships are valid
        assert constraint.rule_id == rule.id
        assert zone.jurisdiction_id == jurisdiction.id
        assert use_type.id in rule.applies_to_uses
        
    def test_override_hierarchy(self):
        """Test override superseding local constraint."""
        # Local constraint
        local_constraint = Constraint(
            id="austin_tx:LDC:25-2-492:height_max",
            rule_id="austin_tx:LDC:25-2-492",
            metric="height_max",
            operator="lte",
            value=35,  # Austin says max 35 feet
            unit="ft",
            applies_to="building"
        )
        
        # State override
        state_override = Override(
            id="texas:SB-840:height",
            bill_id="SB-840",
            jurisdiction_id="texas",
            metric="height_max",
            override_type="floor",  # Floor means cities can't go below this
            value=45,  # State says at least 45 feet allowed
            unit="ft",
            effective_date=date(2025, 9, 1)
        )
        
        # Override relationship
        override_edge = OverriddenBy(
            source_constraint_id=local_constraint.id,
            target_override_id=state_override.id,
            resolution="max"  # Take the higher value
        )
        
        # The effective value should be max(35, 45) = 45
        effective_height = max(local_constraint.value, state_override.value)
        assert effective_height == 45

