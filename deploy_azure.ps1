# deploy_azure.ps1
# Automates the deployment of Employee API and MCP Server to Azure Container Apps

# Configuration - CHANGE THESE AS NEEDED
$RESOURCE_GROUP = "employee-mcp-rg"
$LOCATION = "eastus"
$ACR_NAME = "employeemcpacr" + (Get-Random -Maximum 10000) # Must be unique
$ENVIRONMENT_NAME = "employee-mcp-env"
$BACKEND_APP_NAME = "employee-api"
$MCP_APP_NAME = "mcp-server"

Write-Host "--- Starting Azure Deployment ---" -ForegroundColor Cyan

# 1. Create Resource Group
Write-Host "1. Creating Resource Group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. Create Azure Container Registry
Write-Host "2. Creating Azure Container Registry: $ACR_NAME"
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# 3. Build and Push Images
Write-Host "3. Building and Pushing Images to ACR"
$ACR_LOGIN_SERVER = "$ACR_NAME.azurecr.io"

# Retrieve ACR credentials for ACA pull access
Write-Host "   -> Retrieving ACR credentials..."
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query username -o tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv

# Build Backend API
Write-Host "   -> Building Backend API..."
az acr build --registry $ACR_NAME --image "${BACKEND_APP_NAME}:latest" ./employee-api

# Build MCP Server
Write-Host "   -> Building MCP Server..."
az acr build --registry $ACR_NAME --image "${MCP_APP_NAME}:latest" ./mcp-server

# 4. Create Container App Environment
Write-Host "4. Creating Container App Environment: $ENVIRONMENT_NAME"
az containerapp env create --name $ENVIRONMENT_NAME --resource-group $RESOURCE_GROUP --location $LOCATION

# 5. Deploy Backend API
Write-Host "5. Deploying Backend API..."
az containerapp create `
  --name $BACKEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $ENVIRONMENT_NAME `
  --image "$ACR_LOGIN_SERVER/${BACKEND_APP_NAME}:latest" `
  --target-port 9000 `
  --ingress external `
  --registry-server $ACR_LOGIN_SERVER `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --env-vars "DATABASE_URL=sqlite:////app/employees.db" `
  --query properties.configuration.ingress.fqdn

$BACKEND_URL = "https://" + (az containerapp show --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)
Write-Host "   Backend API URL: $BACKEND_URL" -ForegroundColor Green

# 6. Deploy MCP Server
Write-Host "6. Deploying MCP Server..."
az containerapp create `
  --name $MCP_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $ENVIRONMENT_NAME `
  --image "$ACR_LOGIN_SERVER/${MCP_APP_NAME}:latest" `
  --target-port 9000 `
  --ingress external `
  --registry-server $ACR_LOGIN_SERVER `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --env-vars "BASE_URL=$BACKEND_URL" "MCP_API_KEY=dev_secret_key_123"

$MCP_URL = "https://" + (az containerapp show --name $MCP_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)

# Update MCP Server with its own URL so OpenAPI is correct
Write-Host "7. Finalizing MCP Server configuration..."
az containerapp update `
  --name $MCP_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --set-env-vars "MCP_SERVER_URL=$MCP_URL"

Write-Host "`n--- DEPLOYMENT COMPLETE ---" -ForegroundColor Cyan
Write-Host "MCP SERVER URL: $MCP_URL" -ForegroundColor Green
Write-Host "BACKEND API URL: $BACKEND_URL" -ForegroundColor Green
Write-Host "`nNEXT STEPS:"
Write-Host "1. Set local environment variable: `$env:MCP_SERVER_URL = '$MCP_URL'`"
Write-Host "2. Run: `python mcp-server/generate_openapi.py`"
Write-Host "3. Upload the generated 'openapi.json' to Azure AI Foundry."
Write-Host "4. Use the MCP SERVER URL ($MCP_URL) as the Base URL in Azure."
