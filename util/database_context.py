import pymysql

class DatabaseContext:
    @staticmethod
    def get_connection():
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='root',  # replace with your actual password
                database='payxpert1',      # your database name
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except pymysql.MySQLError as e:
            print("Database connection failed:", e)
            return None
