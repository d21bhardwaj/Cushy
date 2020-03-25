import requests
from django.conf import settings
OTP_KEY = settings.OTP_KEY

def otp_send(mobile):
	url= "https://2factor.in/API/V1/"+str(OTP_KEY)+"/SMS/+91"+str(mobile)+"/AUTOGEN"
	response = requests.post(url)
	#{ "Status": "Success", "Details": "5D6EBEE6-EC04-4776-846D"}
	#print(response.json()['Details'])
	return response.json()['Details']

def otp_recieve(session_id,otp):
	url = "https://2factor.in/API/V1/"+str(OTP_KEY)+"/SMS/VERIFY/"+str(session_id)+"/"+str(otp)
	response = requests.post(url)
	#{ "Status": "Success", "Details": "OTP Matched" }
	return response.json()['Details']
