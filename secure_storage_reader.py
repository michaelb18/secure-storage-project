from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
class SecureStorageDatabase:
	def __init__(self,sheet_id='1rjKDa-Hww2HJNnt8jB5jJhyWlMDrmdrsled9qpoLzSY',scop='https://www.googleapis.com/auth/spreadsheets'):
		self.id=sheet_id
		self.scope=scop
		store = file.Storage('token.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
			creds = tools.run_flow(flow, store)
		self.service = build('sheets', 'v4', http=creds.authorize(Http()))
	def read(self,bitrange,inoutrange):
		sheet = self.service.spreadsheets()
		bits = sheet.values().get(spreadsheetId=sheet_id,
									range=bitrange).execute()
		io=sheet.values().get(spreadsheetId=sheet_id,range=inoutrange).execute()								
		bitvalues = bits.get('values', [])
		iovalues = io.get('values',[])
		return bitvalues,iovalues
	def takeOutBit(self,bitnumber):
		values = [
			['FALSE']
		]
		body = {
			'values': values
		}
		inRange='B'+str(bitnumber)
		result = self.service.spreadsheets().values().update(
			spreadsheetId=sheet_id, range=inRange,
			valueInputOption='RAW', body=body).execute()	
	def returnBit(self,bitnumber):
		values = [
			['TRUE']
		]
		body = {
			'values': values
		}
		inRange='B'+str(bitnumber)
		result = self.service.spreadsheets().values().update(
			spreadsheetId=sheet_id, range=inRange,
			valueInputOption='RAW', body=body).execute()	

def main():
	
	s=SecureStorageDatabase()
	bits,stats=s.read('A2:A5','B2:B5')
	print(bits,stats)
	s.takeOutBit(2)
	s.returnBit(3)
if __name__ == '__main__':
	main()