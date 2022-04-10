import os
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
       :param conn: Connection object
       :param create_table_sql: a CREATE TABLE statement
       :return:
       """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)

    except Error as e:
        print(e)


def main():
    database = r".\db\pythonsqlite.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS USERS (
                                        username varchar(100) PRIMARY KEY,
                                        password varchar(100) NOT NULL,
                                        public_key varchar(200),
                                        private_key varchar(200)
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)


    else:
        print("Error! cannot create the database connection.")


def getcurConn():
    database = r".\db\pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    return conn, cur


if __name__ == '__main__':
    main()
