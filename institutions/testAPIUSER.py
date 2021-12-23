import requests
id=91
r = requests.get('http://127.0.0.1:8000/api/auth/users/{id}')

print(r.status_code)