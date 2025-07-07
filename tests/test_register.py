import requests

# Login test
url = "http://127.0.0.1:8000/login/"
data = {
    "email": "john@example.com",
    "password": "securepassword123"
}

response = requests.post(url, params=data)
print(response.status_code)
print(response.json())
