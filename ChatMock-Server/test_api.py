#!/usr/bin/env python3
"""
Simple test script for ChatMock API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_models():
    """Test models endpoint"""
    print("Testing models endpoint...")
    response = requests.get(f"{BASE_URL}/v1/models")
    print(f"Status: {response.status_code}")
    print(f"Models: {json.dumps(response.json(), indent=2)}")
    print()

def test_chat_completion():
    """Test chat completion endpoint"""
    print("Testing chat completion endpoint...")
    payload = {
        "model": "gpt-5",
        "messages": [
            {"role": "user", "content": "Say hello in one sentence."}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data['choices'][0]['message']['content']}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.Timeout:
        print("Request timed out - ChatGPT may be processing")
    except Exception as e:
        print(f"Error: {str(e)}")
    print()

def test_obsidian_summarize():
    """Test Obsidian summarize endpoint"""
    print("Testing Obsidian summarize endpoint...")
    payload = {
        "content": "# My Note\n\nThis is a test note with some content. It has multiple paragraphs and discusses various topics related to project management and automation.",
        "path": "Test/MyNote.md"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/obsidian/summarize",
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Summary: {data.get('summary', 'N/A')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("ChatMock API Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_models()
        test_chat_completion()
        test_obsidian_summarize()
        
        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to ChatMock server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Start it with: ./start_chatmock.sh")

