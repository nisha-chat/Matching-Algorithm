import requests, json 

api_key ='AIzaSyBTUUu3JBhGZtLNz_k8ScwlqwtTyyWg1qc'
 
# Returns minutes distance between coordinates
# Return -1 if request returns invalid value
def getDistanceFromCoordinates(volunteer, match):
	url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
 
	r = requests.get(url + 'origins = ' + volunteer +
                   '&destinations = ' + match +
                   '&key = ' + api_key) 
                     	
	r = requests.get(url + 'origins=' + volunteer +
                   '&destinations=' + match +
                   '&key=' + api_key) 
	# json method of response object 
	# return json format result 
	try:
		minutes = r.json()['rows'][0]['elements'][0]['duration']['value'] / 60
	except:
		minutes = -1

	return minutes


  
