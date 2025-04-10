import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dao.employee_service import EmployeeService
from dao.payroll_service import PayrollService
from dao.tax_service import TaxService
from dao.financialrecord_service import FinancialRecordService
from util.database_context import DatabaseContext
from exception.custom_exceptions import *
from entity.Employee import Employee
from entity.Payroll import Payroll
from entity.Tax import Tax

import datetime

class MainModule:
    def __init__(self):
        # Establishing DB connection
        self.connection = DatabaseContext.get_connection()
        if not self.connection:
            raise DatabaseConnectionException("Could not connect to database.")

        # Injecting DB connection into services
        self.employee_service = EmployeeService(self.connection)
        self.payroll_service = PayrollService(self.connection)
        self.tax_service = TaxService(self.connection)
        self.financial_service = FinancialRecordService(self.connection)

    def menu(self):
        while True:
            print("\n========== EMPLOYEE MANAGEMENT SYSTEM ==========")
            print("1. Add Employee")
            print("2. View All Employees")
            print("3. Get Employee by ID")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Generate Payroll")
            print("7. View Payrolls for an Employee")
            print("8. Calculate Tax")
            print("9. View Taxes for an Employee")
            print("10. Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == '1':
                    self.add_employee()
                elif choice == '2':
                    self.view_all_employees()
                elif choice == '3':
                    self.get_employee_by_id()
                elif choice == '4':
                    self.update_employee()
                elif choice == '5':
                    self.delete_employee()
                elif choice == '6':
                    self.generate_payroll()
                elif choice == '7':
                    self.view_payrolls_for_employee()
                elif choice == '8':
                    self.calculate_tax()
                elif choice == '9':
                    self.view_taxes_for_employee()
                elif choice == '10':
                    print("Exiting...")
                    break



                else:
                    print("Invalid choice. Try again.")

            except Exception as e:
                print(f"Error: {str(e)}")

    def add_employee(self):
        print("\nEnter Employee Details:")
        try:
            emp = Employee(
                employee_id=input("Employee ID: "),
                first_name=input("First Name: "),
                last_name=input("Last Name: "),
                date_of_birth=input("Date of Birth (YYYY-MM-DD): "),
                gender=input("Gender: "),
                email=input("Email: "),
                phone_number=input("Phone Number: "),
                address=input("Address: "),
                position=input("Position: "),
                joining_date=input("Joining Date (YYYY-MM-DD): "),
                termination_date=input("Termination Date (YYYY-MM-DD) or leave blank: ") or None
            )
            self.employee_service.add_employee(emp)
            print("Employee added successfully.")
        except InvalidInputException as e:
            print(f"Invalid input: {str(e)}")

    def view_all_employees(self):
        employees = self.employee_service.get_all_employees()
        if not employees:
            print("No employees found.")
        for emp in employees:
            print(f"ID: {emp.get_employee_id()} | Name: {emp.get_first_name()} {emp.get_last_name()} | Email: {emp.get_email()}")

    def get_employee_by_id(self):
        emp_id = input("Enter Employee ID: ")
        emp = self.employee_service.get_employee_by_id(emp_id)
        if emp:
            print(f"""
            Employee Details:
            ID: {emp.get_employee_id()}
            First Name: {emp.get_first_name()}
            Last Name: {emp.get_last_name()}
            Date of Birth: {emp.get_date_of_birth()}
            Gender: {emp.get_gender()}
            Email: {emp.get_email()}
            Phone Number: {emp.get_phone_number()}
            Address: {emp.get_address()}
            Position: {emp.get_position()}
            Joining Date: {emp.get_joining_date()}
            Termination Date: {emp.get_termination_date()}
            """)
        else:
            print("Employee not found.")

    def update_employee(self):
        emp_id = input("Enter Employee ID to update: ")
        employee = self.employee_service.get_employee_by_id(emp_id)
        if not employee:
            print("Employee not found.")
            return
        print("Leave field blank to keep current value.")
        employee.set_first_name(input("First Name: ") or employee.get_first_name())
        employee.set_last_name(input("Last Name: ") or employee.get_last_name())
        employee.set_email(input("Email: ") or employee.get_email())
        employee.set_phone_number(input("Phone Number: ") or employee.get_phone_number())
        self.employee_service.update_employee(employee)
        print("Employee updated.")

    def delete_employee(self):
        emp_id = input("Enter Employee ID to delete: ")
        self.employee_service.remove_employee(emp_id)
        print("Employee deleted.")

    def generate_payroll(self):
        emp_id = input("Enter Employee ID: ")
        start_date = input("Enter Pay Period Start Date (YYYY-MM-DD): ")
        end_date = input("Enter Pay Period End Date (YYYY-MM-DD): ")
        basic_salary = float(input("Enter Basic Salary: "))
        overtime = float(input("Enter Overtime Pay: "))
        deductions = float(input("Enter Deductions: "))

        # Calculate net salary
        net_salary = basic_salary + overtime - deductions

        # Create Payroll object
        payroll = Payroll(
            employee_id=emp_id,
            pay_period_start_date=start_date,
            pay_period_end_date=end_date,
            basic_salary=basic_salary,
            overtime_pay=overtime,
            deductions=deductions,
            net_salary=net_salary
        )

        # Pass Payroll object to service
        self.payroll_service.generate_payroll(payroll)
        print("Payroll generated.")

    def calculate_tax(self):
        emp_id = input("Enter Employee ID: ")
        year = input("Enter Tax Year (e.g., 2024): ")
        self.tax_service.calculate_tax(emp_id, year)
        print("Tax calculated.")

    def view_payrolls_for_employee(self):
        emp_id = input("Enter Employee ID: ")
        payrolls = self.payroll_service.get_payrolls_for_employee(emp_id)

        if not payrolls:
            print("No payroll records found.")
            return

        for p in payrolls:
            print(f"""
    Payroll ID: {p.get_payroll_id()}
    Employee ID: {p.get_employee_id()}
    Pay Period: {p.get_pay_period_start_date()} to {p.get_pay_period_end_date()}
    Basic Salary: {p.get_basic_salary()}
    Overtime Pay: {p.get_overtime_pay()}
    Deductions: {p.get_deductions()}
    Net Salary: {p.get_net_salary()}
    ------------------------------""")

    def view_taxes_for_employee(self):
        emp_id = input("Enter Employee ID: ")
        taxes = self.tax_service.get_taxes_for_employee(emp_id)

        if not taxes:
            print("No tax records found.")
            return

        for tax in taxes:
            print(f"""
    Tax ID: {tax.get_tax_id()}
    Employee ID: {tax.get_employee_id()}
    Tax Year: {tax.get_tax_year()}
    Taxable Income: ₹{tax.get_taxable_income():.2f}
    Tax Amount: ₹{tax.get_tax_amount():.2f}
    ------------------------------""")


# Entry point
if __name__ == "__main__":
    MainModule().menu()
