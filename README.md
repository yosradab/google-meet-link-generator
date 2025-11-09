# Google Meet Web Generator  
**Instant Google Meet Links via Calendar API – CLI to Full-Stack Web App**

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120.1-009688)](https://fastapi.tiangolo.com/)
[![React + Vite](https://img.shields.io/badge/React%20%2B%20Vite-18.2.0-61DAFB)](https://vitejs.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Developer Advocate Test Submission** – From a CLI script to a production-ready **web dashboard** that creates Google Meet links programmatically using the **Google Calendar API**.

---

## Features

| Feature | Status |
|-------|--------|
| Check **OAuth 2.0 Desktop Flow**  | Done |
| Check **Create Meet Link** with title, time, duration, attendees | Done |
| Check **Auto-Copy to Clipboard** | Done |
| Check **List Upcoming Meets** (real-time refresh) | Done |
| Check **Responsive Web UI** (React + Vite) | Done |
| Check **Backend API** (FastAPI) | Done |
| Check **No Secrets in Git** (`token.json`, `credentials.json` ignored) | Done |
| Check **Python 3.13 Compatible** | Done |

---

## Project Structure

```
FullstackApp/
├── backend/
│   ├── main.py               # FastAPI endpoints
│   ├── auth.py               # OAuth 2.0 (reused from CLI)
│   ├── google_calendar.py    # Event creation + listing
│   ├── requirements.txt      # Python deps
│   └── credentials.json      # ← YOU ADD THIS (ignored)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main layout
│   │   └── components/
│   │       ├── CreateMeeting.jsx
│   │       └── MeetingList.jsx
│   ├── package.json
│   └── vite.config.js        # Proxy to backend
│
├── README.md                 # ← You are here
└── .gitignore

google-meet-creator/          
├── .gitignore                # Git ignore rules
├── pycache/                  # Python bytecode cache (auto-generated)
├── README.md                 # Project documentation
├── dev-notes.md              # Developer diary (REQUIRED)
├── main.py                   # backend entry point
├── requirements.txt          # Python dependencies
└── README.md 

```
## Quick Start (Windows)

### 1. **Clone & Setup**

```powershell
git clone https://github.com/yosradab/google-meet-link-generator.git
cd google-meet-link-generator
```

### 2. **Google Cloud Setup**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable **Google Calendar API**
3. **OAuth Consent Screen** → External → Fill required → Save
4. **Credentials** → Create OAuth Client ID → **Desktop Application**
5. Download JSON → Rename to `credentials.json` → Place in `backend/`

> Warning: `credentials.json` is **ignored by Git** – safe to share repo.

### 3. **Backend (FastAPI)**

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port=8000
```

### 4. **Frontend (React + Vite)**

```powershell
cd ../frontend
npm install
npm run dev
```

### 5. **Open App**

Visit: [http://localhost:3000](http://localhost:3000)

---

## First Run: OAuth Flow

1. Click **"Create Meet Link"**
2. Browser opens → Google login → **Allow**
3. `token.json` created in `backend/` (auto-saved)
4. **Meet link appears + copy button works!**

## Developer Diary

See: dev-notes.md – Full journey from CLI to web, including:

- Python 3.13 `google-auth` bug (fixed with `==2.27.0`)
- `calendar.py` → `google_calendar.py` (naming conflict)
- `timedelta` missing import
- Vite proxy setup
- Clipboard API usage

---

## Bonus Improvements

| Idea | Implemented? |
|------|--------------|
| Check **Add Attendees** (comma-separated emails) | Done |
| Check **List Upcoming Meets** | Done |
| Check **Copy to Clipboard** | Done |
| **Send via Email** | Future |
| **Recurring Events** | Future |

---


## Deployment (Future)

| Part | Platform |
|------|----------|
| Frontend | [Vercel](https://vercel.com) / Netlify |
| Backend | [Render](https://render.com) / Railway |

---



**Want the ZIP?** → Run this:

```powershell
Compress-Archive -Path * -DestinationPath ..\google-meet-web-submission.zip -Exclude venv,node_modules,credentials.json,token.json
```






