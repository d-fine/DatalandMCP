# Dataland MCP Server

This directory contains a Model Context Protocol (MCP) server that provides tools for interacting with Dataland APIs.

## Running with Docker

The MCP server is containerized for easy deployment.

### Starting the Docker Container

From the repository root directory:

1. **Start the MCP server with Swagger UI:**
   ```bash
   docker compose up
   ```

2. **Build and start:**
   ```bash
   docker compose up --build
   ```

3. **Run in the background:**
   ```bash
   docker compose up -d
   ```

### Accessing the Service

- **Swagger UI**: Available at `http://localhost:8000/DatalandMCP/docs`

### Container Behavior

The container will automatically:
1. Generate the latest Dataland API clients
2. Install Python dependencies
3. Start the MCP server with Swagger UI on port 8000

### Stopping the Container

```bash
docker compose down
```

### Alternative: Direct Docker Commands

If you prefer to use Docker directly instead of `docker compose`:

```bash
# Build the image
docker build -t dataland-mcp ./mcp_server

# Run the container
docker run -p 8000:8000 --name dataland-mcp-server dataland-mcp
```