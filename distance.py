import requests, json 

api_key ='AIzaSyCo9ixCxYM5pDJQe88YSawWHx84AqvSLzc'
 
# Returns minutes distance between addresses
# Return -1 if request returns invalid value
def getDistanceFromCoordinates(volunteer, match):
	url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
	request_url = url + 'key=' + api_key + '&origins=' + volunteer + '&destinations=' + match
	r = requests.get(request_url) 
	# json method of response object 
	# return json format result 
	try:
		minutes = r.json()['rows'][0]['elements'][0]['duration']['value'] / 60
	except:
		print(r.json())
		minutes = -1

	return int(minutes)

# match: tuple (key, value)
# volunteerMap: (key -> value)
# key: address, value: name + phone number
def getClosestThreeVolunteers(match, volunteerMap):
	minDist = 1000
	# ranked list of volunteers 
	volunteerMinutes = [1000, 1001, 1002]
	volunteerInfo = [(('',''), 0), (('',''), 0), (('',''), 0)]
	volCount = 0
	for key in volunteerMap:
		volCount += 1
		dist = getDistanceFromCoordinates(key, match)
		if dist != -1:
			for i in range(3):
				if dist < volunteerMinutes[i]:
					volunteerMinutes[i] = dist
					volunteerInfo[i] = (volunteerMap[key], dist)
					break
		else:
			print('could not find distance between: (' + match + ', ' + key)
	return volunteerInfo

  
