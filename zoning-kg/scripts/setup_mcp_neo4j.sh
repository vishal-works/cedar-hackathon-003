#!/bin/bash
# Setup Neo4j MCP Server for Graphiti Knowledge Graph

set -e

WORKSPACE_DIR="/Users/vishal-works/Documents/cedar/misc/cedar-hackathon-003"
MCP_DIR="$WORKSPACE_DIR/mcp-neo4j"
SERVER_DIR="$MCP_DIR/servers/mcp-neo4j-cypher"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="organism_password"

echo "========================================"
echo "Neo4j MCP Server Setup (Python)"
echo "========================================"
echo ""

# 1. Clone the repository (already done based on error)
if [ ! -d "$MCP_DIR" ]; then
    echo "1. Cloning mcp-neo4j repository..."
    cd "$WORKSPACE_DIR"
    git clone https://github.com/neo4j-contrib/mcp-neo4j.git
    echo "✅ Repository cloned"
else
    echo "1. Repository already exists"
    echo "✅ Repository found"
fi

echo ""

# 2. Check Python and uv
echo "2. Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv (Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for this session
    export PATH="$HOME/.local/bin:$PATH"
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✅ uv installed"
else
    echo "✅ uv found: $(uv --version)"
fi

# Ensure uv is in PATH
export PATH="$HOME/.local/bin:$PATH"

echo ""

# 3. Install dependencies using uv
echo "3. Installing dependencies..."
cd "$SERVER_DIR"
uv sync
echo "✅ Dependencies installed"

echo ""

# 4. Test Neo4j connection
echo "4. Testing Neo4j connection..."
cd "$WORKSPACE_DIR/zoning-kg"
source venv/bin/activate
python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('$NEO4J_URI', auth=('$NEO4J_USER', '$NEO4J_PASSWORD'))
with driver.session() as s:
    result = s.run('MATCH (n) RETURN count(n) as c').single()
    print(f'✅ Neo4j connected: {result[\"c\"]:,} nodes')
driver.close()
"

echo ""

# 5. Create MCP configuration
MCP_CONFIG_FILE="$HOME/.cursor/mcp.json"

echo "5. Creating MCP configuration..."

# Check if mcp.json exists
if [ -f "$MCP_CONFIG_FILE" ]; then
    echo "⚠️  MCP config already exists at: $MCP_CONFIG_FILE"
    echo ""
    echo "Please manually add this server configuration to your existing config:"
else
    mkdir -p "$(dirname $MCP_CONFIG_FILE)"
    cat > "$MCP_CONFIG_FILE" <<EOF
{
  "mcpServers": {
    "neo4j-zoning-kg": {
      "command": "uv",
      "args": [
        "--directory",
        "$SERVER_DIR",
        "run",
        "mcp-neo4j-cypher"
      ],
      "env": {
        "NEO4J_URI": "$NEO4J_URI",
        "NEO4J_USERNAME": "$NEO4J_USER",
        "NEO4J_PASSWORD": "$NEO4J_PASSWORD"
      }
    }
  }
}
EOF
    echo "✅ MCP config created at: $MCP_CONFIG_FILE"
fi

echo ""
echo "========================================"
echo "MCP Server Configuration"
echo "========================================"
cat <<EOF

Add this to your MCP client config:

{
  "mcpServers": {
    "neo4j-zoning-kg": {
      "command": "uv",
      "args": [
        "--directory",
        "$SERVER_DIR",
        "run",
        "mcp-neo4j-cypher"
      ],
      "env": {
        "NEO4J_URI": "$NEO4J_URI",
        "NEO4J_USERNAME": "$NEO4J_USER",
        "NEO4J_PASSWORD": "$NEO4J_PASSWORD"
      }
    }
  }
}

For Claude Desktop, the config file is at:
- macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
- Windows: %APPDATA%/Claude/claude_desktop_config.json

For Cursor, the config file is at:
- ~/.cursor/mcp.json

EOF

echo ""
echo "========================================"
echo "Test the Server"
echo "========================================"
echo ""
echo "You can test the server directly:"
echo ""
echo "cd $SERVER_DIR"
echo "uv run mcp-neo4j-cypher"
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Restart Cursor or Claude Desktop"
echo "2. The MCP server will provide these tools:"
echo "   - query: Execute Cypher queries"
echo "   - schema: Get database schema"
echo ""
echo "Example queries to try:"
echo "- 'Show me all zones in Austin'"
echo "- 'What are the constraints for townhouses?'"
echo "- 'List all state overrides from SB-840'"
echo "- 'Find orphan nodes in the graph'"
echo ""
echo "Server directory: $SERVER_DIR"
echo "Neo4j URI: $NEO4J_URI"
echo ""
