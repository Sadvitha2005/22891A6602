import requests

# URL to send request
url = "http://20.244.56.144/evaluation-service/auth"

# Payload (fill with your actual details)
payload = {
    "email": "sadvithaaitharaju@gmail.com",
    "name": "Sadvitha",
    "rollno": "22891A6602",
    "accesscode": "YzuJeU",
    "clientID": "a4c6cf47-5049-45c4-8c46-0c1fcc5a3aee",
    "clientSecret": "AFuKvnHvRXaVGDnH"}
try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)

except requests.exceptions.RequestException as e:
    print("Error:", e)