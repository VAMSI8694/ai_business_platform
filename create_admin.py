import requests

response = requests.post("http://localhost:8000/auth/register", json={
    "username": "admin",
    "email": "krishna@ikpeden.com",
    "password": "Admin@123456"
})
print(response.json())