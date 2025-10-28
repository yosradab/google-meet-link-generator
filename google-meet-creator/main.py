
import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes required for creating calendar events
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate():
    """
    Handles OAuth 2.0 authentication flow.
    Returns authenticated credentials.
    """
    creds = None
    
    # Check if we have saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("✓ Authentication successful!\n")
    
    return creds

def create_meet_event(service, title, start_time, duration_minutes, attendees=None):
    """
    Creates a Google Calendar event with a Meet link.
    
    Args:
        service: Authenticated Calendar API service
        title: Event title
        start_time: datetime object for event start
        duration_minutes: Duration in minutes
        attendees: List of email addresses (optional)
    
    Returns:
        Dictionary with event details and Meet link
    """
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    # Build event body
    event = {
        'summary': title,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f"meet-{datetime.now().timestamp()}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
    }
    
    # Add attendees if provided
    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]
    
    try:
        # Create event with conferenceDataVersion=1 to generate Meet link
        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1,
            sendUpdates='all' if attendees else 'none'
        ).execute()
        
        return {
            'id': event['id'],
            'title': event['summary'],
            'start': event['start']['dateTime'],
            'end': event['end']['dateTime'],
            'meet_link': event['conferenceData']['entryPoints'][0]['uri'],
            'html_link': event['htmlLink'],
            'attendees': [a['email'] for a in event.get('attendees', [])]
        }
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def list_upcoming_meetings(service, max_results=5):
    """
    Lists upcoming calendar events with Meet links.
    
    Args:
        service: Authenticated Calendar API service
        max_results: Maximum number of events to return
    
    Returns:
        List of upcoming events with Meet links
    """
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        meet_events = []
        
        for event in events:
            if 'conferenceData' in event:
                meet_events.append({
                    'title': event['summary'],
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'meet_link': event['conferenceData']['entryPoints'][0]['uri']
                })
        
        return meet_events
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def main():
    """Main function to demonstrate Meet link creation"""
    print("=" * 60)
    print("Google Meet Link Generator")
    print("=" * 60)
    print()
    
    # Authenticate
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)
    
    # Create a sample meeting
    print("Creating a sample meeting...")
    start_time = datetime.now() + timedelta(hours=1)
    
    meeting = create_meet_event(
        service=service,
        title="Team Sync - Demo Meeting",
        start_time=start_time,
        duration_minutes=30,
        attendees=None  # Add emails like ['alice@example.com'] to test
    )
    
    if meeting:
        print("\n✓ Meeting created successfully!")
        print("-" * 60)
        print(f"Title:      {meeting['title']}")
        print(f"Start:      {meeting['start']}")
        print(f"End:        {meeting['end']}")
        print(f"Meet Link:  {meeting['meet_link']}")
        print(f"Calendar:   {meeting['html_link']}")
        print(f"Event ID:   {meeting['id']}")
        if meeting['attendees']:
            print(f"Attendees:  {', '.join(meeting['attendees'])}")
        print("-" * 60)
    
    # List upcoming meetings
    print("\n\nFetching upcoming meetings with Meet links...")
    upcoming = list_upcoming_meetings(service, max_results=5)
    
    if upcoming:
        print(f"\nFound {len(upcoming)} upcoming meeting(s):")
        print("-" * 60)
        for i, evt in enumerate(upcoming, 1):
            print(f"{i}. {evt['title']}")
            print(f"   Start: {evt['start']}")
            print(f"   Link:  {evt['meet_link']}\n")
    else:
        print("No upcoming meetings found with Meet links.")
    
    print("\n✓ Demo complete!")

if __name__ == '__main__':
    main()