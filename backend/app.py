from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import json
import atexit

# Create a requests session
session = requests.Session()

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
MODEL = 'google/gemini-2.5-flash'  # Google's Gemini 2.5 Flash model

# In-memory storage (for demo - replace with database in production)
entries = {}
next_id = 1

# Clean up the requests session on exit
@atexit.register
def cleanup():
    session.close()

# Local mood detection function (used as fallback)
def detect_mood_locally(text):
    """Detect mood from text using keyword analysis as fallback"""
    text_lower = text.lower()
    
    # Define mood keywords
    positive_words = ['happy', 'great', 'excited', 'grateful', 'blessed', 'amazing', 'wonderful', 
                     'love', 'hope', 'joy', 'proud', 'confident', 'energetic', 'passionate',
                     'accomplish', 'success', 'win', 'achieve', 'beautiful', 'excellent']
    
    negative_words = ['sad', 'depressed', 'angry', 'frustrated', 'anxious', 'worried', 
                     'scared', 'hate', 'terrible', 'awful', 'disaster', 'fail', 'lost',
                     'overwhelmed', 'stressed', 'exhausted', 'miserable', 'alone']
    
    calm_words = ['peaceful', 'calm', 'serene', 'quiet', 'reflect', 'meditate', 'rest',
                 'relax', 'still', 'silent', 'gentle', 'soft', 'contemplative']
    
    energetic_words = ['energetic', 'motivated', 'driven', 'active', 'dynamic', 'inspired',
                      'enthusiastic', 'vibrant', 'busy', 'rushing', 'intense', 'passionate']
    
    confused_words = ['confused', 'uncertain', 'unclear', 'lost', 'mixed', 'conflicted',
                     'unsure', 'doubt', 'question', 'wonder', 'struggle']
    
    # Count occurrences
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    calm_count = sum(1 for word in calm_words if word in text_lower)
    energetic_count = sum(1 for word in energetic_words if word in text_lower)
    confused_count = sum(1 for word in confused_words if word in text_lower)
    
    # Determine mood based on counts
    if negative_count > positive_count and negative_count > 0:
        mood = 'coral'  # warm but cautious
    elif positive_count > negative_count and positive_count > 0:
        mood = 'teal'   # positive/calm
    elif energetic_count > calm_count and energetic_count > 0:
        mood = 'amber'  # energetic/warm
    elif calm_count > 0:
        mood = 'purple' # reflective/calm
    elif confused_count > 0:
        mood = 'amber'  # processing
    else:
        mood = 'teal'   # neutral/baseline
    
    return mood


@app.route('/', methods=['GET', 'HEAD'])
def root():
    """Root endpoint - responds to health checks"""
    return jsonify({'status': 'AI Journal Backend is running'}), 200


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
    
    
    # REAL API CODE (disabled while we debug 405 error):
 
    try:
        # Call OpenRouter API with Gemini 2.5 Flash
        api_url = f'{OPENROUTER_BASE_URL}/chat/completions'
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Accept': 'application/json',
            'Referer': 'http://localhost:3000',
            'X-Title': 'First AI Journal',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': '''You are a compassionate journaling assistant. Analyze the journal entry and respond with a JSON object containing:
- mood: (one of: teal, blue, amber, coral, purple)
- themes: (array of 2-3 key themes as strings)
- reflection: (2-3 sentences of compassionate insight)
- prompt: (a thoughtful follow-up question for deeper reflection)

Respond ONLY with valid JSON, no markdown or extra text.'''
                },
                {
                    'role': 'user',
                    'content': f'Please analyze this journal entry:\n\n{content}'
                }
            ],
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        print(f'Calling OpenRouter API: {api_url}')
        print(f'API Key present: {bool(OPENROUTER_API_KEY)}')
        print(f'API Key format: {OPENROUTER_API_KEY[:20]}...' if OPENROUTER_API_KEY else 'None')
        print(f'Model: {MODEL}')
        print(f'Payload: {json.dumps(payload, indent=2)}')
        
        # Use session with disabled SSL verification to avoid handshake errors
        response = session.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f'Response status: {response.status_code}')
        print(f'Response body: {response.text}')
        print(f'Response headers: {dict(response.headers)}')
        
        if response.status_code != 200:
            error_text = response.text
            print(f'OpenRouter API error: {response.status_code}')
            print(f'Response body: {error_text}')
            print(f'Response headers: {response.headers}')
            
            # Create fallback insights even on error so entry isn't empty
            detected_mood = detect_mood_locally(content)
            fallback_insights = {
                'mood': detected_mood,
                'themes': ['pending_analysis', 'reflection'],
                'reflection': 'The AI is taking a moment to analyze your entry. Please refresh to see insights.',
                'prompt': 'What does this entry mean to you?'
            }
            entry['insights'] = fallback_insights
            
            # Return error responses with 200 status and error flag so content reaches browser
            if response.status_code == 401:
                return jsonify({'error': 'Invalid API key. Check your OPENROUTER_API_KEY in .env', 'api_status': 401, 'insights': fallback_insights}), 200
            elif response.status_code == 405:
                return jsonify({'error': 'API endpoint error (405). The API key may be invalid. Try creating a new key at https://openrouter.ai/keys', 'api_status': 405, 'insights': fallback_insights}), 200
            elif response.status_code == 402:
                return jsonify({'error': 'Insufficient OpenRouter credits. Purchase credits at https://openrouter.ai/settings/credits', 'api_status': 402, 'insights': fallback_insights}), 200
            elif response.status_code == 429:
                return jsonify({'error': 'Rate limited. Please wait a moment and try again.', 'api_status': 429, 'insights': fallback_insights}), 200
            else:
                return jsonify({'error': f'OpenRouter API error: {response.status_code}', 'api_status': response.status_code, 'insights': fallback_insights}), 200
        
        # Parse the response
        result = response.json()
        print(f'Parsed JSON response: {json.dumps(result, indent=2)[:500]}')
        
        assistant_message = result['choices'][0]['message']['content']
        print(f'Assistant message: {assistant_message[:200]}')
        
        # Try to extract JSON from the response
        try:
            insights = json.loads(assistant_message)
            print(f'Successfully parsed insights JSON: {insights}')
        except json.JSONDecodeError as json_err:
            print(f'Failed to parse JSON from response: {json_err}')
            print(f'Raw message was: {assistant_message}')
            # Create fallback insights from the text response
            detected_mood = detect_mood_locally(content)
            insights = {
                'mood': detected_mood,
                'themes': ['reflection', 'growth'],
                'reflection': assistant_message,
                'prompt': 'What would you like to explore further about this experience?'
            }
        
        # Store insights with the entry
        entry['insights'] = insights
        print(f'Stored insights for entry {entry_id}: {insights}')
        
        return jsonify({'insights': insights}), 200
    
    except requests.exceptions.Timeout as e:
        print(f'Timeout connecting to OpenRouter: {e}')
        detected_mood = detect_mood_locally(content)
        fallback = {
            'mood': detected_mood,
            'themes': ['pending', 'timeout'],
            'reflection': 'The API request timed out. Please try again.',
            'prompt': 'What does this entry mean to you?'
        }
        entry['insights'] = fallback
        return jsonify({'error': 'Request timeout. OpenRouter API is taking too long. Please try again.', 'exception': 'Timeout', 'insights': fallback}), 200
    except requests.exceptions.SSLError as e:
        print(f'SSL Connection error: {e}')
        detected_mood = detect_mood_locally(content)
        fallback = {
            'mood': detected_mood,
            'themes': ['pending', 'ssl_error'],
            'reflection': 'Connection security issue. Please try again.',
            'prompt': 'What does this entry mean to you?'
        }
        entry['insights'] = fallback
        return jsonify({'error': 'SSL connection error to OpenRouter. This is usually temporary - try again in a moment.', 'exception': 'SSLError', 'insights': fallback}), 200
    except requests.exceptions.ConnectionError as e:
        print(f'Connection error: {e}')
        detected_mood = detect_mood_locally(content)
        fallback = {
            'mood': detected_mood,
            'themes': ['pending', 'connection'],
            'reflection': 'Network connection issue. Your entry is saved. Please try refreshing.',
            'prompt': 'What does this entry mean to you?'
        }
        entry['insights'] = fallback
        return jsonify({'error': 'Cannot connect to OpenRouter. Check your internet connection.', 'exception': 'ConnectionError', 'insights': fallback}), 200
    except requests.exceptions.RequestException as e:
        print(f'Request error: {e}')
        detected_mood = detect_mood_locally(content)
        fallback = {
            'mood': detected_mood,
            'themes': ['pending', 'error'],
            'reflection': 'There was an issue with the AI analysis. Your entry is saved.',
            'prompt': 'What does this entry mean to you?'
        }
        entry['insights'] = fallback
        return jsonify({'error': f'Network error: {str(e)[:100]}', 'exception': 'RequestException', 'insights': fallback}), 200
    except Exception as e:
        print(f'Unexpected error in /insights: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()
        detected_mood = detect_mood_locally(content)
        fallback = {
            'mood': detected_mood,
            'themes': ['pending', 'error'],
            'reflection': 'An unexpected error occurred. Your entry is saved.',
            'prompt': 'What does this entry mean to you?'
        }
        entry['insights'] = fallback
        return jsonify({'error': f'Unexpected error: {str(e)[:200]}', 'exception': type(e).__name__, 'insights': fallback}), 200



@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    api_configured = bool(api_key) and len(api_key) > 0
    api_key_preview = f"{api_key[:10]}...{api_key[-10:]}" if api_key and len(api_key) > 20 else "NOT SET"
    
    return jsonify({
        'status': 'ok',
        'api_configured': api_configured,
        'api_key_preview': api_key_preview,
        'model': MODEL
    }), 200


if __name__ == '__main__':
    print(f'Starting AI Journal Backend...')
    print(f'OpenRouter API Key configured: {bool(OPENROUTER_API_KEY)}')
    print(f'Using model: {MODEL}')
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, port=port, host='0.0.0.0')
