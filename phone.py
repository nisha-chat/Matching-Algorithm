#from twilio.rest import Client
import phonenumbers

def text(phone_num2, body, text = False):
	# Your Account Sid and Auth Token from twilio.com/console
	# DANGER! This is insecure. See http://twil.io/secure
	if text: 
		account_sid = 'ACa18305b9e39ade90e53ff9873b0a0a9f'
		auth_token = '48d41d795ab2a1faf9eaddf964207699'
		client = Client(account_sid, auth_token)

		message = client.messages.create(body=body,from_='+18187226129',to=phone_num2)

	print('Sending this message: ' + body)
	print('To: ' +  phone_num2)
	print('///////////////////')

def cleanNumber(num):
	x = phonenumbers.parse(num,region="US")
	x = str(x)
	x = x[33:]
	return x

#print(cleanNumber('4237186971'))

