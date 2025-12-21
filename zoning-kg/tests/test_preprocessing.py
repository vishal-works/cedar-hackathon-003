"""
Test cases for the ORGAnIZM preprocessing pipeline.

Run tests with:
    pytest tests/test_preprocessing.py -v
    python -m pytest tests/test_preprocessing.py -v
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessing.section_splitter import Section, split_document_text
from src.preprocessing.patterns import ALL_PATTERNS, ZONE_PATTERNS
from src.preprocessing.normalizer import (
    normalize_zone,
    normalize_measurement,
    normalize_metric,
    normalize_section_ref,
    normalize_use_type,
    normalize_operator,
    normalize_entity
)
from src.preprocessing.ner_pipeline import (
    create_ner_pipeline,
    process_text,
    TaggedEntity,
    TaggedSection
)


# ============================================================================
# Section Splitter Tests
# ============================================================================

class TestSectionSplitter:
    """Tests for section splitting functionality."""
    
    def test_section_splitting_basic(self):
        """Test that sections are split correctly with Source: markers."""
        sample = """
* § 25-2-775 - TOWNHOUSES.
* § 25-2-776 - CONDOMINIUMS.

### ARTICLE 1. - RESIDENTIAL.

Section 25-2-775 - TOWNHOUSES.

(A) The minimum lot width is 20 feet.

(B) The minimum lot area is 2,500 square feet.

Source: Ord. 123.

Section 25-2-776 - CONDOMINIUMS.

(A) The minimum site area is 14,000 square feet.

(B) Maximum building coverage is 50%.

Source: Ord. 456.
"""
        sections = split_document_text(sample)
        
        # Should find at least 1 section (may merge based on structure)
        assert len(sections) >= 1
        
        # Check that content is captured
        all_content = ' '.join(s.content for s in sections)
        assert "lot width" in all_content.lower()
        assert "20 feet" in all_content
    
    def test_section_dataclass(self):
        """Test Section dataclass creation and serialization."""
        section = Section(
            id="25-2-775",
            title="TOWNHOUSES",
            level=2,
            parent_id="chapter-25-2",
            content="Test content",
            start_line=1,
            end_line=10,
            subsections=["25-2-775-A", "25-2-775-B"]
        )
        
        # Test to_dict
        data = section.to_dict()
        assert data["id"] == "25-2-775"
        assert data["title"] == "TOWNHOUSES"
        assert data["level"] == 2
        assert len(data["subsections"]) == 2
        
        # Test from_dict
        restored = Section.from_dict(data)
        assert restored.id == section.id
        assert restored.title == section.title


# ============================================================================
# NER Pipeline Tests
# ============================================================================

class TestNERPipeline:
    """Tests for NER pipeline functionality."""
    
    @pytest.fixture(scope="class")
    def nlp(self):
        """Create NER pipeline once for all tests."""
        return create_ner_pipeline()
    
    def test_zone_pattern_matches(self, nlp):
        """Test that zone codes are recognized correctly."""
        doc = nlp("The SF-5 zone allows townhouses.")
        zones = [ent for ent in doc.ents if ent.label_ == "ZONE"]
        
        assert len(zones) >= 1
        assert any(z.text == "SF-5" for z in zones)
    
    def test_zone_patterns_multiple(self, nlp):
        """Test multiple zone code patterns."""
        doc = nlp("Zoning includes SF-1, SF-2, MF-4, and CBD districts.")
        zones = [ent for ent in doc.ents if ent.label_ == "ZONE"]
        
        zone_texts = [z.text for z in zones]
        assert "SF-1" in zone_texts
        assert "SF-2" in zone_texts
        assert "MF-4" in zone_texts
        assert "CBD" in zone_texts
    
    def test_use_type_patterns(self, nlp):
        """Test use type recognition."""
        doc = nlp("Townhouses and condominiums are permitted.")
        use_types = [ent for ent in doc.ents if ent.label_ == "USE_TYPE"]
        
        # Should find at least townhouse
        assert len(use_types) >= 1
    
    def test_measurement_patterns(self, nlp):
        """Test measurement recognition."""
        doc = nlp("The minimum lot width is 20 feet and coverage is 40%.")
        measurements = [ent for ent in doc.ents if ent.label_ == "MEASUREMENT"]
        
        assert len(measurements) >= 2
        measurement_texts = [m.text for m in measurements]
        assert "20 feet" in measurement_texts
        assert "40%" in measurement_texts
    
    def test_metric_patterns(self, nlp):
        """Test metric recognition."""
        doc = nlp("Requirements include lot width, setback, and building coverage.")
        metrics = [ent for ent in doc.ents if ent.label_ == "METRIC"]
        
        assert len(metrics) >= 2
    
    def test_section_ref_patterns(self, nlp):
        """Test section reference recognition."""
        doc = nlp("See § 25-2-775 and Section 25-2-776 for details.")
        refs = [ent for ent in doc.ents if ent.label_ == "SECTION_REF"]
        
        assert len(refs) >= 2
    
    def test_operator_patterns(self, nlp):
        """Test operator recognition."""
        doc = nlp("The minimum height is required, maximum is not exceed 35 feet.")
        operators = [ent for ent in doc.ents if ent.label_ == "OPERATOR"]
        
        assert len(operators) >= 1
    
    def test_process_text_function(self, nlp):
        """Test the process_text helper function."""
        entities = process_text(nlp, "SF-5 zone with 20 feet minimum lot width")
        
        assert len(entities) >= 2
        assert all(isinstance(e, TaggedEntity) for e in entities)
        
        labels = [e.label for e in entities]
        assert "ZONE" in labels
        assert "MEASUREMENT" in labels


# ============================================================================
# Normalizer Tests
# ============================================================================

class TestNormalizer:
    """Tests for entity normalization."""
    
    def test_zone_normalization_uppercase(self):
        """Test zone code uppercase normalization."""
        result = normalize_zone("sf-5")
        assert result["code"] == "SF-5"
    
    def test_zone_normalization_hyphen(self):
        """Test zone code hyphen addition."""
        result = normalize_zone("SF5")
        assert result["code"] == "SF-5"
    
    def test_zone_normalization_space(self):
        """Test zone code space to hyphen."""
        result = normalize_zone("SF 5")
        assert result["code"] == "SF-5"
    
    def test_zone_normalization_name(self):
        """Test zone name to code mapping."""
        result = normalize_zone("urban family residence")
        assert result["code"] == "SF-5"
        assert result["name"] == "urban family residence"
    
    def test_measurement_normalization_feet(self):
        """Test feet measurement normalization."""
        result = normalize_measurement("20 feet")
        assert result["value"] == 20
        assert result["unit"] == "ft"
    
    def test_measurement_normalization_sqft(self):
        """Test square feet normalization."""
        result = normalize_measurement("5750 square feet")
        assert result["value"] == 5750
        assert result["unit"] == "sqft"
    
    def test_measurement_normalization_percent(self):
        """Test percentage normalization."""
        result = normalize_measurement("40%")
        assert result["value"] == 40
        assert result["unit"] == "%"
    
    def test_measurement_normalization_percent_word(self):
        """Test percentage word normalization."""
        result = normalize_measurement("40 percent")
        assert result["value"] == 40
        assert result["unit"] == "%"
    
    def test_measurement_normalization_ratio(self):
        """Test ratio normalization."""
        result = normalize_measurement("1:1")
        assert result["value"] == "1:1"
        assert result["unit"] == "ratio"
        assert result["numerator"] == 1
        assert result["denominator"] == 1
    
    def test_measurement_normalization_density(self):
        """Test density normalization."""
        result = normalize_measurement("17 units per acre")
        assert result["value"] == 17
        assert result["unit"] == "units/acre"
    
    def test_metric_normalization_lot_width(self):
        """Test lot width metric normalization."""
        assert normalize_metric("lot width") == "lot_width_min"
        assert normalize_metric("minimum lot width") == "lot_width_min"
    
    def test_metric_normalization_setback(self):
        """Test setback metric normalization."""
        assert normalize_metric("setback") == "setback_min"
    
    def test_metric_normalization_height(self):
        """Test height metric normalization."""
        assert normalize_metric("height") == "height_max"
        assert normalize_metric("building height") == "height_max"
    
    def test_metric_normalization_coverage(self):
        """Test coverage metric normalization."""
        assert normalize_metric("building coverage") == "building_coverage_max"
    
    def test_section_ref_normalization_basic(self):
        """Test basic section reference normalization."""
        result = normalize_section_ref("§ 25-2-775")
        assert result["section"] == "25-2-775"
        assert result["subsection"] is None
    
    def test_section_ref_normalization_with_subsection(self):
        """Test section reference with subsection."""
        result = normalize_section_ref("§25-2-775(B)")
        assert result["section"] == "25-2-775"
        assert result["subsection"] == "B"
    
    def test_section_ref_normalization_section_word(self):
        """Test 'Section' prefix normalization."""
        result = normalize_section_ref("Section 25-2-492")
        assert result["section"] == "25-2-492"
    
    def test_use_type_normalization(self):
        """Test use type normalization."""
        assert normalize_use_type("townhouses") == "townhouse"
        assert normalize_use_type("condominiums") == "condominium"
        assert normalize_use_type("single-family") == "single_family"
    
    def test_operator_normalization(self):
        """Test operator normalization."""
        assert normalize_operator("minimum") == "min"
        assert normalize_operator("maximum") == "max"
        assert normalize_operator("at least") == "gte"
        assert normalize_operator("not exceed") == "lte"
    
    def test_normalize_entity_dispatch(self):
        """Test unified normalize_entity function."""
        # Zone
        zone_result = normalize_entity("SF-5", "ZONE")
        assert zone_result["code"] == "SF-5"
        
        # Measurement
        meas_result = normalize_entity("20 feet", "MEASUREMENT")
        assert meas_result["value"] == 20
        assert meas_result["unit"] == "ft"
        
        # Metric
        metric_result = normalize_entity("lot width", "METRIC")
        assert metric_result == "lot_width_min"


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for the full pipeline."""
    
    @pytest.fixture(scope="class")
    def nlp(self):
        """Create NER pipeline once for all tests."""
        return create_ner_pipeline()
    
    def test_full_pipeline_sample_text(self, nlp):
        """Test full pipeline on sample zoning text."""
        sample_text = """
        § 25-2-775 - TOWNHOUSES.
        
        (A) In an SF-5 district, the minimum lot width for a townhouse is 20 feet.
        
        (B) The minimum site area is 14,000 square feet.
        
        (C) Maximum building coverage shall not exceed 40%.
        
        (D) Height is limited to 35 feet or 3 stories.
        """
        
        entities = process_text(nlp, sample_text)
        
        # Should find entities of various types
        labels = set(e.label for e in entities)
        assert "ZONE" in labels
        assert "MEASUREMENT" in labels
        
        # Check specific entities
        zones = [e for e in entities if e.label == "ZONE"]
        assert any("SF-5" in e.text for e in zones)
        
        measurements = [e for e in entities if e.label == "MEASUREMENT"]
        assert any("20 feet" in e.text for e in measurements)
    
    def test_tagged_section_serialization(self, nlp):
        """Test TaggedSection serialization."""
        entities = process_text(nlp, "SF-5 zone with 20 feet minimum")
        
        section = TaggedSection(
            section_id="test-section",
            content="SF-5 zone with 20 feet minimum",
            entities=entities
        )
        
        # Test serialization
        data = section.to_dict()
        assert data["section_id"] == "test-section"
        assert len(data["entities"]) == len(entities)
        
        # Test deserialization
        restored = TaggedSection.from_dict(data)
        assert restored.section_id == section.section_id
        assert len(restored.entities) == len(section.entities)


# ============================================================================
# Pattern Tests
# ============================================================================

class TestPatterns:
    """Tests for pattern definitions."""
    
    def test_all_patterns_not_empty(self):
        """Verify patterns are defined."""
        assert len(ALL_PATTERNS) > 0
    
    def test_zone_patterns_exist(self):
        """Verify zone patterns are defined."""
        assert len(ZONE_PATTERNS) > 0
    
    def test_pattern_structure(self):
        """Verify pattern structure is valid."""
        for pattern in ALL_PATTERNS:
            assert "label" in pattern
            assert "pattern" in pattern
            assert pattern["label"] in [
                "ZONE", "USE_TYPE", "SECTION_REF",
                "METRIC", "MEASUREMENT", "OPERATOR"
            ]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

