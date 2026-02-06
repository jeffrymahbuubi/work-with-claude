#!/bin/bash
# Wrapper script to launch Copilot CLI with project-specific XDG_CONFIG_HOME

# Get the project root directory (parent of scripts/)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Update XDG_CONFIG_HOME in ~/.bashrc
if grep -q 'export XDG_CONFIG_HOME=' ~/.bashrc; then
    # Replace existing line
    sed -i "s|^export XDG_CONFIG_HOME=.*|export XDG_CONFIG_HOME=\"$PROJECT_DIR\"|" ~/.bashrc
    echo "Updated XDG_CONFIG_HOME in ~/.bashrc to: $PROJECT_DIR"
else
    # Add new line
    echo "export XDG_CONFIG_HOME=\"$PROJECT_DIR\"" >> ~/.bashrc
    echo "Added XDG_CONFIG_HOME to ~/.bashrc: $PROJECT_DIR"
fi

# Export for current session
export XDG_CONFIG_HOME="$PROJECT_DIR"

# Load .env file from project root if it exists
ENV_FILE="$PROJECT_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    set -a  # automatically export all variables
    source "$ENV_FILE"
    set +a  # stop automatically exporting
    echo "Loaded environment variables from $ENV_FILE"
fi

# Launch Copilot CLI
copilot "$@"
