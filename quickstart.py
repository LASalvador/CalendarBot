from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES2 = ['https://www.googleapis.com/auth/calendar']

def listaEventos():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    print('[main - INICIO]')

    service = configurarCred()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def criaEvento():
    
    service = configurarCred()

    event = {
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2015-05-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2015-05-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    link = event.get('htmlLink')
    print(f'Event created: {link}')

def alterarEvento():
    service = configurarCred()
    events = service.events().list(calendarId='primary').execute()
    for event in events['items']:
        if event['summary'] == "Google I/O 2015":
            eventoId = event['id']

    event = service.events().get(calendarId='primary', eventId=eventoId).execute()

    event['summary'] = 'Mudei essa porra'
    
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    print(updated_event['updated'])

def deletarEvento():
    
    service = configurarCred()

    events = service.events().list(calendarId='primary').execute()
    for event in events['items']:
        if event['summary'] == "Google I/O 2015":
            eventoId = event['id']
    service.events().delete(calendarId='primary', eventId=eventoId).execute()
    return None        
def selecionarUmEvento():
    service = configurarCred()
    events = service.events().list(calendarId='primary').execute()
    for event in events['items']:
        if event['summary'] == "Trabalho de estrutura de dados":
            print(event)

    

def configurarCred():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES2)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


