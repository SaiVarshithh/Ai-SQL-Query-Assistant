import pymysql
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

from src.schemas import PostDatabaseSchema
from src.config.log_handler import logger

load_dotenv()


def get_database_connection(
    host: str, user: str,
    password: str, port: int = 45567,
    database: str = None
):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )
        if connection.is_connected():
            return connection
    except Error as e:
        logger.log_error(f"Error while connecting to MySQL: {e}")
        return None

def get_databases(
    host: str, user: str,
    password: str, port: str = 45567,
    database: str = None
):
    system_databases = ["information_schema", "performance_schema", "mysql", "sys", "query_table"]
    connection = get_database_connection(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            res = cursor.fetchall()
            databases = [
                db[0]
                for db in res
                if db[0] not in system_databases
            ]
        return databases
    finally:
        connection.close()

def get_database_schema(connection):
    schema = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                schema[table_name] = []

                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                for column in columns:
                    schema[table_name].append(
                        {
                            "Column Name": column[0],
                            "Data Type": column[1],
                        }
                    )
    except Exception as e:
        logger.log_error(f"Error fetching database schema: {e}")
        raise

    return schema

def post_database(
    post_database_details: PostDatabaseSchema
):
    try:
        response = str(post_database_details.response)

        with post_database_details.connection.cursor() as cursor:
            sql = f"""
            INSERT INTO {post_database_details.database}.query_table (user_name, user_input, processed_query, response)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    post_database_details.user,
                    post_database_details.user_query,
                    post_database_details.processed_query,
                    response
                ),
            )
            post_database_details.connection.commit()

    except pymysql.MySQLError as e:
        logger.log_info(f"Insertion failed, chat skipped!! {e}")
        return

    finally:
        post_database_details.connection.close()
