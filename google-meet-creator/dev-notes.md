# **Developer Diary**  
## *Google Meet Link Generator – From CLI to Full-Stack Web*  
**Full-Stack Productivity Tool | Google Calendar API | OAuth 2.0 | FastAPI + React**



| **Author** | Yosra Dab |
|------------|------------------|
| **GitHub** | [github.com/yosradab/google-meet-link-generator](https://github.com/yosradab/google-meet-link-generator) |
| **Video Demo** | [3-Min Walkthrough](https://drive.google.com/file/d/1xFQMESQZawqQirDji-qxEX6vZN2UnLrf/view?usp=sharing) |
| **Status** | **COMPLETE – Production-Ready** |

---

## Project Goal
> **No more Calendar UI clicking.**  
> Instantly generate **Google Meet links** with **title, time, duration, and attendees** — via **API**.

**Evolution**:  
CLI Script → **Full-Stack Web Dashboard** (FastAPI + React/Vite)

---

## Day 1: CLI Foundation

### Key Discovery
> **Google Meet ≠ Standalone API**  
> Meet links are **Calendar events** with `conferenceData`

| Critical Param | Purpose |
|----------------|--------|
| `conferenceDataVersion=1` | **Triggers Meet link** |
| `requestId` | Must be **unique per call** |

### Google Cloud Setup
1. Enabled **Calendar API**  
2. Created **OAuth Desktop App**  
3. Downloaded `credentials.json`  
4. Scope: `calendar.events` (least privilege)




### Challenges Solved
| Bug | Fix |
|-----|-----|
| No Meet link | Added `conferenceDataVersion=1` |
| Re-auth every run | Saved `token.json` + auto-refresh |
| Timezone bugs | `datetime.now(timezone.utc)` |

**Bonus**: `list_upcoming_meetings()` → filters Meet events

---

## Day 2: Full-Stack Web Dashboard

### Architecture
```
backend/ (FastAPI) → /create, /upcoming
frontend/ (React + Vite) → Form + Real-Time List
```

### Backend (`main.py`, `auth.py`, `google_calendar.py`)
- **Renamed** `calendar.py` → `google_calendar.py` (**fixed import conflict**)
- Endpoints:
  - `POST /create` → title, time, attendees
  - `GET /upcoming` → next 10 Meet events
- **100% reused CLI logic**

### Frontend (`CreateMeeting.jsx`, `MeetingList.jsx`)
| Feature | Implementation |
|--------|----------------|
| **Form** | Title, minutes, duration, attendees |
| **Result** | Meet link + **Copy button** |
| **List** | Auto-refresh on create |

```js
// Vite Proxy
proxy: { '/api': 'http://localhost:8000' }
```

---

## Day 3: Real-World Debugging

| Bug | Root Cause | Fix |
|-----|-----------|-----|
| `uvicorn` crash | `venv` path broken | `Remove-Item venv -Recurse && python -m venv venv` |
| `ImportError: calendar` | Shadowed built-in | Renamed to `google_calendar.py` |
| `NameError: timedelta` | Missing import | `from datetime import timedelta` |
| Python 3.13 crash | `google-auth` circular import | Pinned `google-auth==2.27.0` |
| `ECONNREFUSED` | Proxy error | Vite config + CORS |
| `ModuleNotFoundError` | Missing deps | Added `packaging`, `cryptography` |

**Every fix = a lesson** — **teachable debugging**

---

## Bonus Features (Beyond Brief)

| Feature | Status |
|--------|--------|
| **Attendee invites** | `sendUpdates='all'` |
| **Clipboard copy** | `navigator.clipboard` |
| **Real-time list** | Auto-refresh |
| **Responsive UI** | Mobile-friendly |
| **One-click start** | `start.ps1` |

---

## Resources

- [Calendar API Quickstart](https://developers.google.com/calendar/api/quickstart/python)
- [Conference Data Docs](https://developers.google.com/calendar/api/v3/reference/events/insert)
- [FastAPI](https://fastapi.tiangolo.com)
- [Vite Proxy](https://vitejs.dev/config/#server-proxy)

---

## Lessons Learned

| Insight | Takeaway |
|--------|--------|
| **Meet = Calendar** | `conferenceDataVersion=1` is key |
| **Naming matters** | `calendar.py` = disaster |
| **Reuse = win** | CLI → Web in **<2 hours** |
| **Debugging = teaching** | Every error = a story |

---

## Production Ready

| Item | Status |
|------|--------|
| `.gitignore` (secrets) | Done |
| Pinned `requirements.txt` | Done |
| Responsive UI | Done |
| Error handling | Done |
| Deployable (Vercel + Render) | Done |

---

## Final Demo (3:12 Video)

1. **CLI Run** → OAuth → Meet link  
2. **Web App** → Form → Create → Copy → List updates  
3. **Show `dev-notes.md`** → Scroll bugs/fixes  
4. **End**: “I teach through code. Let’s make APIs magical.”

---

## File Structure
```
google-meet-link-generator/
├── backend/
│   ├── main.py, auth.py, google_calendar.py
│   ├── requirements.txt
│   └── credentials.json (ignored)
├── frontend/
│   ├── src/components/
│   │   ├── CreateMeeting.jsx
│   │   └── MeetingList.jsx
│   ├── package.json, vite.config.js
├── README.md
└── .gitignore
```

---


**AUTHOR**:Yosra Dab
**EMAIL**: Dabyosra@gmail.com
**STATUS**: **COMPLETE **
