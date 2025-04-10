from dao.iemployee_service import IEmployeeService
from entity.Employee import Employee

class EmployeeService(IEmployeeService):
    def __init__(self, connection):
        self.conn = connection

    def get_employee_by_id(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE Employee_ID = %s", (employee_id,))
        row = cursor.fetchone()
        if row:
            return Employee(
                employee_id=row['Employee_ID'],
                first_name=row['First_Name'],
                last_name=row['Last_Name'],
                date_of_birth=row['Date_of_Birth'],
                gender=row['Gender'],
                email=row['Email'],
                phone_number=row['Phone_Number'],
                address=row['Address'],
                position=row['Position'],
                joining_date=row['Joining_Date'],
                termination_date=row['Termination_Date']
            )

        return None

    def get_all_employees(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employee")
        rows = cursor.fetchall()
        return [Employee(
            employee_id=row['Employee_ID'],
            first_name=row['First_Name'],
            last_name=row['Last_Name'],
            date_of_birth=row['Date_of_Birth'],
            gender=row['Gender'],
            email=row['Email'],
            phone_number=row['Phone_Number'],
            address=row['Address'],
            position=row['Position'],
            joining_date=row['Joining_Date'],
            termination_date=row['Termination_Date']
        ) for row in rows]

    def add_employee(self, employee):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO employee (Employee_ID, First_Name, Last_Name, Date_of_Birth, Gender,
                                  Email, Phone_Number, Address, Position, Joining_Date, Termination_Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            employee.get_employee_id(), employee.get_first_name(), employee.get_last_name(),
            employee.get_date_of_birth(), employee.get_gender(), employee.get_email(),
            employee.get_phone_number(), employee.get_address(), employee.get_position(),
            employee.get_joining_date(), employee.get_termination_date()
        )
        cursor.execute(query, values)
        self.conn.commit()

    def update_employee(self, employee):
        cursor = self.conn.cursor()
        query = """
            UPDATE employee
            SET First_Name=%s, Last_Name=%s, Email=%s, Phone_Number=%s
            WHERE Employee_ID = %s
        """
        values = (
            employee.get_first_name(), employee.get_last_name(),
            employee.get_email(), employee.get_phone_number(),
            employee.get_employee_id()
        )
        cursor.execute(query, values)
        self.conn.commit()

    def remove_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM employee WHERE Employee_ID = %s", (employee_id,))
        self.conn.commit()
