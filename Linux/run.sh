#!/bin/bash

VENV_DIR="$(cd "$(dirname "$(readlink -f .venv)")" && pwd -P)/$(basename .venv)"

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd -P)"

echo "Running application from $SCRIPT_DIR"
echo "Using virtualenv at $VENV_DIR"

source "$VENV_DIR/bin/activate"

"$VENV_DIR/bin/python3" "$SCRIPT_DIR/app.py"
