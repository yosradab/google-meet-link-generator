from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_meet(service, title, start_time, duration, attendees):
    end_time = start_time + timedelta(minutes=duration)
    event = {
        'summary': title,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
        'conferenceData': {
            'createRequest': {
                'requestId': f"meet-{datetime.now().timestamp()}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
        'attendees': [{'email': e} for e in attendees] if attendees else []
    }

    try:
        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1,
            sendUpdates='all' if attendees else 'none'
        ).execute()
        return {
            'title': event['summary'],
            'start': event['start']['dateTime'],
            'meet_link': event['conferenceData']['entryPoints'][0]['uri'],
            'html_link': event['htmlLink']
        }
    except HttpError as e:
        raise Exception(f"Calendar API error: {e}")

def list_upcoming(service, max_results=10):
    now = datetime.now(timezone.utc).isoformat()
    try:
        events = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])

        return [
            {
                'title': e['summary'],
                'start': e['start'].get('dateTime'),
                'meet_link': e['conferenceData']['entryPoints'][0]['uri']
            }
            for e in events if 'conferenceData' in e
        ]
    except HttpError as e:
        raise Exception(f"List error: {e}")