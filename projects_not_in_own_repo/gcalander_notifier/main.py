"""
Calander API stuff ripped from https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""
import datetime
import pickle
import os.path
import pytz
import tkinter as tk
from  dateutil import parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

utc=pytz.UTC

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'client_secret_307417093131-435eeuus7qvsftss10ll2sr73f7hiuuu.apps.googleusercontent.com.json'

def get_calendar_service():
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
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service



def main():
    service = get_calendar_service()
    # Call the Calendar API
    print('Getting list of calendars')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])

    if not calendars:
       print('No calendars found.')
    for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""
       print("%s\t%s\t%s" % (summary, id, primary))


    events_str = list()

    # Call the Calendar API
    now_datetime = datetime.datetime.utcnow()
    now = now_datetime.isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = parser.parse(start)
        if (utc.localize(now_datetime) + datetime.timedelta(minutes = 5) >= start_date):
            description = "\n"
            if 'description' in event:
                description = "\n{}\n\n".format(event['description'])
            events_str.append("{}: {} {}".format(start, event['summary'], description))

    if len(events_str):
        def close():
            window.quit()

        window = tk.Tk()
        window.attributes('-topmost', True)
        greeting = tk.Label(text="CALANDER EVENTS IMMINANT\n\n\n{}".format(
            "\n".join(events_str)
        ))
        greeting.pack()
        window.attributes('-fullscreen', True)
        button = tk.Button(window, text="Acknolwedge", command=close)
        button.pack()
        window.mainloop()

if __name__ == '__main__':
   main()


