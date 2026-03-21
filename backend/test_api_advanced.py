"""
Advanced test to debug OpenRouter API 405 error
Tests multiple approaches to find the right format
"""

import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv('OPENROUTER_API_KEY')

print("Testing multiple API approaches...")
print(f"API Key: {API_KEY[:20]}...{API_KEY[-20:]}")
print()

# Test 1: Current approach (failing)
print("=" * 60)
print("TEST 1: Current approach (with verify=False)")
print("=" * 60)

try:
    response = requests.post(
        'https://openrouter.io/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Referer': 'http://localhost:3000',
            'X-Title': 'First AI Journal',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'google/gemini-2.5-flash',
            'messages': [
                {'role': 'system', 'content': 'Test'},
                {'role': 'user', 'content': 'Test'}
            ],
        },
        timeout=30,
        verify=False  # Disable SSL verification
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200] if response.text else 'EMPTY'}")
except Exception as e:
    print(f"ERROR: {e}")

print()

# Test 2: With proper SSL verification
print("=" * 60)
print("TEST 2: With proper SSL verification (verify=True)")
print("=" * 60)

try:
    response = requests.post(
        'https://openrouter.io/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Referer': 'http://localhost:3000',
            'X-Title': 'First AI Journal',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'google/gemini-2.5-flash',
            'messages': [
                {'role': 'system', 'content': 'Test'},
                {'role': 'user', 'content': 'Test'}
            ],
        },
        timeout=30,
        verify=True  # Enable SSL verification
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200] if response.text else 'EMPTY'}")
except Exception as e:
    print(f"ERROR: {e}")

print()

# Test 3: Check available models endpoint
print("=" * 60)
print("TEST 3: Check available models (info endpoint)")
print("=" * 60)

try:
    response = requests.get(
        'https://openrouter.io/api/v1/models',
        headers={
            'Authorization': f'Bearer {API_KEY}',
        },
        timeout=30,
        verify=True
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        models = response.json()
        print(f"Number of models: {len(models.get('data', []))}")
        # Find gemini models
        gemini_models = [m for m in models.get('data', []) if 'gemini' in m.get('id', '').lower()]
        print(f"Gemini models available: {len(gemini_models)}")
        for model in gemini_models[:3]:
            print(f"  - {model.get('id')}")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"ERROR: {e}")

print()

# Test 4: Try with minimal headers
print("=" * 60)
print("TEST 4: Minimal headers (only Authorization)")
print("=" * 60)

try:
    response = requests.post(
        'https://openrouter.io/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
        },
        json={
            'model': 'google/gemini-2.5-flash',
            'messages': [
                {'role': 'system', 'content': 'Test'},
                {'role': 'user', 'content': 'Test'}
            ],
        },
        timeout=30,
        verify=True
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200] if response.text else 'EMPTY'}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("=" * 60)
print("Tests complete!")
