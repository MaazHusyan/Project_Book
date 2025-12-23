# Context7Parser MCP Integration

This directory contains the MCP (Model Context Protocol) server integration for Context7Parser, which enables Claude Code to interact with the Context7Parser service for repository analysis and AI context generation.

## Overview

The Context7Parser MCP server allows Claude Code to:
- Parse code repositories and websites into structured AI context
- Monitor parsing project status
- Refresh existing projects
- Search through parsed context using vector search

## Components

### 1. MCP Configuration
- **File**: `config.yaml`
- **Purpose**: Defines the Context7Parser MCP server capabilities and configuration
- **Features**:
  - Repository parsing capability
  - Project status monitoring
  - Project refresh functionality
  - Vector search capability

### 2. MCP Adapter
- **File**: `context7-mcp-adapter.js`
- **Purpose**: Node.js Express server that acts as an MCP adapter
- **Features**:
  - Translates MCP requests to Context7Parser API calls
  - Handles authentication with Context7Parser API
  - Provides MCP discovery endpoint
  - Implements health checks

### 3. Package Configuration
- **File**: `package.json`
- **Purpose**: Defines dependencies for the MCP adapter
- **Dependencies**: express, axios, cors

## Setup and Usage

### Prerequisites
- Node.js 18+ installed
- Context7Parser API key

### Installation
1. Navigate to the MCP directory:
   ```bash
   cd sample-and-tests/context7-mcp/.mcp
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Configuration
Set the required environment variables:
```bash
export CONTEXT7_API_KEY="your-context7-api-key"
export CONTEXT7_API_URL="https://api.context7.com"  # Optional, defaults to this
```

### Running the MCP Server
Start the MCP adapter:
```bash
npm start
# or
node context7-mcp-adapter.js
```

The server will start on port 8081 by default.

### MCP Discovery
The MCP server provides a discovery endpoint at:
```
http://localhost:8081/.well-known/mcp-server
```

## MCP Capabilities

### 1. Parse Repository
- **Endpoint**: `POST /mcp/context7-parser/parse_repository`
- **Purpose**: Submit a repository or website for parsing
- **Parameters**:
  - `url`: Repository or website URL
  - `type`: "repository" or "website"
  - `options`: Parsing options (optional)

### 2. Get Project Status
- **Endpoint**: `POST /mcp/context7-parser/get_project_status`
- **Purpose**: Check the status of a parsing project
- **Parameters**:
  - `projectId`: Unique identifier for the project

### 3. Refresh Project
- **Endpoint**: `POST /mcp/context7-parser/refresh_project`
- **Purpose**: Refresh an existing project by re-parsing
- **Parameters**:
  - `projectId`: Unique identifier for the project
  - `forceRebuild`: Whether to force a complete rebuild

### 4. Search Context
- **Endpoint**: `POST /mcp/context7-parser/search_context`
- **Purpose**: Search through parsed project context
- **Parameters**:
  - `projectId`: Unique identifier for the project
  - `query`: Search query for semantic code search
  - `limit`: Maximum number of results (default: 10)

## Integration with Claude Code

Once the MCP server is running, Claude Code will automatically detect and use the Context7Parser capabilities if they are configured in your MCP settings.

## Security

- The MCP server requires a valid Context7Parser API key
- All requests to the Context7Parser API are authenticated
- Rate limiting is configured in the MCP configuration

## Testing

To verify the MCP server is running:
```bash
curl http://localhost:8081/health
```

To check MCP discovery:
```bash
curl http://localhost:8081/.well-known/mcp-server
```

## Troubleshooting

- Ensure the `CONTEXT7_API_KEY` environment variable is set
- Verify the Context7Parser API is accessible
- Check that the MCP server is running on the correct port
- Review logs for any error messages