from dao.ifinancialrecord_service import IFinancialRecordService
from exception.custom_exceptions import FinancialRecordException
from entity.FinancialRecord import FinancialRecord

class FinancialRecordService(IFinancialRecordService):
    def __init__(self, connection):
        self.conn = connection

    def add_financial_record(self, record: FinancialRecord):
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO financialrecord (Employee_ID, Record_Date, Description_Category, Amount, Record_Type)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                record.get_employee_id(),
                record.get_record_date(),
                record.get_description(),
                record.get_amount(),
                record.get_record_type()
            )
            cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            raise FinancialRecordException(f"Failed to add financial record: {str(e)}")

    def get_financial_record_by_id(self, record_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM financialrecord WHERE Record_ID = %s", (record_id,))
            row = cursor.fetchone()
            if row:
                return FinancialRecord(
                    record_id=row["Record_ID"],
                    employee_id=row["Employee_ID"],
                    record_date=row["Record_Date"],
                    description=row["Description_Category"],
                    amount=row["Amount"],
                    record_type=row["Record_Type"]
                )
            return None
        except Exception as e:
            raise FinancialRecordException(f"Failed to fetch financial record: {str(e)}")

    def get_financial_records_for_employee(self, employee_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM financialrecord WHERE Employee_ID = %s", (employee_id,))
            rows = cursor.fetchall()
            return [
                FinancialRecord(
                    record_id=row["Record_ID"],
                    employee_id=row["Employee_ID"],
                    record_date=row["Record_Date"],
                    description=row["Description_Category"],
                    amount=row["Amount"],
                    record_type=row["Record_Type"]
                ) for row in rows
            ]
        except Exception as e:
            raise FinancialRecordException(f"Failed to retrieve records for employee: {str(e)}")

    def get_financial_records_for_date(self, date):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM financialrecord WHERE Record_Date = %s", (date,))
            rows = cursor.fetchall()
            return [
                FinancialRecord(
                    record_id=row["Record_ID"],
                    employee_id=row["Employee_ID"],
                    record_date=row["Record_Date"],
                    description=row["Description_Category"],
                    amount=row["Amount"],
                    record_type=row["Record_Type"]
                ) for row in rows
            ]
        except Exception as e:
            raise FinancialRecordException(f"Failed to fetch records for the date: {str(e)}")
