"""
Section splitter for Austin Land Development Code (LDC).

Splits the LDC markdown into logical sections based on header patterns.
The LDC uses numbered sections like:
- `* § 25-X-XXX - TITLE` (TOC format)
- `§ 25-X-XXX - TITLE` (inline format)
- Subsections: (A), (B), (1), (a), etc.
"""
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, List, Tuple


@dataclass
class Section:
    """Represents a section of the Land Development Code."""
    
    id: str  # e.g., "25-2-775"
    title: str  # e.g., "Townhouses"
    level: int  # 1 = article, 2 = section, 3 = subsection
    parent_id: Optional[str]
    content: str  # The full text of this section
    start_line: int  # For traceability
    end_line: int
    subsections: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert section to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Section":
        """Create section from dictionary."""
        return cls(**data)


# Regex patterns for section detection
# Primary section pattern: § 25-X-XXX format (with or without leading *)
SECTION_PATTERN = re.compile(
    r'^[\*\s]*§\s*(\d+-\d+-\d+[A-Z]?)\s*[-–—]\s*(.+?)\.?\s*$',
    re.MULTILINE
)

# Alternative section header pattern (markdown headers with section numbers)
MARKDOWN_SECTION_PATTERN = re.compile(
    r'^#+\s*(?:§\s*)?(\d+-\d+-\d+[A-Z]?)\s*[-–—]\s*(.+?)\.?\s*$',
    re.MULTILINE
)

# TOC-style pattern: * § 25-X-XXX - TITLE
TOC_SECTION_PATTERN = re.compile(
    r'^\*\s*§\s*(\d+-\d+-\d+[A-Z]?)\s*[-–—]\s*(.+?)\.?\s*$',
    re.MULTILINE
)

# Subsection patterns
SUBSECTION_LETTER_PATTERN = re.compile(r'^\(([A-Z])\)\s*$', re.MULTILINE)
SUBSECTION_NUMBER_PATTERN = re.compile(r'^\((\d+)\)\s*$', re.MULTILINE)
SUBSECTION_LOWER_PATTERN = re.compile(r'^\(([a-z])\)\s*$', re.MULTILINE)

# Article and Division patterns
ARTICLE_PATTERN = re.compile(
    r'^\*?\s*ARTICLE\s+(\d+)[.\s]*[-–—]?\s*(.+?)\.?\s*$',
    re.MULTILINE | re.IGNORECASE
)

DIVISION_PATTERN = re.compile(
    r'^\*?\s*Division\s+(\d+)[.\s]*[-–—]?\s*(.+?)\.?\s*$',
    re.MULTILINE | re.IGNORECASE
)

CHAPTER_PATTERN = re.compile(
    r'^\*?\s*CHAPTER\s+(\d+-\d+)[.\s]*[-–—]?\s*(.+?)\.?\s*$',
    re.MULTILINE | re.IGNORECASE
)

SUBCHAPTER_PATTERN = re.compile(
    r'^\*?\s*Subchapter\s+([A-Z])[.\s]*[-–—]?\s*(.+?)\.?\s*$',
    re.MULTILINE | re.IGNORECASE
)


def find_all_sections(text: str) -> List[Tuple[int, int, str, str, int]]:
    """
    Find all section boundaries in the text.
    
    Returns a list of tuples: (start_pos, line_number, section_id, title, level)
    """
    sections = []
    lines = text.split('\n')
    
    current_pos = 0
    current_chapter = None
    current_article = None
    current_division = None
    current_subchapter = None
    
    for line_num, line in enumerate(lines, 1):
        # Check for chapter
        chapter_match = CHAPTER_PATTERN.match(line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            title = chapter_match.group(2).strip()
            section_id = f"chapter-{current_chapter}"
            sections.append((current_pos, line_num, section_id, title, 1))
            current_pos += len(line) + 1
            continue
        
        # Check for subchapter
        subchapter_match = SUBCHAPTER_PATTERN.match(line)
        if subchapter_match:
            current_subchapter = subchapter_match.group(1)
            title = subchapter_match.group(2).strip()
            parent = f"chapter-{current_chapter}" if current_chapter else None
            section_id = f"subchapter-{current_subchapter}"
            if current_chapter:
                section_id = f"{current_chapter}-{section_id}"
            sections.append((current_pos, line_num, section_id, title, 1))
            current_pos += len(line) + 1
            continue
        
        # Check for article
        article_match = ARTICLE_PATTERN.match(line)
        if article_match:
            current_article = article_match.group(1)
            current_division = None  # Reset division
            title = article_match.group(2).strip()
            section_id = f"article-{current_article}"
            sections.append((current_pos, line_num, section_id, title, 1))
            current_pos += len(line) + 1
            continue
        
        # Check for division
        division_match = DIVISION_PATTERN.match(line)
        if division_match:
            current_division = division_match.group(1)
            title = division_match.group(2).strip()
            section_id = f"division-{current_division}"
            if current_article:
                section_id = f"article-{current_article}-{section_id}"
            sections.append((current_pos, line_num, section_id, title, 1))
            current_pos += len(line) + 1
            continue
        
        # Check for primary sections (non-TOC)
        # Skip lines that start with * (TOC entries)
        if not line.strip().startswith('*'):
            section_match = SECTION_PATTERN.match(line)
            if section_match:
                section_id = section_match.group(1)
                title = section_match.group(2).strip()
                sections.append((current_pos, line_num, section_id, title, 2))
                current_pos += len(line) + 1
                continue
        
        current_pos += len(line) + 1
    
    return sections


def extract_sections_from_toc(text: str) -> dict:
    """
    Extract section metadata from TOC entries.
    
    Returns a dict mapping section_id to title.
    """
    toc_sections = {}
    
    for match in TOC_SECTION_PATTERN.finditer(text):
        section_id = match.group(1)
        title = match.group(2).strip()
        toc_sections[section_id] = title
    
    return toc_sections


def find_section_content_blocks(text: str, toc_sections: dict) -> List[Section]:
    """
    Find content blocks for each section using various heuristics.
    
    The LDC structure often has section content following the TOC,
    so we look for content blocks that match section IDs.
    """
    sections = []
    lines = text.split('\n')
    
    # First pass: find all section headers and their positions
    section_positions = []  # (line_num, section_id, title, level)
    
    current_context = {
        'chapter': None,
        'subchapter': None,
        'article': None,
        'division': None
    }
    
    for line_num, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines and TOC entries (those starting with *)
        if not stripped or stripped.startswith('*'):
            continue
        
        # Check for chapter headers
        if stripped.upper().startswith('CHAPTER'):
            chapter_match = CHAPTER_PATTERN.match(stripped)
            if chapter_match:
                current_context['chapter'] = chapter_match.group(1)
                current_context['subchapter'] = None
                current_context['article'] = None
                current_context['division'] = None
                section_positions.append((
                    line_num,
                    f"chapter-{chapter_match.group(1)}",
                    chapter_match.group(2).strip(),
                    1
                ))
                continue
        
        # Check for subchapter
        subchapter_match = SUBCHAPTER_PATTERN.match(stripped)
        if subchapter_match:
            current_context['subchapter'] = subchapter_match.group(1)
            current_context['article'] = None
            current_context['division'] = None
            section_id = f"subchapter-{subchapter_match.group(1)}"
            if current_context['chapter']:
                section_id = f"{current_context['chapter']}-{section_id}"
            section_positions.append((
                line_num,
                section_id,
                subchapter_match.group(2).strip(),
                1
            ))
            continue
        
        # Check for article
        article_match = ARTICLE_PATTERN.match(stripped)
        if article_match:
            current_context['article'] = article_match.group(1)
            current_context['division'] = None
            section_id = f"article-{article_match.group(1)}"
            section_positions.append((line_num, section_id, article_match.group(2).strip(), 1))
            continue
        
        # Check for division
        division_match = DIVISION_PATTERN.match(stripped)
        if division_match:
            current_context['division'] = division_match.group(1)
            section_id = f"division-{division_match.group(1)}"
            if current_context['article']:
                section_id = f"article-{current_context['article']}-{section_id}"
            section_positions.append((line_num, section_id, division_match.group(2).strip(), 1))
            continue
        
        # Check for section references (§ 25-X-XXX format in content)
        # Look for lines that reference a section ID from the TOC
        for section_id, title in toc_sections.items():
            # Check if this line contains a section reference
            if section_id in stripped and title.upper() in stripped.upper():
                section_positions.append((line_num, section_id, title, 2))
                break
    
    # Second pass: create sections with content
    for i, (line_num, section_id, title, level) in enumerate(section_positions):
        # Determine end line (next section or end of file)
        if i + 1 < len(section_positions):
            end_line = section_positions[i + 1][0] - 1
        else:
            end_line = len(lines) - 1
        
        # Extract content
        content_lines = lines[line_num:end_line + 1]
        content = '\n'.join(content_lines)
        
        # Skip very short sections (likely duplicates or noise)
        if len(content.strip()) < 50:
            continue
        
        # Determine parent
        parent_id = None
        if level == 2:
            # Find the most recent level 1 section
            for j in range(i - 1, -1, -1):
                if section_positions[j][3] == 1:
                    parent_id = section_positions[j][1]
                    break
        
        sections.append(Section(
            id=section_id,
            title=title,
            level=level,
            parent_id=parent_id,
            content=content,
            start_line=line_num + 1,  # 1-indexed
            end_line=end_line + 1,
            subsections=[]
        ))
    
    return sections


def split_by_toc_sections(text: str) -> List[Section]:
    """
    Split document based on TOC section entries.
    
    This approach uses the TOC as the authoritative list of sections
    and finds corresponding content blocks.
    """
    lines = text.split('\n')
    toc_entries = []  # (line_num, section_id, title)
    
    # Find all TOC entries
    for line_num, line in enumerate(lines):
        toc_match = TOC_SECTION_PATTERN.match(line.strip())
        if toc_match:
            section_id = toc_match.group(1)
            title = toc_match.group(2).strip()
            toc_entries.append((line_num, section_id, title))
    
    # Now find content blocks - sections appear after TOC in the document
    # Look for content that mentions each section
    sections = []
    
    # Track where content sections start (after TOC)
    content_start = 0
    in_toc = False
    for line_num, line in enumerate(lines):
        if line.strip().startswith('* §'):
            in_toc = True
        elif in_toc and not line.strip().startswith('*') and line.strip():
            # Found first non-TOC, non-empty line after TOC
            content_start = line_num
            in_toc = False
            break
    
    # Track hierarchical context
    current_chapter = None
    current_article = None
    
    # Create sections by finding content blocks
    for i, (_, section_id, title) in enumerate(toc_entries):
        # Search for this section's content in the document
        # Look for lines containing the section ID
        pattern = re.compile(
            rf'(?:^|\s)(?:§\s*)?{re.escape(section_id)}(?:\s|[-–—]|\.|$)',
            re.IGNORECASE
        )
        
        content_start_line = None
        for line_num in range(content_start, len(lines)):
            if pattern.search(lines[line_num]):
                # Skip if this is a TOC entry
                if lines[line_num].strip().startswith('*'):
                    continue
                content_start_line = line_num
                break
        
        if content_start_line is not None:
            # Find the end of this section (next section or end of file)
            end_line = len(lines) - 1
            
            # Look for next section start
            for next_line in range(content_start_line + 1, len(lines)):
                # Check if this line starts a new section
                for next_id, next_title in [(e[1], e[2]) for e in toc_entries]:
                    if next_id != section_id:
                        next_pattern = re.compile(
                            rf'(?:^|\s)(?:§\s*)?{re.escape(next_id)}(?:\s|[-–—]|\.|$)',
                            re.IGNORECASE
                        )
                        if next_pattern.search(lines[next_line]):
                            if not lines[next_line].strip().startswith('*'):
                                end_line = next_line - 1
                                break
                else:
                    continue
                break
            
            # Extract content
            content_lines = lines[content_start_line:end_line + 1]
            content = '\n'.join(content_lines)
            
            # Determine level and parent
            level = 2
            parent_id = None
            
            # Extract chapter from section ID (e.g., 25-2-xxx -> chapter 25-2)
            id_parts = section_id.split('-')
            if len(id_parts) >= 2:
                current_chapter = f"{id_parts[0]}-{id_parts[1]}"
                parent_id = f"chapter-{current_chapter}"
            
            # Find subsections in content
            subsections = []
            for match in SUBSECTION_LETTER_PATTERN.finditer(content):
                subsections.append(f"{section_id}-{match.group(1)}")
            
            sections.append(Section(
                id=section_id,
                title=title,
                level=level,
                parent_id=parent_id,
                content=content,
                start_line=content_start_line + 1,
                end_line=end_line + 1,
                subsections=subsections
            ))
    
    return sections


def split_document_text(text: str) -> List[Section]:
    """
    Split document text into sections.
    
    This is the main entry point for splitting document text.
    """
    # First, extract TOC section metadata
    toc_sections = extract_sections_from_toc(text)
    
    if toc_sections:
        # Use TOC-based splitting
        return split_by_toc_sections(text)
    else:
        # Fall back to content-based splitting
        return find_section_content_blocks(text, {})


def split_document(input_path: Path) -> List[Section]:
    """
    Split a document file into sections.
    
    Args:
        input_path: Path to the input markdown file
        
    Returns:
        List of Section objects
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    return split_document_text(text)


def write_sections(sections: List[Section], output_dir: Path) -> None:
    """
    Write sections to individual JSON files and create an index.
    
    Args:
        sections: List of Section objects
        output_dir: Directory to write output files
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write individual section files
    for section in sections:
        # Sanitize filename
        filename = section.id.replace('/', '-').replace('\\', '-')
        filepath = output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(section.to_dict(), f, indent=2, ensure_ascii=False)
    
    # Create index file
    index = {
        "total_sections": len(sections),
        "sections": [
            {
                "id": s.id,
                "title": s.title,
                "level": s.level,
                "parent_id": s.parent_id,
                "start_line": s.start_line,
                "end_line": s.end_line,
                "num_subsections": len(s.subsections)
            }
            for s in sections
        ]
    }
    
    index_path = output_dir / "index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Quick test
    sample = """
* § 25-2-775 - TOWNHOUSES.
* § 25-2-776 - CONDOMINIUMS.

Some preamble text.

§ 25-2-775 - TOWNHOUSES.

(A) The minimum lot width is 20 feet.

(B) The minimum lot area is 2,500 square feet.

§ 25-2-776 - CONDOMINIUMS.

(A) The minimum site area is 14,000 square feet.

(B) Maximum building coverage is 50%.
"""
    
    sections = split_document_text(sample)
    for s in sections:
        print(f"Section {s.id}: {s.title}")
        print(f"  Lines: {s.start_line}-{s.end_line}")
        print(f"  Subsections: {s.subsections}")
        print(f"  Content preview: {s.content[:100]}...")
        print()

