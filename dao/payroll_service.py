from dao.ipayroll_service import IPayrollService
from entity.Payroll import Payroll

class PayrollService(IPayrollService):
    def __init__(self, connection):
        self.conn = connection

    def generate_payroll(self, payroll: Payroll):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO payroll (Employee_ID, Payperiod_Start_Date, Payperiod_End_Date,
                                 Basic_Salary, Overtime_Pay, Deductions, Net_Salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            payroll.get_employee_id(),
            payroll.get_pay_period_start_date(),
            payroll.get_pay_period_end_date(),
            payroll.get_basic_salary(),
            payroll.get_overtime_pay(),
            payroll.get_deductions(),
            payroll.get_net_salary()
        )
        cursor.execute(query, values)
        self.conn.commit()

    def get_payroll_by_id(self, payroll_id):
        return self.payrolls.get(payroll_id)

    def get_payrolls_for_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM payroll WHERE Employee_ID = %s", (employee_id,))
        rows = cursor.fetchall()

        from entity.Payroll import Payroll
        return [Payroll(
            payroll_id=row["Payroll_ID"],
            employee_id=row["Employee_ID"],
            pay_period_start_date=row["Payperiod_Start_Date"],
            pay_period_end_date=row["Payperiod_End_Date"],
            basic_salary=row["Basic_Salary"],
            overtime_pay=row["Overtime_Pay"],
            deductions=row["Deductions"],
            net_salary=row["Net_Salary"]
        ) for row in rows]

    def get_payrolls_for_period(self, start_date, end_date):
        return [p for p in self.payrolls.values() if start_date <= p.pay_period_start_date <= end_date]
