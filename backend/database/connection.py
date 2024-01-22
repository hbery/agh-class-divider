# -*- coding: utf-8 -*-
# vim: ts=4 : sts=4 : sw=4 : et : ai :

from os import getenv
from sqlite3 import Error, connect

from dbml_sqlite import toSQLite
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


class DatabaseCreationError(SystemError):
    pass


def create_database(
    database_schema_file: str,
) -> None:
    """Create a .sql SQLite database from .dbml file."""
    connection = None
    sql_script = toSQLite(database_schema_file)
    database_file = getenv("DB_LOCATION") or ""

    if type(sql_script) is not str and sql_script is not None:
        sql_script = " ".join(sql_script)
    elif sql_script is None:
        raise DatabaseCreationError(
            f"Failed to parse .dbml file: {database_schema_file}"
        )

    try:
        connection = connect(database_file)
        with connection:
            connection.executescript(sql_script)
    except Error as e:
        raise e
    finally:
        if connection is not None:
            connection.close()


def get_dbengine(database_file: str | None = None) -> Engine:
    if database_file is None:
        database_file = getenv("DB_LOCATION")
    return create_engine(f"sqlite:///{database_file}")


def get_session(database_file: str | None = None) -> Session:
    engine = get_dbengine(database_file)
    return Session(engine)
