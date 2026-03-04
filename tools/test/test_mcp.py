import asyncio
from mcp_server import create_employee, get_all_employees, EmployeeInput

async def main():
    # Test create_employee
    new_emp = EmployeeInput(name="Alice", role="Manager", department="HR")
    print(await create_employee(new_emp))

    # Test get_all_employees
    print(await get_all_employees())

if __name__ == "__main__":
    asyncio.run(main())

