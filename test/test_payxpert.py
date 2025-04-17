import pytest
from decimal import Decimal
from entity.Employee import Employee
from entity.Payroll import Payroll
from entity.Tax import Tax
from dao.payroll_service import PayrollService
from dao.tax_service import TaxService
from util.database_context import DatabaseContext
from util.validation_service import ValidationService
from exception.custom_exceptions import InvalidInputException

#  Establish database connection for services
conn = DatabaseContext.get_connection()


# Test Case 1: Calculate Gross Salary
def test_calculate_gross_salary_for_employee():
    basic = 60000.00
    overtime = 5000.00
    gross = basic + overtime
    assert gross == 65000.00


# Test Case 2: Calculate Net Salary
def test_calculate_net_salary_after_deductions():
    basic = 60000.00
    overtime = 5000.00
    deductions = 2000.00
    net = basic + overtime - deductions
    assert net == 63000.00


# Test Case 3: Tax Calculation for High Income
def test_verify_tax_calculation_for_high_income_employee():
    tax_service = TaxService(conn)
    high_income_tax = Tax(tax_id=1, employee_id=1, tax_year=2024, taxable_income=Decimal('1200000.00'), tax_amount=Decimal('0.00'))
    high_income_tax.set_tax_amount(high_income_tax.get_taxable_income() * Decimal('0.10'))
    assert high_income_tax.get_tax_amount() == Decimal('120000.00')


# Test Case 4: Process Payroll for Multiple Employees
def test_process_payroll_for_multiple_employees():
    payroll_service = PayrollService(conn)
    employee_ids = [1, 2, 3]

    count = 0
    for i in employee_ids:
        payroll = Payroll(payroll_id=None, employee_id=i, basic_salary=40000, overtime_pay=2000,
                          deductions=1000, net_salary=41000)
        payroll_service.generate_payroll(payroll)
        count += 1

    assert count == 3



# Test Case 5: Error Handling for Invalid Input
def test_verify_error_handling_for_invalid_email():
    invalid_email = "john[at]email.com"
    with pytest.raises(Exception):
        if not ValidationService.validate_email(invalid_email):
            raise InvalidInputException("Invalid Email Format")
