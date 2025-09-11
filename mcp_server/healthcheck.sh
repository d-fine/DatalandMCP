#!/bin/bash

success=0

# Check if DatalandMCP is running on port 8001
curl -f http://localhost:8001/health || success=1

# Check if MCPO DatalandMCP is running on port 8000
curl -f http://localhost:8000/DatalandMCP/docs || success=1

exit $success