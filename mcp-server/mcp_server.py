import os
import logging
import httpx
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

app=FastAPI(
    title="Employee MCP Server",
    description="Bridge API for Employee Management System. Provides AI-agent compatible tools to Create, Read, Update, and Delete employee records.",
    version="1.0",
    servers=[
         {"url": "https://employee-mcp-api.niceground-961645f1.eastus.azurecontainerapps.io", "description": "Production MCP Server"}
     ],
    docs_url="/docs",
    redoc_url=None
)
app.router.responses ={200:{"description":"Success"}}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://employee-mcp-api.niceground-961645f1.eastus.azurecontainerapps.io", "description": "Production MCP Server"}
    ]
    
    # Change top-level version
    openapi_schema["openapi"] = "3.0.3"
    
    # Ensure security scheme is declared (FastAPI natively handles injecting this when using Security(APIKeyHeader))
    
    # Recursive function to rigorously enforce OpenAPI 3.0.x compliance
    def sanitize_openapi_30(node):
        if isinstance(node,dict):

            #convert anyOf to nullable
            if "anyOf" in node:
                any_of =node["anyOf"]
                non_nulls = [
                    item for item in any_of
                    if isinstance(item,dict) and item.get("type") != "null"
                ]

                if len(non_nulls) == 1:
                    new_props = non_nulls[0].copy()
                    node.update(new_props)
                    node["nullable"] = True
                    del node["anyOf"]
                    
                #hotfix for fastapi validationerror
                elif len(non_nulls)>1 and any(
                    isinstance(item,dict) and item.get("type") == "string"
                    for item in non_nulls
                ):
                    node["type"] = "string"
                    del node["anyOf"]
                    
            #remove 422 responses
            if "responses" in node and isinstance(node["responses"],dict):
                node["responses"].pop("422",None)
            
            #No empty schemas
            if len(node)==0:
                node["type"]="object"
                return
            
            #recurse through children
            keys = list(node.keys())
            for key in keys:
                if key in ["exclusiveMinimum","exclusiveMaximum"] and isinstance(node[key],bool):
                    del node[key]
                elif key in node:
                    sanitize_openapi_30(node[key])
        elif isinstance(node,list):
            for item in node:
                sanitize_openapi_30(item)


                
    # Run the rigorous sanitization over the entire schema
    sanitize_openapi_30(openapi_schema)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

#prevents cross origin issues when AI Foundry or other frontends call MCP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://employee-api.niceground-961645f1.eastus.azurecontainerapps.io"

# Security
API_KEY_NAME = "dev_secret_key_123"
API_KEY = os.getenv("MCP_API_KEY", "dev_secret_key_123")  # Replace in production
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key():
    return True
    
class MessageResponse(BaseModel):
    message: str

#creating response 
class EmployeeResponse(BaseModel):
    id: int #| None = Field(default=None, description="The unique auto-generated ID of the employee (used for updates and deletions).")
    name: str #| None = Field(default=None, description="The full name of the employee.")
    role: str #| None = Field(default=None, description="The job title or role.")
    department: str #| None = Field(default=None, description="The department the employee belongs to.")

class EmployeeInput(BaseModel):
    name: str = Field(..., description="The full name of the employee, e.g., 'Jane Doe'.")
    role: str = Field(..., description="The job title or role, e.g., 'Software Engineer' or 'Manager'.")
    department: str = Field(..., description="The department name, e.g., 'Engineering' or 'HR'.")
    

#create employee
@app.post(
    "/employees",
    tags=["Employee CREATE Operation"],
    response_model= MessageResponse,
    operation_id="CreateEmployee",
    summary="Create a new employee record",
    description="Tool to create a new employee in the database. Use this when a user asks to onboard, add, or create a new employee. Requires name, role, and department.",
    responses={200:{"description":"Employee created successfully"},422:{"description":"Invalid request"}},
    response_model_exclude_none=True
)
async def create_employee(emp: EmployeeInput):
    logging.info("CREATE employee called")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/employees",json=emp.model_dump(),timeout=5.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTPStatusError: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

#get all employees
@app.get(
    "/employees",
    tags=["Employee READ Operation"],
    response_model=list[EmployeeResponse],
    operation_id="GetAllEmployees",
    summary="Retrieve all employee records",
    description="Tool to fetch the full list of all employees in the system. Use this when the user asks 'who works here', 'list all employees', or needs to find a specific person's ID before updating them.",
    responses={200:{"description":"Employee list retrieved successfully"},422:{"description":"Invalid request"}},
    response_model_exclude_none=True
)
async def get_all_employees():
    logging.info("GET all employees called")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/employees",timeout=5.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTPStatusError: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

#update an employee
@app.put(
    "/employees/{emp_id}",
    tags=["Employee UPDATE operation"],
    response_model=MessageResponse,
    operation_id="UpdateEmployee",
    summary="Update an employee record",
    description="Tool to modify an existing employee's details (like name, role, or department). You must provide the numeric emp_id in the path alongside the new payload. Use GetAllEmployees first if you don't know the emp_id.",
    responses={200:{"description":"Employee updated successfully"},422:{"description":"Invalid request"}},
    response_model_exclude_none=True
)
async def update_employee(emp_id: int, emp: EmployeeInput):
    logging.info("UPDATE employee called")
    try:
         async with httpx.AsyncClient() as client:
            response = await client.put(f"{BASE_URL}/employees/{emp_id}",json=emp.model_dump(),timeout=5.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTPStatusError: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

#delete an employee
@app.delete(
    "/employees/{emp_id}",
    tags=["Employee DELETE Operation"],
    response_model=MessageResponse,
    operation_id="DeleteEmployee",
    summary="Delete an employee record",
    description="Tool to remove an employee from the system. Requires the numeric emp_id. Use this when a user asks to terminate, remove, or delete an employee.",
    responses={200:{"description":"Employee deleted successfully"},422:{"description":"Invalid request"}},
    response_model_exclude_none=True    
)
async def delete_employee(emp_id: int):
    logging.info("DELETE employee called")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{BASE_URL}/employees/{emp_id}",timeout=5.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTPStatusError: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

#health check
@app.get("/health",include_in_schema=False)
def health():
    return{"status":"ok"}