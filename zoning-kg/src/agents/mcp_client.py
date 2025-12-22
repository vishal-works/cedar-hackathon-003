"""Neo4j client for graph queries via Bolt driver.

Note: The MCP server (mcp-neo4j-cypher) provides schema and read_cypher tools,
but calling it via subprocess from Python is complex. Since both MCP and this
client connect to the same Neo4j instance, we use the Bolt driver directly
for the Python pipeline, while MCP is used in Cursor chat.
"""

import os
import json
from typing import Any, Optional
from dataclasses import dataclass

from neo4j import GraphDatabase


@dataclass
class MCPResponse:
    """Response from Neo4j query."""
    success: bool
    data: Any
    error: Optional[str] = None


class Neo4jMCPClient:
    """Client for Neo4j queries via Bolt driver.
    
    Uses the same credentials as the MCP server configuration.
    """
    
    def __init__(self):
        self._driver = None
        self._schema_cache: Optional[dict] = None
    
    def _get_driver(self):
        """Get or create Neo4j driver."""
        if self._driver is None:
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = os.getenv("NEO4J_USERNAME", "neo4j")
            password = os.getenv("NEO4J_PASSWORD", "organism_password")
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
        return self._driver
    
    def close(self):
        """Close the driver connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def get_schema(self) -> MCPResponse:
        """Get the graph schema from Neo4j.
        
        Returns node labels, relationship types, and properties.
        """
        if self._schema_cache:
            return MCPResponse(success=True, data=self._schema_cache)
        
        try:
            driver = self._get_driver()
            with driver.session() as session:
                # Get node labels
                labels_result = session.run("CALL db.labels()")
                labels = [r["label"] for r in labels_result]
                
                # Get relationship types
                rel_result = session.run("CALL db.relationshipTypes()")
                rel_types = [r["relationshipType"] for r in rel_result]
                
                # Get relationship semantic names (r.name values)
                rel_names_result = session.run("""
                    MATCH ()-[r]->() 
                    WHERE r.name IS NOT NULL 
                    RETURN DISTINCT r.name AS name 
                    ORDER BY name 
                    LIMIT 100
                """)
                rel_names = [r["name"] for r in rel_names_result]
                
                # Get node properties by label
                props_result = session.run("CALL db.schema.nodeTypeProperties()")
                node_props = {}
                for r in props_result:
                    label = r.get("nodeType", "").replace(":`", "").replace("`", "")
                    prop = r.get("propertyName")
                    if label and prop:
                        if label not in node_props:
                            node_props[label] = []
                        if prop not in node_props[label]:
                            node_props[label].append(prop)
                
                schema = {
                    "node_labels": labels,
                    "relationship_types": rel_types,
                    "relationship_names": rel_names[:50],  # Limit to top 50
                    "node_properties": node_props
                }
                self._schema_cache = schema
                return MCPResponse(success=True, data=schema)
                
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    def read_query(self, cypher: str) -> MCPResponse:
        """Execute a read-only Cypher query.
        
        Args:
            cypher: Cypher query string
            
        Returns:
            MCPResponse with query results
        """
        try:
            driver = self._get_driver()
            with driver.session() as session:
                result = session.run(cypher)
                records = [dict(r) for r in result]
                
                # Convert Neo4j types to JSON-serializable
                def serialize(obj):
                    if hasattr(obj, '__iter__') and not isinstance(obj, (str, dict)):
                        return list(obj)
                    return obj
                
                clean_records = []
                for record in records:
                    clean = {}
                    for k, v in record.items():
                        clean[k] = serialize(v)
                    clean_records.append(clean)
                
                return MCPResponse(
                    success=True,
                    data={
                        "cypher": cypher,
                        "results": clean_records,
                        "count": len(clean_records)
                    }
                )
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    def format_schema_for_prompt(self) -> str:
        """Format schema as a string for LLM prompts."""
        schema_resp = self.get_schema()
        if not schema_resp.success:
            return f"Error fetching schema: {schema_resp.error}"
        
        schema = schema_resp.data
        parts = []
        
        parts.append("## Node Labels")
        parts.append(", ".join(schema.get("node_labels", [])))
        
        parts.append("\n## Relationship Types")
        parts.append(", ".join(schema.get("relationship_types", [])))
        
        parts.append("\n## Semantic Relationship Names (r.name)")
        rel_names = schema.get("relationship_names", [])
        parts.append(", ".join(rel_names[:30]))
        if len(rel_names) > 30:
            parts.append(f"... and {len(rel_names) - 30} more")
        
        parts.append("\n## Node Properties")
        for label, props in schema.get("node_properties", {}).items():
            # Skip embedding properties
            filtered = [p for p in props if "embedding" not in p.lower()]
            if filtered:
                parts.append(f"- {label}: {', '.join(filtered[:10])}")
        
        return "\n".join(parts)
    
    def format_results_for_prompt(self, results: list) -> str:
        """Format query results as a string for LLM prompts."""
        if not results:
            return "No results found."
        
        parts = []
        for i, row in enumerate(results[:30], 1):  # Limit to 30 rows
            row_parts = []
            for k, v in row.items():
                if v is not None and "embedding" not in k.lower():
                    # Truncate long values
                    v_str = str(v)
                    if len(v_str) > 200:
                        v_str = v_str[:200] + "..."
                    row_parts.append(f"{k}: {v_str}")
            parts.append(f"{i}. {', '.join(row_parts)}")
        
        if len(results) > 30:
            parts.append(f"... and {len(results) - 30} more results")
        
        return "\n".join(parts)


# Singleton instance
_mcp_client: Optional[Neo4jMCPClient] = None


def get_mcp_client() -> Neo4jMCPClient:
    """Get or create MCP client singleton."""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = Neo4jMCPClient()
    return _mcp_client
