import mysql.connector

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",   # Replace with your MySQL username
        password="123456",   # Replace with your MySQL password
        database="ecommerce"  # Replace with your actual database name
    )