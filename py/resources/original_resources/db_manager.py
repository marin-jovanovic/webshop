"""
backend module implementation for database logging
"""

import datetime
import sqlite3
import time
from os.path import join
from shutil import copy


class DatabaseManager():
    DEFAULT_DB_FILENAME = "sql_db.db"
    DEFAULT_DB_FOLDER = "db_log"

    DEFAULT_ARCHIVE_FOLDER = "db_archive"

    def __init__(self, db_path=DEFAULT_DB_FILENAME, index_time=180,
                 log_buffer=5000, log_folder=DEFAULT_ARCHIVE_FOLDER, db_folder=DEFAULT_DB_FOLDER):

        self.last_index_time = datetime.datetime.fromtimestamp(time.time())
        # self.index_time = index_time
        # self.log_buffer = log_buffer
        self.db_path = db_path
        self.log_folder = log_folder

        from pathlib import Path
        Path(log_folder).mkdir(parents=True, exist_ok=True)

        Path(db_folder).mkdir(parents=True, exist_ok=True)

        # super().__init__(True)

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


        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS t
        #                (date text,
        #                asdu integer,
        #                io integer,
        #                value real)''')

        # Save (commit) the changes
        self.connection.commit()

    def _close(self):
        """
        closes connection with database

        """

        # self.check_connection()

        self.connection.close()
        self.is_opened = False

    def insert_wrapper(self, asdu, io, value):
        self._insert(asdu, io, value)

        self._indexing_handler()
        self._cleanup()

    # def _cleanup(self):
    #     """
    #     create backup and empty current db
    #
    #     """
    #
    #     self.check_connection()
    #
    #     num_of_rows = self.cursor.execute("SELECT COUNT(*) FROM t;").fetchone()[0]
    #     print(num_of_rows)
    #
    #     if num_of_rows >= self.log_buffer:
    #         current_time = str(datetime.datetime.fromtimestamp(time.time())).replace(" ", "_")
    #         full_path = join(self.log_folder, current_time + ".db")
    #         open(full_path, "w+")
    #         copy(self.db_full_path, full_path)
    #
    #         self.cursor.execute("DELETE FROM t")
    #
    #     self.connection.commit()

    # def _create_index(self):
    #     self.check_connection()
    #
    #     self.cursor.execute('''DROP INDEX IF EXISTS t_index''')
    #
    #     self.cursor.execute('''CREATE UNIQUE INDEX t_index ON t (asdu, io, date)''')
    #
    #     # Save (commit) the changes
    #     self.connection.commit()

    # def _indexing_handler(self):
    #     self.check_connection()
    #
    #     current_time = datetime.datetime.fromtimestamp(time.time())
    #
    #     if current_time - datetime.timedelta(seconds=self.index_time) > self.last_index_time:
    #         self._create_index()
    #         print("reindexing")
    #         self.last_index_time = current_time

    # def _insert(self, asdu, io, value):
    #     """
    #     inserts params into database
    #
    #     """
    #     self.check_connection()
    #
    #     current_time = datetime.datetime.fromtimestamp(time.time())
    #
    #     self.cursor.execute(
    #         f"INSERT INTO t VALUES "
    #         f"(\"{current_time}\", {asdu}, {io}, {value})"
    #     )
    #
    #     self.connection.commit()

    def _custom_insert(self, table, *params):
        """
        inserts params into database

        """
        # self.check_connection()
        # print(str(params))
        # Insert a row of data
        self.cursor.execute("INSERT INTO " + table + " VALUES " + str(params))

        self.connection.commit()

    def get_rows(self, table):
        return self.cursor.execute("select * from " + table)


def insert_multiple(table, rows):
    db = DatabaseManager()

    for k,v in rows.items():
        db._custom_insert(table, k, v)

    db._close()

if __name__ == '__main__':
    """"""
    #
    #     self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
    #                    (customer_id text,
    #                    products_list text)''')
    #
    #     self.cursor.execute('''CREATE TABLE IF NOT EXISTS items
    #                    (product text,
    #                    product_id text)''')

    db = DatabaseManager()

    db._custom_insert("users", "2", "[2, 3, 4]")
    db._custom_insert("items", "2", "[2, 3, 4, 254]")

    [print(i) for i in db.get_rows("users")]

    #
    # db._cleanup()
    #
    # while True:
    #     db._insert("t", 2, 3, 2.4)
    #     db._indexing_handler()
    #     db._cleanup()

    # print(time.time())
    # current_time = datetime.datetime.fromtimestamp(time.time())
    # print(current_time)

    # create_index()
    #
    # db_init()
    # for row in cur.execute('pragma index_info("t_index")'):
    #     print(row)
    # db_close()

    # db_init()
    #
    # create_db()
    #
    # db_insert_into_t("t", 20, 4, 35.14)
    # db_insert_into_t("t", 22, 41, 33.14)
    # db_insert_into_t("t", 23, 44, 31.14)
    #
      #
    db._close()
