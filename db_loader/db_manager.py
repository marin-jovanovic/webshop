"""
backend module implementation for database logging
"""

import datetime
import json
import sqlite3
import time
from os.path import join

from pathlib import Path
from ast import literal_eval


class DatabaseManager():
    DEFAULT_DB_FILENAME = "sql_db.db"
    DEFAULT_DB_FOLDER = "db_log"

    DEFAULT_ARCHIVE_FOLDER = "db_archive"

    def __init__(self,
                 db_path=DEFAULT_DB_FILENAME,
                 db_folder=DEFAULT_DB_FOLDER):
        self.last_index_time = datetime.datetime.fromtimestamp(time.time())

        self.db_path = db_path

        Path(db_folder).mkdir(parents=True, exist_ok=True)

        full_path = join(db_folder, db_path)
        self.db_full_path = full_path

        self.connection = sqlite3.connect(full_path)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                       (hash text,  
                       user_id text)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS prod
                       (product_id text,  
                       product text)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reccom
                       (user_id text,  
                       l_1 text,
                       l_2 text,
                       l_3 text,
                       l_4 text,
                       l_5 text,
                       l_6 text,
                       l_7 text,
                       l_8 text,
                       l_9 text,
                       l_10 text                       
                       )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reccom_migrated
                       (user_id text,  
                        l_list text
                       )''')

        # Save (commit) the changes
        self.connection.commit()

    def _close(self):
        """
        closes connection with database

        """

        self.connection.close()
        self.is_opened = False

    def _custom_insert(self, table, *params):
        """
        inserts params into database

        """
        # self.check_connection()
        # print(str(params))
        # Insert a row of data
        self.cursor.execute("INSERT INTO " + table + " VALUES " + str(params))

        self.connection.commit()

    def get_rows(self, query):
        return self.cursor.execute(query)

        # rows = self.cursor.fetchall()
        #
        # print("rows", rows)
        #
        # print("rows", rows)
        # print("---")
        # [print(i) for i in rows]
        #
        #
        # # formatted_rows = []
        # # for line in rows:
        # #     print("line", line)
        # #
        # #     formatted_rows.append(
        # #         [literal_eval(i) for i in line]
        # #     )
        #
        # return formatted_rows


def insert_multiple(table, rows):
    db = DatabaseManager()

    for k, v in rows.items():
        db._custom_insert(table, k, v)

    db._close()


if __name__ == '__main__':
    """"""

    db = DatabaseManager(db_path="tmep")

    # db._custom_insert("users", "2", "[2, 3, 4]")
    # db._custom_insert("items", "2", "[2, 3, 4, 254]")

    # db._custom_insert("reccom_migrated", 2, json.dumps([2, 3, 5, 6]))

    # [print(i) for i in db.get_rows("reccom_migrated")]

    rows = db.get_rows("select * from reccom_migrated")

    for r in rows:

        for elem in r:
            # print(type(elem), elem)
            t = literal_eval(elem)
            print(t)
            # print(type(t), t)
            # print()

    db._close()
