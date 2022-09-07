"""
Calander API stuff ripped from https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

https://blog.salrashid.dev/articles/2021/cloud_sdk_missing_manual/override_trust_certificates_for_tls/
https://googleapis.dev/python/google-auth/latest/reference/google.auth.transport.grpc.html
"""
import datetime
import pickle
import time
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
   # If you are behind an HTTPS proxy look for your cert file in cat /etc/ssl/certs
   # and copy it into the file printed out below... VERY HACKY bute cant be arsed to do
   # better
   import certifi
   print(certifi.where()) ##<< COPY AND PASTE THE ZSCALER CERRTICIATE FROM HERE

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
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service



def main(silenced):
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
    events_tag = list()

    # Call the Calendar API
    now_datetime = datetime.datetime.utcnow()
    now = now_datetime.isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        if event['etag'] in silenced:
            print("**** event ID was silenced {} ****".format(event['etag']))
        else:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_date = parser.parse(start)
            if (utc.localize(now_datetime) + datetime.timedelta(minutes = 5) >= start_date):
                print("**** event ID will start soon {} ****".format(event['etag']))
                description = "\n"
                if 'description' in event:
                    description = "\n{}\n\n".format(event['description'])
                print("**** event ID being added to alert list {} ****".format(event['etag']))
                events_str.append("{}: {} {}".format(start, event['summary'], description))
                events_tag.append(event['etag'])

    if len(events_str):
        def close():
            window.quit()
            window.destroy()

        def silence(tag):
            silenced.add(tag)
            close()

        window = tk.Tk()
        window.attributes('-topmost', True)
        greeting = tk.Label(text="CALANDER EVENTS IMMINANT\n\n\n{}".format(events_str[0]))
        greeting.pack()
        window.attributes('-fullscreen', True)
        button = tk.Button(window, text="Silence", command=lambda: silence(events_tag[0]))
        button.pack()
        button = tk.Button(window, text="Sleep", command=close)
        button.pack()

        if len(events_str) > 1:
            greeting = tk.Label(text="\n\nThere are more events pending after this:\n\n{}".format(
                "\n* ".join(events_str[1:]))
            )
            greeting.pack()

        window.mainloop()

if __name__ == '__main__':
    import fcntl
    import os
   
    # Will throw if cannot lock the file and abort - makes sure only one instance runs
    handle = os.open("LOCK_FILE.LOCK", os.O_RDONLY)
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
   
    silenced = set()

    while True:
        main(silenced)
        print(silenced)
        time.sleep(10) # Every minute



