import codecs
import hashlib

# import pandas as pd

# from sklearn.cross_validation import train_test_split
from db_manager import DatabaseManager

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

    c_id_to_prod_id['recommendedProducts'] = c_id_to_prod_id['recommendedProducts'].apply(
        lambda x: [int(i) for i in x.split('|')])

    # print(c_id_to_prod_id)

    d = c_id_to_prod_id["recommendedProducts"].to_dict()

    # for k, v in d.items():
    #     print(k, "->", v)

    return d


def load_data_from_file(source_filename, skip_num_of_lines=0, is_reversed=False):
    d = []

    skip_num_of_lines += 1

    # with codecs.open('resources/my_users.csv', "r", encoding="utf-8", newline='') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #
    #     for row in spamreader:
    #         print(row)

    with codecs.open(source_filename, "r", "utf-8") as f:

        l = f.readlines()
        for i in l:
            skip_num_of_lines -= 1

            if skip_num_of_lines > 0:
                continue

            i = i[:-1]
            t = i.replace("|", ",").split(",")

            print(t)

            if is_reversed:
                d.append(t.reverse())

            else:
                d.append(t)

            # if not is_reversed:
            #     d["".join(i for i in t[:-1])] = t[-1]
            #
            # else:
            #     d[t[-1]] = "".join(i for i in t[:-1])

    # [print(i) for i in d.items()]

    return d


def save_users():

    db = DatabaseManager()

    for i in load_data_from_file(
        source_filename="resources/users_hash.txt",
        skip_num_of_lines=0,
        is_reversed=True
    ):
        print(i)

        # db._custom_insert("users", k, v)

    db._close()


def save_prod():
    db = DatabaseManager()

    for k, v in load_data_from_file(
        source_filename="resources/item_id.txt",
        skip_num_of_lines=0,
        is_reversed=True
    ).items():
        print(k,v)

        # db._custom_insert("prod", k, v)

    db._close()


def save_reccom():
    db = DatabaseManager()

    # for k, v in get_reccom().items():
    #     print(k,v)

    for i in get_reccom():
        print(i)

    db._close()


def get_reccom():
    d = []

    with codecs.open("resources/my_users.csv", "r", "utf-8") as f:
        l = f.readlines()
        for i in l[1:]:
            i = i[:-1]
            t = i.split(",")

            r = t[-1].split("|")

            d.append([t[0]] + r)

    return d


def base_fill():
    save_users()
    # save_prod()
    # save_reccom()


def main():
    """"""

    # todo fix isreversed for more than 1

    base_fill()

    # base_fill()

    # f = load_data_from_file(source_filename="tmp.txt",
    #                     is_reversed=True,
    #                     skip_num_of_lines=2)
    #
    # print(len(f))
    # base_fill()

    # get_users_hash(24, "Luca", "male", "Stolnici")

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
