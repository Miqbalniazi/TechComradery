import requests

url = "https://chatbot.techcomrad.com:8080/check/"

payload={'email': 'test@1234.com'}
files=[]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

print(response.text)
