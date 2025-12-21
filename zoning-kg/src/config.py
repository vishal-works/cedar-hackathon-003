"""Configuration settings for ORGAnIZM preprocessing pipeline."""
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration settings for the preprocessing pipeline."""
    
    # Base paths
    project_root: Path = Path(__file__).parent.parent
    data_dir: Path = project_root / "data"
    
    # Input paths
    raw_dir: Path = data_dir / "raw"
    ldc_file: Path = raw_dir / "ldc.md"
    
    # Output paths
    processed_dir: Path = data_dir / "processed"
    sections_dir: Path = processed_dir / "sections"
    tagged_dir: Path = processed_dir / "tagged"
    
    # spaCy model
    spacy_model: str = "en_core_web_sm"
    
    # Section splitter settings
    min_section_length: int = 50  # Minimum characters for a valid section
    
    def ensure_directories(self) -> None:
        """Create output directories if they don't exist."""
        self.sections_dir.mkdir(parents=True, exist_ok=True)
        self.tagged_dir.mkdir(parents=True, exist_ok=True)


# Default configuration instance
config = Config()

