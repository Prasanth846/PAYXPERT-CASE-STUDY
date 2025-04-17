import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dao.employee_service import EmployeeService
from dao.payroll_service import PayrollService
from dao.tax_service import TaxService
from dao.financialrecord_service import FinancialRecordService
from util.database_context import DatabaseContext
from util.validation_service import *
from exception.custom_exceptions import *
from entity.Employee import Employee
from entity.Payroll import Payroll
from entity.Tax import Tax

import datetime

class MainModule:
    def __init__(self, role, emp_id=None):
        self.connection = DatabaseContext.get_connection()
        self.role = role
        self.emp_id = emp_id

        if not self.connection:
            raise DatabaseConnectionException("Could not connect to database.")

        self.employee_service = EmployeeService(self.connection)
        self.payroll_service = PayrollService(self.connection)
        self.tax_service = TaxService(self.connection)
        self.financial_service = FinancialRecordService(self.connection)

    def menu(self):
        while True:
            print("\n========== EMPLOYEE MANAGEMENT SYSTEM ==========")

            if self.role == 'admin':
                print("1. Add Employee")
                print("2. View All Employees")
                print("3. Get Employee by ID")
                print("4. Update Employee")
                print("5. Delete Employee")
                print("6. Generate Payroll")
                print("7. View Payrolls for an Employee")
                print("8. Calculate Tax")
                print("9. View Taxes for an Employee")
                print("10. Logout")
            elif self.role == 'employee':
                print("1. View Payroll")
                print("2. View Tax")
                print("3. Logout")
            else:
                print("Invalid role. Exiting...")
                break

            choice = input("Enter your choice: ")

            try:
                if self.role == 'admin':
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
                        print("Logging out to login screen...")
                        from main.LoginModule import LoginModule
                        LoginModule().login()
                        break
                    else:
                        print("Invalid choice. Try again.")

                elif self.role == 'employee':
                    if choice == '1':
                        self.view_payrolls_for_employee(self.emp_id)
                    elif choice == '2':
                        self.view_taxes_for_employee(self.emp_id)
                    elif choice == '3':
                        print("Logging out to login screen...")
                        from main.LoginModule import LoginModule
                        LoginModule().login()
                        break
                    else:
                        print("Invalid choice. Try again.")
            except Exception as e:
                print(f"Error: {str(e)}")


    def add_employee(self):
        print("\nEnter Employee Details:")
        try:
            emp_id = input("Employee ID: ")

            # Check if Employee ID already exists
            existing_emp = self.employee_service.get_employee_by_id(emp_id)
            if existing_emp:
                raise EmployeeAlreadyExistsException(f"Employee ID {emp_id} already exists.")

            # Proceed to collect other details only if ID is unique
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
            gender = input("Gender: ")
            email = input("Email: ")
            phone_number = input("Phone Number: ")

            # 🔐 Validation
            if not ValidationService.validate_email(email):
                raise InvalidInputException("Invalid email format.")
            if not ValidationService.validate_phone(phone_number):
                raise InvalidInputException("Phone number must be exactly 10 digits.")

            address = input("Address: ")
            position = input("Position: ")
            joining_date = input("Joining Date (YYYY-MM-DD): ")
            termination_date = input("Termination Date (YYYY-MM-DD) or leave blank: ") or None

            emp = Employee(
                employee_id=emp_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                email=email,
                phone_number=phone_number,
                address=address,
                position=position,
                joining_date=joining_date,
                termination_date=termination_date
            )
            self.employee_service.add_employee(emp)
            print("Employee added successfully.")

        except EmployeeAlreadyExistsException as e:
            print(f"Error: {str(e)}")
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
        try:
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
                raise EmployeeNotFoundException(f"Employee ID {emp_id} not found.")
        except EmployeeNotFoundException as e:
            print(f"Error: {str(e)}")

    def update_employee(self):
        try:
            emp_id = input("Enter Employee ID to update: ")
            employee = self.employee_service.get_employee_by_id(emp_id)
            if not employee:
                raise EmployeeNotFoundException(f"Employee ID {emp_id} not found.")

            print("Leave field blank to keep current value.")
            employee.set_first_name(input("First Name: ") or employee.get_first_name())
            employee.set_last_name(input("Last Name: ") or employee.get_last_name())
            employee.set_email(input("Email: ") or employee.get_email())
            employee.set_phone_number(input("Phone Number: ") or employee.get_phone_number())
            employee.set_address(input("Address: ") or employee.get_address())

            self.employee_service.update_employee(employee)
            print("Employee updated.")

        except EmployeeNotFoundException as e:
            print(f"Error: {str(e)}")

    def delete_employee(self):
        try:
            emp_id = input("Enter Employee ID to delete: ")
            self.employee_service.remove_employee(emp_id)
            print("Employee deleted.")
        except EmployeeNotFoundException as e:
            print(f"Error: {e}")

    def generate_payroll(self):
        from datetime import datetime, timedelta
        from dateutil.relativedelta import relativedelta

        try:
            emp_id = input("Enter Employee ID: ")
            start_date_str = input("Enter Pay Period Start Date (YYYY-MM-DD): ")
            end_date_str = input("Enter Pay Period End Date (YYYY-MM-DD): ")

            basic_salary = float(input("Enter Basic Salary (per month): "))
            overtime = float(input("Enter Overtime Pay (per month): "))
            deductions = float(input("Enter Deductions (per month): "))

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date().replace(day=1)
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date().replace(day=1)

            current_date = start_date

            while current_date <= end_date:
                month_start = current_date
                month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)

                net_salary = basic_salary + overtime - deductions

                payroll = Payroll(
                    employee_id=emp_id,
                    pay_period_start_date=month_start,
                    pay_period_end_date=month_end,
                    basic_salary=basic_salary,
                    overtime_pay=overtime,
                    deductions=deductions,
                    net_salary=net_salary
                )

                self.payroll_service.generate_payroll(payroll)
                current_date += relativedelta(months=1)

            print("Payroll generated successfully.")

        except Exception as e:
            raise PayrollGenerationException(f"Payroll generation failed: {str(e)}")

        print("Payroll generated for each month in the range.")

    def calculate_tax(self):
        try:
            emp_id = input("Enter Employee ID: ")
            year = input("Enter Tax Year (e.g., 2024): ")
            self.tax_service.calculate_tax(emp_id, year)
            print("Tax calculated.")

        except TaxCalculationException as e:
            print(f"Error: {str(e)}")

    def view_payrolls_for_employee(self, emp_id=None):
        if self.role == 'admin':
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

    def view_taxes_for_employee(self, emp_id=None):
        try:
            if self.role == 'admin':
                emp_id = input("Enter Employee ID: ")

            taxes = self.tax_service.get_taxes_for_employee(emp_id)

            if not taxes:
                raise TaxCalculationException(f"No tax records found for Employee ID {emp_id}.")

            for tax in taxes:
                print(f"""
        Tax ID: {tax.get_tax_id()}
        Employee ID: {tax.get_employee_id()}
        Tax Year: {tax.get_tax_year()}
        Taxable Income: ₹{tax.get_taxable_income():.2f}
        Tax Amount: ₹{tax.get_tax_amount():.2f}
        ------------------------------""")

        except TaxCalculationException as e:
            print(f"Error: {str(e)}")


# Entry point
if __name__ == "__main__":
    MainModule().menu()
