import requests

BASE = "http://127.0.0.1:8000"

# 1. Create employee
create = requests.post(f"{BASE}/employees", json={
    "name": "Auto Test",
    "role": "Tester",
    "department": "QA"
}).json()
print("CREATE:", create)

emp_id = create.get("id")

# 2. Get all employees
print("GET ALL:", requests.get(f"{BASE}/employees").json())

# 3. Get employee by ID
print("GET ONE:", requests.get(f"{BASE}/employees/{emp_id}").json())

# 4. Update employee
print("UPDATE:", requests.put(
    f"{BASE}/employees/{emp_id}",
    json={"name": "Updated User", "role": "Senior QA", "department": "QA"}).json())

# 5. Delete employee
print("DELETE:", requests.delete(f"{BASE}/employees/{emp_id}").json())

# 6. Confirm deletion
print("VERIFY DELETE:", requests.get(f"{BASE}/employees").json())
