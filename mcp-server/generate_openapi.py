import json
import sys
import os

# Import the FastAPI app
try:
    from mcp_server import app
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

try:
    # Generate the schema (this triggers the custom_openapi override)
    schema = app.openapi()
    
    # Save to file with explicit UTF-8 encoding
    with open('openapi.json', 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    
    print("Successfully generated openapi.json")
    
    # Also print the EmployeeResponse schema for manual verification
    if "components" in schema and "schemas" in schema["components"] and "EmployeeResponse" in schema["components"]["schemas"]:
        print("\n--- EmployeeResponse Schema ---")
        print(json.dumps(schema["components"]["schemas"]["EmployeeResponse"], indent=2))
    else:
        print("\nEmployeeResponse schema not found in components!")

except Exception as e:
    print(f"Error generating OpenAPI: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
