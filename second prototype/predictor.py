import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow import feature_column


# extract data from the cs
# dataset = pd.read_csv("TRAIN_TEST.csv", header=0)

dataset = pd.read_csv(
    "TRAIN_TEST.csv", header=0, 
    usecols = ["tweets_number", "friends_number", "followers_number", "account_age_days", "tweets_per_day", "gender", "emojis_pondered", "classifier"])

# TODO: use the features in indivitual tweets

# split the dataset into train and test
# train, test = train_test_split(dataset, test_size=0.2, random_state=420, shuffle=True)

train, test = train_test_split(dataset, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)

# print(len(train), 'train examples')
# print(len(val), 'validation examples')
# print(len(test), 'test examples')

# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('classifier')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds


batch_size = 1 # A small batch sized is used for demonstration purposes
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

# for feature_batch, label_batch in train_ds.take(1):
#   print('Every feature:', list(feature_batch.keys()))
#   print('A batch of genders:', feature_batch['gender'])
#   print('A batch of targets:', label_batch )


# We will use this batch to demonstrate several types of feature columns
example_batch = next(iter(train_ds))[0]



feature_columns = []
# numeric cols
for header in ['tweets_number', 'friends_number', 'account_age_days', 'tweets_per_day', 'emojis_pondered']:
    feature_columns.append(feature_column.numeric_column(header))

# indicator_columns
indicator_column_names = ['gender']
for col_name in indicator_column_names:
    categorical_column = feature_column.categorical_column_with_vocabulary_list(
        col_name, dataset[col_name].unique())
    indicator_column = feature_column.indicator_column(categorical_column)
    feature_columns.append(indicator_column)

# capa de entidades
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

# entrenar y crear el modelo
model = tf.keras.Sequential([
  feature_layer,
  layers.Dense(128, activation='relu'),
  layers.Dense(128, activation='relu'),
  layers.Dropout(.1),
  layers.Dense(1)
])

model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

model.fit(train_ds, validation_data=val_ds, epochs=10)

loss, accuracy = model.evaluate(test_ds)
print("Accuracy", accuracy)

tweets_number = 100
friends_number = 110
followers_number = 10
account_age_days = 2000
tweets_per_day = 10
gender = 'female'
emojis_pondered = 10
classifier = 1

dataset = dataset.append(pd.Series([tweets_number, friends_number, followers_number, account_age_days, tweets_per_day, gender, emojis_pondered, classifier], index = dataset.columns), ignore_index=True)

test_subject = df_to_dataset(dataset.tail(1), shuffle=False, batch_size=batch_size)
loss, manual_test = model.evaluate(test_subject)

print('prediction: ', manual_test)

