#!/usr/bin/env python3
"""
Split LDC markdown into sections.

Usage:
    python scripts/01_split_sections.py --input data/raw/ldc.md
    python scripts/01_split_sections.py --input data/raw/ldc.md --output data/processed/sections
"""
import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessing.section_splitter import split_document, write_sections


def main():
    parser = argparse.ArgumentParser(
        description="Split LDC markdown into sections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/01_split_sections.py --input data/raw/ldc.md
    python scripts/01_split_sections.py --input ../TX/source_documents/ldc.md --output data/processed/sections
        """
    )
    parser.add_argument(
        "--input", "-i",
        default="data/raw/ldc.md",
        help="Input LDC markdown file (default: data/raw/ldc.md)"
    )
    parser.add_argument(
        "--output", "-o",
        default="data/processed/sections",
        help="Output directory for sections (default: data/processed/sections)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print verbose output"
    )
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output)
    
    # Validate input
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    print(f"Reading input file: {input_path}")
    
    # Split document
    sections = split_document(input_path)
    
    print(f"Split into {len(sections)} sections")
    
    if args.verbose:
        print("\nSections found:")
        for s in sections[:20]:  # Show first 20
            print(f"  {s.id}: {s.title[:50]}..." if len(s.title) > 50 else f"  {s.id}: {s.title}")
        if len(sections) > 20:
            print(f"  ... and {len(sections) - 20} more")
    
    # Write sections
    write_sections(sections, output_dir)
    
    print(f"\nWritten to: {output_dir}")
    print(f"  - {len(sections)} section files")
    print(f"  - 1 index file (index.json)")


if __name__ == "__main__":
    main()

