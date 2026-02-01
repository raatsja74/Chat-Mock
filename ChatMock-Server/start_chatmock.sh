#!/bin/bash
# ChatMock Server Startup Script

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting ChatMock Server...${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Install Playwright browsers if needed
if ! command -v playwright &> /dev/null || [ ! -d "$HOME/.cache/ms-playwright" ]; then
    echo -e "${YELLOW}Installing Playwright browsers...${NC}"
    playwright install chromium
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}.env file not found. Creating from .env.example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}Please edit .env file with your settings before running again.${NC}"
    fi
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start the server
echo -e "${GREEN}Starting ChatMock server on port ${CHATMOCK_PORT:-8000}...${NC}"
echo -e "${GREEN}Access the API at: http://localhost:${CHATMOCK_PORT:-8000}${NC}"
echo -e "${GREEN}API endpoint: http://localhost:${CHATMOCK_PORT:-8000}/v1/chat/completions${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

python3 chatmock_server.py

