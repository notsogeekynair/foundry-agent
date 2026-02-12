import requests

print(requests.get("http://127.0.0.1:9000/employees").json())