# 🎯 First AI Journal - Complete Web Application

A beautiful, interactive web journal application powered by **Google's Gemini 2.5 Flash AI** via OpenRouter. Write freely and get compassionate AI insights, mood detection, theme identification, and reflective prompts.

## ✨ Features

✅ **Write Journal Entries** - Beautiful textarea with character counter (up to 5000 chars)
✅ **AI-Powered Insights** - Google Gemini 2.5 Flash analyzes each entry in seconds
✅ **Mood Detection** - AI identifies your emotional state (5 moods with distinct colors)
✅ **Theme Identification** - Extracts 2-3 key themes from your writing
✅ **Reflective Guidance** - Gets compassionate, supportive insights about your thoughts
✅ **Follow-up Questions** - Prompts for deeper self-reflection
✅ **Past Entries Sidebar** - View, search, and click to view previous entries
✅ **Entry Details Modal** - Full entry view with all insights
✅ **Delete Entries** - Remove entries you no longer need
✅ **Responsive Design** - Works on desktop and mobile
✅ **Real-time Feedback** - Loading states, toast notifications, smooth animations

## 🚀 Quick Start (30 Seconds)

### 1️⃣ Get Free API Key
```
Open: https://openrouter.io/keys
Sign up (1 minute)
Create key → Copy it
```

### 2️⃣ Install Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ Configure API Key
Create `.env` file in project root:
```
OPENROUTER_API_KEY=sk_your_key_here
```

### 4️⃣ Start Backend
```bash
python backend/app.py
```
You should see: `Running on http://0.0.0.0:8000`

### 5️⃣ Open Frontend
```bash
cd frontend
python -m http.server 3000
# Visit: http://localhost:3000
```

**That's it! 🎉 Your AI journal is ready to use.**

## 📁 Project Structure

```
First AI Journal/
├── README.md                 # This file
├── QUICKSTART.md            # Quick setup guide
├── SETUP_GUIDE.md          # Detailed setup & features
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
│
├── frontend/               # Web application
│   ├── index.html         # Journal UI
│   ├── app.js             # JavaScript logic
│   └── style.css          # Beautiful styling
│
└── backend/               # Python API server
    ├── app.py             # Flask application
    ├── requirements.txt   # Dependencies
    └── README.md          # API documentation
```

## 🤖 How It Works

```
User writes journal entry
         ↓
   Frontend saves it
         ↓
   Backend stores entry
         ↓
   OpenRouter API called
         ↓
   Google Gemini 2.5 Flash analyzes
         ↓
   AI returns insights JSON
         ↓
   Frontend displays mood,
   themes, reflection, prompt
```

## 📚 Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **Vanilla JavaScript** - No frameworks, lightweight
- **Responsive Design** - Works on all devices

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin requests
- **OpenRouter API** - AI provider
- **python-dotenv** - Environment config

### AI
- **Model**: Google Gemini 2.5 Flash
- **Provider**: OpenRouter
- **Cost**: Free tier available
- **Speed**: < 1 second per analysis

## 🎨 Design Highlights

- **Clean, minimalist UI** - Focus on your thoughts
- **Dark-friendly colors** - Easy on the eyes
- **Smooth animations** - Delightful interactions
- **Mobile responsive** - Write from anywhere
- **Accessible design** - Proper semantic HTML
- **Fast performance** - No heavy frameworks

## 🎯 Mood System

Your emotions are represented with 5 distinct moods and colors:

| Mood | Color | Use Case |
|------|-------|----------|
| 🟢 Teal | #1D9E75 | Peaceful, content, grateful |
| 🔵 Blue | #2B6CB0 | Reflective, calm, thoughtful |
| 🟠 Amber | #C47A1E | Energetic, interested, excited |
| 🔴 Coral | #C05337 | Passionate, intense, emotional |
| 🟣 Purple | #5B4DBE | Creative, imaginative, thoughtful |

## 📖 Complete User Flow

1. **Write** - Open the journal, write your thoughts (up to 5000 characters)
2. **Save** - Click "Save entry" button
3. **Watch** - See loading animation as AI analyzes
4. **Review** - Read mood, themes, reflection, and prompt
5. **Explore** - Click sidebar to view past entries
6. **Reflect** - Click any past entry to see full details and insights
7. **Delete** - Remove entries from the modal

## 🔐 Security & Privacy

- ✅ API key stored locally in `.env` (never in code)
- ✅ `.env` is in `.gitignore` (won't be committed)
- ✅ Entries stored locally (in-memory, can add database)
- ✅ No account required (add authentication for cloud)
- ✅ No data sent to anywhere except OpenRouter

## 💡 API Endpoints

All backend API endpoints:

```
GET  /health               - Check server status
POST /entries              - Save journal entry
GET  /entries              - Get all entries
GET  /entries/{id}         - Get specific entry
DELETE /entries/{id}       - Delete entry
POST /insights             - Generate AI analysis
```

Full API documentation in [`backend/README.md`](backend/README.md)

## ⚙️ Customization

### Change the AI Model
Edit `backend/app.py` line 16:
```python
MODEL = 'google/gemini-2.5-flash'  # Change to other OpenRouter model
```

Other options:
- `openai/gpt-4-turbo` - Advanced reasoning
- `anthropic/claude-3-opus` - Great for analysis
- `meta-llama/llama-2-70b-chat` - Open source

### Change AI Behavior
Edit the system prompt in `backend/app.py` to customize how the AI analyzes entries.

### Add Database
Replace in-memory storage with SQLite, PostgreSQL, or MongoDB (see backend README).

### Deploy to Production
See deployment guides in backend README for Railway, Heroku, AWS, etc.

## 🐛 Troubleshooting

### "Something went wrong. Is the backend running?"
- ✓ Check terminal shows "Running on http://0.0.0.0:8000"
- ✓ Verify `.env` file exists in project root
- ✓ Restart backend server

### "Failed to generate insights"
- ✓ Verify API key at https://openrouter.io/keys
- ✓ Check internet connection
- ✓ See backend console for error details

### Port 8000 already in use
Change port in `backend/app.py` and frontend `app.js`

### Insights don't match entry
- ✓ Clear browser cache
- ✓ Restart backend server
- ✓ Check `temperature` setting in backend

See **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for more detailed troubleshooting.

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup in 5 steps
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete feature guide
- **[backend/README.md](backend/README.md)** - Full API documentation
- **[.env.example](.env.example)** - Environment variables template

## 🎓 Learning Resources

This project teaches you:

- ✅ Full-stack web development (frontend + backend)
- ✅ REST API design and implementation
- ✅ Integration with AI/LLM APIs
- ✅ Frontend-backend communication
- ✅ Environment configuration & secrets management
- ✅ Responsive web design
- ✅ Error handling & user feedback

Perfect for learning or as a template for similar projects!

## 🚀 Next Steps

### Phase 2 (Easy)
- [ ] Add database (SQLite or PostgreSQL)
- [ ] Continue entries across browser sessions
- [ ] Export journal as PDF
- [ ] Add entry search/filtering

### Phase 3 (Medium)
- [ ] User authentication (sign up/login)
- [ ] Cloud deployment (Railway, Vercel)
- [ ] Multiple journals/categories
- [ ] Mood trending chart
- [ ] Pattern analysis (what themes appear most?)

### Phase 4 (Advanced)
- [ ] Mobile React Native app
- [ ] Sharing with friends (with permissions)
- [ ] Collaborative journaling
- [ ] Custom AI assistant training
- [ ] Voice journal entries (audio → text)

## 📞 Support

**Issues with OpenRouter API?**
- Docs: https://openrouter.io/docs
- Keys: https://openrouter.io/keys
- Models: https://openrouter.io/models

**Questions about Gemini 2.5 Flash?**
- https://openrouter.io/models/google/gemini-2.5-flash

**Flask documentation?**
- https://flask.palletsprojects.com/

**Stuck?**
- Check error message in browser console (F12)
- Check backend terminal output
- See troubleshooting in SETUP_GUIDE.md

## 📝 License

Open source - modify and use however you like!

## 🙏 Credits

Built with:
- 🔷 Google Gemini AI via OpenRouter
- 🐍 Python & Flask backend
- 🎨 Vanilla CSS for beautiful styling
- ❤️ Passion for journaling and self-reflection

---

**Happy journaling! 📔✨**

Start writing and let AI help you understand yourself better.
