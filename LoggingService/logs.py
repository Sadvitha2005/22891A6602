import requests

URL = "http://20.244.56.144/evaluation-service/logs"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJzYWR2aXRoYWFpdGhhcmFqdUBnbWFpbC5jb20iLCJleHAiOjE3NTY5NzE1ODAsImlhdCI6MTc1Njk3MDY4MCwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjhkNDg0Zjk3LTM3MDgtNDhlMy1iZGFkLTYzYmRjNTJjZGEwNiIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6InNhZHZpdGhhIiwic3ViIjoiYTRjNmNmNDctNTA0OS00NWM0LThjNDYtMGMxZmNjNWEzYWVlIn0sImVtYWlsIjoic2Fkdml0aGFhaXRoYXJhanVAZ21haWwuY29tIiwibmFtZSI6InNhZHZpdGhhIiwicm9sbE5vIjoiMjI4OTFhNjYwMiIsImFjY2Vzc0NvZGUiOiJZenVKZVUiLCJjbGllbnRJRCI6ImE0YzZjZjQ3LTUwNDktNDVjNC04YzQ2LTBjMWZjYzVhM2FlZSIsImNsaWVudFNlY3JldCI6IkFGdUt2bkh2UlhhVkdEbkgifQ.WfV_4oPVOJv9M5f_KaBL8ZPwWRB9eOjpk6xYSuI1DqY"  # <-- put your token here

def log(stack: str, level: str, package: str, message: str):
    """
    Sends log data to the evaluation service with authorization.

    Args:
        stack (str): The stack name (e.g., 'python', 'nodejs').
        level (str): Log level (e.g., 'INFO', 'ERROR', 'DEBUG').
        package (str): The package/module name.
        message (str): Log message.
    """
    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",  # add auth header
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        try:
            print("Response JSON:", response.json())
        except Exception:
            print("Response Text:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending log:", e)


# Example usage
if __name__ == "__main__":
    log("backend", "error", "handler", "Authorization successful")
