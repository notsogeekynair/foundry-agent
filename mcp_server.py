import requests,logging
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

app=FastAPI(
    title="Employee MCP Server",
    description="Bridge API for Employee Management System",
    version="1.0"
)

#prevents cross origin issues when AI Foundry or other frontends call MCP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "http://localhost:8000"

#creating response 
class EmployeeResponse(BaseModel):
    id:int | None=None
    name:str | None=None
    role:str | None=None
    department:str | None:None


class EmployeeInput(BaseModel):
    name:str
    role:str
    department:str
    


#create employee
@app.post("/employees",tags=["Employee CREATE Operation"],response_model=list[EmployeeResponse],summary="Create a new employee record")
def create_employee(emp:EmployeeInput):
    logging.info("CREATE employee called")
    try:
        return requests.post(f"{BASE_URL}/employees",json=emp.dict(),timeout=5).json()
    except Exception as e:
        return{"Error":str(e)}

#get all employees
@app.get("/employees",tags=["Employee READ Operation"],response_model=list[EmployeeResponse],summary="Retrieve all employee records")
def get_all_employees():
    logging.info("GET all employees called")
    try:
        return requests.get(f"{BASE_URL}/employees",timeout=5).json()
    except Exception as e:
        return {"Error": str(e)}

#update an employee
@app.put("/employees/{emp_id}",tags=["Employee UPDATE operation"],response_model=list[EmployeeResponse],summary="Update an employee record")
def update_employee(emp_id:int,emp:EmployeeInput):
    logging.info("UPDATE employee called")
    try:
        return requests.put(
            f"{BASE_URL}/employees/{emp_id}",
            json=emp.dict(),timeout=5
        ).json()
    except Exception as e:
        return {"Error": str(e)}
    

#delete an employee
@app.delete("/employees/{emp_id}",tags=["Employee DELETE Operation"],response_model=list[EmployeeResponse],summary="Delete an employee record")
def delete_employee(emp_id:int):
    logging.info("DELETE employee called")
    try:
        return requests.delete(f"{BASE_URL}/employees/{emp_id}",timeout=5).json()
    except Exception as e:
        return {"Error":str(e)}

#health check
@app.get("/health")
def health():
    return{"status":"ok"}