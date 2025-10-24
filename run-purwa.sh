#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

VENV_ACTIVATE="$SCRIPT_DIR/venv/bin/activate"
PURWA_CLI_COMMAND="$SCRIPT_DIR/venv/bin/purwa-cli"

source "$VENV_ACTIVATE"

"$PURWA_CLI_COMMAND" "$@"