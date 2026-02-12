from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SessionLocal,Employee as DBEmployee


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
    db=SessionLocal()
    new_emp=DBEmployee(name=emp.name, role=emp.role,department=emp.department)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    db.close()
    return {"id":new_emp.id}

#get all employees
@app.get("/employees")
def get_employees():
    db=SessionLocal()
    data=db.query(DBEmployee).all()
    db.close()
    return data

#get an employee by ID
@app.get("/employees/{emp_id}")
def get_employee(emp_id:int):
    db=SessionLocal()
    emp=db.query(DBEmployee).filter(DBEmployee.id==emp_id).first()
    db.close()
    if not emp:
        raise HTTPException(status_code=404,detail="Employee not found")
    return emp

#delete an employee
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id:int):
    db=SessionLocal()
    emp=db.query(DBEmployee).filter(DBEmployee.id==emp_id).first()
    if not emp:
        db.close()
        raise HTTPException(status_code=404,detail="Employee not found")
    db.delete(emp)
    db.commit()
    db.close()
    return{"message":"Employee deleted"}

@app.put("/employees/{emp_id}")
def update_employee(emp_id:int ,emp:Employee):
    db=SessionLocal()
    existing = db.query(DBEmployee).filter(DBEmployee.id==emp_id).first()

    if not existing:
        db.close()
        raise HTTPException(status_code=404,detail="Empoloyee not found")

    existing.name=emp.name
    existing.role=emp.role
    existing.department=emp.department

    db.commit()
    db.close()

    return{"message":"Employee updated"}