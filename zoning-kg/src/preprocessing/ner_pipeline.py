"""
spaCy NER pipeline for zoning entities.

Creates a custom spaCy pipeline with EntityRuler patterns
to recognize zoning-specific entities.
"""
import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Optional, Dict, Any

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from .patterns import ALL_PATTERNS, LABEL_CATEGORIES
from .normalizer import normalize_entity


@dataclass
class TaggedEntity:
    """Represents a tagged entity from the NER pipeline."""
    
    text: str  # Original text span
    label: str  # Entity label (ZONE, METRIC, etc.)
    start: int  # Character offset start
    end: int  # Character offset end
    normalized: Any  # Normalized form with structured data
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class TaggedSection:
    """Represents a section with tagged entities."""
    
    section_id: str
    content: str
    entities: List[TaggedEntity] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert section to dictionary for JSON serialization."""
        return {
            "section_id": self.section_id,
            "content": self.content,
            "entities": [e.to_dict() for e in self.entities]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TaggedSection":
        """Create TaggedSection from dictionary."""
        entities = [TaggedEntity(**e) for e in data.get("entities", [])]
        return cls(
            section_id=data["section_id"],
            content=data["content"],
            entities=entities
        )


def create_ner_pipeline(model_name: str = "en_core_web_sm") -> Language:
    """
    Create a spaCy NLP pipeline with custom EntityRuler for zoning entities.
    
    Args:
        model_name: The spaCy model to use as base
        
    Returns:
        Configured spaCy Language object
    """
    # Load base model
    nlp = spacy.load(model_name)
    
    # Add EntityRuler BEFORE the NER component
    # This ensures our patterns take precedence
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    ruler.add_patterns(ALL_PATTERNS)
    
    return nlp


def extract_entities(doc: Doc) -> List[TaggedEntity]:
    """
    Extract tagged entities from a spaCy Doc.
    
    Args:
        doc: Processed spaCy Doc object
        
    Returns:
        List of TaggedEntity objects
    """
    entities = []
    
    for ent in doc.ents:
        # Only process entities with our custom labels
        if ent.label_ in LABEL_CATEGORIES:
            # Normalize the entity
            normalized = normalize_entity(ent.text, ent.label_)
            
            entities.append(TaggedEntity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char,
                normalized=normalized
            ))
    
    return entities


def process_text(nlp: Language, text: str) -> List[TaggedEntity]:
    """
    Process text and extract zoning entities.
    
    Args:
        nlp: Configured spaCy pipeline
        text: Text to process
        
    Returns:
        List of TaggedEntity objects
    """
    doc = nlp(text)
    return extract_entities(doc)


def process_section(
    nlp: Language,
    section_id: str,
    content: str
) -> TaggedSection:
    """
    Process a section and return tagged entities.
    
    Args:
        nlp: Configured spaCy pipeline
        section_id: Section identifier
        content: Section content text
        
    Returns:
        TaggedSection with entities
    """
    entities = process_text(nlp, content)
    
    return TaggedSection(
        section_id=section_id,
        content=content,
        entities=entities
    )


def process_section_file(
    nlp: Language,
    section_path: Path
) -> TaggedSection:
    """
    Process a section from a JSON file.
    
    Args:
        nlp: Configured spaCy pipeline
        section_path: Path to section JSON file
        
    Returns:
        TaggedSection with entities
    """
    with open(section_path, 'r', encoding='utf-8') as f:
        section_data = json.load(f)
    
    return process_section(
        nlp,
        section_data["id"],
        section_data["content"]
    )


def write_tagged_section(
    tagged_section: TaggedSection,
    output_path: Path
) -> None:
    """
    Write tagged section to JSON file.
    
    Args:
        tagged_section: TaggedSection to write
        output_path: Path to output file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tagged_section.to_dict(), f, indent=2, ensure_ascii=False)


def process_sections_directory(
    nlp: Language,
    input_dir: Path,
    output_dir: Path,
    section_id: Optional[str] = None
) -> List[TaggedSection]:
    """
    Process all sections in a directory.
    
    Args:
        nlp: Configured spaCy pipeline
        input_dir: Directory containing section JSON files
        output_dir: Directory to write tagged output
        section_id: Optional specific section to process
        
    Returns:
        List of TaggedSection objects
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    tagged_sections = []
    
    # Find section files
    if section_id:
        section_files = [input_dir / f"{section_id}.json"]
    else:
        section_files = list(input_dir.glob("*.json"))
        # Exclude index.json
        section_files = [f for f in section_files if f.name != "index.json"]
    
    for section_file in section_files:
        if not section_file.exists():
            print(f"Warning: Section file not found: {section_file}")
            continue
        
        try:
            tagged = process_section_file(nlp, section_file)
            tagged_sections.append(tagged)
            
            # Write output
            output_path = output_dir / f"{section_file.stem}.json"
            write_tagged_section(tagged, output_path)
            
            print(f"Processed {section_file.stem}: {len(tagged.entities)} entities found")
        except Exception as e:
            print(f"Error processing {section_file}: {e}")
    
    return tagged_sections


def get_entity_summary(tagged_sections: List[TaggedSection]) -> Dict[str, Any]:
    """
    Generate a summary of entities across all tagged sections.
    
    Args:
        tagged_sections: List of TaggedSection objects
        
    Returns:
        Dictionary with entity statistics
    """
    summary = {
        "total_sections": len(tagged_sections),
        "total_entities": 0,
        "entities_by_label": {},
        "unique_values": {}
    }
    
    for section in tagged_sections:
        for entity in section.entities:
            summary["total_entities"] += 1
            
            # Count by label
            if entity.label not in summary["entities_by_label"]:
                summary["entities_by_label"][entity.label] = 0
            summary["entities_by_label"][entity.label] += 1
            
            # Track unique values
            if entity.label not in summary["unique_values"]:
                summary["unique_values"][entity.label] = set()
            summary["unique_values"][entity.label].add(entity.text)
    
    # Convert sets to lists for JSON serialization
    for label in summary["unique_values"]:
        summary["unique_values"][label] = sorted(list(summary["unique_values"][label]))
    
    return summary


if __name__ == "__main__":
    # Quick test
    print("Creating NER pipeline...")
    nlp = create_ner_pipeline()
    
    test_text = """
    The SF-5 zone allows townhouses with a minimum lot width of 20 feet.
    According to § 25-2-775, the minimum site area is 14,000 square feet.
    Maximum building coverage is 40% and height is limited to 35 feet.
    """
    
    print("\nProcessing test text...")
    entities = process_text(nlp, test_text)
    
    print(f"\nFound {len(entities)} entities:")
    for ent in entities:
        print(f"  {ent.text!r} -> {ent.label} (normalized: {ent.normalized})")

