import pandas as pd 
# for getting the list of tweets back
import ast

# open the final dataset we are using for the training
df = pd.read_csv('emoji_T_SET.csv')

# generate a new df with the new tabs
column_names = ["name", "twitter_username", "twitter_description", "tweets_number", "friends_number", "followers_number", "account_age_days", "tweets_per_day", "most_used_hashtags", "gender", "emojis_pondered", "classifier", "tweets_list"]
final_df = pd.DataFrame(columns = column_names)

# iterate over the rows of the dataset extracting the data
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
    gender = row['gender']
    emojis_pondered = row['emojis_pondered']
    tweets_list = list(ast.literal_eval(row['tweets_list']))

    # insert the classifier
    classifier = 1

    # insert into the final
    final_df = final_df.append(pd.Series([name, twitter_username, twitter_description, tweets_number, friends_number, followers_number, account_age_days, tweets_per_day, most_used_hashtags, gender, emojis_pondered, classifier, tweets_list], index = final_df.columns), ignore_index=True)

# after execution generate a new csv with gender
final_df.to_csv('FINAL_T_SET.csv', index=None)