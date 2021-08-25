
# How to Build a Recommendation System for Purchase Data (Step-by-Step)
## Problem statement
## 1. Import modules

%load_ext autoreload
%autoreload 2

import pandas as pd
import numpy as np
import time
import turicreate as tc
from sklearn.cross_validation import train_test_split

import sys
sys.path.append("..")
import scripts.data_layer as data_layer

## 2. Load data

customers = pd.read_csv('../data/recommend_1.csv')
transactions = pd.read_csv('../data/trx_data.csv')
print(customers.shape)
customers.head()
print(transactions.shape)
transactions.head()

## 3. Data preparation

# example 1: split product items
transactions['products'] = transactions['products'].apply(lambda x: [int(i) for i in x.split('|')])
transactions.head(2).set_index('customerId')['products'].apply(pd.Series).reset_index()
# example 2: organize a given table into a dataframe with customerId, single productId, and purchase count
pd.melt(transactions.head(2).set_index('customerId')['products'].apply(pd.Series).reset_index(), 
             id_vars=['customerId'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['customerId', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})

### 3.1. Create data with user, item, and target field

s=time.time()

data = pd.melt(transactions.set_index('customerId')['products'].apply(pd.Series).reset_index(), 
             id_vars=['customerId'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['customerId', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})
data['productId'] = data['productId'].astype(np.int64)

print("Execution time:", round((time.time()-s)/60,2), "minutes")
print(data.shape)
data.head()

### 3.2. Create dummy

def create_data_dummy(data):
    data_dummy = data.copy()
    data_dummy['purchase_dummy'] = 1
    return data_dummy
data_dummy = create_data_dummy(data)

### 3.3. Normalize item values across users

df_matrix = pd.pivot_table(data, values='purchase_count', index='customerId', columns='productId')
df_matrix.head()
(df_matrix.shape)
df_matrix_norm = (df_matrix-df_matrix.min())/(df_matrix.max()-df_matrix.min())
print(df_matrix_norm.shape)
df_matrix_norm.head()
# create a table for input to the modeling

d = df_matrix_norm.reset_index()
d.index.names = ['scaled_purchase_freq']
data_norm = pd.melt(d, id_vars=['customerId'], value_name='scaled_purchase_freq').dropna()
print(data_norm.shape)
data_norm.head()

#### Define a function for normalizing data
def normalize_data(data):
    df_matrix = pd.pivot_table(data, values='purchase_count', index='customerId', columns='productId')
    df_matrix_norm = (df_matrix-df_matrix.min())/(df_matrix.max()-df_matrix.min())
    d = df_matrix_norm.reset_index()
    d.index.names = ['scaled_purchase_freq']
    return pd.melt(d, id_vars=['customerId'], value_name='scaled_purchase_freq').dropna()



## 4. Split train and test set

train, test = train_test_split(data, test_size = .2)
print(train.shape, test.shape)
# Using turicreate library, we convert dataframe to SFrame - this will be useful in the modeling part

train_data = tc.SFrame(train)
test_data = tc.SFrame(test)
train_data
test_data

#### Define a `split_data` function for splitting data to training and test set
# We can define a function for this step as follows

def split_data(data):
    '''
    Splits dataset into training and test set.
    
    Args:
        data (pandas.DataFrame)
        
    Returns
        train_data (tc.SFrame)
        test_data (tc.SFrame)
    '''
    train, test = train_test_split(data, test_size = .2)
    train_data = tc.SFrame(train)
    test_data = tc.SFrame(test)
    return train_data, test_data
# lets try with both dummy table and scaled/normalized purchase table

train_data_dummy, test_data_dummy = split_data(data_dummy)
train_data_norm, test_data_norm = split_data(data_norm)

## 5. Baseline Model
### 5.1. Using a Popularity model as a baseline
#### Using purchase counts
# variables to define field names
user_id = 'customerId'
item_id = 'productId'
target = 'purchase_count'
users_to_recommend = list(transactions[user_id])
n_rec = 10 # number of items to recommend
n_display = 30
popularity_model = tc.popularity_recommender.create(train_data, 
                                                    user_id=user_id, 
                                                    item_id=item_id, 
                                                    target=target)
# Get recommendations for a list of users to recommend (from customers file)
# Printed below is head / top 30 rows for first 3 customers with 10 recommendations each

popularity_recomm = popularity_model.recommend(users=users_to_recommend, k=n_rec)
popularity_recomm.print_rows(n_display)

#### Define a `model` function for model selection
# Since turicreate is very accessible library, we can define a model selection function as below

def model(train_data, name, user_id, item_id, target, users_to_recommend, n_rec, n_display):
    if name == 'popularity':
        model = tc.popularity_recommender.create(train_data, 
                                                    user_id=user_id, 
                                                    item_id=item_id, 
                                                    target=target)
    elif name == 'cosine':
        model = tc.item_similarity_recommender.create(train_data, 
                                                    user_id=user_id, 
                                                    item_id=item_id, 
                                                    target=target, 
                                                    similarity_type='cosine')
    elif name == 'pearson':
        model = tc.item_similarity_recommender.create(train_data, 
                                                    user_id=user_id, 
                                                    item_id=item_id, 
                                                    target=target, 
                                                    similarity_type='pearson')
        
    recom = model.recommend(users=users_to_recommend, k=n_rec)
    recom.print_rows(n_display)
    return model
# variables to define field names
# constant variables include:
user_id = 'customerId'
item_id = 'productId'
users_to_recommend = list(customers[user_id])
n_rec = 10 # number of items to recommend
n_display = 30 # to print the head / first few rows in a defined dataset

#### Using purchase dummy
# these variables will change accordingly
name = 'popularity'
target = 'purchase_dummy'
pop_dummy = model(train_data_dummy, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

#### Using normalized purchase count
name = 'popularity'
target = 'scaled_purchase_freq'
pop_norm = model(train_data_norm, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

#### Notes

train.groupby(by=item_id)['purchase_count'].mean().sort_values(ascending=False).head(20)

## 6. Collaborative Filtering Model


### 6.1. `Cosine` similarity


#### Using purchase count
# these variables will change accordingly
name = 'cosine'
target = 'purchase_count'
cos = model(train_data, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

#### Using purchase dummy
# these variables will change accordingly
name = 'cosine'
target = 'purchase_dummy'
cos_dummy = model(train_data_dummy, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

#### Using normalized purchase count
name = 'cosine'
target = 'scaled_purchase_freq'
cos_norm = model(train_data_norm, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

### 6.2. `Pearson` similarity


#### Using purchase count
# these variables will change accordingly
name = 'pearson'
target = 'purchase_count'
pear = model(train_data, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

#### Using purchase dummy
# these variables will change accordingly
name = 'pearson'
target = 'purchase_dummy'
pear_dummy = model(train_data_dummy, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

#### Using normalized purchase count
name = 'pearson'
target = 'scaled_purchase_freq'
pear_norm = model(train_data_norm, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

#### Note


## 7. Model Evaluation

# create initial callable variables

models_w_counts = [popularity_model, cos, pear]
models_w_dummy = [pop_dummy, cos_dummy, pear_dummy]
models_w_norm = [pop_norm, cos_norm, pear_norm]

names_w_counts = ['Popularity Model on Purchase Counts', 'Cosine Similarity on Purchase Counts', 'Pearson Similarity on Purchase Counts']
names_w_dummy = ['Popularity Model on Purchase Dummy', 'Cosine Similarity on Purchase Dummy', 'Pearson Similarity on Purchase Dummy']
names_w_norm = ['Popularity Model on Scaled Purchase Counts', 'Cosine Similarity on Scaled Purchase Counts', 'Pearson Similarity on Scaled Purchase Counts']

#### Models on purchase counts
eval_counts = tc.recommender.util.compare_models(test_data, models_w_counts, model_names=names_w_counts)

#### Models on purchase dummy
eval_dummy = tc.recommender.util.compare_models(test_data_dummy, models_w_dummy, model_names=names_w_dummy)

#### Models on normalized purchase frequency
eval_norm = tc.recommender.util.compare_models(test_data_norm, models_w_norm, model_names=names_w_norm)

## 8. Model Selection
### 8.1. Evaluation summary


#### Notes


## 8. Final Output

users_to_recommend = list(customers[user_id])

final_model = tc.item_similarity_recommender.create(tc.SFrame(data_dummy), 
                                            user_id=user_id, 
                                            item_id=item_id, 
                                            target='purchase_dummy', 
                                            similarity_type='cosine')

recom = final_model.recommend(users=users_to_recommend, k=n_rec)
recom.print_rows(n_display)

### 8.1. CSV output file
df_rec = recom.to_dataframe()
print(df_rec.shape)
df_rec.head()
df_rec['recommendedProducts'] = df_rec.groupby([user_id])[item_id].transform(lambda x: '|'.join(x.astype(str)))
df_output = df_rec[['customerId', 'recommendedProducts']].drop_duplicates().sort_values('customerId').set_index('customerId')

#### Define a function to create a desired output
def create_output(model, users_to_recommend, n_rec, print_csv=True):
    recomendation = model.recommend(users=users_to_recommend, k=n_rec)
    df_rec = recomendation.to_dataframe()
    df_rec['recommendedProducts'] = df_rec.groupby([user_id])[item_id] \
        .transform(lambda x: '|'.join(x.astype(str)))
    df_output = df_rec[['customerId', 'recommendedProducts']].drop_duplicates() \
        .sort_values('customerId').set_index('customerId')
    if print_csv:
        df_output.to_csv('../output/option1_recommendation.csv')
        print("An output file can be found in 'output' folder with name 'option1_recommendation.csv'")
    return df_output
df_output = create_output(pear_norm, users_to_recommend, n_rec, print_csv=True)
print(df_output.shape)
df_output.head()

### 8.2. Customer recommendation function
def customer_recomendation(customer_id):
    if customer_id not in df_output.index:
        print('Customer not found.')
        return customer_id
    return df_output.loc[customer_id]
customer_recomendation(4)
customer_recomendation(21)

## Summary


