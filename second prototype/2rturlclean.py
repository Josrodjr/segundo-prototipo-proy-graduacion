import pandas as pd 
# regular expressions
import re
# for getting the list of tweets back
import ast
# import the emoji library for emoji manipulation
import emoji

emoji_pondering = {
    # extremely bad
    ':pistol:': 20,
    ':electric_plug:': 20,
    ':skull:': 20,
    ':crying_face:': 20,
    ':loudly_crying_face:': 10,
    ':face_with_open_mouth_and_cold_sweat:': 10,
    ':face_with_cold_sweat:': 10,
    ':broken_heart:': 10,
    ':anguished_face:': 10,
    ':squared_sos:': 10,
    ':worried_face:': 10,
    ':dissapointed_but_relieved_face:': 10,
    ':clown_face:': 10,
    

    # bad
    ':ballot_box:': 2,
    ':box_drawings_light_quadruple_dash_horizontal:': 2,
    ':fish_cake_with_swirl_design:': 2,
    ':imp:': 2,
    ':white_frowning_face:': 2,
    ':box_drawings_heavy_up_and_horizontal:': 2,
    ':wrench:': 2,
    ':battery:': 2,
    ':confused_face:': 2,
    ':pushpin:': 2,
    ':weary_face:': 2,
    ':unamused_face:': 2,
    ':pouting_cat_face:': 2,
    ':melon:': 2,
    ':crying_cat_face:': 2,
    ':person_frowning:': 2,
    ':black_scissors:': 2,
    ':angry_face:': 2,
    ':neutral_face:': 2,
    ':frowning_face_with_open_mouth:': 2,
    ':persevering_face:': 2,
    ':no_entry_sign:': 2,


    # the medium level
    ':school:': 1,
    ':object_replacement_character:': 1,
    ':puting_face:': 1,
    ':expresionless_face:': 1,
    ':black_square:': 1,
    ':thumbs_down_sign:': 1,
    ':tired_face:': 1,
    ':confunded_face:': 1,
    ':dissapointed_face:': 1,
    ':face_with_look_of_triumph:': 1,
    ':police_officer:': 1,
    ':box_drawings_heavy_down_and_horizontal:': 1,
    ':droplet:': 1,
    ':face_with_medical_mask:': 1,
    ':pensive_face:': 1,
    ':face_with_no_good_gesture:': 1,
    ':curly_loop:': 1,
    ':guardsman:': 1,
    ':person_with_pouting_face:': 1

}

def ponder_emojis(all_emojis):
    numeric_value_emoji = 0
    for eji in all_emojis:
        demojied = emoji.demojize(eji)
        if demojied in emoji_pondering:
            numeric_value_emoji += emoji_pondering[demojied]

    return numeric_value_emoji

def extract_emojis(s):
    return ''.join(c for c in s if c in emoji.UNICODE_EMOJI)

def text_without_emojis(s):
    return ''.join(c for c in s if c not in emoji.UNICODE_EMOJI)

def remove_emoji_hard(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def remove_rt(tweet):
    return re.compile('\#').sub('', re.compile('RT @').sub('@', tweet).strip())

def filter_urls(tweet):
    # remove the links
    tweet = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '', tweet, flags=re.MULTILINE)
    # remove the url and other links
    tweet = re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '', tweet, flags=re.MULTILINE)
    # remove twitter urls 
    tweet = re.sub(r"http\S+", "", tweet)
    return tweet

def remove_hashtags(tweet):
    tweet = re.sub(r'#(\w+)', ' ', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'@(\w+)', ' ', tweet, flags=re.MULTILINE)
    return tweet

def remove_colon(tweet):
    tweet = tweet.replace(':','')
    # finish the filter by removing the end and start spaces
    tweet = tweet.strip()
    return tweet

# open the final dataset we are using for the training
df = pd.read_csv('gendered_T_SET_ANY.csv')

# generate a new df with the new tabs
column_names = ["name", "twitter_username", "twitter_description", "tweets_number", "friends_number", "followers_number", "account_age_days", "tweets_per_day", "most_used_hashtags", "gender", "emojis_pondered", "tweets_list"]
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
    tweets_list = list(ast.literal_eval(row['tweets_list']))

    new_list = []
    # print(len(tweets_list))
    for tweet in tweets_list:
        # print(tweet)
        tweet = remove_rt(tweet)
        tweet = filter_urls(tweet)
        tweet = remove_hashtags(tweet)
        tweet = remove_colon(tweet)
        new_list.append(tweet)
    
    all_emojis = ''
    filtered_emojis = []
    for tweet in new_list:
        # get all the emojis in the list
        emojis = extract_emojis(tweet)
        # concat the emojis
        all_emojis += emojis

        # the clean texts
        text_no_emoji = remove_emoji_hard(tweet)
        text_no_emoji = text_without_emojis(text_no_emoji)
        filtered_emojis.append(text_no_emoji)
        
    # print(filtered_emojis)
    # get numeric value of the string of emoji from user
    em_ponder = ponder_emojis(all_emojis)

    # insert into the final
    final_df = final_df.append(pd.Series([name, twitter_username, twitter_description, tweets_number, friends_number, followers_number, account_age_days, tweets_per_day, most_used_hashtags, gender, em_ponder, filtered_emojis], index = final_df.columns), ignore_index=True)

# after execution generate a new csv with gender
final_df.to_csv('emoji_T_SET_ANY.csv', index=None)