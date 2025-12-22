#!/usr/bin/env python3
"""CLI interface for zoning queries."""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.orchestrator import ZoningQueryPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Query the ORGAnIZM zoning knowledge graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/query_zoning.py "Can I build townhouses in SF-5?"
  python scripts/query_zoning.py "What's the maximum height in MF-4?" --verbose
  python scripts/query_zoning.py "What are parking requirements for multifamily in GR zone?"
        """,
    )
    parser.add_argument("question", help="Natural language zoning question")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show intermediate analysis steps")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON without validation")

    args = parser.parse_args()

    # Create pipeline
    pipeline = ZoningQueryPipeline(verbose=args.verbose)

    # Run query
    if args.raw:
        result = pipeline.query(args.question)
        if result.raw_response:
            import json

            print(json.dumps(result.raw_response, indent=2))
        else:
            print(f"Error: {result.error}")
            sys.exit(1)
    else:
        print(pipeline.query_json(args.question))


if __name__ == "__main__":
    main()

