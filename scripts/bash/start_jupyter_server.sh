#!/bin/bash
# Start Jupyter Server for MCP integration
# This runs JupyterLab with collaboration enabled for jupyter-mcp-server

# Change to your project directory
cd /path/to/your/project

# Activate virtual environment (if using one)
# source .venv/bin/activate

# Start JupyterLab with collaboration features enabled
# Token must match the one in your MCP configuration
jupyter lab --port 8888 \
  --IdentityProvider.token=my_secure_token_123 \
  --ServerApp.allow_origin='*' \
  --ServerApp.allow_remote_access=true \
  --ip=0.0.0.0 \
  --no-browser \
  --LabApp.collaborative=true
