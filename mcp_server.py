import requests
from fastapi import FastAPI

app=FastAPI()

BASE_URL = "http://127.0.0.1:8000"



@app.post("/employees")
def create_employee(name,role,department):
    data ={"name":name,"role":role,"department":department}
    return requests.post(f"{BASE_URL}/employees",json=data).json()
@app.get("/employees")
def get_all_employees():
    return requests.get(f"{BASE_URL}/employees").json()