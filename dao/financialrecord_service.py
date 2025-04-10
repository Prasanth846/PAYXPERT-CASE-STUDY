from dao.ifinancialrecord_service import IFinancialRecordService

class FinancialRecordService(IFinancialRecordService):
    def __init__(self, connection):
        self.conn = connection

    def add_financial_record(self, record):
        self.records[record.record_id] = record

    def get_financial_record_by_id(self, record_id):
        return self.records.get(record_id)

    def get_financial_records_for_employee(self, employee_id):
        return [r for r in self.records.values() if r.employee_id == employee_id]

    def get_financial_records_for_date(self, date):
        return [r for r in self.records.values() if r.record_date == date]
