import pandas as pd
# open both the final csvs we got
df = pd.read_csv('final_dataset.csv')
df1 = pd.read_csv('final_dataset_1.csv')

# set the final columns
column_names = ["name", "twitter_username", "twitter_description", "tweets_number", "friends_number", "followers_number", "account_age_days", "tweets_per_day", "most_used_hashtags", "tweets_list"]
final_df = pd.DataFrame(columns = column_names)

# iterate over the rows of one dataset inserting it to the final one
for index, row in df.iterrows():
    name = row['name']
    twitter_username =  row['twitter_username']
    twitter_description = row['twitter_description']
    tweets_number = row['tweets_number']
    friends_number = row['friends_number']
    followers_number = row['followers_number']
    account_age_days = row['account_age_days']
    tweets_per_day = row['tweets_per_day']
    most_used_hashtags = row['most_used_hashtags']
    tweets_list = row['tweets_list']

    # insert into the final
    final_df = final_df.append(pd.Series([name, twitter_username, twitter_description, tweets_number, friends_number, followers_number, account_age_days, tweets_per_day, most_used_hashtags, tweets_list], index = final_df.columns), ignore_index=True)

# print total columns so far
total_rows = final_df.count()
print(total_rows+1)

# iterate over the second one inserting it to final dataset
for index, row in df1.iterrows():
    name = row['name']
    twitter_username =  row['twitter_username']
    twitter_description = row['twitter_description']
    tweets_number = row['tweets_number']
    friends_number = row['friends_number']
    followers_number = row['followers_number']
    account_age_days = row['account_age_days']
    tweets_per_day = row['tweets_per_day']
    most_used_hashtags = row['most_used_hashtags']
    tweets_list = row['tweets_list']

    # insert into the final
    final_df = final_df.append(pd.Series([name, twitter_username, twitter_description, tweets_number, friends_number, followers_number, account_age_days, tweets_per_day, most_used_hashtags, tweets_list], index = final_df.columns), ignore_index=True)

# print total rows in whole set
total_rows = final_df.count()
print(total_rows+1)

# save the merged set
final_df.to_csv('T_SET.csv', index=None)