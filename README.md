Employee Management System(AI+MCP+FastAPI)

Employee Management System that allows Artificial Intelligence agents or other frontends to interface with employee data. The project uses a two-tier backend architecture consisting of a primary CRUD API and an MCP (Model Context Protocol) bridge.

Core Components
The Primary Backend API app.py & database.py

Built with FastAPI and uses SQLAlchemy with a local SQLite database (employees.db).
Handles the actual database interactions (Create, Read, Update, Delete) for Employee records.
Each employee has the following attributes: id, name, role, and department.
Running this (e.g., via uvicorn app:app --reload) starts the core server, typically on port 8000.
The MCP Bridge Server (mcp_server.py)

Another FastAPI application designed specifically to act as an intermediary (or bridge) between AI platforms (like AI Foundry) and the core API.
It exposes endpoints for Employee CRUD operations and forwards those calls to the Primary Backend at http://localhost:8000 using the Python requests library.
It includes CORS middleware to prevent cross-origin issues when AI frontends attempt to communicate with it. It's meant to run on port 9000.
Testing and Simulation Scrips (agent_simulator.py & test_mcp.py)

Short scripts written to simulate requests and test if the MCP bridge and the underlying backend are communicating properly.

test_mcp.py - tests local proxy creation/reading functions.

agent_simulator.py -uses the standard HTTP client to make a call directly to the mcp_server.



Dockerfile to containerize the application for easier deployment.
How it All Connects (The Flow)
An AI Agent or frontend will send a request (e.g., "Add a new employee named Alice") to the MCP Server (http://localhost:9000/employees).
The MCP Server (mcp_server.py) catches it and proxies a fresh HTTP request over to the Primary API (http://localhost:8000/employees).
The Primary API (app.py) updates the SQLite Database (database.py) and returns the final success response back up the chain.

##Components

-FastAPI Backend (Employee CRUD)
-MCP Server (API Bridge)
- SQLite Database

## How to Run

##Backend API
uvicorn app:app --reload

##MCP Server
uvicorn mcp_server:app --reload --port 9000

##Install Dependencies
pip install -r requirements.txt