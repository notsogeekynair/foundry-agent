# Azure CLI Deployment & AI Foundry Integration Guide

Follow these exact commands in your terminal (PowerShell or Bash) to deploy your system to Azure.

## 0. Set Variables
First, define these variables to make the commands easier to run:
```powershell
$RG="employee-mcp-rg"
$LOC="eastus"
$ACR="employeemcpacr" + (Get-Random -Maximum 9999)
$ENV="employee-mcp-env"
```

## 1. Prepare Infrastructure
Login and create the core resources:
```powershell
az login
az group create --name $RG --location $LOC
az acr create --resource-group $RG --name $ACR --sku Basic --admin-enabled true
```

## 2. Build and Push Images
Run these from the project root directory:
```powershell
# Build Backend
az acr build --registry $ACR --image "employee-api:latest" ./employee-api

# Build MCP Server
az acr build --registry $ACR --image "mcp-server:latest" ./mcp-server
```

## 3. Deploy to Container Apps
Create the environment and deploy the services:
```powershell
# Create Environment
az containerapp env create --name $ENV --resource-group $RG --location $LOC

# Deploy Backend
az containerapp create --name "employee-api" --resource-group $RG --environment $ENV --image "$ACR.azurecr.io/employee-api:latest" --target-port 9000 --ingress external

# Get Backend URL
$BACKEND_URL = "https://" + (az containerapp show --name "employee-api" --resource-group $RG --query properties.configuration.ingress.fqdn -o tsv)

# Deploy MCP Server
az containerapp create --name "mcp-server" --resource-group $RG --environment $ENV --image "$ACR.azurecr.io/mcp-server:latest" --target-port 9000 --ingress external --env-vars "BASE_URL=$BACKEND_URL" "MCP_API_KEY=your_secret_key"

# Get MCP URL
$MCP_URL = "https://" + (az containerapp show --name "mcp-server" --resource-group $RG --query properties.configuration.ingress.fqdn -o tsv)

# Final Update (Tell MCP its own URL)
az containerapp update --name "mcp-server" --resource-group $RG --set-env-vars "MCP_SERVER_URL=$MCP_URL"
```

## 4. Generate & Upload Schema
Now that the server is live, generate the final validated schema:
```powershell
$env:MCP_SERVER_URL = $MCP_URL
python mcp-server/generate_openapi.py
```

## 5. Configure Azure AI Foundry
1. In your Agent's **Actions**, click **Add Action** -> **OpenAPI 3.0 specified tool**.
2. **Upload**: Select the [openapi.json](file:///d:/Projects/foundry-agent/foundry-agent/openapi.json) just created.
3. **Base URL**: Paste the `$MCP_URL` from your terminal.
4. **Auth**: 
   - Type: **API Key**
   - Name: `X-API-Key`
   - Value: `your_secret_key` (the one you used in step 3).
