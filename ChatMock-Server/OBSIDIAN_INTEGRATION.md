# Obsidian Integration Guide

This guide shows how to integrate ChatMock Server with Obsidian for AI-powered note management.

## Overview

ChatMock Server provides an OpenAI-compatible API that works seamlessly with Obsidian's Smart Connections plugin and other AI tools. It's specifically optimized for Obsidian workflows with built-in endpoints for:

- Note summarization
- Automatic tagging
- Wikilink suggestions
- Q&A over your notes

## Quick Setup

### 1. Start ChatMock Server

```bash
cd "★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"
./start_chatmock.sh
```

The server will start on `http://localhost:8000`

### 2. Configure Smart Connections

1. **Install Smart Connections Plugin**
   - Open Obsidian Settings → Community Plugins
   - Search for "Smart Connections"
   - Install and enable

2. **Configure API Connection**
   - Settings → Smart Connections → **Model Provider**
   - Select: `Custom Local (OpenAI format)`
   
3. **Enter Connection Details**
   ```
   Protocol: http
   Host: localhost
   Port: 8000
   Path: /v1/chat/completions
   API Key: chatmock-local (any non-empty string)
   ```

4. **Set Model Parameters**
   - Model: `gpt-5` (or `gpt-5-turbo`, `gpt-4`)
   - Max tokens: `3000-4000`
   - Temperature: `0.7`

5. **Test Connection**
   - Click "Send sample request"
   - You should see a response from ChatGPT

### 3. Use Smart Connections

Once configured, you can:

- **Smart Chat**: Command Palette → "Smart Connections: Smart Chat"
- **Note Suggestions**: Smart Connections will suggest related notes
- **Context Links**: AI-generated connections between notes

## Obsidian-Specific Endpoints

ChatMock includes special endpoints optimized for Obsidian workflows.

### Summarize Notes

Use this to automatically summarize notes:

```python
import requests

response = requests.post(
    "http://localhost:8000/obsidian/summarize",
    json={
        "content": "# My Note\n\nLong note content...",
        "path": "Projects/MyProject.md"
    }
)

summary = response.json()["summary"]
```

### Generate Tags

Automatically generate relevant tags:

```python
response = requests.post(
    "http://localhost:8000/obsidian/tag",
    json={
        "content": "Your note content here..."
    }
)

tags = response.json()["tags"]
# Returns: #tag1 #tag2 #tag3
```

### Suggest Wikilinks

Get AI-suggested wikilinks for your notes:

```python
response = requests.post(
    "http://localhost:8000/obsidian/link",
    json={
        "content": "Your note content...",
        "vault_path": "/path/to/your/vault"
    }
)

links = response.json()["suggested_links"]
# Returns: [[Note 1]] [[Note 2]] [[Note 3]]
```

## Use Cases from ChatMock.md

Based on your [[ChatMock.md]] document, here are the high-value use cases:

### 1. Automatic Note Summarization & Tagging

**Setup**: Create an Obsidian plugin or use Templater to call ChatMock when notes are created/modified.

**Workflow**:
1. New note created in Obsidian
2. Trigger automation (plugin, shortcut, etc.)
3. Send note content to `/obsidian/summarize`
4. Update note with summary and tags

**Value**: Saves time, improves note discoverability

### 2. Meeting & Project Briefs

**Workflow**:
1. Paste meeting transcript or project doc into Obsidian
2. Use Smart Chat: "Extract action items, key decisions, and deadlines from this note"
3. AI generates structured brief
4. Save as new note or append to existing

**Value**: Quick extraction of actionable information

### 3. Refine & Reformat Snippets

**Workflow**:
1. Clip web content or research snippets
2. Use Smart Chat to clean formatting
3. Convert to your preferred template (Zettelkasten, daily log, etc.)
4. Apply suggested tags and links

**Value**: Consistent note formatting, better organization

### 4. Q&A Over Notes

**Workflow**:
1. Use Smart Chat in Obsidian
2. Ask questions about your notes: "What did I learn about project management last month?"
3. Smart Connections searches your vault and provides answers

**Value**: Quick information retrieval, knowledge synthesis

## Advanced: Custom Frames Integration

Embed ChatMock directly in Obsidian:

1. **Install Custom Frames Plugin**
   - Settings → Community Plugins → Browse
   - Search "Custom Frames"
   - Install and enable

2. **Add ChatMock Frame**
   - Settings → Custom Frames → Add new frame
   - Name: `ChatMock`
   - URL: `http://localhost:8000`
   - Icon: Choose chat icon
   - Display: `Right sidebar` or `Center pane`

3. **Access**
   - Use ribbon icon or Command Palette
   - ChatMock opens in Obsidian sidebar
   - Full ChatGPT interface within Obsidian

## Automation Ideas

### Templater Template

Create a template that auto-summarizes notes:

```javascript
<%*
// Get current note content
const content = tp.file.content;

// Call ChatMock API
const response = await fetch('http://localhost:8000/obsidian/summarize', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        content: content,
        path: tp.file.path
    })
});

const data = await response.json();
-%>
## Summary
<%- data.summary %>

## Tags
<%- data.tags %>
```

### Dataview Query

Query notes that need summarization:

```dataview
LIST
FROM ""
WHERE !summary
SORT file.mtime DESC
LIMIT 10
```

### Make.com / n8n Automation

1. Watch Obsidian vault folder for new files
2. Read note content
3. Call ChatMock `/obsidian/summarize` endpoint
4. Update note with summary and tags
5. Schedule: Run every hour or on file change

## Troubleshooting

### Smart Connections Not Connecting

1. **Verify server is running**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check Smart Connections settings**
   - Path must be exactly: `/v1/chat/completions`
   - Protocol: `http` (not `https`)
   - Host: `localhost` (not `127.0.0.1`)

3. **Test with curl**
   ```bash
   curl http://localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt-4","messages":[{"role":"user","content":"test"}]}'
   ```

### Slow Responses

- ChatGPT web interface can be slower than API
- Consider using OpenAI API key instead (see README.md)
- Increase timeout in Smart Connections settings

### Browser Window Issues

- Keep the browser window open (don't close it)
- If it closes, restart ChatMock server
- Check that you're logged into ChatGPT

## Next Steps

1. ✅ Set up Smart Connections
2. ✅ Test with a few notes
3. ✅ Create automation workflows
4. ✅ Set up ngrok for remote access (optional)
5. ✅ Explore advanced use cases from [[ChatMock.md]]

## Related Documents

- [[ChatMock.md]] - Original strategy guide
- [[ChatMock Connection.md]] - Connection reference
- `README.md` - Full server documentation
- `SETUP.md` - Installation guide

