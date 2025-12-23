#!/bin/bash
# test-context7-mcp.sh - Test script for Context7Parser MCP integration

echo "Testing Context7Parser MCP Integration"

# Check if MCP adapter is running
echo "Checking if MCP adapter is running on port 8081..."
if curl -s http://localhost:8081/health > /dev/null 2>&1; then
    echo "✓ MCP adapter is running"
else
    echo "✗ MCP adapter is not running"
    echo "Please start the MCP adapter with: cd .mcp && node context7-mcp-adapter.js"
    exit 1
fi

# Check MCP discovery endpoint
echo "Checking MCP discovery endpoint..."
if curl -s http://localhost:8081/.well-known/mcp-server > /dev/null 2>&1; then
    echo "✓ MCP discovery endpoint is accessible"
else
    echo "✗ MCP discovery endpoint is not accessible"
    exit 1
fi

# Test MCP configuration file exists
if [ -f ".mcp/config.yaml" ]; then
    echo "✓ MCP configuration file exists"
else
    echo "✗ MCP configuration file does not exist"
    exit 1
fi

# Check if package.json exists for MCP adapter
if [ -f ".mcp/package.json" ]; then
    echo "✓ MCP adapter package.json exists"
else
    echo "✗ MCP adapter package.json does not exist"
    exit 1
fi

# Check if adapter file exists
if [ -f ".mcp/context7-mcp-adapter.js" ]; then
    echo "✓ MCP adapter implementation exists"
else
    echo "✗ MCP adapter implementation does not exist"
    exit 1
fi

echo ""
echo "Integration Summary:"
echo "- MCP adapter: .mcp/context7-mcp-adapter.js"
echo "- MCP configuration: .mcp/config.yaml"
echo "- MCP package.json: .mcp/package.json"
echo ""
echo "To use the Context7Parser MCP server with Claude Code:"
echo "1. Set CONTEXT7_API_KEY environment variable with your Context7Parser API key"
echo "2. Start the MCP adapter: cd .mcp && node context7-mcp-adapter.js"
echo "3. Claude Code will automatically detect and use the MCP server"
echo ""
echo "✓ All integration components are in place!"