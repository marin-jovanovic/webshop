import hashlib
from ast import literal_eval

import numpy as np
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
import codecs

# from sklearn.cross_validation import train_test_split

"""
users
    customer id -> age, name, sex, last name

item_id
    recommended products -> recommended products id
    
users_hash
    hash -> customer id

my_users
    customer id -> recommended products id

"""

def get_users_hash(age, first_name, gender, last_name):
    age = 24
    first_name = "Luca"
    gender = "male"
    last_name = "Stolnici"

    buffer = [age, first_name, gender, last_name]
    # buffer = [i["age"], i["firstName"], i["gender"], i["lastName"]]

    print("str", str(buffer).encode())
    hash_object = hashlib.md5(str(buffer).encode())
    hex_dig = hash_object.hexdigest()

    print(hex_dig)

    return hex_dig

    # users = load_users_hash()
    #
    # for k,v in users.items():
    #     print(k, "->", v)

def get_my_users():

    c_id_to_prod_id = pd.read_csv('resources/my_users.csv')

    # print(c_id_to_prod_id)

    c_id_to_prod_id['recommendedProducts'] = c_id_to_prod_id['recommendedProducts'].apply(lambda x: [int(i) for i in x.split('|')])

    # print(c_id_to_prod_id)

    d = c_id_to_prod_id["recommendedProducts"].to_dict()

    # for k, v in d.items():
    #     print(k, "->", v)

    return d


def get_item_id_reversed():

    d = {}

    # c_id_to_c = pd.read_csv("resources/users.csv")
    with codecs.open("resources/item_id.txt", "r", "utf-8") as f:
        l = f.readlines()
        for i in l:
            i = i[:-1]
            # print(i)
            t = i.split(",")

            d[t[-1]] = "".join(i for i in t[:-1])

    # [print(i) for i in d.items()]


    return d


def get_users_hash_log():

    d = {}

    # c_id_to_c = pd.read_csv("resources/users.csv")
    with codecs.open("resources/users_hash.txt", "r", "utf-8") as f:
        l = f.readlines()
        for i in l:
            i = i[:-1]
            # print(i)
            t = i.split(",")

            d["".join(i for i in t[:-1])] = t[-1]

    [print(i) for i in d.items()]

    return d


def save_users():
    #     def insert_multiple(table, rows):
    from db_manager import insert_multiple
    # insert_multiple("users", )

    from db_manager import DatabaseManager

    db = DatabaseManager()

    for k,v in get_users_hash_log().items():
        # print(k,v)

        db._custom_insert("users", k, v)
    # db._custom_insert("users", "2", "[2, 3, 4]")
    # db._custom_insert("items", "2", "[2, 3, 4, 254]")

    db._close()


# self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                (hash text,
#                user_id text)''')
#
# self.cursor.execute('''CREATE TABLE IF NOT EXISTS prod
#                (product_id text,
#                product text)''')
#
# self.cursor.execute('''CREATE TABLE IF NOT EXISTS reccom
#                (user_id text,
#                list_prod_id text)''')

def save_prod():
    from db_manager import DatabaseManager

    db = DatabaseManager()

    for k,v in get_item_id_reversed().items():
        # print(k,v)

        db._custom_insert("prod", k, v)
    # db._custom_insert("users", "2", "[2, 3, 4]")
    # db._custom_insert("items", "2", "[2, 3, 4, 254]")

    db._close()


def save_reccom():
    from db_manager import DatabaseManager

    db = DatabaseManager()

    for k,v in get_reccom().items():
        # print(k,v)
        #
        db._custom_insert("reccom", k,
                          v[0],
                          v[1],
                          v[2],
                          v[3],
                          v[4],
                          v[5],
                          v[6],
                          v[7],
                          v[8],
                          v[9]
                          )

    #         self.cursor.execute('''CREATE TABLE IF NOT EXISTS reccom
    #                        (user_id text,
    #                        l_1 text,
    #                        l_2 text,
    #                        l_3 text,
    #                        l_4 text,
    #                        l_5 text,
    #                        l_6 text,
    #                        l_7 text,
    #                        l_8 text,
    #                        l_9 text,
    #                        l_10 text
    #                        )''')
    db._close()


def get_reccom():

    d = {}

    # c_id_to_c = pd.read_csv("resources/users.csv")
    with codecs.open("resources/my_users.csv", "r", "utf-8") as f:
        l = f.readlines()
        for i in l[1:]:
            i = i[:-1]
            t = i.split(",")

            r = t[-1].split("|")

            # print(len(r))

            d["".join(i for i in t[:-1])] = r

    # [print(i) for i in d.items()]

    return d

def base_fill():
    save_users()
    # ok
    save_prod()
    # ok
    save_reccom()

def reformat():
    pass
def main():
    """"""

    # base_fill()

    get_users_hash(24, "Luca", "male", "Stolnici")


    # lis = []
    #
    # with codecs.open("resources/my_users.csv", "r", "utf-8") as f:
    #     l = f.readlines()
    #     for i in l:
    #         i = i[:-1]
    #         t = i.split(",")
    #
    #         t = t[0]
    #
    #         lis.append(t)
    #         print(t)
    #
    # print("llen", len(lis))
    #
    # sys.path.append("..")
    # import scripts.data_layer as data_layer

    # ## 2. Load data
    # Two datasets are used in this exercise, which can be found in `data` folder:
    # * `recommend_1.csv` consisting of a list of 1000 customer IDs to recommend as output
    # * `trx_data.csv` consisting of user transactions
    #
    # The format is as follows.

    # In[2]:

    # customers = pd.read_csv('../data/recommend_1.csv')
    # transactions = pd.read_csv('../data/trx_data.csv')


    # transactions = pd.read_csv('../data/trx.csv')

    # print(d)

    # output = literal_eval(i)
    # print(output)
    # print(type(output))

    # print(l)
    # print(c_id_to_c)
    # breakpoint()

    # for i in customers:
    #     print(i)



def load_users_hash():
    users = {}
    with codecs.open("resources/users_hash.txt", "r", "utf-8") as f:
        l = f.readlines()
        for i in l:
            i = i[:-1].split(",")
            users[i[0]] = i[1]
            # print(i)
    return users


if __name__ == '__main__':
    main()
