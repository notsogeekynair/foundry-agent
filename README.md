Employee Management System(AI+MCP+FastAPI)

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