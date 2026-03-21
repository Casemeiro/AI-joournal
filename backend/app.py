from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import json

# Suppress SSL warnings for development (we use verify=False)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = 'https://openrouter.io/api/v1'
MODEL = 'google/gemini-2.5-flash'  # Google's Gemini 2.5 Flash model

# In-memory storage (for demo - replace with database in production)
entries = {}
next_id = 1


@app.route('/entries', methods=['POST'])
def save_entry():
    """Save a journal entry"""
    global next_id
    
    data = request.get_json()
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': 'Content cannot be empty'}), 400
    
    entry_id = next_id
    entry = {
        'id': entry_id,
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'insights': None
    }
    
    entries[entry_id] = entry
    next_id += 1
    
    return jsonify(entry), 201


@app.route('/entries', methods=['GET'])
def get_entries():
    """Get all journal entries"""
    return jsonify(list(entries.values())), 200


@app.route('/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    """Get a specific journal entry"""
    if entry_id not in entries:
        return jsonify({'error': 'Entry not found'}), 404
    
    return jsonify(entries[entry_id]), 200


@app.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a journal entry"""
    if entry_id not in entries:
        return jsonify({'error': 'Entry not found'}), 404
    
    del entries[entry_id]
    return jsonify({'message': 'Entry deleted'}), 200


@app.route('/insights', methods=['POST'])
def generate_insights():
    """Generate AI insights for a journal entry using OpenRouter"""
    data = request.get_json()
    entry_id = data.get('entry_id')
    
    if entry_id not in entries:
        return jsonify({'error': 'Entry not found'}), 404
    
    entry = entries[entry_id]
    content = entry['content']
    
    if not OPENROUTER_API_KEY:
        return jsonify({'error': 'OpenRouter API key not configured'}), 500
    
    try:
        # Call OpenRouter API with Gemini 2.5 Flash
        # Add verify=False to handle SSL issues, timeout for connection issues
        response = requests.post(
            f'{OPENROUTER_BASE_URL}/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'HTTP-Referer': 'http://localhost:3000',  # Your app URL
                'X-Title': 'First AI Journal',
                'Content-Type': 'application/json'
            },
            json={
                'model': MODEL,
                'messages': [
                    {
                        'role': 'system',
                        'content': '''You are a compassionate journaling assistant. Analyze the user's journal entry and provide:
1. MOOD: One primary emotion/mood (teal, blue, amber, coral, or purple)
2. THEMES: 2-3 key themes or topics mentioned
3. REFLECTION: A brief, supportive reflection or insight (2-3 sentences)
4. PROMPT: A gentle follow-up question for deeper reflection

Format your response as JSON with these exact keys: mood, themes, reflection, prompt'''
                    },
                    {
                        'role': 'user',
                        'content': f'Please analyze this journal entry:\n\n{content}'
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 500
            },
            timeout=30,  # 30 second timeout
            verify=False  # Disable SSL verification (for development)
        )
        
        if response.status_code != 200:
            error_text = response.text
            print(f'OpenRouter API error: {response.status_code}')
            print(f'Response: {error_text}')
            
            # Check if it's an auth error
            if response.status_code == 401:
                return jsonify({'error': 'Invalid API key. Check your OPENROUTER_API_KEY in .env'}), 500
            elif response.status_code == 429:
                return jsonify({'error': 'Rate limited. Please wait a moment and try again.'}), 500
            else:
                return jsonify({'error': f'OpenRouter API error: {response.status_code}'}), 500
        
        # Parse the response
        result = response.json()
        assistant_message = result['choices'][0]['message']['content']
        
        # Try to extract JSON from the response
        try:
            insights = json.loads(assistant_message)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured response from the text
            insights = {
                'mood': 'blue',
                'themes': ['reflection', 'growth'],
                'reflection': assistant_message,
                'prompt': 'What would you like to explore further about this experience?'
            }
        
        # Store insights with the entry
        entry['insights'] = insights
        
        return jsonify({'insights': insights}), 200
    
    except requests.exceptions.Timeout as e:
        print(f'Timeout connecting to OpenRouter: {e}')
        return jsonify({'error': 'Request timeout. OpenRouter API is taking too long. Please try again.'}), 500
    except requests.exceptions.ConnectionError as e:
        print(f'Connection error: {e}')
        return jsonify({'error': 'Cannot connect to OpenRouter. Check your internet connection.'}), 500
    except requests.exceptions.RequestException as e:
        print(f'Request error: {e}')
        return jsonify({'error': f'Network error: {str(e)[:100]}'}), 500
    except Exception as e:
        print(f'Unexpected error: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    api_configured = bool(OPENROUTER_API_KEY)
    return jsonify({
        'status': 'ok',
        'api_configured': api_configured,
        'model': MODEL
    }), 200


if __name__ == '__main__':
    print(f'Starting AI Journal Backend...')
    print(f'OpenRouter API Key configured: {bool(OPENROUTER_API_KEY)}')
    print(f'Using model: {MODEL}')
    app.run(debug=True, port=8000, host='0.0.0.0')
