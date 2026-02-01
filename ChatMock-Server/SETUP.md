# ChatMock Server - Quick Setup Guide

## Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows
- ChatGPT account (paid subscription recommended)

## Installation Steps

### 1. Navigate to Directory

```bash
cd "★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"
```

### 2. Run Setup Script

```bash
./start_chatmock.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Install Playwright browsers
- Create `.env` file from template
- Start the server

### 3. First-Time Browser Login

When the server starts:
1. A browser window will open to ChatGPT
2. **Log in to ChatGPT** in that browser window
3. Keep the browser window open (don't close it)
4. The server will use this session for all requests

### 4. Verify It's Working

Open a new terminal and test:

```bash
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "proxy_active": true,
  "timestamp": "..."
}
```

### 5. Configure Obsidian

See the main [README.md](README.md) for Obsidian Smart Connections setup.

## Alternative: Using OpenAI API

If you have an OpenAI API key and prefer not to use browser automation:

1. Edit `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

2. Restart the server

The server will automatically use the API instead of browser automation.

## Troubleshooting

### "Port already in use"

Change the port in `.env`:
```
CHATMOCK_PORT=8001
```

### "Browser not found"

Install Playwright browsers:
```bash
source .venv/bin/activate
playwright install chromium
```

### "Can't connect to ChatGPT"

- Make sure you're logged into ChatGPT in the browser window
- Check your internet connection
- Try restarting the server

## Running in Background (macOS/Linux)

Use `tmux` or `screen`:

```bash
# Using tmux
tmux new -s chatmock
./start_chatmock.sh
# Press Ctrl+B then D to detach

# Reattach later
tmux attach -t chatmock
```

## Next Steps

- Set up Obsidian Smart Connections (see README.md)
- Configure ngrok for remote access (optional)
- Test the Obsidian-specific endpoints

