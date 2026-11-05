# Google Meet Link Generator

Création instantanée de liens **Google Meet** via l'**API Google Calendar** : d'abord un script en ligne de commande, puis une application web full stack (FastAPI + React).

Réalisé pour un **test technique Developer Advocate**. 🎥 [Démo vidéo (3 min)](https://drive.google.com/file/d/1xFQMESQZawqQirDji-qxEX6vZN2UnLrf/view?usp=sharing)

## Fonctionnalités

| Fonctionnalité | Statut |
|---|---|
| Authentification **OAuth 2.0** (flux Desktop) | ✅ |
| Création d'un lien Meet avec titre, heure de début, durée et participants | ✅ |
| Copie automatique dans le presse-papiers | ✅ |
| Liste des réunions à venir | ✅ |
| Interface web responsive (React + Vite) | ✅ |
| API backend (FastAPI) | ✅ |
| Aucun secret dans Git (`credentials.json`, `token.json` ignorés) | ✅ |
| Envoi du lien par e-mail | À venir |
| Réunions récurrentes | À venir |

## Architecture

```
FullstackApp/
├── backend/                 # API FastAPI → http://localhost:8000
│   ├── main.py              # Endpoints : GET /, POST /create, GET /upcoming
│   ├── auth.py              # OAuth 2.0 (repris du CLI)
│   ├── google_calendar.py   # Création et listing des événements avec lien Meet
│   └── requirements.txt
└── frontend/                # React + Vite → http://localhost:3000
    ├── src/App.jsx
    ├── src/components/      # CreateMeeting.jsx, MeetingList.jsx
    └── vite.config.js       # Proxy /api → backend

google-meet-creator/         # Version CLI d'origine (Python)
├── main.py
└── dev-notes.md             # Journal de développement
```

## Stack technique

| Élément | Technologie |
|---|---|
| Backend | Python 3.13, FastAPI, Uvicorn |
| Google | Google Calendar API, google-auth, google-auth-oauthlib, google-api-python-client |
| Frontend | React 18, Vite 5, Axios |

## Installation

### 1. Configurer Google Cloud

1. Ouvrir la [Google Cloud Console](https://console.cloud.google.com/) et créer un projet
2. Activer l'**API Google Calendar**
3. Configurer l'**écran de consentement OAuth** (type *Externe*)
4. Créer un **ID client OAuth** de type *Application de bureau*
5. Télécharger le JSON, le renommer `credentials.json` et le placer dans `FullstackApp/backend/`

### 2. Lancer le backend

```bash
cd FullstackApp/backend
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Lancer le frontend

```bash
cd FullstackApp/frontend
npm install
npm run dev                     # http://localhost:3000
```

### 4. Premier lancement

1. Cliquer sur **Create Meet Link**
2. Le navigateur s'ouvre : se connecter à Google et autoriser l'accès
3. Le fichier `token.json` est créé dans `backend/`
4. Le lien Meet s'affiche, prêt à être copié

## Journal de développement

[`google-meet-creator/dev-notes.md`](google-meet-creator/dev-notes.md) retrace le passage du CLI au web, notamment :

- un bug de `google-auth` avec Python 3.13 (corrigé en épinglant la version `2.27.0`)
- le renommage de `calendar.py` en `google_calendar.py` (conflit avec le module standard)
- la configuration du proxy Vite
- l'utilisation de l'API Clipboard

## Déploiement envisagé

| Partie | Plateforme |
|---|---|
| Frontend | Vercel / Netlify |
| Backend | Render / Railway |

## Auteur

**Yosra Dab** — Ingénieure logiciel Full Stack · [Portfolio](https://yosradab.vercel.app) · [GitHub](https://github.com/yosradab) · [LinkedIn](https://linkedin.com/in/yosradab)
