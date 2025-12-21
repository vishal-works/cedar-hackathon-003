"""
Section splitter for Austin Land Development Code (LDC).

The LDC has a specific structure:
1. Preamble (metadata, council members, copyright)
2. TOC blocks (lines starting with `*` listing sections)
3. Content blocks (actual regulations with ### headers)

This splitter extracts the content blocks while using TOC for section metadata.
"""
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Set


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


# Patterns for content structure markers
MARKDOWN_HEADER_PATTERN = re.compile(r'^(#{1,4})\s+(.+)$')

# Article/Division/Chapter headers in content (with ### prefix)
ARTICLE_HEADER = re.compile(r'^#{1,4}\s*ARTICLE\s+(\d+)[.\s]*[-–—]?\s*(.*)$', re.IGNORECASE)
DIVISION_HEADER = re.compile(r'^#{1,4}\s*Division\s+(\d+)[.\s]*[-–—]?\s*(.*)$', re.IGNORECASE)
CHAPTER_HEADER = re.compile(r'^#{1,4}\s*CHAPTER\s+([\d-]+)[.\s]*[-–—]?\s*(.*)$', re.IGNORECASE)
SUBCHAPTER_HEADER = re.compile(r'^#{1,4}\s*(?:Subchapter|SUBCHAPTER)\s+([A-Z])[.\s]*[-–—]?\s*(.*)$')

# Source citation marks end of section content
SOURCE_PATTERN = re.compile(r'^Source:', re.IGNORECASE)

# TOC pattern for extracting section metadata
TOC_SECTION_PATTERN = re.compile(r'^\*\s*§\s*([\d-]+[A-Z]?)\s*[-–—]\s*(.+?)\.?\s*$')

# Subsection patterns
SUBSECTION_PATTERN = re.compile(r'^\(([A-Z])\)$')


def extract_toc_metadata(lines: List[str]) -> Dict[str, str]:
    """
    Extract section ID to title mapping from TOC entries.
    
    Returns:
        Dict mapping section_id to title
    """
    toc = {}
    for line in lines:
        match = TOC_SECTION_PATTERN.match(line.strip())
        if match:
            section_id = match.group(1)
            title = match.group(2).strip().rstrip('.')
            if section_id not in toc:
                toc[section_id] = title
    return toc


def find_content_boundaries(lines: List[str]) -> List[Tuple[int, str, str, int]]:
    """
    Find all content section boundaries.
    
    Returns list of (start_line, section_id, title, level):
    - start_line: 0-indexed line number
    - section_id: Extracted ID or generated hierarchical ID
    - title: Section title
    - level: 1=chapter/article, 2=section
    """
    boundaries = []
    current_chapter = None
    current_article = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip TOC lines
        if stripped.startswith('*'):
            continue
        
        # Chapter header
        chapter_match = CHAPTER_HEADER.match(stripped)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            current_article = None
            title = chapter_match.group(2).strip().rstrip('.')
            boundaries.append((i, f"chapter-{current_chapter}", title or f"Chapter {current_chapter}", 1))
            continue
        
        # Article header
        article_match = ARTICLE_HEADER.match(stripped)
        if article_match:
            current_article = article_match.group(1)
            title = article_match.group(2).strip().rstrip('.')
            article_id = f"article-{current_article}"
            if current_chapter:
                article_id = f"{current_chapter}-{article_id}"
            boundaries.append((i, article_id, title or f"Article {current_article}", 1))
            continue
        
        # Division header
        division_match = DIVISION_HEADER.match(stripped)
        if division_match:
            div_num = division_match.group(1)
            title = division_match.group(2).strip().rstrip('.')
            div_id = f"division-{div_num}"
            boundaries.append((i, div_id, title or f"Division {div_num}", 1))
            continue
        
        # Subchapter header
        subchapter_match = SUBCHAPTER_HEADER.match(stripped)
        if subchapter_match:
            sub_letter = subchapter_match.group(1)
            title = subchapter_match.group(2).strip().rstrip('.')
            sub_id = f"subchapter-{sub_letter}"
            if current_chapter:
                sub_id = f"{current_chapter}-{sub_id}"
            boundaries.append((i, sub_id, title or f"Subchapter {sub_letter}", 1))
            continue
    
    return boundaries


def find_section_references_in_content(lines: List[str], toc: Dict[str, str]) -> List[Tuple[int, str, str]]:
    """
    Find lines that explicitly reference section IDs from the TOC.
    
    These help identify where section content is being discussed.
    Returns list of (line_num, section_id, context)
    """
    refs = []
    section_id_pattern = re.compile(r'(?:Section\s+|§\s*)([\d]+-[\d]+-[\d]+[A-Z]?)')
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('*'):
            continue
        
        for match in section_id_pattern.finditer(stripped):
            section_id = match.group(1)
            if section_id in toc:
                refs.append((i, section_id, stripped[:50]))
    
    return refs


def split_by_source_citations(lines: List[str]) -> List[Tuple[int, int]]:
    """
    Find content blocks delimited by 'Source:' citations.
    
    Each 'Source:' line marks the end of a section's content.
    Returns list of (start_line, end_line) for content blocks.
    """
    blocks = []
    content_start = None
    in_toc = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track TOC regions
        if stripped.startswith('*'):
            if content_start is not None and not in_toc:
                # End of content block before TOC
                blocks.append((content_start, i - 1))
                content_start = None
            in_toc = True
            continue
        
        if in_toc and stripped and not stripped.startswith('*'):
            in_toc = False
        
        if in_toc:
            continue
        
        # Start of content
        if content_start is None and stripped:
            content_start = i
        
        # Source citation ends a section
        if SOURCE_PATTERN.match(stripped):
            if content_start is not None:
                blocks.append((content_start, i))
                content_start = None
    
    # Handle final block
    if content_start is not None:
        blocks.append((content_start, len(lines) - 1))
    
    return blocks


def extract_section_id_from_content(lines: List[str], start: int, end: int, toc: Dict[str, str]) -> Optional[str]:
    """
    Try to extract a section ID from a content block.
    
    Looks for section references at the beginning of the block.
    """
    section_pattern = re.compile(r'(?:Section\s+|§\s*)([\d]+-[\d]+-[\d]+[A-Z]?)')
    
    # Look in first 5 lines of the block
    for i in range(start, min(start + 5, end + 1)):
        line = lines[i].strip()
        match = section_pattern.search(line)
        if match:
            section_id = match.group(1)
            if section_id in toc:
                return section_id
    
    return None


def split_document_text(text: str) -> List[Section]:
    """
    Split document text into sections.
    
    Strategy:
    1. Extract TOC for section ID -> title mapping
    2. Find content blocks using Source: citations and headers
    3. Assign section IDs based on references in content
    """
    lines = text.split('\n')
    
    # Get TOC metadata
    toc = extract_toc_metadata(lines)
    print(f"  Found {len(toc)} section IDs in TOC")
    
    # Find structural boundaries (chapters, articles, etc.)
    structure_bounds = find_content_boundaries(lines)
    print(f"  Found {len(structure_bounds)} structural boundaries")
    
    # Find content blocks by Source: citations
    source_blocks = split_by_source_citations(lines)
    print(f"  Found {len(source_blocks)} content blocks (by Source: markers)")
    
    sections = []
    processed_ids: Set[str] = set()
    
    # Process structural boundaries
    for i, (line_num, section_id, title, level) in enumerate(structure_bounds):
        if section_id in processed_ids:
            continue
        
        # Find end (next structural boundary or end of file)
        if i + 1 < len(structure_bounds):
            end_line = structure_bounds[i + 1][0] - 1
        else:
            end_line = len(lines) - 1
        
        # Extract content
        content_lines = lines[line_num:end_line + 1]
        content = '\n'.join(content_lines)
        
        # Skip tiny sections
        if len(content.strip()) < 50:
            continue
        
        # Find subsections
        subsections = []
        for match in SUBSECTION_PATTERN.finditer(content):
            subsections.append(f"{section_id}-{match.group(1)}")
        
        sections.append(Section(
            id=section_id,
            title=title,
            level=level,
            parent_id=None,
            content=content,
            start_line=line_num + 1,
            end_line=end_line + 1,
            subsections=subsections
        ))
        processed_ids.add(section_id)
    
    # Process source-delimited blocks and assign to TOC sections
    for start, end in source_blocks:
        section_id = extract_section_id_from_content(lines, start, end, toc)
        
        if section_id and section_id not in processed_ids:
            title = toc.get(section_id, "Unknown")
            content_lines = lines[start:end + 1]
            content = '\n'.join(content_lines)
            
            if len(content.strip()) < 50:
                continue
            
            # Determine parent from section ID
            id_parts = section_id.split('-')
            parent_id = f"chapter-{id_parts[0]}-{id_parts[1]}" if len(id_parts) >= 2 else None
            
            # Find subsections
            subsections = []
            for match in SUBSECTION_PATTERN.finditer(content):
                subsections.append(f"{section_id}-{match.group(1)}")
            
            sections.append(Section(
                id=section_id,
                title=title,
                level=2,
                parent_id=parent_id,
                content=content,
                start_line=start + 1,
                end_line=end + 1,
                subsections=subsections
            ))
            processed_ids.add(section_id)
    
    # For remaining TOC sections, try to find their content by searching
    remaining = set(toc.keys()) - processed_ids
    print(f"  Searching for {len(remaining)} remaining sections...")
    
    for section_id in remaining:
        title = toc[section_id]
        
        # Search for this section ID in content
        pattern = re.compile(rf'(?:Section\s+|§\s*){re.escape(section_id)}\b')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('*'):
                continue
            
            if pattern.search(line):
                # Found a reference - extract surrounding content
                # Find the content block this is in
                block_start = i
                block_end = i
                
                # Look backward for start (previous Source: or structural header)
                for j in range(i - 1, max(0, i - 100), -1):
                    if SOURCE_PATTERN.match(lines[j].strip()):
                        block_start = j + 1
                        break
                    if ARTICLE_HEADER.match(lines[j].strip()) or CHAPTER_HEADER.match(lines[j].strip()):
                        block_start = j
                        break
                
                # Look forward for end (next Source:)
                for j in range(i + 1, min(len(lines), i + 200)):
                    if SOURCE_PATTERN.match(lines[j].strip()):
                        block_end = j
                        break
                    if lines[j].strip().startswith('*'):
                        block_end = j - 1
                        break
                
                content_lines = lines[block_start:block_end + 1]
                content = '\n'.join(content_lines)
                
                if len(content.strip()) >= 50 and section_id not in processed_ids:
                    id_parts = section_id.split('-')
                    parent_id = f"chapter-{id_parts[0]}-{id_parts[1]}" if len(id_parts) >= 2 else None
                    
                    sections.append(Section(
                        id=section_id,
                        title=title,
                        level=2,
                        parent_id=parent_id,
                        content=content,
                        start_line=block_start + 1,
                        end_line=block_end + 1,
                        subsections=[]
                    ))
                    processed_ids.add(section_id)
                    break
    
    # Sort by start line
    sections.sort(key=lambda s: s.start_line)
    
    print(f"  Total sections extracted: {len(sections)}")
    print(f"  TOC sections found: {len(processed_ids)} / {len(toc)}")
    
    return sections


def split_document(input_path: Path) -> List[Section]:
    """
    Split a document file into sections.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    return split_document_text(text)


def write_sections(sections: List[Section], output_dir: Path) -> None:
    """
    Write sections to individual JSON files and create an index.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Keep the section with most content for each ID
    unique_sections: Dict[str, Section] = {}
    for section in sections:
        if section.id in unique_sections:
            if len(section.content) > len(unique_sections[section.id].content):
                unique_sections[section.id] = section
        else:
            unique_sections[section.id] = section
    
    # Write section files
    for section in unique_sections.values():
        filename = section.id.replace('/', '-').replace('\\', '-')
        filepath = output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(section.to_dict(), f, indent=2, ensure_ascii=False)
    
    # Create index
    index = {
        "total_sections": len(sections),
        "unique_sections": len(unique_sections),
        "sections": [
            {
                "id": s.id,
                "title": s.title,
                "level": s.level,
                "parent_id": s.parent_id,
                "start_line": s.start_line,
                "end_line": s.end_line,
                "content_length": len(s.content),
                "num_subsections": len(s.subsections)
            }
            for s in sorted(unique_sections.values(), key=lambda x: x.start_line)
        ]
    }
    
    with open(output_dir / "index.json", 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"Wrote {len(unique_sections)} unique section files")


if __name__ == "__main__":
    sample = """
* § 25-2-775 - TOWNHOUSES.
* § 25-2-776 - CONDOMINIUMS.

### ARTICLE 1. - RESIDENTIAL.

Section 25-2-775 - TOWNHOUSES.

(A) The minimum lot width is 20 feet.

Source: Ord. 123.

Section 25-2-776 - CONDOMINIUMS.

(A) The minimum site area is 14,000 square feet.

Source: Ord. 456.
"""
    sections = split_document_text(sample)
    for s in sections:
        print(f"Section {s.id}: {s.title}")
        print(f"  Content: {s.content[:80]}...")
