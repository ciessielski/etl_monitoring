from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import asyncio
import nest_asyncio
import slack

#array with descriptions
#array with thresholds

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id,name, createdTime, modifiedTime, mimeType)").execute()
items = results.get('files', [])


files_to_check = []
for name in files_to_check:
    object = next(x for x in results["files"] if x["name"] == name)
    object_name = object["name"]
    object_modifiedTime = object["modifiedTime"]
    datetime_str = str(object_modifiedTime)
    object_modifiedTime
    datetime_object = datetime.strptime(datetime_str.replace("T"," ").replace("Z", "").replace(".000", ""), '%Y-%m-%d %H:%M:%S')
    datetime_object
    datetime.now()
    # tom = datetime(2020, 12, 19, 6, 25, 35, 588020)
    td = datetime.now() - datetime_object
    # td = tom - datetime_object
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    days
    hours
    minutes
    type(days)

    str(datetime.now() - datetime_object)
    # hours_since_modified = int(since_last_modification.seconds/3600)
    since_modified = int(hours)
    since_modified
    report_str = "`" + object_name + "` was updated `" + str(hours) + " h` ago."

    nest_asyncio.apply()
    token = ""
    client = slack.WebClient(token=token)
    # bl = [{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}, {"type": "section", "text": {"type": "plain_text", "text": "Hello world2"}}]
    color = ""
    if days > 0 | hours > 8:
        color = "#d9232e"
        report_str = report_str + " @here"
    else:
        color = "00ce00"
    attch = [{"color": color, "blocks": [{"type": "section", "text": { "type": "mrkdwn", "text": report_str}}]}]

    client.chat_postMessage(channel="", text="", attachments=attch)
