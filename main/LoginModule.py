import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.database_context import DatabaseContext
from main.MainModule import MainModule
import msvcrt

class LoginModule:
    def __init__(self):
        self.connection = DatabaseContext.get_connection()

    def get_hidden_password(self, prompt="Enter admin password: "):
        print(prompt, end='', flush=True)
        password = []
        while True:
            char = msvcrt.getch()
            if char in (b'\r', b'\n'):  # Enter key
                print()  # Move to next line
                break
            elif char == b'\x08':  # Backspace
                if password:
                    password.pop()
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                password.append(char.decode('utf-8'))
                sys.stdout.write('*')
                sys.stdout.flush()
        return ''.join(password)

    def login(self):
        while True:
            print("\n====== PAYXPERT LOGIN ======")
            print("1. Admin Login")
            print("2. Employee Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter admin username: ")
                password = self.get_hidden_password()  # Use custom function for masked input
                if username == 'admin' and password == 'admin123':
                    print("Admin login successful.")
                    MainModule(role='admin').menu()
                else:
                    print("Invalid admin credentials.")
            elif choice == '2':
                emp_id = input("Enter Employee ID: ")
                email = input("Enter Email: ")
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM employee WHERE Employee_ID = %s AND Email = %s", (emp_id, email))
                if cursor.fetchone():
                    print("Employee login successful.")
                    MainModule(role='employee', emp_id=emp_id).menu()
                else:
                    print("Invalid employee credentials.")
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    LoginModule().login()