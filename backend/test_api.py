"""
Test script to diagnose OpenRouter API connection
Run this to see exactly what's happening
"""

import requests
import os
from dotenv import load_dotenv
import json

# Load environment
load_dotenv()

API_KEY = os.getenv('OPENROUTER_API_KEY')
print(f"✓ API Key loaded: {API_KEY[:20]}...{API_KEY[-20:]}")
print()

# Test URL
url = 'https://openrouter.io/api/v1/chat/completions'
print(f"Testing URL: {url}")
print()

# Test headers
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Referer': 'http://localhost:3000',
    'X-Title': 'First AI Journal',
    'Content-Type': 'application/json',
    'User-Agent': 'PythonTest/1.0'
}

print("Headers:")
for key, value in headers.items():
    if key == 'Authorization':
        print(f"  {key}: Bearer {value[7:20]}...")
    else:
        print(f"  {key}: {value}")
print()

# Test payload
payload = {
    'model': 'google/gemini-2.5-flash',
    'messages': [
        {
            'role': 'system',
            'content': 'You are helpful. Return JSON with keys: mood, themes, reflection, prompt'
        },
        {
            'role': 'user',
            'content': 'Test message'
        }
    ],
    'temperature': 0.7,
    'max_tokens': 500
}

print("Payload:")
print(json.dumps(payload, indent=2))
print()

# Try the request
print("=" * 60)
print("SENDING REQUEST...")
print("=" * 60)
print()

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
        verify=False
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text}")
    print()
    
    if response.status_code == 200:
        print("✓ SUCCESS! API is working!")
        print(response.json())
    else:
        print(f"✗ ERROR {response.status_code}")
        
except Exception as e:
    print(f"✗ EXCEPTION: {e}")
    print(f"Type: {type(e).__name__}")

print()
print("=" * 60)
print("Test complete!")
