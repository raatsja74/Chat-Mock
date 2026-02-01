#!/usr/bin/env python3
"""
ChatMock Server - OpenAI-compatible API proxy for ChatGPT
Customized for Obsidian integration

This server exposes an OpenAI-compatible API endpoint that forwards requests
to ChatGPT via browser automation, allowing Obsidian Smart Connections and
other tools to use ChatGPT without an API key.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ChatMock Server",
    description="OpenAI-compatible API proxy for ChatGPT (Obsidian-optimized)",
    version="1.0.0"
)

# CORS middleware for Obsidian and other local tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
CONFIG = {
    "port": int(os.getenv("CHATMOCK_PORT", "8000")),
    "host": os.getenv("CHATMOCK_HOST", "0.0.0.0"),
    "browser": os.getenv("CHATMOCK_BROWSER", "chrome"),
    "model": os.getenv("CHATMOCK_MODEL", "gpt-5"),
    "max_tokens": int(os.getenv("CHATMOCK_MAX_TOKENS", "4000")),
    "obsidian_vault_path": os.getenv("OBSIDIAN_VAULT_PATH", ""),
}

# Request/Response Models
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = Field(default="gpt-5", description="Model name")
    messages: List[Message] = Field(..., description="Conversation messages")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    stream: Optional[bool] = Field(default=False, description="Stream responses")
    tools: Optional[List[Dict[str, Any]]] = Field(default=None, description="Tool definitions")
    tool_choice: Optional[str] = Field(default=None, description="Tool choice strategy")

class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str = "openai"

# Import ChatGPT browser automation
try:
    from chatmock_chatgpt import ChatGPTBrowser, ChatGPTAPI
    CHATGPT_MODULE_AVAILABLE = True
except ImportError:
    logger.warning("chatmock_chatgpt module not available. Using mock implementation.")
    CHATGPT_MODULE_AVAILABLE = False

# ChatGPT Browser Automation
class ChatGPTProxy:
    """Handles communication with ChatGPT via browser automation"""
    
    def __init__(self, browser: str = "chromium", use_api: bool = False, api_key: Optional[str] = None):
        self.browser_type = browser
        self.use_api = use_api
        self.api_key = api_key
        self.session_active = False
        self.chatgpt_browser: Optional[ChatGPTBrowser] = None
        self.chatgpt_api: Optional[ChatGPTAPI] = None
        
    async def initialize(self):
        """Initialize browser session or API client"""
        if self.use_api and self.api_key:
            logger.info("Initializing ChatGPT API client")
            if CHATGPT_MODULE_AVAILABLE:
                self.chatgpt_api = ChatGPTAPI(api_key=self.api_key)
            self.session_active = True
        else:
            logger.info(f"Initializing ChatGPT proxy with {self.browser_type} browser")
            if CHATGPT_MODULE_AVAILABLE:
                self.chatgpt_browser = ChatGPTBrowser(
                    browser_type=self.browser_type,
                    headless=False  # Keep visible for manual login
                )
                await self.chatgpt_browser.initialize()
            self.session_active = True
        
    async def chat_completion(
        self,
        messages: List[Message],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send messages to ChatGPT and get completion
        """
        # Convert messages to format needed by ChatGPT
        conversation_text = self._messages_to_text(messages)
        
        # Obsidian-specific processing
        if CONFIG["obsidian_vault_path"]:
            conversation_text = self._enhance_for_obsidian(conversation_text)
        
        try:
            if self.use_api and self.chatgpt_api:
                # Use OpenAI API
                api_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
                response_data = await self.chatgpt_api.send_message(
                    messages=api_messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Convert to OpenAI-compatible format
                return {
                    "id": response_data.get("id", f"chatcmpl-{datetime.now().timestamp()}"),
                    "object": "chat.completion",
                    "created": response_data.get("created", int(datetime.now().timestamp())),
                    "model": model,
                    "choices": response_data.get("choices", []),
                    "usage": response_data.get("usage", {})
                }
            elif self.chatgpt_browser:
                # Use browser automation
                response_content = await self.chatgpt_browser.send_message(
                    message=conversation_text,
                    model=model
                )
                
                completion_id = f"chatcmpl-{datetime.now().timestamp()}"
                
                return {
                    "id": completion_id,
                    "object": "chat.completion",
                    "created": int(datetime.now().timestamp()),
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response_content
                        },
                        "finish_reason": "stop"
                    }],
                    "usage": {
                        "prompt_tokens": len(conversation_text) // 4,
                        "completion_tokens": len(response_content) // 4,
                        "total_tokens": (len(conversation_text) + len(response_content)) // 4
                    }
                }
            else:
                # Fallback mock response
                logger.warning("Using mock response - ChatGPT integration not available")
                await asyncio.sleep(0.5)
                response_content = f"[Mock Response] Processing: {conversation_text[:100]}..."
                
                completion_id = f"chatcmpl-{datetime.now().timestamp()}"
                
                return {
                    "id": completion_id,
                    "object": "chat.completion",
                    "created": int(datetime.now().timestamp()),
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response_content
                        },
                        "finish_reason": "stop"
                    }],
                    "usage": {
                        "prompt_tokens": len(conversation_text) // 4,
                        "completion_tokens": len(response_content) // 4,
                        "total_tokens": (len(conversation_text) + len(response_content)) // 4
                    }
                }
        except Exception as e:
            logger.error(f"Error getting ChatGPT response: {str(e)}", exc_info=True)
            raise
    
    def _messages_to_text(self, messages: List[Message]) -> str:
        """Convert message list to conversation text"""
        # For browser automation, we'll send the last user message
        # In a full implementation, we'd maintain conversation history
        user_messages = [msg.content for msg in messages if msg.role == "user"]
        if user_messages:
            return user_messages[-1]
        return messages[-1].content if messages else ""
    
    def _enhance_for_obsidian(self, message: str) -> str:
        """Enhance prompts with Obsidian-specific context"""
        obsidian_keywords = ["note", "vault", "markdown", "[[", "tag", "link"]
        if any(keyword in message.lower() for keyword in obsidian_keywords):
            enhancement = "\n\n[Context: User is working in Obsidian. Consider markdown formatting, wikilinks [[like this]], and tag structures when responding.]"
            return message + enhancement
        return message
    
    async def close(self):
        """Close browser session"""
        if self.chatgpt_browser:
            await self.chatgpt_browser.close()
        self.session_active = False
        logger.info("ChatGPT proxy session closed")

# Initialize proxy
use_api = os.getenv("OPENAI_API_KEY") is not None
api_key = os.getenv("OPENAI_API_KEY")
# Map browser names (chrome -> chromium for Playwright)
browser_map = {"chrome": "chromium", "firefox": "firefox", "safari": "webkit"}
browser_type = browser_map.get(CONFIG["browser"], "chromium")
chatgpt_proxy = ChatGPTProxy(
    browser=browser_type,
    use_api=use_api,
    api_key=api_key
)

@app.on_event("startup")
async def startup_event():
    """Initialize ChatGPT proxy on startup"""
    await chatgpt_proxy.initialize()
    logger.info(f"ChatMock server starting on {CONFIG['host']}:{CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await chatgpt_proxy.close()
    logger.info("ChatMock server shutting down")

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "ChatMock",
        "version": "1.0.0",
        "obsidian_optimized": True,
        "endpoints": {
            "models": "/v1/models",
            "chat": "/v1/chat/completions",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "proxy_active": chatgpt_proxy.session_active,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI-compatible)"""
    models = [
        ModelInfo(
            id="gpt-5",
            created=1723017600,  # August 7, 2025
            owned_by="openai"
        ),
        ModelInfo(
            id="gpt-5-turbo",
            created=1723017600,
            owned_by="openai"
        ),
        ModelInfo(
            id="gpt-4",
            created=1677610602,
            owned_by="openai"
        ),
        ModelInfo(
            id="gpt-4-turbo",
            created=1704067936,
            owned_by="openai"
        ),
        ModelInfo(
            id="gpt-3.5-turbo",
            created=1677649963,
            owned_by="openai"
        ),
    ]
    
    return {
        "object": "list",
        "data": [model.dict() for model in models]
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    Chat completions endpoint (OpenAI-compatible)
    
    This endpoint forwards requests to ChatGPT and returns responses
    in OpenAI API format for compatibility with Obsidian Smart Connections.
    """
    try:
        logger.info(f"Received chat completion request: model={request.model}, messages={len(request.messages)}")
        
        # Process the request
        response = await chatgpt_proxy.chat_completion(
            messages=request.messages,
            model=request.model or CONFIG["model"],
            temperature=request.temperature,
            max_tokens=request.max_tokens or CONFIG["max_tokens"],
            stream=request.stream or False
        )
        
        if request.stream:
            # TODO: Implement streaming response
            async def generate_stream():
                yield f"data: {json.dumps(response)}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/event-stream"
            )
        else:
            return JSONResponse(content=response)
            
    except Exception as e:
        logger.error(f"Error processing chat completion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Obsidian-specific endpoints

@app.post("/obsidian/summarize")
async def obsidian_summarize(request: Request):
    """Obsidian-specific endpoint for note summarization"""
    data = await request.json()
    note_content = data.get("content", "")
    note_path = data.get("path", "")
    
    prompt = f"""Summarize the following Obsidian note in 2-3 sentences. 
    Extract key topics and suggest 3-5 relevant tags.
    
    Note path: {note_path}
    Content:
    {note_content}
    
    Provide:
    1. A concise summary
    2. A list of suggested tags (format: #tag1 #tag2 #tag3)
    3. Key topics or themes"""
    
    messages = [Message(role="user", content=prompt)]
    response = await chatgpt_proxy.chat_completion(messages=messages)
    
    return {
        "summary": response["choices"][0]["message"]["content"],
        "note_path": note_path,
        "processed_at": datetime.now().isoformat()
    }

@app.post("/obsidian/tag")
async def obsidian_tag(request: Request):
    """Generate tags for an Obsidian note"""
    data = await request.json()
    note_content = data.get("content", "")
    
    prompt = f"""Analyze this Obsidian note and suggest 5-7 relevant tags.
    Consider: topics, themes, projects, people, concepts.
    Return only the tags in format: #tag1 #tag2 #tag3
    
    Note content:
    {note_content[:2000]}"""
    
    messages = [Message(role="user", content=prompt)]
    response = await chatgpt_proxy.chat_completion(messages=messages)
    
    return {
        "tags": response["choices"][0]["message"]["content"],
        "processed_at": datetime.now().isoformat()
    }

@app.post("/obsidian/link")
async def obsidian_link(request: Request):
    """Suggest wikilinks for an Obsidian note"""
    data = await request.json()
    note_content = data.get("content", "")
    vault_path = data.get("vault_path", CONFIG["obsidian_vault_path"])
    
    prompt = f"""Analyze this Obsidian note and suggest 5-10 relevant wikilinks.
    Consider existing notes in the vault and create links in format: [[Note Name]].
    Only suggest links that make semantic sense.
    
    Note content:
    {note_content[:2000]}"""
    
    messages = [Message(role="user", content=prompt)]
    response = await chatgpt_proxy.chat_completion(messages=messages)
    
    return {
        "suggested_links": response["choices"][0]["message"]["content"],
        "processed_at": datetime.now().isoformat()
    }

def main():
    """Main entry point"""
    uvicorn.run(
        "chatmock_server:app",
        host=CONFIG["host"],
        port=CONFIG["port"],
        log_level="info",
        reload=False
    )

if __name__ == "__main__":
    main()

