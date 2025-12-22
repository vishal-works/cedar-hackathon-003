# Neo4j MCP Server Setup for Graphiti Knowledge Graph

This guide helps you set up the Model Context Protocol (MCP) server for your Neo4j knowledge graph, enabling natural language queries through Claude Desktop or Cursor.

## Quick Setup

Run the automated setup script:

```bash
cd /Users/vishal-works/Documents/cedar/misc/cedar-hackathon-003/zoning-kg
chmod +x scripts/setup_mcp_neo4j.sh
./scripts/setup_mcp_neo4j.sh
```

This will:
1. Clone the `mcp-neo4j` repository
2. Install dependencies
3. Build the MCP server
4. Test Neo4j connection
5. Configure MCP for Cursor/Claude Desktop

---

## Manual Setup (if script fails)

### 1. Clone Repository

```bash
cd ~/Documents/cedar/misc/cedar-hackathon-003
git clone https://github.com/neo4j-contrib/mcp-neo4j.git
```

### 2. Install & Build

```bash
cd mcp-neo4j/servers/mcp-neo4j-cypher
npm install
npm run build
```

### 3. Configure MCP

Create or update `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "neo4j-zoning-kg": {
      "command": "node",
      "args": [
        "/Users/vishal-works/Documents/cedar/misc/cedar-hackathon-003/mcp-neo4j/servers/mcp-neo4j-cypher/dist/index.js"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "organism_password"
      }
    }
  }
}
```

### 4. Restart Cursor/Claude Desktop

After saving the configuration, restart your MCP client.

---

## Using the MCP Server

Once configured, you can query your knowledge graph using natural language:

### Example Queries

**Basic Queries:**
- "Show me all zones in Austin"
- "List all use types"
- "What are the jurisdictions in the graph?"

**Complex Queries:**
- "What are the constraints for townhouses in SF-5 zone?"
- "Show me all state overrides from SB-840"
- "Find rules that apply in multiple zones"
- "List orphan nodes in the graph"

**Analysis Queries:**
- "How many relationships does each zone have?"
- "What are the most common edge types?"
- "Find duplicate entity names"

### Available MCP Tools

The server provides these tools:

1. **`query`** - Execute Cypher queries directly
   - Natural language queries are converted to Cypher automatically
   
2. **`schema`** - Get database schema information
   - Node labels, relationship types, property keys

---

## Example MCP Interactions

### Query All Zones
```
User: "Show me all zones that allow townhouses"

MCP converts to:
MATCH (z:Zone)-[r:RELATES_TO]->(u:UseType)
WHERE r.name = 'ALLOWS_USE' AND u.name CONTAINS 'Townhouse'
RETURN z.name, z.code, z.family
```

### Get State Overrides
```
User: "What are the SB-840 overrides?"

MCP converts to:
MATCH (o:Override)
WHERE o.bill_id = 'SB-840'
RETURN o.name, o.metric, o.override_value, o.unit, o.summary
```

### Find Orphan Nodes
```
User: "Show me orphan nodes"

MCP converts to:
MATCH (n)
WHERE NOT (n)-[:RELATES_TO]-() AND NOT (n)<-[:RELATES_TO]-()
  AND NOT n:Episodic
RETURN labels(n) as type, n.name as name
```

---

## Troubleshooting

### Connection Issues

**Check Neo4j is running:**
```bash
docker ps | grep neo4j
```

**Test connection manually:**
```bash
cd zoning-kg
source venv/bin/activate
python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'organism_password'))
with driver.session() as s:
    print(s.run('MATCH (n) RETURN count(n) as c').single()['c'])
driver.close()
"
```

### MCP Server Not Loading

1. Check Cursor/Claude Desktop logs
2. Verify the path in `mcp.json` is correct
3. Ensure Node.js is installed: `node --version`
4. Rebuild the server: `cd mcp-neo4j/servers/mcp-neo4j-cypher && npm run build`

### Permission Issues

If the script fails with permission errors:
```bash
chmod +x scripts/setup_mcp_neo4j.sh
```

---

## Advanced Configuration

### Custom Neo4j Instance

If using a different Neo4j instance, update the environment variables:

```json
{
  "mcpServers": {
    "neo4j-zoning-kg": {
      "command": "node",
      "args": ["path/to/index.js"],
      "env": {
        "NEO4J_URI": "bolt://your-host:7687",
        "NEO4J_USERNAME": "your-username",
        "NEO4J_PASSWORD": "your-password"
      }
    }
  }
}
```

### Multiple Databases

You can configure multiple MCP servers for different databases:

```json
{
  "mcpServers": {
    "neo4j-zoning-kg": { ... },
    "neo4j-production": { ... },
    "neo4j-dev": { ... }
  }
}
```

---

## Resources

- **MCP Neo4j Repository**: https://github.com/neo4j-contrib/mcp-neo4j
- **Model Context Protocol**: https://modelcontextprotocol.io
- **Neo4j Cypher Documentation**: https://neo4j.com/docs/cypher-manual/
- **Knowledge Graph Documentation**: See `zoning_kg.md` for complete graph schema

---

## Graph Statistics

Current knowledge graph (as of last export):
- **Nodes**: 1,211
- **Relationships**: 9,772
- **Episodes**: 306
- **Entity Types**: 10 (Jurisdiction, Zone, UseType, Rule, Constraint, Condition, Override, DocumentSource, Entity, Episodic)
- **Edge Types**: 1,196 unique semantic edges

See `zoning_kg.md` for complete documentation.


