import os
from google.cloud.sql.connector import Connector, IPTypes
import pymysql

# Retrieve environment variables
is_prod = os.getenv('APP_RUNNING_ENV') == 'PROD'

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
cloud_sql_connection_name = os.getenv('CLOUD_SQL_CONNECTION_NAME')


if is_prod:
    connector = Connector() 
else:
    connector = pymysql


# Function to create a connection to the MySQL database
def connect_to_mysql():
    connection = None

    # PROD ENV - GOOGLE CLOUD CONNECTOR 
    if is_prod:
        connection = connector.connect(
            cloud_sql_connection_name,  # Cloud SQL connection name
            "pymysql",                  # Using pymysql for MySQL
            user=db_user,               # Database username
            password=db_pass,           # Database password
            db=db_name,                  # Database name
            ip_type=IPTypes.PRIVATE     # PRIVATE IP, CONNECT THRU VPC SERVERLESS ACCESS
        )

    # DEV ENV
    else:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            db=db_name
        )

    return connection


# def fetch_data():
#     connection = connect_to_mysql()
#     cursor = connection.cursor()

#     try:
#         # Example query to fetch all rows from a table
#         cursor.execute("SELECT * FROM your_table_name")
#         rows = cursor.fetchall()

#         for row in rows:
#             print(row)

#     except Exception as e:
#         print(f"Error fetching data: {e}")
#     finally:
#         cursor.close()
#         connection.close()

# if __name__ == "__main__":
#     fetch_data()