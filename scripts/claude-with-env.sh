#!/bin/bash
# Wrapper script to launch Claude Code with environment variables from .env

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load .env file from parent directory if it exists
ENV_FILE="$SCRIPT_DIR/../.env"
if [ -f "$ENV_FILE" ]; then
    set -a  # automatically export all variables
    source "$ENV_FILE"
    set +a  # stop automatically exporting
    echo "Loaded environment variables from $ENV_FILE"
else
    echo "Warning: .env file not found in $ENV_FILE"
fi

# Launch Claude Code with all passed arguments
claude "$@"
