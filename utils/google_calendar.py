from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

# Define the SCOPES your app needs
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_credentials.json', SCOPES)
            creds = flow.run_local_server(port=50001, access_type='offline', prompt='consent')
        
        # Save the new credentials to 'token.json'
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_appointment(date, time, details):
    credentials = get_google_credentials()  # Get credentials using OAuth flow
    service = build('calendar', 'v3', credentials=credentials)

    # Combine the provided date and time into a datetime object
    time_obj = datetime.combine(date, time)  # Use the `date` parameter here
    end_time_obj = time_obj + timedelta(hours=1)  # Add 1 hour to the time

    # Format the times into the correct format for Google Calendar API
    start_time = time_obj.strftime('%Y-%m-%dT%H:%M:%S')  # Format start time
    end_time = end_time_obj.strftime('%Y-%m-%dT%H:%M:%S')  # Format end time

    # Create the event with the adjusted times
    event = {
        'summary': details,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',  # IST timezone
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',  # IST timezone
        },
    }

    # Insert the event into the calendar
    service.events().insert(calendarId='primary', body=event).execute()
    print("Appointment Scheduled!")