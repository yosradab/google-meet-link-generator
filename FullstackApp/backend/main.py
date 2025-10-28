from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import pytz

from auth import get_credentials
from google_calendar import create_meet,list_upcoming
from googleapiclient.discovery import build

app = FastAPI(title="Google Meet Web Generator")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateMeetingRequest(BaseModel):
    title: str
    start_in_minutes: int = 5
    duration: int = 30
    attendees: list = []

@app.get("/")
def home():
    return {"message": "Google Meet Web API - Use /create and /upcoming"}

@app.post("/create")
def create_meeting(req: CreateMeetingRequest):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    start_time = datetime.now(pytz.UTC) + timedelta(minutes=req.start_in_minutes)

    try:
        result = create_meet(
            service=service,
            title=req.title,
            start_time=start_time,
            duration=req.duration,
            attendees=req.attendees
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/upcoming")
def get_upcoming():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    try:
        return list_upcoming(service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))