# from fastapi import FastAPI, HTTPException
# from sqlalchemy import create_engine, text
# import logging
# from sqlalchemy.exc import SQLAlchemyError
# import os

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI()

# # Railway provides database connection details as environment variables
# DB_HOST = os.getenv("MYSQLHOST", "mysql.railway.internal")
# DB_USER = os.getenv("MYSQLUSER", "root")
# DB_PASSWORD = os.getenv("MYSQLPASSWORD", "VKwsbjfDIiHCbPGBLjGrSsrAkagWcjth")
# DB_NAME = os.getenv("MYSQLDATABASE", "railway")
# DB_PORT = os.getenv("MYSQLPORT", "3306")

# # Construct the database URL
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # Log the database URL (make sure to remove any sensitive information in production)
# logger.info(f"Attempting to connect to database: {DATABASE_URL}")

# try:
#     # Create a SQLAlchemy engine
#     engine = create_engine(DATABASE_URL)
#     logger.info("SQLAlchemy engine created successfully")
# except ImportError as e:
#     logger.error(f"ImportError: {e}")
#     logger.error("Please install required packages using: pip install fastapi sqlalchemy pymysql uvicorn")
#     exit(1)
# except Exception as e:
#     logger.error(f"An unexpected error occurred while creating the engine: {e}")
#     exit(1)

# @app.get("/connect")
# async def connect_to_database():
#     try:
#         # Try to connect to the database and execute a simple query
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             print(result)
#             result.fetchone()
#         logger.info("Successfully connected to the database")
#         return {"message": "Successfully connected to the MySQL database!"}
#     except SQLAlchemyError as e:
#         logger.error(f"Database connection failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the FastAPI MySQL Connection Test"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001)






import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse

def connect_to_mysql(connection_string):
    try:
        result = urlparse(connection_string)
        
        username = result.username
        password = result.password
        host = result.hostname
        port = result.port
        database = result.path.lstrip('/')

        print(username, password, host, port, database)

        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Example connection string
connection_string = 'mysql://root:VKwsbjfDIiHCbPGBLjGrSsrAkagWcjth@roundhouse.proxy.rlwy.net:45567'

# Connect to the database
connection = connect_to_mysql(connection_string)

# Perform the SELECT * FROM my_table operation
if connection and connection.is_connected():
    query = "SELECT * FROM railway.my_table"
    try:
        results = execute_query(connection, query)
        for row in results:
            print(row)
    except Error as e:
        print(f"Error while executing query: {e}")
    finally:
        connection.close()
        print("MySQL connection is closed")

