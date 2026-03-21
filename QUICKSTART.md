# Quick Start Guide - AI Journal with Gemini 2.5 Flash

## 30-Second Setup

### 1. Get Your API Key (Free)
1. Go to https://openrouter.io/keys
2. Sign up (takes 1 minute)
3. Click "Create Key"
4. Copy the key

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Add API Key to .env
Create a `.env` file in the project root (copy from `.env.example`):
```
OPENROUTER_API_KEY=sk_your_key_here
```

### 4. Start Backend
```bash
python backend/app.py
```
You should see:
```
Starting AI Journal Backend...
OpenRouter API Key configured: True
Using model: google/gemini-2.5-flash
 * Running on http://0.0.0.0:8000
```

### 5. Open Frontend
Open `frontend/index.html` in your browser, or use a local server:

**Option A - Python:**
```bash
cd frontend
python -m http.server 3000
# Then go to http://localhost:3000
```

**Option B - Node.js:**
```bash
npx http-server frontend -p 3000
# Then go to http://localhost:3000
```

## That's It! 🎉

You now have a fully functional AI Journal that:
- ✅ Saves your journal entries
- ✅ Uses Google's Gemini 2.5 Flash AI to analyze entries
- ✅ Detects mood from your writing
- ✅ Identifies themes and patterns
- ✅ Provides thoughtful reflections
- ✅ Suggests questions for deeper reflection

## How It Works

1. **Write** your journal entry in the textarea
2. **Click** "Save entry"
3. **Watch** as the AI analyzes your thoughts within seconds
4. **See** mood, themes, reflection, and a follow-up question
5. **View** all past entries in the sidebar

## Troubleshooting

### "Something went wrong. Is the backend running?"
- Check that the terminal shows "Running on http://0.0.0.0:8000"
- Make sure you're accessing the frontend from the same network

### "Failed to generate insights"
- Go to https://openrouter.io/keys and verify your API key is valid
- Make sure `.env` file has the correct key
- Restart the backend server

### Port 8000 already in use?
Edit `backend/app.py` line ~167:
```python
app.run(debug=True, port=9000, host='0.0.0.0')  # Change 8000 to 9000
```
Then update `frontend/app.js` line 1:
```javascript
const API = 'http://localhost:9000';
```

## API Costs

**Good news:** The free tier on OpenRouter works great!
- First request is free
- Generous free tier limits
- GPT-4 and Claude also available if you want to experiment

## What's Next?

- **Deploy to web:** Use Vercel (frontend) + Railway/Heroku (backend)
- **Add database:** Replace in-memory storage with PostgreSQL or SQLite
- **Add auth:** Let users create accounts and login
- **Mobile app:** Turn into a React Native or Flutter app

## Key Files

- `backend/app.py` - Flask server that handles AI insights
- `frontend/app.js` - JavaScript that handles UI and API calls
- `frontend/index.html` - Journal interface
- `frontend/style.css` - Beautiful styling
- `.env` - Your API key (keep secret!)

## Model Information

**Google Gemini 2.5 Flash:**
- Very fast (< 1 second response)
- Latest Google AI model
- Great for reasoning and understanding context
- Available through OpenRouter

Want to try other models? Edit `backend/app.py` line 16:
```python
MODEL = 'openai/gpt-4-turbo'  # or 'anthropic/claude-3-opus'
```

See all available models at https://openrouter.io/models
