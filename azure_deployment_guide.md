# Azure Deployment & AI Foundry Integration Guide

This guide provides the exact steps to deploy the Employee Management System to Azure using the provided automation script.

## 1. Prerequisites
- [Azure CLI](https://aka.ms/installazurecli) installed.
- Logged in to Azure: `az login`.
- A valid subscription selected: `az account set --subscription "Your-Subscription-ID"`.

## 2. One-Click Deployment
The `deploy_azure.ps1` script automates resource creation, image building, and deployment with all necessary authentication.

1. Open PowerShell in the project root.
2. Run the deployment script:
   ```powershell
   ./deploy_azure.ps1
   ```
3. **Wait for completion**. The script will output your final **MCP SERVER URL** and **BACKEND API URL**.

## 3. Generate & Upload Schema
Once the server is live, you must generate the validated OpenAPI schema for AI Foundry.

1. Set the server URL in your terminal (using the URL from the script output):
   ```powershell
   $env:MCP_SERVER_URL = "https://your-mcp-server-url.azurecontainerapps.io"
   ```
2. Run the generator:
   ```powershell
   python mcp-server/generate_openapi.py
   ```
   *This updates [openapi.json](file:///d:/Projects/foundry-agent/foundry-agent/openapi.json) with your production URL.*

## 4. Configure Azure AI Foundry
1. In your Agent's **Actions**, click **Add Action** -> **OpenAPI 3.0 specified tool**.
2. **Upload**: Select the `openapi.json` file.
3. **Base URL**: Paste the MCP Server URL.
4. **Auth**: 
   - Type: **API Key**
   - Name: `X-API-Key`
   - Value: `dev_secret_key_123` (or the key you set in the script).

## 5. Troubleshooting
- **Unauthorized Errors**: The script now handles ACR credentials automatically. If you see pull errors, ensure `admin-enabled` is true on your ACR (`az acr update -n <acr_name> --admin-enabled true`).
- **Persistence**: Database changes are ephemeral in this setup. For production data, configure an external database or Azure file share volume.
