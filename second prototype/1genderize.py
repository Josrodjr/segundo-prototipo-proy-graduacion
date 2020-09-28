import pandas as pd 
# import the genderize for gender inference
from gender import getGenders
# second gender identifier
import gender_guesser.detector as gndr
# third gender identifier spanish
import genderator

def most_votes(votes):
    male = votes['male']
    female = votes['female']
    unknown = votes['unknown']

    if male == female == unknown:
        return 'unknown'
    if male > female:
        return 'male'
    if female > male:
        return 'female'
    if female == male:
        return 'andy'

def gender_voter(name):
    votes = {
        "male": 0,
        "female": 0,
        "unknown": 0
    }
    # fist gender detector (male, female, None)
    found_gender, precision, n_docs = getGenders(name)[0]

    # second gender detector (male, female, mostly_male, mostly_female, andy, unknown)
    d = gndr.Detector(case_sensitive=False)
    found_gender_2 = d.get_gender(name)

    # spanish better detector (Male, Female)
    guesser = genderator.Parser()
    answer = guesser.guess_gender(name)
    if answer:
        spanish_gender = answer['gender']
    else:
        spanish_gender = 'not found'

    # VOTING
    # add votes from first generator
    if found_gender == 'male':
        votes['male'] += 1
    if found_gender == 'female':
        votes['female'] += 1

    # add votes from second generator
    if found_gender_2 == 'male':
        votes['male'] += 1
    if found_gender_2 == 'female':
        votes['female'] += 1
    if found_gender_2 == 'mostly_male':
        votes['male'] += 1
    if found_gender_2 == 'mostly_female':
        votes['female'] += 1
    if found_gender_2 == 'andy':
        votes['male'] += 1
        votes['female'] += 1

    # add votes from third spanish gen
    if spanish_gender == 'Male':
        votes['male'] += 1
    if spanish_gender == 'Female':
        votes['female'] += 1

    return most_votes(votes)


# open the final dataset we are using for the training
df = pd.read_csv('T_SET_ANY.csv')

# generate a new df with the new tabs
column_names = ["name", "twitter_username", "twitter_description", "tweets_number", "friends_number", "followers_number", "account_age_days", "tweets_per_day", "most_used_hashtags", "gender", "tweets_list"]
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
    tweets_list = row['tweets_list']

    # get the gender of the user
    gender = gender_voter(name)
    print(gender)

    # insert into the final
    final_df = final_df.append(pd.Series([name, twitter_username, twitter_description, tweets_number, friends_number, followers_number, account_age_days, tweets_per_day, most_used_hashtags, gender, tweets_list], index = final_df.columns), ignore_index=True)

# after execution generate a new csv with gender
final_df.to_csv('gendered_T_SET_ANY.csv', index=None)