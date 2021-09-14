import codecs
import csv
import hashlib
import json


def main():
    create_files()


def create_files():
    create_users_hash()


def create_users_hash():
    # only hash
    user_dict = {}

    user_counter = 0

    with open("../10kshoppers_beautifier.json", encoding="utf-8") as f:

        data = json.load(f)

        for i in data:
            buffer = [i["age"], i["firstName"], i["gender"], i["lastName"]]

            hash_object = hashlib.md5(str(buffer).encode())
            hex_dig = hash_object.hexdigest()

            user_dict[hex_dig] = user_counter
            user_counter += 1

    with codecs.open("../users_hash.txt", "w", "utf-8") as f:
        for k, v in user_dict.items():
            f.write(str(str(k) + "," + str(v)) + "\n")


def create_trx():
    interests_lot = set()
    items_lot = set()
    # only hash
    user_dict = {}

    items_dict = {}
    counter = 0

    user_counter = 0

    with open("../10kshoppers_beautifier.json", encoding="utf-8") as f:

        data = json.load(f)

        for i in data:
            hex_dig = user_counter
            user_counter += 1

            interests = i["interests"]
            items = i["itemHistory"]

            for item in items:
                if item not in items_dict:
                    items_dict[item] = counter
                    counter += 1

            user_dict[hex_dig] = "".join([str(items_dict.get(i)) + "|" for i in items])[:-1]

            [interests_lot.add(i) for i in interests]
            [items_lot.add(i) for i in items]

    with codecs.open("../item_id.txt", "w", "utf-8") as f:
        for k, v in items_dict.items():
            f.write(str(str(k) + "," + str(v)) + "\n")

    f = csv.writer(codecs.open('../trx.csv', 'w', "utf-8"))
    f.writerow(["customerId", "products"])

    for k, v in user_dict.items():
        f.writerow([k, v])


def create_user_id_log():
    interests_lot = set()
    items_lot = set()
    # only hash
    user_dict = []
    user_counter = 0
    with open("../10kshoppers_beautifier.json", encoding="utf-8") as f:

        data = json.load(f)

        for i in data:
            hex_dig = user_counter
            user_counter += 1

            user_dict.append((hex_dig))

            interests = i["interests"]
            items = i["itemHistory"]

            [interests_lot.add(i) for i in interests]
            [items_lot.add(i) for i in items]

    with codecs.open("../users_id.csv", "w", "utf-8") as f:
        f.write("customerId\n")
        for i in user_dict:
            f.write(str(i) + "\n")


def create_users():
    interests_lot = set()
    items_lot = set()
    # hash -> age, first name, gender, last name
    user_dict = []
    user_counter = 0

    with open("../10kshoppers_beautifier.json", encoding="utf-8") as f:
        data = json.load(f)

        for i in data:
            buffer = [i["age"], i["firstName"], i["gender"], i["lastName"]]
            hex_dig = user_counter
            user_counter += 1

            user_dict.append((hex_dig, buffer))

            interests = i["interests"]
            items = i["itemHistory"]

            [interests_lot.add(i) for i in interests]
            [items_lot.add(i) for i in items]

    with codecs.open("../users.csv", "w", "utf-8") as f:
        for i in user_dict:
            f.write(str(i) + "\n")


if __name__ == '__main__':
    main()
