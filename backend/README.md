# Backend API Documentation

## Overview

This Flask backend provides REST API endpoints for the AI Journal application. It integrates with OpenRouter's API to provide AI-powered insights using Google's Gemini 2.5 Flash model.

## Technology Stack

- **Framework**: Flask (Python)
- **CORS Support**: Flask-CORS (for frontend communication)
- **AI Provider**: OpenRouter (via HTTP API)
- **Model**: Google Gemini 2.5 Flash
- **Environment Management**: python-dotenv

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Create `.env` file in project root:**
```bash
# Copy from .env.example
cp .env.example .env
```

3. **Add your OpenRouter API key:**
Edit `.env`:
```
OPENROUTER_API_KEY=sk_your_key_here
```

### Get Your API Key

1. Visit [OpenRouter.io](https://openrouter.io/keys)
2. Sign up (free account)
3. Click "Create Key"
4. Copy the key to your `.env` file

**Cost**: OpenRouter has a generous free tier. You can use Gemini 2.5 Flash extensively for free.

## Running the Server

```bash
python app.py
```

You should see:
```
Starting AI Journal Backend...
OpenRouter API Key configured: True
Using model: google/gemini-2.5-flash
 * Running on http://0.0.0.0:8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

**GET** `/health`

Check if backend is running and API is configured.

**Response:**
```json
{
  "status": "ok",
  "api_configured": true,
  "model": "google/gemini-2.5-flash"
}
```

---

### Create Entry

**POST** `/entries`

Save a new journal entry.

**Request:**
```json
{
  "content": "Today was a good day. I accomplished a lot at work..."
}
```

**Response (201):**
```json
{
  "id": 1,
  "content": "Today was a good day...",
  "timestamp": "2026-03-21T14:30:45.123456",
  "insights": null
}
```

**Error (400):**
```json
{
  "error": "Content cannot be empty"
}
```

---

### Get All Entries

**GET** `/entries`

Retrieve all saved journal entries.

**Response:**
```json
[
  {
    "id": 1,
    "content": "Today was great...",
    "timestamp": "2026-03-21T14:30:45.123456",
    "insights": {
      "mood": "teal",
      "themes": ["work", "accomplishment"],
      "reflection": "You're experiencing positive momentum...",
      "prompt": "What contributed most to your sense of accomplishment?"
    }
  },
  {
    "id": 2,
    "content": "Feeling overwhelmed...",
    "timestamp": "2026-03-21T10:15:20.654321",
    "insights": null
  }
]
```

---

### Get Single Entry

**GET** `/entries/{id}`

Retrieve a specific journal entry by ID.

**Response (200):**
```json
{
  "id": 1,
  "content": "Today was great...",
  "timestamp": "2026-03-21T14:30:45.123456",
  "insights": {...}
}
```

**Error (404):**
```json
{
  "error": "Entry not found"
}
```

---

### Delete Entry

**DELETE** `/entries/{id}`

Delete a journal entry by ID.

**Response (200):**
```json
{
  "message": "Entry deleted"
}
```

**Error (404):**
```json
{
  "error": "Entry not found"
}
```

---

### Generate Insights

**POST** `/insights`

Generate AI insights for a journal entry using Gemini 2.5 Flash.

**Request:**
```json
{
  "entry_id": 1
}
```

**Response (200):**
```json
{
  "insights": {
    "mood": "teal",
    "themes": ["achievement", "growth", "reflection"],
    "reflection": "You're showing strong self-awareness and positive momentum...",
    "prompt": "How do you want to build on this positive energy?"
  }
}
```

**Response Structure:**
- `mood` (string): One of: `teal`, `blue`, `amber`, `coral`, `purple`
- `themes` (array): 2-3 key topics identified in the entry
- `reflection` (string): Compassionate, supportive insight about the entry
- `prompt` (string): A thoughtful follow-up question for deeper reflection

**Error (404):**
```json
{
  "error": "Entry not found"
}
```

**Error (500):**
```json
{
  "error": "Failed to generate insights"
}
```

## How AI Insights Work

### System Prompt

The AI is guided by this system prompt:

```
You are a compassionate journaling assistant. Analyze the user's journal entry and provide:
1. MOOD: One primary emotion/mood (teal, blue, amber, coral, or purple)
2. THEMES: 2-3 key themes or topics mentioned
3. REFLECTION: A brief, supportive reflection or insight (2-3 sentences)
4. PROMPT: A gentle follow-up question for deeper reflection

Format your response as JSON with these exact keys: mood, themes, reflection, prompt
```

### Model Configuration

```python
MODEL = 'google/gemini-2.5-flash'
temperature = 0.7           # Balanced creativity
max_tokens = 500           # Keep responses concise
```

### Response Processing

The backend:
1. Sends the journal entry to OpenRouter's API
2. Receives AI-generated JSON response
3. Validates and stores the insights with the entry
4. Returns formatted insights to frontend

## Mood Colors

The mood system uses specific colors for visual differentiation:

| Mood | Color | Hex Code |
|------|-------|----------|
| Teal | #1D9E75 | Peaceful, content |
| Blue | #2B6CB0 | Reflective, calm |
| Amber | #C47A1E | Energetic, interested |
| Coral | #C05337 | Passionate, intense |
| Purple | #5B4DBE | Creative, thoughtful |

## Data Storage

Currently, entries are stored in **memory** (they'll be lost when the server restarts).

### To Add Persistent Storage

Replace the in-memory `entries` dictionary with a database:

**Option 1: SQLite (Simple)**
```python
import sqlite3

conn = sqlite3.connect('journal.db')
cursor = conn.cursor()

cursor.execute('''
  CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    insights TEXT
  )
''')
```

**Option 2: PostgreSQL (Production)**
```bash
pip install psycopg2
```

**Option 3: MongoDB (NoSQL)**
```bash
pip install pymongo
```

## Environment Variables

### Required
- `OPENROUTER_API_KEY` - Your OpenRouter API key

### Optional
- `FLASK_ENV` - Set to `development` or `production`
- `FLASK_DEBUG` - Set to `1` to enable debug mode

## Error Handling

The API provides clear error messages:

```python
# Missing API key
if not OPENROUTER_API_KEY:
    return {'error': 'OpenRouter API key not configured'}, 500

# Entry not found
if entry_id not in entries:
    return {'error': 'Entry not found'}, 404

# API connection issues
except requests.exceptions.RequestException as e:
    return {'error': 'Failed to connect to OpenRouter API'}, 500
```

## CORS Configuration

The backend enables CORS for all origins:

```python
CORS(app)
```

This allows requests from:
- `http://localhost:3000` (frontend dev server)
- `http://localhost:8000` (same server)
- Any other origin

To restrict to specific origins:
```python
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"]
    }
})
```

## Customization Guide

### Change the AI Model

Edit line 16 in `app.py`:

```python
MODEL = 'google/gemini-2.5-flash'  # Change this
```

**Other popular models on OpenRouter:**
- `openai/gpt-4-turbo` - Advanced reasoning
- `anthropic/claude-3-opus` - Great for analysis
- `meta-llama/llama-2-70b-chat` - Open source
- `neeva/ns-8b` - Super fast
- `mistralai/mixtral-8x7b` - Balanced

See all models: https://openrouter.io/models

### Modify AI Behavior

Edit the system prompt in `app.py` around line 105:

```python
'content': '''You are a compassionate journaling assistant...'''
```

**Example variations:**
```python
# For goal-oriented insights
'content': '''Analyze this journal entry and provide:
1. MOOD: The primary emotion
2. GOALS: What goals can you identify?
3. OBSTACLES: What challenges are mentioned?
4. ACTION_PLAN: 2-3 concrete steps forward'''
```

### Adjust Temperature

Line ~125 in `app.py`:

```python
'temperature': 0.7,  # Range: 0-1
```

- `0.0` - Consistent, predictable responses
- `0.5` - Balanced
- `1.0` - Creative, varied responses

### Adjust Max Tokens

Line ~126 in `app.py`:

```python
'max_tokens': 500,  # Max response length
```

## Testing the API

### Using cURL

```bash
# Check health
curl http://localhost:8000/health

# Create entry
curl -X POST http://localhost:8000/entries \
  -H "Content-Type: application/json" \
  -d '{"content": "Today was great!"}'

# Get insights
curl -X POST http://localhost:8000/insights \
  -H "Content-Type: application/json" \
  -d '{"entry_id": 1}'

# Get all entries
curl http://localhost:8000/entries

# Delete entry
curl -X DELETE http://localhost:8000/entries/1
```

### Using Python

```python
import requests

# Check health
response = requests.get('http://localhost:8000/health')
print(response.json())

# Create entry
entry = requests.post('http://localhost:8000/entries', json={
    'content': 'My journal entry...'
}).json()

# Generate insights
insights = requests.post('http://localhost:8000/insights', json={
    'entry_id': entry['id']
}).json()
```

## Troubleshooting

### "OpenRouter API key not configured"
- Check that `.env` file exists in project root
- Verify `OPENROUTER_API_KEY=sk_...` is set correctly
- Restart the server

### "Failed to generate insights"
- Verify your API key is valid at https://openrouter.io/keys
- Check your internet connection
- Check backend console for error details
- Ensure you have remaining API calls/credits

### "CORS error" on frontend
- Make sure backend is running at `http://localhost:8000`
- Check that frontend fetch requests match the API URL
- CORS is enabled by default, so this usually means backend isn't running

### Port 8000 already in use
Change the port in `app.py` line ~167:

```python
app.run(debug=True, port=9000, host='0.0.0.0')
```

Then update frontend `app.js` line 1:

```javascript
const API = 'http://localhost:9000';
```

## Deployment

### Deploy to Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Add environment variable
railway variables set OPENROUTER_API_KEY=sk_...

# Deploy
railway up
```

### Deploy to Heroku

```bash
# Install Heroku CLI
brew install heroku  # macOS
# or choco install heroku-cli  # Windows

# Login
heroku login

# Create app
heroku create your-journal-api

# Set environment variable
heroku config:set OPENROUTER_API_KEY=sk_...

# Deploy
git push heroku main
```

### Deploy to AWS/GCP/Azure
Requires more setup but offers more flexibility. Platform-specific guides available on the respective cloud provider docs.

## Performance Considerations

### Current Limitations
- In-memory storage (lost on restart)
- Single-threaded
- No database indexing

### Optimization Tips
1. Add database for persistence
2. Implement caching with Redis
3. Use async operations with async Flask
4. Add rate limiting to prevent abuse
5. Batch process insights for multiple entries

## Security Considerations

- ✅ API key stored in `.env` (not in code)
- ✅ `.env` added to `.gitignore`
- ⚠️ No authentication (add if deploying publicly)
- ⚠️ CORS open to all origins (restrict if needed)
- ⚠️ No rate limiting (add if public)

For production deployments, consider:
- User authentication (OAuth, JWT)
- Database encryption
- HTTPS/TLS
- Request rate limiting
- Input validation
- API key rotation

## Next Steps

1. **Add authentication** - Let users create accounts
2. **Add database** - Persist entries beyond server restarts
3. **Add more AI features** - Mood trending, pattern analysis
4. **Add exports** - PDF/journal entries
5. **Add sharing** - Share entries with friends
6. **Mobile app** - React Native or Flutter

## Support

- **OpenRouter Docs**: https://openrouter.io/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **Gemini Model Info**: https://openrouter.io/models/google/gemini-2.5-flash

## License

This project is open source. Feel free to modify and use it however you like.
