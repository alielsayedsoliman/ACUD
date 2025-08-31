import pyodbc

class Config:
    DRIVER = "ODBC Driver 17 for SQL Server"
    SERVER = r"localhost\MSSQLSERVER2022"   # Use raw string for backslash
    DATABASE = "ACUD"

    @staticmethod
    def get_connection():
        conn_str = (
            f"DRIVER={{{Config.DRIVER}}};"
            f"SERVER={Config.SERVER};"
            f"DATABASE={Config.DATABASE};"
            "Trusted_Connection=yes;"
        )
        return pyodbc.connect(conn_str)
