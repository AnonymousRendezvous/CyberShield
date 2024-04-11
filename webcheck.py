import requests, json
url = "https://webapi.namescan.io/v1/freechecks/email/breaches"

email = input("Your email address: ")
payload={
    "email": email
}
headers = {
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text , response.status_code)
