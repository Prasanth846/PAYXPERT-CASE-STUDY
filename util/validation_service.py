import re

class ValidationService:
    @staticmethod
    def validate_email(email):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) == 10
