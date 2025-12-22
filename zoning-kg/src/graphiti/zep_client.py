"""
Zep Cloud client for the ORGAnIZM zoning knowledge graph.

This module provides integration with Zep Cloud for viewing and managing
the knowledge graph through the Zep Playground.

Docs: https://help.getzep.com/
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Zep Cloud configuration
ZEP_API_KEY = os.getenv("ZEP_API_KEY")
ZEP_PROJECT_ID = os.getenv("ZEP_PROJECT_ID")
ZEP_ACCOUNT_ID = os.getenv("ZEP_ACCOUNT_ID")


def get_zep_config():
    """Get Zep Cloud configuration."""
    return {
        "api_key": ZEP_API_KEY,
        "project_id": ZEP_PROJECT_ID,
        "account_id": ZEP_ACCOUNT_ID,
        "project_url": f"https://app.getzep.com/projects/{ZEP_PROJECT_ID}"
    }


def print_zep_info():
    """Print Zep Cloud project information."""
    config = get_zep_config()
    print("=" * 60)
    print("ZEP CLOUD PROJECT INFO")
    print("=" * 60)
    print(f"Project ID:  {config['project_id']}")
    print(f"Account ID:  {config['account_id']}")
    print(f"Project URL: {config['project_url']}")
    print("=" * 60)


if __name__ == "__main__":
    print_zep_info()

