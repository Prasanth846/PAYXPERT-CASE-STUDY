class Tax:
    def __init__(self, tax_id=None, employee_id=None, tax_year=None,
                 taxable_income=0.0, tax_amount=0.0):
        self.__tax_id = tax_id
        self.__employee_id = employee_id
        self.__tax_year = tax_year
        self.__taxable_income = taxable_income
        self.__tax_amount = tax_amount

    def get_tax_id(self):
        return self.__tax_id
    def set_tax_id(self, value):
        self.__tax_id = value

    def get_employee_id(self):
        return self.__employee_id
    def set_employee_id(self, value):
        self.__employee_id = value

    def get_tax_year(self):
        return self.__tax_year
    def set_tax_year(self, value):
        self.__tax_year = value

    def get_taxable_income(self):
        return self.__taxable_income
    def set_taxable_income(self, value):
        self.__taxable_income = value

    def get_tax_amount(self):
        return self.__tax_amount
    def set_tax_amount(self, value):
        self.__tax_amount = value
