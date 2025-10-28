Developer Diary: Google Meet Link Generator - From CLI to Full-Stack Web
Project Overview
Started with a CLI tool (main.py) for programmatic Google Meet creation via Calendar API. Goal: Extend to a web dashboard for teams, reusing CLI logic for coherence. 
Day 1: CLI Foundation (Recap)

Approach: Used Google Calendar API v3 (no standalone Meet API—links generated via conferenceData). Enabled API in Google Cloud, created OAuth Desktop app, downloaded credentials.json.
Key Decisions: calendar.events scope (least privilege). InstalledAppFlow for local auth. Unique requestId with timestamp to avoid duplicates.
Issues Solved:

No Meet link: Added conferenceDataVersion=1 (critical param).
Token re-auth: Saved token.json, auto-refresh with creds.refresh(Request()).
Timezone: Used America/New_York (configurable later).
Deprecation: datetime.utcnow() → datetime.now(timezone.utc).


Resources: Google Calendar API Quickstart , Conference Data Docs, Stack Overflow threads on Meet creation.

Improvement in CLI: Added list_upcoming_meetings() to filter/show Meet-enabled events—bonus for visibility.
Day 2: Web Extension

Approach: Backend: FastAPI for /create and /upcoming endpoints, reusing auth.py and calendar.py logic. Frontend: React/Vite for interactive form + list, with Axios proxy via Vite config. Coherent with CLI: Same auth/event functions, but web adds UI polish (clipboard copy via navigator.clipboard).
Key Decisions: CORS middleware for localhost. UTC timezone for simplicity. Pydantic for request validation.
Issues Solved:

Import conflict: Renamed calendar.py → google_calendar.py (shadowed built-in calendar module).
Python 3.13 bug: Pinned google-auth==2.27.0 to avoid circular import in _helpers.copy_docstring.
Proxy errors: Vite config rewrites /api to backend port 8000.
Missing import: Added timedelta in main.py.
Dependencies: Added packaging, cryptography after ModuleNotFoundError.


Resources: FastAPI Docs, Vite Proxy Guide, GitHub gists for Calendar quickstarts .

Bonus Improvement: Automatic clipboard copy + attendee invites (from CLI). Web UI shows results with copy button; emails get invites via sendUpdates='all'.
Lessons Learned:

API integration: Meet is Calendar feature—conferenceDataVersion=1 is key.
Debugging: Naming conflicts (e.g., calendar.py) cause subtle circular imports.
Full-stack: Reuse CLI logic saves time; web adds UX (e.g., real-time list refresh).
Google Cloud: Enable Calendar API, create OAuth Desktop app, download credentials.json to backend/.
Backend: cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --port=8000.
Frontend: cd frontend && npm install && npm run dev.
Open http://localhost:3000. First run triggers OAuth.

One-Click (Windows): Run start.ps1 (creates terminals for both).