# 🚀 Startup Instructions - Step by Step

Follow these exact steps to get your AI journal running in under 5 minutes.

---

## STEP 1: Get OpenRouter API Key (1 minute)

### 1.1 Visit OpenRouter
Open this link in your browser:
```
https://openrouter.io/keys
```

### 1.2 Sign Up (or Login)
- Click "Sign Up" if you don't have an account (takes ~1 minute)
- Enter email and password
- Verify email

### 1.3 Create API Key
- Click blue "Create Key" button
- A new key starting with `sk_` will appear
- **Copy the entire key** (click the copy button)

### 1.4 Save It Temporarily
Paste it somewhere safe for now - you'll use it in a moment.

---

## STEP 2: Install Python Dependencies (1 minute)

### 2.1 Open PowerShell/Terminal
Open Windows PowerShell as administrator.

### 2.2 Navigate to Project
```powershell
cd "C:\Users\CHIEMELIE\OneDrive\Desktop\PythonClass\casemeiro web class\First AI journal"
```

### 2.3 Install Backend Requirements
```powershell
cd backend
pip install -r requirements.txt
```

Wait for it to finish (should show `Successfully installed Flask`, `Flask-CORS`, etc.)

---

## STEP 3: Create .env File (30 seconds)

### 3.1 Create File
In the project root directory (not in backend), create a new file called `.env`

The file should contain:
```
OPENROUTER_API_KEY=sk_PASTE_YOUR_KEY_HERE
```

**Replace `sk_PASTE_YOUR_KEY_HERE`** with the actual key you copied from step 1.3

### 3.2 Save File
Save the file. It should be located here:
```
C:\Users\CHIEMELIE\OneDrive\Desktop\PythonClass\casemeiro web class\First AI journal\.env
```

**Important**: The `.env` file has NO file extension (not `.txt`, not `.env.txt`, just `.env`)

---

## STEP 4: Start Backend Server (30 seconds)

### 4.1 Open PowerShell Terminal 1
Make sure you're in the backend folder:
```powershell
# You should already be here from Step 2
cd "C:\Users\CHIEMELIE\OneDrive\Desktop\PythonClass\casemeiro web class\First AI journal\backend"
```

### 4.2 Start Flask Server
```powershell
python app.py
```

### 4.3 Wait for "Running" Message
You should see:
```
Starting AI Journal Backend...
OpenRouter API Key configured: True
Using model: google/gemini-2.5-flash
 * Running on http://0.0.0.0:8000
 * Press CTRL+C to quit
```

**✅ If you see this, the backend is working!**

---

## STEP 5: Start Frontend Server (30 seconds)

### 5.1 Open PowerShell Terminal 2 (NEW TERMINAL)
Open a NEW PowerShell window (don't close the first one).

### 5.2 Navigate to Frontend
```powershell
cd "C:\Users\CHIEMELIE\OneDrive\Desktop\PythonClass\casemeiro web class\First AI journal\frontend"
```

### 5.3 Start Web Server
```powershell
python -m http.server 3000
```

### 5.4 Wait for "Serving" Message
You should see:
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

**✅ If you see this, the frontend is ready!**

---

## STEP 6: Open Journal in Browser (10 seconds)

### 6.1 Open Your Browser
- Chrome
- Firefox
- Edge
- Safari
- Any browser

### 6.2 Go to This URL
```
http://localhost:3000/index.html
```

### 6.3 You Should See
A beautiful journal interface with:
- "What happened today?" prompt
- Large text area for writing
- "Save entry" button
- Empty sidebar (no past entries yet)

**🎉 YOU'RE DONE! Your AI Journal is Ready!**

---

## STEP 7: Test It Out (2 minutes)

### 7.1 Write Something
Click the text area and write a journal entry. Example:
```
Today was a really good day! I finished a big project at work 
and got great feedback from my team. Feeling accomplished and 
excited about what's next. Also managed to go to the gym, which 
made me feel energized.
```

### 7.2 Click "Save entry"
Click the blue "Save entry" button.

### 7.3 Watch It Load
You'll see:
1. "Saving…" in the button
2. Loading skeletons appear below (animated gray bars)
3. After ~1 second: AI insights appear!

### 7.4 You'll See AI Analysis
- **Mood**: A colored dot showing your emotional state
- **Key themes**: #hashtags showing what the AI found
- **Reflection**: What the AI thinks about your entry
- **Prompt**: A question to help you reflect deeper

### 7.5 Try the Sidebar
- Click the hamburger menu (≡) at top left
- You'll see your entry in "Past entries"
- Click it to see full details in the modal
- You can delete it using the "Delete entry" button

---

## ✅ Troubleshooting Quick Fixes

### Problem: "Something went wrong. Is the backend running?"

**Solution**: 
1. Check Terminal 1 shows "Running on http://0.0.0.0:8000"
2. If not, restart it:
   - Press `CTRL+C` in Terminal 1
   - Run `python app.py` again

### Problem: "API key not configured"

**Solution**:
1. Check `.env` file exists in project root
2. Check it contains: `OPENROUTER_API_KEY=sk_...`
3. Restart backend (CTRL+C, then `python app.py`)

### Problem: Browser shows error about localhost:3000

**Solution**:
1. Check Terminal 2 shows "Serving HTTP on 0.0.0.0 port 3000"
2. Try refresh (F5 or CTRL+R)
3. Try different browser

### Problem: API key was rejected

**Solution**:
1. Go to https://openrouter.io/keys
2. Create a NEW key
3. Update `.env` file with new key
4. Restart backend

---

## 📋 Quick Reference

### Keep Two Terminals Open
- **Terminal 1**: Backend (python app.py)
- **Terminal 2**: Frontend (python -m http.server 3000)

### URLs You Need

| What | URL |
|------|-----|
| Journal | http://localhost:3000/index.html |
| OpenRouter Keys | https://openrouter.io/keys |
| Backend Health | http://localhost:8000/health |

### Files You Need to Edit
- `.env` - Add your API key here
- That's it! Everything else is pre-configured.

### Commands You Need
```powershell
# Terminal 1 - Backend
cd "C:\Users\CHIEMELIE\OneDrive\Desktop\PythonClass\casemeiro web class\First AI journal\backend"
python app.py

# Terminal 2 - Frontend
cd "C:\Users\CHIEMELIE\OneDrive\Desktop\PythonClass\casemeiro web class\First AI journal\frontend"
python -m http.server 3000
```

---

## 🎓 Understanding What's Happening

### When You Write & Save:
1. Your text is sent to Flask backend
2. Backend stores it with timestamp
3. Backend sends it to OpenRouter API
4. OpenRouter sends to Google Gemini
5. Gemini analyzes for mood, themes, etc.
6. Results come back as JSON
7. Frontend displays beautiful insights

### The AI Looks For:
✅ **Mood** - Your emotional state (teal, blue, amber, coral, purple)
✅ **Themes** - Main topics in your writing
✅ **Reflection** - Compassionate insight about your thoughts
✅ **Prompt** - A question for deeper thinking

---

## 🎉 Success Checklist

- [ ] Created `.env` file with API key
- [ ] Ran `pip install -r requirements.txt` successfully
- [ ] Terminal 1 shows "Running on http://0.0.0.0:8000"
- [ ] Terminal 2 shows "Serving HTTP on 0.0.0.0 port 3000"
- [ ] Browser shows journal interface at localhost:3000
- [ ] Wrote test entry
- [ ] Clicked "Save entry"
- [ ] AI insights appeared within 1 second
- [ ] Can see past entry in sidebar
- [ ] Can click past entry to see details

**If all checkmarks are done: 🎊 YOU'RE READY TO JOURNAL!**

---

## Next Adventures

Once you're comfortable with the basic setup:

1. **Customize AI** - Edit system prompt in `backend/app.py`
2. **Try Other Models** - Change model name in `backend/app.py` line 16
3. **Deploy** - Put it online using Vercel (frontend) + Railway (backend)
4. **Add Database** - Store entries permanently (beyond server restarts)
5. **Add Authentication** - Let multiple users have their own journals

See documentation files for detailed guides on each of these.

---

## 📞 Need Help?

1. **Check error messages** - They're usually helpful
2. **Read SETUP_GUIDE.md** - Has detailed troubleshooting
3. **Check backend console** - Terminal 1 shows detailed errors
4. **Check browser console** - Press F12 in browser

---

**Ready? Let's go! 🚀 Follow Steps 1-6 above, then start writing! ✍️**
