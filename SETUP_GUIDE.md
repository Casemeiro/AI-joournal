# AI Journal Application - Complete Setup Guide

## Overview
This is a web-based journal application that uses AI (Google's Gemini 2.5 Flash via OpenRouter) to provide guidance and insights on your journal entries.

## Architecture
```
├── frontend/           # React/Vanilla JS web interface
│   ├── index.html     # Main HTML
│   ├── app.js         # Frontend logic
│   └── style.css      # Styling
│
└── backend/           # Python Flask API
    ├── app.py         # Backend application
    └── requirements.txt # Python dependencies
```

## Setup Instructions

### 1. Get an OpenRouter API Key
1. Go to [OpenRouter.io](https://openrouter.io/keys)
2. Sign up for a free account
3. Click "Create Key" to generate an API key
4. Copy your API key

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables
1. In the project root directory, create a `.env` file (copy from `.env.example`)
2. Paste your OpenRouter API key:
```
OPENROUTER_API_KEY=sk_xxxxxxxxxxxxxxxxxxxx
```

### 4. Run the Backend
```bash
# From the backend directory
python app.py
```

The backend will start at `http://localhost:8000`

### 5. Open the Frontend
Simply open `frontend/index.html` in your web browser, or use a local server:
```bash
# Python 3
python -m http.server 3000 --directory frontend

# Or with Node.js
npx http-server frontend -p 3000
```

Then navigate to `http://localhost:3000`

## Features

### Journal Entry
- Write freely up to 5000 characters
- Auto-save functionality with visual feedback
- Character count display

### AI Insights (Powered by Gemini 2.5 Flash)
After saving an entry, the AI analyzes it and provides:
- **Mood Detection**: Categorizes your emotional state (teal, blue, amber, coral, purple)
- **Theme Identification**: Extracts 2-3 key topics or themes
- **Reflective Guidance**: Offers compassionate insights about your entry
- **Follow-up Question**: Suggests a question for deeper self-reflection

### Entry Management
- View all past entries in the sidebar
- Click entries to view full details
- Delete entries you no longer need
- Insights saved with each entry

### Real-time Features
- Character counter as you type
- Loading states during AI processing
- Toast notifications for actions
- Responsive modal for viewing past entries

## API Endpoints

### POST `/entries`
Save a new journal entry
```json
{
  "content": "Your journal text here..."
}
```

### GET `/entries`
Retrieve all journal entries

### GET `/entries/{id}`
Retrieve a specific entry

### DELETE `/entries/{id}`
Delete a journal entry

### POST `/insights`
Generate AI insights for an entry
```json
{
  "entry_id": 1
}
```

### GET `/health`
Check backend status and API configuration

## How the AI Works

The application uses the **Google Gemini 2.5 Flash** model through OpenRouter:

- **Model**: `google/gemini-2.5-flash`
- **Temperature**: 0.7 (balanced between creative and consistent)
- **Max Tokens**: 500 (keeps responses concise)

The system prompt guides the AI to:
1. Analyze journal entries with compassion
2. Identify moods and themes
3. Provide supportive reflections
4. Suggest reflective prompts

## Troubleshooting

### "API key not configured" error
- Make sure you created a `.env` file
- Verify your OpenRouter API key is correctly copied
- Restart the backend server

### CORS errors
- The backend has CORS enabled for all origins
- Make sure the frontend is accessing `http://localhost:8000`

### "Failed to connect to OpenRouter API"
- Check your internet connection
- Verify your OpenRouter API key is valid at https://openrouter.io/keys
- Check the backend console for detailed error messages

### Entry not found
- Make sure you wait for the "Entry saved ✓" confirmation before requesting insights
- Clear your browser cache if needed

## Customization

### Change the AI Model
Edit `app.py` line ~16:
```python
MODEL = 'google/gemini-2.5-flash'  # Change this to another OpenRouter model
```

Other popular models on OpenRouter:
- `openai/gpt-4-turbo`
- `anthropic/claude-3-opus`
- `meta-llama/llama-2-70b-chat`

### Modify AI Behavior
Edit the system prompt in `app.py` around line 105-108 to change how the AI analyzes entries.

### Add Data Persistence
Replace the in-memory `entries` dictionary with:
- SQLite (simple)
- PostgreSQL (production-ready)
- MongoDB (NoSQL)

## Next Steps

1. **Deploy**: Host the frontend on Vercel/Netlify and backend on Railway/Heroku
2. **Database**: Add a real database instead of in-memory storage
3. **Authentication**: Add user accounts with login
4. **Mobile**: Turn the web app into a mobile app with React Native
5. **Advanced Analytics**: Add charts showing mood trends over time

## Support

For OpenRouter API documentation: https://openrouter.io/docs
For Gemini 2.5 Flash details: https://openrouter.io/models/google/gemini-2.5-flash
