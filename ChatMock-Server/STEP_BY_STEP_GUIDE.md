# ChatMock Server - Complete Step-by-Step Guide

This guide will walk you through setting up ChatMock from scratch and connecting it to Obsidian.

## Prerequisites Checklist

Before starting, make sure you have:
- [ ] Python 3.8 or higher installed
- [ ] A ChatGPT account with a paid subscription (for GPT-5 access)
- [ ] Obsidian installed
- [ ] Terminal/command line access

---

## Part 1: Install ChatMock Server

### Step 1: Navigate to ChatMock Directory

Open Terminal and run:

```bash
cd "/Users/jadenraats/Library/Mobile Documents/com~apple~CloudDocs/★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"
```

**Tip**: If you get an error about the path, you can also:
1. Open Finder
2. Navigate to: `★ Main Vault` → `♛ Ops Hub` → `Systems` → `ChatMock-Server`
3. Right-click the folder → "Services" → "New Terminal at Folder"

### Step 2: Run the Setup Script

```bash
./start_chatmock.sh
```

**What this does:**
- Creates a Python virtual environment (`.venv`)
- Installs all required packages
- Installs Playwright browsers
- Creates a `.env` configuration file
- Starts the server

**First time only**: The script will take a few minutes to download dependencies.

### Step 3: Wait for Browser Window

When the server starts, a browser window will automatically open to ChatGPT.

**IMPORTANT**: 
- **Log in to ChatGPT** in this browser window
- **Keep the browser window open** (don't close it)
- The server uses this session to communicate with ChatGPT

### Step 4: Verify Server is Running

Open a **new terminal window** (keep the server running in the first one) and test:

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

**✅ Success!** Your ChatMock server is running.

---

## Part 2: Connect to Obsidian Copilot

### Step 5: Install Copilot Plugin

1. Open Obsidian
2. Go to **Settings** (gear icon in bottom left)
3. Click **Community Plugins**
4. Click **Browse** (if not already there)
5. Search for: `Copilot`
6. Click **Install** on the "Copilot" plugin by Logan Yang
7. Click **Enable** after installation

### Step 6: Configure Copilot with ChatMock

1. In Obsidian Settings, go to **Copilot** → **Settings**
2. Click the **"Model"** tab
3. Click **"Add Custom Model"** button
4. Fill in the form:

   ```
   Model Name: ChatMock GPT-5
   Provider: 3rd party (OpenAI format)
   Base URL: http://localhost:8000/v1
   Model Name: gpt-5
   API Key: chatmock-local
   ```

5. Click **"Add Model"**
6. Select **"ChatMock GPT-5"** from the model dropdown at the top

### Step 7: Test Copilot

1. Press `Cmd+P` (or `Ctrl+P` on Windows/Linux) to open Command Palette
2. Type: `Copilot: Open Chat`
3. Press Enter
4. Type a test message like: "Hello, can you hear me?"
5. You should get a response from ChatGPT via ChatMock!

**✅ Success!** Copilot is now connected to ChatMock.

---

## Part 3: Connect to Obsidian Smart Connections (Optional)

Smart Connections provides additional features like note linking and context awareness.

### Step 8: Install Smart Connections Plugin

1. In Obsidian Settings → **Community Plugins** → **Browse**
2. Search for: `Smart Connections`
3. Click **Install** and **Enable**

### Step 9: Configure Smart Connections

1. In Obsidian Settings, go to **Smart Connections** → **Settings**
2. Find **"Model Provider"** section
3. Select: **"Custom Local (OpenAI format)"**

4. Fill in the connection details:
   ```
   Protocol: http
   Host: localhost
   Port: 8000
   Path: /v1/chat/completions
   API Key: chatmock-local
   ```

5. Set model parameters:
   - **Model**: `gpt-5`
   - **Max tokens**: `4000`
   - **Temperature**: `0.7`

6. Click **"Send sample request"** to test
   - You should see a response appear
   - If you see an error, check troubleshooting below

**✅ Success!** Smart Connections is now connected.

---

## Part 4: Using ChatMock

### Using Copilot

**Quick Chat:**
1. `Cmd+P` → `Copilot: Open Chat`
2. Type your question
3. Get AI responses powered by GPT-5

**From a Note:**
1. Select text in any note
2. `Cmd+P` → `Copilot: Chat with Selection`
3. Ask questions about the selected text

### Using Smart Connections

**Smart Chat:**
1. `Cmd+P` → `Smart Connections: Smart Chat`
2. Ask questions about your entire vault
3. Get context-aware answers

**Note Suggestions:**
- Smart Connections automatically suggests related notes
- Look for the Smart Connections icon in your notes

### Using Obsidian-Specific Endpoints

You can also use ChatMock's special endpoints for note processing:

**Summarize a Note:**
```bash
curl -X POST http://localhost:8000/obsidian/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# My Note\n\nLong content here...",
    "path": "Projects/MyProject.md"
  }'
```

**Generate Tags:**
```bash
curl -X POST http://localhost:8000/obsidian/tag \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your note content here..."
  }'
```

---

## Part 5: Running ChatMock in Background

### Option 1: Using tmux (Recommended)

1. Install tmux (if not already installed):
   ```bash
   brew install tmux  # macOS
   ```

2. Start a tmux session:
   ```bash
   tmux new -s chatmock
   ```

3. Navigate and start ChatMock:
   ```bash
   cd "/Users/jadenraats/Library/Mobile Documents/com~apple~CloudDocs/★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"
   ./start_chatmock.sh
   ```

4. Detach from tmux (server keeps running):
   - Press `Ctrl+B`, then `D`

5. Reattach later:
   ```bash
   tmux attach -t chatmock
   ```

### Option 2: Keep Terminal Open

Simply keep the terminal window with ChatMock running open. You can minimize it.

---

## Troubleshooting

### Problem: "Port 8000 already in use"

**Solution:**
1. Find what's using the port:
   ```bash
   lsof -ti:8000
   ```
2. Kill the process:
   ```bash
   lsof -ti:8000 | xargs kill
   ```
3. Or change the port in `.env`:
   ```
   CHATMOCK_PORT=8001
   ```

### Problem: Browser window closes or won't open

**Solution:**
1. Make sure Playwright browsers are installed:
   ```bash
   cd "/Users/jadenraats/Library/Mobile Documents/com~apple~CloudDocs/★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"
   source .venv/bin/activate
   playwright install chromium
   ```
2. Restart ChatMock server

### Problem: Copilot/Smart Connections can't connect

**Solution:**
1. Verify server is running:
   ```bash
   curl http://localhost:8000/health
   ```
2. Check the Base URL in Copilot settings:
   - Must be: `http://localhost:8000/v1` (with `/v1`)
   - NOT: `http://localhost:8000/v1/chat/completions`
3. Check the Path in Smart Connections:
   - Must be: `/v1/chat/completions`
4. Make sure you're logged into ChatGPT in the browser window

### Problem: "GPT-5 not available" or wrong model

**Solution:**
1. Check what models are available:
   ```bash
   curl http://localhost:8000/v1/models
   ```
2. If GPT-5 isn't in your ChatGPT account, use `gpt-4` instead:
   - In Copilot: Change model name to `gpt-4`
   - In Smart Connections: Change model to `gpt-4`

### Problem: Slow responses

**Solution:**
- Browser automation is slower than direct API
- Consider using OpenAI API key instead (see README.md)
- Be patient - first response may take 10-30 seconds

### Problem: Server stops working after closing terminal

**Solution:**
- Use tmux (see Part 5 above)
- Or keep the terminal window open
- Or create a launch script that runs in background

---

## Quick Reference

### Start ChatMock
```bash
cd "/Users/jadenraats/Library/Mobile Documents/com~apple~CloudDocs/★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"
./start_chatmock.sh
```

### Check if Running
```bash
curl http://localhost:8000/health
```

### Stop ChatMock
- Press `Ctrl+C` in the terminal running ChatMock
- Or close the terminal (if not using tmux)

### Test API
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5","messages":[{"role":"user","content":"Hello!"}]}'
```

### Copilot Settings
- Model: `ChatMock GPT-5`
- Base URL: `http://localhost:8000/v1`
- Model Name: `gpt-5`
- API Key: `chatmock-local`

### Smart Connections Settings
- Protocol: `http`
- Host: `localhost`
- Port: `8000`
- Path: `/v1/chat/completions`
- API Key: `chatmock-local`
- Model: `gpt-5`

---

## Next Steps

Once everything is working:

1. ✅ **Explore Copilot features** - Try different chat modes
2. ✅ **Use Smart Connections** - Let it build your note graph
3. ✅ **Set up automations** - Use ChatMock with Make.com, n8n, or Shortcuts
4. ✅ **Remote access** - Set up ngrok for access from other devices (optional)

## Getting Help

- Check `README.md` for full documentation
- Check `COPILOT_SETUP.md` for Copilot-specific help
- Check `OBSIDIAN_INTEGRATION.md` for Smart Connections help
- Review server logs in the terminal for error messages

---

**You're all set!** ChatMock is now running and connected to Obsidian. 🎉

