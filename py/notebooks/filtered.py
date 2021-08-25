import sys

import pandas as pd

sys.path.append("..")

customers = pd.read_csv('../data/recommend_1.csv')
transactions = pd.read_csv('../data/trx_data.csv')

print(customers.shape)
customers.head()
