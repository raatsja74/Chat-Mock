---
aliases:
  - ChatMock
---
# ChatMock Server - Obsidian-Optimized

A local server that exposes an OpenAI-compatible API endpoint, forwarding requests to ChatGPT. Customized for Obsidian integration with Smart Connections and other AI-powered workflows.

## Features

- ✅ **OpenAI-compatible API** - Works with Obsidian Smart Connections, Raycast, and other tools
- ✅ **ChatGPT Integration** - Uses browser automation or OpenAI API to access ChatGPT
- ✅ **Obsidian-Specific Endpoints** - Built-in endpoints for note summarization, tagging, and linking
- ✅ **No API Key Required** - Uses your ChatGPT subscription via browser automation
- ✅ **Local & Private** - Runs entirely on your machine
- ✅ **Easy Setup** - One-command startup script

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to the ChatMock-Server directory
cd "★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"

# Run the startup script (it will create venv and install dependencies)
./start_chatmock.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configure

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

Edit `.env`:
- `CHATMOCK_PORT` - Port to run server on (default: 8000)
- `OBSIDIAN_VAULT_PATH` - Path to your Obsidian vault (optional, for enhanced features)
- `CHATMOCK_BROWSER` - Browser to use (chromium, firefox, webkit)

### 3. Start the Server

```bash
./start_chatmock.sh
```

Or manually:

```bash
source .venv/bin/activate
python3 chatmock_server.py
```

The server will start on `http://localhost:8000`

### 4. First-Time Setup (Browser Mode)

If using browser automation (default):
1. A browser window will open to ChatGPT
2. **Log in to ChatGPT manually** in the browser window
3. Once logged in, the server will use that session

## Obsidian Integration

### Smart Connections Setup

1. Open Obsidian → Settings → Smart Connections
2. Go to **Model Provider** → Select `Custom Local (OpenAI format)`
3. Configure:
   - **Protocol:** `http`
   - **Host:** `localhost`
   - **Port:** `8000`
   - **Path:** `/v1/chat/completions`
   - **API Key:** `chatmock-local` (any non-empty string)
4. Set **Max tokens** to 3000-4000
5. Test with "Send sample request"

### Custom Frames (Embedded Chat)

1. Install **Custom Frames** plugin in Obsidian
2. Add a new frame:
   - Name: `ChatMock`
   - URL: `http://localhost:8000`
   - Icon: Choose a chat icon
3. Access via ribbon icon or command palette

## API Endpoints

### Standard OpenAI-Compatible Endpoints

- `GET /` - Health check and info
- `GET /health` - Server health status
- `GET /v1/models` - List available models
- `POST /v1/chat/completions` - Chat completions (main endpoint)

### Obsidian-Specific Endpoints

- `POST /obsidian/summarize` - Summarize a note
  ```json
  {
    "content": "Note content here...",
    "path": "path/to/note.md"
  }
  ```

- `POST /obsidian/tag` - Generate tags for a note
  ```json
  {
    "content": "Note content here..."
  }
  ```

- `POST /obsidian/link` - Suggest wikilinks for a note
  ```json
  {
    "content": "Note content here...",
    "vault_path": "/path/to/vault"
  }
  ```

## Usage Examples

### Using cURL

```bash
# Test the API
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5",
    "messages": [
      {"role": "user", "content": "Summarize this note about project management"}
    ]
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "gpt-5",
        "messages": [
            {"role": "user", "content": "What are the key points?"}
        ]
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### Obsidian Summarization

```python
import requests

response = requests.post(
    "http://localhost:8000/obsidian/summarize",
    json={
        "content": "# My Note\n\nThis is a long note with lots of content...",
        "path": "Projects/MyProject.md"
    }
)

print(response.json()["summary"])
```

## Remote Access (ngrok)

To access ChatMock from other devices or tools:

```bash
# Install ngrok (if not already installed)
# brew install ngrok  # macOS
# or download from https://ngrok.com

# Start tunnel
ngrok http 8000

# Use the ngrok URL in your Obsidian/other tool configurations
# Example: https://abc123.ngrok.io/v1/chat/completions
```

For authenticated access:

```bash
ngrok http 8000 --oauth=google
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHATMOCK_PORT` | Server port | `8000` |
| `CHATMOCK_HOST` | Server host | `0.0.0.0` |
| `CHATMOCK_BROWSER` | Browser type | `chromium` |
| `CHATMOCK_MODEL` | Default model | `gpt-5` |
| `CHATMOCK_MAX_TOKENS` | Max tokens | `4000` |
| `OBSIDIAN_VAULT_PATH` | Vault path | (empty) |
| `OPENAI_API_KEY` | Use API instead of browser | (empty) |

### Using OpenAI API (Alternative)

If you have an OpenAI API key, you can use it instead of browser automation:

1. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

2. The server will automatically use the API instead of browser automation

## Troubleshooting

### Browser doesn't open

- Check that Playwright browsers are installed: `playwright install chromium`
- Try running with `headless=False` in the code (default)

### Authentication issues

- Make sure you're logged into ChatGPT in the browser window
- Check that the browser window stays open (don't close it)
- Try restarting the server

### Port already in use

- Change `CHATMOCK_PORT` in `.env` to a different port (e.g., 8001)
- Or stop the process using port 8000: `lsof -ti:8000 | xargs kill`

### Obsidian Smart Connections not connecting

- Verify server is running: `curl http://localhost:8000/health`
- Check the path is exactly `/v1/chat/completions`
- Try the "Send sample request" button in Smart Connections settings
- Check Obsidian console for errors (Cmd+Option+I)

## Architecture

```
┌─────────────────┐
│   Obsidian      │
│ Smart Connections│
└────────┬────────┘
         │
         │ HTTP POST /v1/chat/completions
         ▼
┌─────────────────┐
│  ChatMock Server │
│  (FastAPI)       │
└────────┬────────┘
         │
         │ Browser Automation or API
         ▼
┌─────────────────┐
│    ChatGPT      │
│  (Web/API)      │
└─────────────────┘
```

## Development

### Project Structure

```
ChatMock-Server/
├── chatmock_server.py      # Main FastAPI server
├── chatmock_chatgpt.py     # ChatGPT browser automation
├── requirements.txt        # Python dependencies
├── start_chatmock.sh      # Startup script
├── .env.example           # Configuration template
└── README.md              # This file
```

### Running in Development

```bash
# With auto-reload
uvicorn chatmock_server:app --reload --port 8000
```

## License

This is a custom implementation for personal use. ChatGPT is a product of OpenAI.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Obsidian Smart Connections documentation
3. Check server logs for error messages

## Roadmap

- [ ] Streaming responses support
- [ ] Conversation history management
- [ ] Multiple model support
- [ ] Rate limiting
- [ ] Authentication/authorization
- [ ] Obsidian plugin integration
- [ ] Better error handling and retries

