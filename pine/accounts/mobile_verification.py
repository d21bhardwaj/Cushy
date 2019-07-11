import requests

def otp_send(mobile):
	url= "https://2factor.in/API/V1/9fd7dc0c-9a31-11e9-ade6-0200cd936042/SMS/+91"+str(mobile)+"/AUTOGEN/cushyroom"
	response = requests.post(url)
	#{ "Status": "Success", "Details": "5D6EBEE6-EC04-4776-846D"}
	#print(response.json()['Details'])
	return response.json()['Details']

def otp_recieve(session_id,otp):
	url = "https://2factor.in/API/V1/9fd7dc0c-9a31-11e9-ade6-0200cd936042/SMS/VERIFY/"+str(session_id)+"/"+str(otp)
	response = requests.post(url)
	#{ "Status": "Success", "Details": "OTP Matched" }
	return response.json()['Details']
