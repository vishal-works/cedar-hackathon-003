#!/usr/bin/env python3
"""
Run NER on split sections.

Usage:
    python scripts/02_run_ner.py
    python scripts/02_run_ner.py --section 25-2-775
    python scripts/02_run_ner.py --input data/processed/sections --output data/processed/tagged
"""
import argparse
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessing.ner_pipeline import (
    create_ner_pipeline,
    process_sections_directory,
    process_section_file,
    write_tagged_section,
    get_entity_summary
)


def main():
    parser = argparse.ArgumentParser(
        description="Run NER on split sections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/02_run_ner.py
    python scripts/02_run_ner.py --section 25-2-775
    python scripts/02_run_ner.py --verbose
        """
    )
    parser.add_argument(
        "--input", "-i",
        default="data/processed/sections",
        help="Input sections directory (default: data/processed/sections)"
    )
    parser.add_argument(
        "--output", "-o",
        default="data/processed/tagged",
        help="Output directory for tagged sections (default: data/processed/tagged)"
    )
    parser.add_argument(
        "--section", "-s",
        help="Process a single section by ID (for testing)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print verbose output including entity details"
    )
    parser.add_argument(
        "--summary", 
        action="store_true",
        help="Print entity summary after processing"
    )
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    # Validate input
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        print("Run 01_split_sections.py first to create sections.")
        sys.exit(1)
    
    print("Creating NER pipeline...")
    nlp = create_ner_pipeline()
    print("  Pipeline loaded successfully")
    
    if args.section:
        # Process single section
        section_file = input_dir / f"{args.section}.json"
        
        if not section_file.exists():
            print(f"Error: Section file not found: {section_file}")
            sys.exit(1)
        
        print(f"\nProcessing section: {args.section}")
        tagged = process_section_file(nlp, section_file)
        
        # Write output
        output_path = output_dir / f"{args.section}.json"
        write_tagged_section(tagged, output_path)
        
        print(f"Found {len(tagged.entities)} entities")
        
        if args.verbose:
            print("\nEntities:")
            for ent in tagged.entities:
                print(f"  {ent.label}: {ent.text!r} -> {ent.normalized}")
        
        print(f"\nOutput written to: {output_path}")
    else:
        # Process all sections
        print(f"\nProcessing all sections in: {input_dir}")
        
        tagged_sections = process_sections_directory(
            nlp, input_dir, output_dir
        )
        
        total_entities = sum(len(s.entities) for s in tagged_sections)
        print(f"\nProcessed {len(tagged_sections)} sections")
        print(f"Total entities found: {total_entities}")
        print(f"Output written to: {output_dir}")
        
        if args.summary or args.verbose:
            summary = get_entity_summary(tagged_sections)
            print("\nEntity Summary:")
            print(f"  Total sections: {summary['total_sections']}")
            print(f"  Total entities: {summary['total_entities']}")
            print("\n  Entities by label:")
            for label, count in sorted(summary['entities_by_label'].items()):
                print(f"    {label}: {count}")
            
            if args.verbose:
                print("\n  Unique values by label:")
                for label, values in sorted(summary['unique_values'].items()):
                    print(f"    {label} ({len(values)} unique):")
                    for val in values[:10]:  # Show first 10
                        print(f"      - {val}")
                    if len(values) > 10:
                        print(f"      ... and {len(values) - 10} more")
            
            # Write summary
            summary_path = output_dir / "summary.json"
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            print(f"\nSummary written to: {summary_path}")


if __name__ == "__main__":
    main()

