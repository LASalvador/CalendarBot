from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES2 = ['https://www.googleapis.com/auth/calendar']
SCOPES1 = ['https://www.googleapis.com/auth/calendar.events']

def listaEventos():
    #Configurando crediciais
    service = configurarCred(SCOPES2)
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


def criaEvento(eventName, year , month , day, hourStart, minutesStart, hourEnd, minutesEnd):

    dateStart = datetime.datetime(year, month, day, hourStart, minutesStart).isoformat()
    dateEnd = datetime.datetime(year, month, day, hourEnd, minutesEnd).isoformat()
    
    service = configurarCred(SCOPES1)

    event = {
      'summary': eventName,
      'start': {
        'dateTime': dateStart,
        'timeZone': 'America/Sao_Paulo',
      },
      'end': {
        'dateTime': dateEnd,
        'timeZone': 'America/Sao_Paulo',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 30},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
    

def alterarEvento(eventName, newName='', newYear='' , newMonth='' , newDay='', newHourStart='', newMinutesStart='', newHourEnd='', newMinutesEnd=''):
    if (not len(eventName)):
        return 0
    
    service = configurarCred(SCOPES2)
    events = service.events().list(calendarId='primary').execute()
    for event in events['items']:
        if event['summary'] == eventName:
            eventoId = event['id']

    event = service.events().get(calendarId='primary', eventId=eventoId).execute()

    event['summary'] = newName
    if (len(newDay) !=0 and len(newYear) !=0 and len(newMonth) !=0):
        dateStart = datetime.datetime(newYear, newMonth, newDay, newHourStart, newMinutesStart).isoformat()
        event['start']['dateTime'] = dateStart
        dateEnd = datetime.datetime(newYear, newMonth, newDay, newHourEnd, newMinutesEnd).isoformat()
        event['end']['dateTime'] = dateEnd

    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    return updated_event.get('htmlLink')

def deletarEvento(eventName):
    
    service = configurarCred(SCOPES1)

    events = service.events().list(calendarId='primary').execute()
    for event in events['items']:
        if event['summary'] == eventName:
            eventoId = event['id']
    service.events().delete(calendarId='primary', eventId=eventoId).execute()
    return None

def selecionarUmEvento(eventName):
    service = configurarCred(SCOPES2)
    events = service.events().list(calendarId='primary').execute()
    for event in events['items']:
        if event['summary'] == eventName:
            return event
    return None
    

def configurarCred(scope):
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
                'credentials.json', scope)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

#import datetime
#b = datetimee.datetime(2017, 11, 28, 23, 55, 59, 342380)
#data = b.isoformat()   
