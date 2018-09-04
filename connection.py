import os
import psycopg2
from psycopg2 import extras


def get_connection_string():
    user_name = os.environ.get("PSQL_USER_NAME")
    user_password = os.environ.get("PSQL_PASSWORD")
    host = os.environ.get("PSQL_HOST")
    database_name = os.environ.get("PSQL_DB_NAME")

    environment_variables_defined = user_name and user_password and host and database_name

    if not environment_variables_defined:
        raise KeyError("Some of the needed environment variables are not defined")
    else:
        connection_string = "postgresql://{user_name}:{password}@{host}/{database_name}".format(
            user_name=user_name,
            password=user_password,
            host=host,
            database_name=database_name
        )
        return connection_string


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print("Database connaction problem")
        raise exception
    return connection


def connection_handler(function_to_wrap):
    def wrapper():
        connection = open_database()
        cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
        returned_value = function_to_wrap(cursor, *args, **kwargs)
        cursor.close()
        connection.close()
        return returned_value
    return wrapper
