from dao.itax_service import ITaxService
from entity.Tax import Tax
from exception.custom_exceptions import TaxCalculationException
from decimal import Decimal

class TaxService(ITaxService):
    def __init__(self, connection):
        self.conn = connection

    def calculate_tax(self, employee_id, tax_year):
        try:
            cursor = self.conn.cursor()

            # Check if employee exists
            cursor.execute("SELECT * FROM employee WHERE Employee_ID = %s", (employee_id,))
            employee = cursor.fetchone()
            if not employee:
                raise TaxCalculationException(f"Employee ID {employee_id} does not exist. Cannot calculate tax.")

            # Get payroll totals
            cursor.execute("""
                SELECT SUM(Basic_Salary + Overtime_Pay - Deductions) AS TaxableIncome
                FROM payroll
                WHERE Employee_ID = %s
            """, (employee_id,))
            result = cursor.fetchone()

            taxable_income = result["TaxableIncome"] if result["TaxableIncome"] else Decimal('0.00')
            tax_amount = taxable_income * Decimal('0.10')

            # Insert into tax table
            cursor.execute("""
                INSERT INTO tax (Employee_ID, Tax_Year, Taxable_Income, Tax_Amount)
                VALUES (%s, %s, %s, %s)
            """, (employee_id, tax_year, taxable_income, tax_amount))

            self.conn.commit()

        except Exception as e:
            raise TaxCalculationException(f"Tax calculation failed: {str(e)}")

    def get_taxes_for_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tax WHERE Employee_ID = %s", (employee_id,))
        rows = cursor.fetchall()

        return [
            Tax(
                tax_id=row["Tax_ID"],
                employee_id=row["Employee_ID"],
                tax_year=row["Tax_Year"],
                taxable_income=row["Taxable_Income"],
                tax_amount=row["Tax_Amount"]
            )
            for row in rows
        ]

    def get_tax_by_id(self, tax_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tax WHERE Tax_ID = %s", (tax_id,))
        row = cursor.fetchone()

        if row:
            return Tax(
                tax_id=row["Tax_ID"],
                employee_id=row["Employee_ID"],
                tax_year=row["Tax_Year"],
                taxable_income=row["Taxable_Income"],
                tax_amount=row["Tax_Amount"]
            )
        return None

    def get_taxes_for_year(self, tax_year):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tax WHERE Tax_Year = %s", (tax_year,))
        rows = cursor.fetchall()

        return [
            Tax(
                tax_id=row["Tax_ID"],
                employee_id=row["Employee_ID"],
                tax_year=row["Tax_Year"],
                taxable_income=row["Taxable_Income"],
                tax_amount=row["Tax_Amount"]
            )
            for row in rows
        ]
