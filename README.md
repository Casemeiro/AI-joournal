# ✍️ First AI Journal - AI-Powered Web Application

A beautiful, intelligent personal journal application powered by **Google Gemini 2.5 Flash AI** via OpenRouter. Write freely and get instant AI insights, mood analysis, theme identification, and reflective guidance.

## 🚀 Quick Start (5 minutes)

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Create .env file with your OpenRouter API key
# Get key at: https://openrouter.io/keys
echo "OPENROUTER_API_KEY=sk_your_key_here" > ../.env

# 3. Start backend
python app.py

# 4. In another terminal, start frontend
cd ../frontend
python -m http.server 3000

# 5. Open browser to http://localhost:3000
```

**That's it! Your AI journal is ready. ✨**

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | 5-step setup guide |
| **[README_FULL.md](README_FULL.md)** | Complete feature overview |
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Detailed setup & troubleshooting |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | How everything works together |
| **[backend/README.md](backend/README.md)** | Full API documentation |

## ✨ Features

✅ Write beautiful journal entries (up to 5000 characters)
✅ AI analyzes each entry in real-time (< 1 second)
✅ **Mood Detection** - AI identifies your emotional state
✅ **Theme Extraction** - Finds key topics in your writing
✅ **Reflective Insights** - Gets compassionate guidance
✅ **Follow-up Prompts** - Suggests deeper reflection questions
✅ **Past Entries** - View, search, and manage previous entries
✅ **Beautiful UI** - Works on desktop and mobile
✅ **Responsive Design** - Perfect on any screen size

## 🏗️ Technology Stack

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Responsive design, smooth animations

**Backend:**
- Python 3.8+ with Flask
- Flask-CORS for API management
- python-dotenv for configuration

**AI:**
- Google Gemini 2.5 Flash (via OpenRouter)
- OpenRouter API integration
- Free tier available

## 🎯 How It Works

```
Write Entry → Save → AI Analysis → Display Insights → View/Manage
    ↓                   ↓               ↓
  UI Form      OpenRouter API    Mood + Themes
               + Gemini 2.5       + Reflection
                                  + Prompt
```

Your journal entries are analyzed for:
1. **Mood** - Emotional tone (5 categories with colors)
2. **Themes** - Key topics and patterns (2-3 items)
3. **Reflection** - Compassionate AI insight (2-3 sentences)
4. **Prompt** - Follow-up question for deeper reflection

## 🔐 Getting Started

### Step 1: Get Free API Key
Go to [OpenRouter.io](https://openrouter.io/keys) and create a free account. Takes 1 minute.

### Step 2: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Set Up Environment
Create `.env` file in project root:
```
OPENROUTER_API_KEY=sk_your_key_from_openrouter
```

### Step 4: Run Backend
```bash
python backend/app.py
# Should show: Running on http://0.0.0.0:8000
```

### Step 5: Run Frontend
```bash
cd frontend
python -m http.server 3000
# Open: http://localhost:3000
```

## 📁 Project Structure

```
First AI Journal/
├── README.md                    ← You are here
├── QUICKSTART.md               ← 5-minute setup
├── SETUP_GUIDE.md              ← Detailed guide
├── ARCHITECTURE.md             ← How it all works
├── .env.example                ← API key template
│
├── frontend/
│   ├── index.html              ← Journal UI
│   ├── app.js                  ← JavaScript logic
│   └── style.css               ← Beautiful styling
│
└── backend/
    ├── app.py                  ← Flask API server
    ├── requirements.txt        ← Python dependencies
    └── README.md               ← API documentation
```

## 🎨 Features in Detail

### Write & Save
- Beautiful textarea editor
- Character counter (5000 max)
- One-click save with feedback

### AI Insights
- Mood detection (teal, blue, amber, coral, purple)
- Theme extraction
- Compassionate reflection
- Thoughtful follow-up question

### Past Entries
- Sidebar shows all entries
- Click to view full details
- Insights saved with each entry
- Delete functionality

## 🧑‍💻 API Endpoints

```
GET  /health          - Check server status
POST /entries         - Save journal entry
GET  /entries         - Get all entries
GET  /entries/{id}    - Get specific entry
DELETE /entries/{id}  - Delete entry
POST /insights        - Generate AI analysis
```

Full documentation: see [backend/README.md](backend/README.md)

## 🎓 What You'll Learn

This project demonstrates:
- Full-stack web development
- REST API design
- AI/LLM integration
- Frontend-backend communication
- Environment management
- Responsive design
- Error handling

Perfect for learning or as a template for similar projects!

## ⚡ Customization

### Change AI Model
Edit `backend/app.py` line 16:
```python
MODEL = 'google/gemini-2.5-flash'  # Change model here
```

Other options: GPT-4, Claude, Llama, Mixtral, etc.

### Modify AI Behavior
Edit system prompt in `backend/app.py` line ~105:

```python
'content': '''You are a compassionate journaling assistant...'''
```

### Add Database
Replace in-memory storage with SQLite, PostgreSQL, or MongoDB.

## 🐛 Troubleshooting

### "Is the backend running?"
- Check backend terminal shows "Running on http://0.0.0.0:8000"
- Verify `.env` file exists
- Restart backend

### "API key not configured"
- Verify `.env` file is in project root
- Check key is correct at https://openrouter.io/keys
- Restart backend

### "Failed to generate insights"
- Check internet connection
- Verify API key is valid
- Check backend console for errors

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

## 📖 Next Steps

1. **Test it** - Write a few entries and see AI in action
2. **Deploy** - Use Vercel (frontend) + Railway (backend)
3. **Customize** - Change AI model or behavior
4. **Enhance** - Add database, authentication, charts

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed next steps.

## 💡 Key Concepts

- **OpenRouter**: Provides access to multiple AI models via single API
- **Gemini 2.5 Flash**: Google's latest, fast AI model
- **REST API**: Frontend talks to backend via HTTP endpoints
- **Flask**: Python web framework for building the backend
- **CORS**: Allows frontend to communicate with backend

## 📞 Support

- **For OpenRouter issues**: https://openrouter.io/docs
- **For API key**: https://openrouter.io/keys
- **For Flask help**: https://flask.palletsprojects.com/
- **For detailed setup**: See SETUP_GUIDE.md

## Getting Started

(To be updated as the project progresses)

## Requirements

(To be updated as the project progresses)

## Contributing

(To be updated as the project progresses)
**
