from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app=FastAPI()
employees ={}
counter =1

class Employee(BaseModel):
    name:str
    role:str
    department : str

@app.get("/")
def home():
    return{"message": "Employee API running"}

#create an employee
@app.post("/employees")
def create_employee(emp: Employee):
    global counter
    employees[counter]= emp.dict()
    counter+=1
    return{"message": "Employee created ","id" : counter-1}

#get all employees
@app.get("/employees")
def get_employees():
    return employees

#get an employee
@app.get("/employees/{emp_id}")
def get_employee(emp_id:int):
    if emp_id not in employees:
        raise HTTPException(status_code=404,detail="Employee not found")
    return employees[emp_id]

#delete an employee
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id:int):
    if emp_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees[emp_id]
    return{"message": "Employee deleted"}