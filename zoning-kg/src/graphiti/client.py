"""
Graphiti client initialization and configuration.
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def get_graphiti_client():
    """
    Initialize and return a Graphiti client connected to Neo4j.
    
    Requires environment variables:
    - NEO4J_URI: e.g., "bolt://localhost:7687"
    - NEO4J_USER: e.g., "neo4j"
    - NEO4J_PASSWORD: your password
    - OPENAI_API_KEY: for LLM extraction
    
    Returns:
        Graphiti: Configured Graphiti client instance
    """
    # Import here to avoid issues if graphiti-core not installed
    from graphiti_core import Graphiti
    
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    
    if not neo4j_password:
        raise ValueError("NEO4J_PASSWORD environment variable is required")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required for Graphiti")
    
    client = Graphiti(
        uri=neo4j_uri,
        user=neo4j_user,
        password=neo4j_password
    )
    
    return client


async def initialize_graph(client) -> None:
    """
    Initialize the graph with required indexes and constraints.
    
    Args:
        client: Graphiti client instance
    """
    await client.build_indices_and_constraints()
    print("Graph indices and constraints initialized.")


def check_neo4j_connection() -> bool:
    """
    Test if Neo4j is accessible.
    
    Returns:
        bool: True if connection successful
    """
    try:
        from neo4j import GraphDatabase
        
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.single()
        driver.close()
        return True
    except Exception as e:
        print(f"Neo4j connection error: {e}")
        return False

