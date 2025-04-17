class EmployeeNotFoundException(Exception):
    def __init__(self, message="Employee not found."):
        super().__init__(message)


class PayrollGenerationException(Exception):
    def __init__(self, message="Error generating payroll."):
        super().__init__(message)


class TaxCalculationException(Exception):
    def __init__(self, message="Error calculating tax."):
        super().__init__(message)


class FinancialRecordException(Exception):
    def __init__(self, message="Error in financial record operation."):
        super().__init__(message)


class InvalidInputException(Exception):
    def __init__(self, message="Invalid input provided."):
        super().__init__(message)


class EmployeeAlreadyExistsException(Exception):
    def __init__(self, message="Employee already exists."):
        super().__init__(message)


class DatabaseConnectionException(Exception):
    def __init__(self, message="Failed to connect to the database."):
        super().__init__(message)
