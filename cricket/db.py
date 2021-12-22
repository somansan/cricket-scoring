import sqlite3
from sqlite3 import Error
from sqlite3 import Connection


def create_connection(db_file):
    """Creates a database connection"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn: Connection, create_statement: str):
    if not conn:
        raise Exception("Empty connection object passed")
    elif not create_statement:
        raise Exception("Empty create statements passed")
    else:
        try:
            cur = conn.cursor()
            cur.execute(create_statement)
        except Error as e:
            print(e)


def insert_into(conn: Connection, statement: str, values: tuple or list = ()):
    if conn:
        cur = conn.cursor()
        if isinstance(values, tuple):
            cur.execute(statement, values)
        elif isinstance(values, list):
            for value in values:
                cur.execute(statement, value)
        conn.commit()


