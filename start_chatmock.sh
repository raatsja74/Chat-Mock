#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install -r requirements.txt

AUTH_HOME="${CHATGPT_LOCAL_HOME:-$HOME/.chatgpt-local}"
if [ ! -f "${AUTH_HOME}/auth.json" ]; then
  python chatmock.py login
fi

python chatmock.py serve
