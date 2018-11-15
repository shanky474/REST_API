import pandas as pd
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SAMPLE_SPREADSHEET_ID = '1n7db-pgjgamJDsNG32vBgXxjXGQeSPU1dEWE3C1kfJg'
SAMPLE_RANGE_NAME = 'Sheet1'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('keys/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    df=pd.DataFrame(values[1:], columns=values[0])
    print(df['Candidate Name'])


if __name__ == '__main__':
    main()