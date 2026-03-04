import json
from openapi_spec_validator import validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

with open('openapi.json', 'r', encoding='utf-8') as f:
    spec = json.load(f)

try:
    validate(spec)
    print("SUCCESS")
except OpenAPIValidationError as e:
    print(f"Validation Error: {e.message}")
    print(f"Path: {e.json_path}")
except Exception as e:
    print(f"Other Error: {e}")
