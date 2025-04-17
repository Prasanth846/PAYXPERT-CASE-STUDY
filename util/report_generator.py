class ReportGenerator:
    @staticmethod
    def generate_payroll_report(payrolls):
        for p in payrolls:
            print(f"{p.payroll_id} - {p.employee_id} - {p.net_salary}")

    @staticmethod
    def generate_tax_summary(taxes):
        for t in taxes:
            print(f"{t.tax_id} - {t.employee_id} - {t.tax_amount}")

    @staticmethod
    def generate_financial_report(records):
        for r in records:
            print(f"{r.record_id} - {r.description} - {r.amount} ({r.record_type})")
