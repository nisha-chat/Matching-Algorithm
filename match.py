import os.path
import os
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/')
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from phone import *
from distance import *
from airtable import Airtable
import re

client_secret = 'usahelpinghands-8b16d1d13352.json'

def main():
	if not os.path.isfile(client_secret):
		print('json file not found')
		sys.exit(1)
	volunteers, matchRequests = getVolMatchRequestDicts()
	for matchAddr in matchRequests:
		closest_volunteers = getClosestThreeVolunteers(matchAddr, volunteers)
		airtableClients = Airtable('appFCRjbeCiFyMZNX', 'Clients')
		clients = get_all(airtableClients)
		id = matchRequests[matchAddr][0]
		matchName = ''
		for client in clients:
			if client['id'] == str(id):
				matchName = client['fields']['Full Name']
		print('Text to: ' + matchName)
		for vol in closest_volunteers:
			volName =  vol[0][0].split()[0].title()
			distance = vol[1]
			phone_num = vol[0][1]
			text('+1' + phone_num, 'Hi ' + volName + '! This is [insert your name] from All Together LA. Thanks so much for signing up to volunteer with us! We have a senior who lives ' + str(distance) + ' minutes from you that needs some help getting groceries, would you be able to help? If so, let me know and I\'ll send over their contact info :)')

def getVolMatchRequestDicts():
	os.environ["AIRTABLE_API_KEY"] = "keylPMRwCflGIr3w7"
	airtableVol = Airtable('appFCRjbeCiFyMZNX','Volunteers')
	volunteers = get_all(airtableVol)
	volAddr = {}
	for row in volunteers:
		row = row['fields']
		if 'Status' not in row and row['Number of Seniors'] != '' and ('# of Seniors Volunteer Can Support' not in row or int(row['Number of Seniors']) < int(row['# of Seniors Volunteer Can Support'])):
			if 'Address' in row and 'Zip Code' in row:
				key = row['Address'] + " " + str(row['Zip Code'])
			elif 'Address' in row:
				key = row['Address']
			elif 'Zip Code' in row:
				key = str(row['Zip Code'])
			key = key.strip()
			key = key.replace('#', 'no. ')
			key = key.replace(" ", "+")
			if 'Phone' in row:
				phone_num = cleanNumber(str(row['Phone']))
				volAddr[key] = [row['Name'], phone_num]

	matchRequests = {}
	airtableMatch = Airtable('appFCRjbeCiFyMZNX','Jobs')
	airtableClients = Airtable('appFCRjbeCiFyMZNX', 'Clients')
	matches =  get_all(airtableMatch)
	clients = get_all(airtableClients)
	for row in matches:
		row = row['fields']
		if 'Status' in row and row['Status'] == 'Ready for Volunteer':
			if 'Address' in row and 'Zip' in row:
				key = row['Address'][0] + " " + str(row['Zip'])
			elif 'Address' in row:
				key = row['Address'][0]
			elif 'Zip' in row:
				key = str(row['Zip'])
			key = key.strip()
			key = key.replace('#', 'no. ')
			key = key.replace(" ", "+")
			if 'Phone Number' in row:
				phone_num = cleanNumber(str(row['Phone Number']))
				matchRequests[key] = (row['Client'][0], phone_num)
	return (volAddr, matchRequests)


def get_client():
	Airtable('base_key', 'table_name')
	scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)
	client = gspread.authorize(creds)
	return client

def get_all(sheet):
	results = sheet.get_all()
	return results

if __name__ == '__main__':
  main()