import ast
import sys

file_path = r'd:\Projects\foundry-agent\foundry-agent\mcp_server.py'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    ast.parse(source)
    print("AST parse successful. No syntax errors found.")
except SyntaxError as e:
    print(f"SyntaxError: {e.msg}")
    print(f"Line: {e.lineno}, Offset: {e.offset}")
    print(f"Text: {e.text.strip() if e.text else 'None'}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
