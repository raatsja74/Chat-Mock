"""
ChatGPT Browser Automation Module
Handles interaction with ChatGPT web interface using Playwright
"""

import asyncio
import json
import logging
from typing import List, Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, Page, BrowserContext

logger = logging.getLogger(__name__)


class ChatGPTBrowser:
    """Manages browser automation for ChatGPT web interface"""
    
    def __init__(self, browser_type: str = "chromium", headless: bool = False):
        self.browser_type = browser_type
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.authenticated = False
        
    async def initialize(self):
        """Initialize browser and navigate to ChatGPT"""
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser
            if self.browser_type == "chromium":
                self.browser = await self.playwright.chromium.launch(
                    headless=self.headless,
                    args=['--disable-blink-features=AutomationControlled']
                )
            elif self.browser_type == "firefox":
                self.browser = await self.playwright.firefox.launch(headless=self.headless)
            elif self.browser_type == "webkit":
                self.browser = await self.playwright.webkit.launch(headless=self.headless)
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            
            # Create context with realistic viewport
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            
            self.page = await self.context.new_page()
            
            # Navigate to ChatGPT
            logger.info("Navigating to ChatGPT...")
            await self.page.goto("https://chat.openai.com", wait_until="networkidle")
            
            # Check if already logged in
            await asyncio.sleep(2)
            if await self._check_logged_in():
                self.authenticated = True
                logger.info("Already authenticated with ChatGPT")
            else:
                logger.warning("Not authenticated. User needs to log in manually.")
                # Keep browser open for manual login
                if not self.headless:
                    logger.info("Browser window open - please log in to ChatGPT")
                    await asyncio.sleep(10)  # Give user time to log in
                    if await self._check_logged_in():
                        self.authenticated = True
                        logger.info("Authentication successful")
            
        except Exception as e:
            logger.error(f"Error initializing browser: {str(e)}", exc_info=True)
            raise
    
    async def _check_logged_in(self) -> bool:
        """Check if user is logged in to ChatGPT"""
        try:
            # Look for common elements that indicate logged-in state
            # This is a simplified check - adjust selectors as needed
            textarea = await self.page.query_selector("textarea")
            if textarea:
                return True
            return False
        except:
            return False
    
    async def send_message(self, message: str, model: str = "gpt-4") -> str:
        """
        Send a message to ChatGPT and get the response
        
        Args:
            message: The message to send
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
        
        Returns:
            The response text from ChatGPT
        """
        if not self.authenticated:
            if not await self._check_logged_in():
                raise Exception("Not authenticated with ChatGPT. Please log in first.")
            self.authenticated = True
        
        try:
            # Find the textarea for input
            textarea = await self.page.wait_for_selector("textarea", timeout=10000)
            if not textarea:
                raise Exception("Could not find ChatGPT input textarea")
            
            # Clear and type the message
            await textarea.click()
            await textarea.fill(message)
            
            # Submit the message (press Enter or click send button)
            await textarea.press("Enter")
            
            # Wait for response
            logger.info("Waiting for ChatGPT response...")
            await self._wait_for_response()
            
            # Extract the response
            response = await self._extract_response()
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending message to ChatGPT: {str(e)}", exc_info=True)
            raise
    
    async def _wait_for_response(self, timeout: int = 60):
        """Wait for ChatGPT to finish generating response"""
        try:
            # Wait for the response to appear and stop generating
            # Look for the stop button to disappear or response to be complete
            await self.page.wait_for_timeout(2000)  # Initial wait
            
            # Poll for response completion
            max_wait = timeout
            waited = 0
            while waited < max_wait:
                # Check if there's a stop button (indicates generation in progress)
                stop_button = await self.page.query_selector('button[aria-label*="Stop"]')
                if not stop_button:
                    # Check if response text is present
                    response_elements = await self.page.query_selector_all(
                        '[data-message-author-role="assistant"]'
                    )
                    if response_elements:
                        await asyncio.sleep(1)  # Give it a moment to finish
                        break
                
                await asyncio.sleep(1)
                waited += 1
            
        except Exception as e:
            logger.warning(f"Timeout or error waiting for response: {str(e)}")
    
    async def _extract_response(self) -> str:
        """Extract the latest response from ChatGPT"""
        try:
            # Find all assistant messages
            assistant_messages = await self.page.query_selector_all(
                '[data-message-author-role="assistant"]'
            )
            
            if not assistant_messages:
                # Fallback: try to find response in other ways
                response_text = await self.page.evaluate("""
                () => {
                    const messages = document.querySelectorAll('[class*="message"]');
                    if (messages.length > 0) {
                        return messages[messages.length - 1].innerText;
                    }
                    return '';
                }
                """)
                return response_text
            
            # Get the last (most recent) assistant message
            last_message = assistant_messages[-1]
            response_text = await last_message.inner_text()
            
            return response_text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting response: {str(e)}", exc_info=True)
            return "Error extracting response from ChatGPT"
    
    async def close(self):
        """Close browser and cleanup"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")


# Alternative: Use OpenAI API if available (more reliable)
class ChatGPTAPI:
    """Alternative implementation using OpenAI API (if API key is available)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
    
    async def send_message(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Send message using OpenAI API"""
        import aiohttp
        
        if not self.api_key:
            raise Exception("OpenAI API key not provided")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error: {response.status} - {error_text}")

