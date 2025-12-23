#!/usr/bin/env node
// context7-mcp-adapter.js
// MCP Adapter for Context7Parser integration

import express from 'express';
import axios from 'axios';
import cors from 'cors';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Configuration
const PORT = process.env.PORT || 8081;
const CONTEXT7_API_URL = process.env.CONTEXT7_API_URL || 'https://api.context7.com';
const CONTEXT7_API_KEY = process.env.CONTEXT7_API_KEY;

// Validate required environment variables
if (!CONTEXT7_API_KEY) {
  console.error('ERROR: CONTEXT7_API_KEY environment variable is required');
  process.exit(1);
}

// MCP Protocol Handler
class Context7MCPHandler {
  constructor() {
    this.apiClient = axios.create({
      baseURL: CONTEXT7_API_URL,
      timeout: 60000,
      headers: {
        'Authorization': `Bearer ${CONTEXT7_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
  }

  // Parse repository endpoint - maps to context7-parser/parse_repository capability
  async parseRepository(req, res) {
    try {
      const { url, type, options } = req.body;

      if (!url || !type) {
        return res.status(400).json({
          success: false,
          error: 'URL and type are required',
          code: 'MISSING_PARAMETERS'
        });
      }

      console.log(`Parsing ${type}: ${url}`);

      const response = await this.apiClient.post('/api/parse', {
        url,
        type,
        options: options || {}
      });

      res.json(response.data);
    } catch (error) {
      console.error('Parse repository error:', error.message);
      res.status(500).json({
        success: false,
        error: error.response?.data?.error || error.message,
        code: error.response?.data?.code || 'PARSE_ERROR'
      });
    }
  }

  // Get project status endpoint - maps to context7-parser/get_project_status capability
  async getProjectStatus(req, res) {
    try {
      const { projectId } = req.body;

      if (!projectId) {
        return res.status(400).json({
          success: false,
          error: 'projectId is required',
          code: 'MISSING_PROJECT_ID'
        });
      }

      console.log(`Getting status for project: ${projectId}`);

      const response = await this.apiClient.get(`/api/project/${projectId}`);

      res.json(response.data);
    } catch (error) {
      console.error('Get project status error:', error.message);
      res.status(500).json({
        success: false,
        error: error.response?.data?.error || error.message,
        code: error.response?.data?.code || 'STATUS_ERROR'
      });
    }
  }

  // Refresh project endpoint - maps to context7-parser/refresh_project capability
  async refreshProject(req, res) {
    try {
      const { projectId, forceRebuild } = req.body;

      if (!projectId) {
        return res.status(400).json({
          success: false,
          error: 'projectId is required',
          code: 'MISSING_PROJECT_ID'
        });
      }

      console.log(`Refreshing project: ${projectId}, forceRebuild: ${forceRebuild}`);

      const response = await this.apiClient.post('/api/refresh', {
        projectId,
        forceRebuild: forceRebuild || false
      });

      res.json(response.data);
    } catch (error) {
      console.error('Refresh project error:', error.message);
      res.status(500).json({
        success: false,
        error: error.response?.data?.error || error.message,
        code: error.response?.data?.code || 'REFRESH_ERROR'
      });
    }
  }

  // Search context endpoint - maps to context7-parser/search_context capability
  async searchContext(req, res) {
    try {
      const { projectId, query, limit } = req.body;

      if (!projectId || !query) {
        return res.status(400).json({
          success: false,
          error: 'projectId and query are required',
          code: 'MISSING_PARAMETERS'
        });
      }

      console.log(`Searching context for project: ${projectId}, query: ${query}`);

      const searchUrl = `/api/search?projectId=${encodeURIComponent(projectId)}&query=${encodeURIComponent(query)}&limit=${limit || 10}`;
      const response = await this.apiClient.get(searchUrl);

      res.json(response.data);
    } catch (error) {
      console.error('Search context error:', error.message);
      res.status(500).json({
        success: false,
        error: error.response?.data?.error || error.message,
        code: error.response?.data?.code || 'SEARCH_ERROR'
      });
    }
  }
}

// Initialize handler
const handler = new Context7MCPHandler();

// MCP-compatible endpoints
app.post('/mcp/context7-parser/parse_repository', (req, res) => {
  handler.parseRepository(req, res);
});

app.post('/mcp/context7-parser/get_project_status', (req, res) => {
  handler.getProjectStatus(req, res);
});

app.post('/mcp/context7-parser/refresh_project', (req, res) => {
  handler.refreshProject(req, res);
});

app.post('/mcp/context7-parser/search_context', (req, res) => {
  handler.searchContext(req, res);
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'context7-mcp-adapter',
    timestamp: new Date().toISOString()
  });
});

// MCP Discovery endpoint (standard for MCP servers)
app.get('/.well-known/mcp-server', (req, res) => {
  res.json({
    name: 'context7-parser',
    version: '1.0.0',
    capabilities: [
      {
        name: 'parse_repository',
        description: 'Parse a code repository or website into structured AI context',
        input_schema: {
          type: 'object',
          required: ['url', 'type'],
          properties: {
            url: { type: 'string', description: 'URL of the repository or website to parse' },
            type: { type: 'string', enum: ['repository', 'website'], description: 'Type of content to parse' },
            options: { type: 'object', description: 'Parsing options' }
          }
        }
      },
      {
        name: 'get_project_status',
        description: 'Get the status of a parsing project',
        input_schema: {
          type: 'object',
          required: ['projectId'],
          properties: {
            projectId: { type: 'string', description: 'Unique identifier for the project' }
          }
        }
      },
      {
        name: 'refresh_project',
        description: 'Refresh an existing project by re-parsing',
        input_schema: {
          type: 'object',
          required: ['projectId'],
          properties: {
            projectId: { type: 'string', description: 'Unique identifier for the project' },
            forceRebuild: { type: 'boolean', description: 'Force a complete rebuild' }
          }
        }
      },
      {
        name: 'search_context',
        description: 'Search through parsed project context using vector search',
        input_schema: {
          type: 'object',
          required: ['projectId', 'query'],
          properties: {
            projectId: { type: 'string', description: 'Unique identifier for the project' },
            query: { type: 'string', description: 'Search query for semantic code search' },
            limit: { type: 'integer', description: 'Maximum number of results to return' }
          }
        }
      }
    ]
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Context7 MCP Adapter running on port ${PORT}`);
  console.log(`MCP Discovery endpoint available at: http://localhost:${PORT}/.well-known/mcp-server`);
  console.log(`Health check available at: http://localhost:${PORT}/health`);
});

export default app;