from abc import ABC, abstractmethod

class IPayrollService(ABC):
    @abstractmethod
    def generate_payroll(self, employee):
        pass

    @abstractmethod
    def get_payroll_by_id(self, payroll_id):
        pass

    @abstractmethod
    def get_payrolls_for_employee(self, employee_id): 
        pass

    @abstractmethod
    def get_payrolls_for_period(self, start_date, end_date):
        pass
