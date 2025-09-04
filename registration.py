import requests

# URL to send request
url = "http://20.244.56.144/evaluation-service/register"

# Payload (fill with your actual details)
payload = {
    "email": "sadvithaaitharaju@gmail.com",
    "name": "Sadvitha",
    "mobileno": "9247812150",
    "githubusername": "Sadvitha2005",
    "rollno": "22891A6602",
    "accesscode": "YzuJeU"
}
try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)

except requests.exceptions.RequestException as e:
    print("Error:", e)