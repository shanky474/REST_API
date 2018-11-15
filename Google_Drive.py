from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import functools


SCOPES = 'https://www.googleapis.com/auth/drive'


def util(func):
    @functools.wraps(func)
    def common(*args,**kwargs):
        store = file.Storage('gdtoken.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('keys/gdcredentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))
        return func(service,*args,**kwargs)
    return common


@util
def createFolder(service,name,*args,**kwargs):
    file_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    file = service.files().create(body=file_metadata, fields='id').execute()


@util
def listFiles(service):
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))





if __name__ == '__main__':
    createFolder('HelloYou')