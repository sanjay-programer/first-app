import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
load_dotenv()

try:
    conn=mysql.connector.connect(
        host=os.getenv("host"),
        username=os.getenv("db_username"),
        database=os.getenv("database"),
        password=os.getenv("password"),
        port=3306
    )

    cursor=conn.cursor()
    if conn.is_connected():
        print(f"connection successful")

except Error as error:
    print(f"connection failed \nError:{error}")