# ChatMock + Obsidian Copilot Setup

Yes! You can use ChatMock with the **Copilot** plugin for Obsidian. Copilot supports custom OpenAI-compatible APIs.

## Quick Setup

### 1. Start ChatMock Server

```bash
cd "★ Main Vault/♛ Ops Hub/Systems/ChatMock-Server"
./start_chatmock.sh
```

Server will run on `http://localhost:8000`

### 2. Configure Copilot Plugin

1. **Open Copilot Settings**
   - Obsidian Settings → Community Plugins → Copilot → Settings
   - Or use Command Palette: "Copilot: Open Settings"

2. **Add Custom Model**
   - Go to the **"Model"** tab
   - Click **"Add Custom Model"**

3. **Fill in the Form**
   ```
   Model Name: ChatMock GPT-5
   Provider: 3rd party (OpenAI format)
   Base URL: http://localhost:8000/v1
   Model Name: gpt-5
   API Key: chatmock-local (any non-empty string)
   ```

4. **Save**
   - Click **"Add Model"**
   - Select your new "ChatMock GPT-5" model from the model dropdown

### 3. Test It

1. Open Copilot chat (Command Palette → "Copilot: Open Chat")
2. Send a test message
3. You should see responses from ChatGPT via ChatMock!

## Configuration Details

| Setting | Value |
|---------|-------|
| **Provider** | `3rd party (OpenAI format)` |
| **Base URL** | `http://localhost:8000/v1` |
| **Model Name** | `gpt-5` (or `gpt-5-turbo`, `gpt-4`, `gpt-4-turbo`) |
| **API Key** | `chatmock-local` (ChatMock ignores this, but Copilot requires it) |

## Remote Access (ngrok)

If you want to use ChatMock from other devices:

1. **Start ngrok tunnel**
   ```bash
   ngrok http 8000
   ```

2. **Use ngrok URL in Copilot**
   ```
   Base URL: https://your-ngrok-url.ngrok.io/v1
   ```

## Benefits of Using Copilot with ChatMock

✅ **No API Key Required** - Uses your ChatGPT subscription  
✅ **Full ChatGPT Features** - Access to GPT-5, GPT-5 Turbo, GPT-4, etc.  
✅ **Obsidian Integration** - Chat directly in Obsidian  
✅ **Cost Effective** - No per-token charges  
✅ **Privacy** - Runs locally on your machine  

## Troubleshooting

### Copilot Can't Connect

1. **Verify ChatMock is running**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check Base URL**
   - Must be: `http://localhost:8000/v1` (with `/v1` suffix)
   - Not: `http://localhost:8000/v1/chat/completions`

3. **Check Model Name**
   - Must match what ChatMock returns in `/v1/models`
   - Try: `gpt-5`, `gpt-5-turbo`, `gpt-4`, or `gpt-4-turbo`

### Slow Responses

- ChatGPT web interface can be slower than direct API
- Consider using OpenAI API key in ChatMock (see README.md)
- Increase timeout in Copilot settings if available

### Browser Window Issues

- Keep the ChatMock browser window open
- Make sure you're logged into ChatGPT in that window
- Restart ChatMock if browser closes

## Comparison: Copilot vs Smart Connections

| Feature | Copilot | Smart Connections |
|---------|---------|-------------------|
| **Chat Interface** | ✅ Built-in chat UI | ✅ Smart Chat command |
| **Note Context** | ✅ Can reference notes | ✅ Full vault context |
| **Embeddings** | ❌ | ✅ Builds embeddings |
| **Note Suggestions** | ❌ | ✅ AI-suggested links |
| **Custom Endpoints** | ✅ | ✅ |

**Recommendation**: Use both!
- **Copilot** for quick AI chat and assistance
- **Smart Connections** for note linking and context-aware features

## Next Steps

1. ✅ Set up Copilot with ChatMock
2. ✅ Test with a few queries
3. ✅ Try Smart Connections too (see OBSIDIAN_INTEGRATION.md)
4. ✅ Explore Copilot's other features (note generation, etc.)

## Related Docs

- `README.md` - Full ChatMock documentation
- `OBSIDIAN_INTEGRATION.md` - Smart Connections setup
- `SETUP.md` - Installation guide

