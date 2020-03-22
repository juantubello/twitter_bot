import tweepy
import random
import os
import time
import codecs
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

def auth_in_tweepy(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY, ACCESS_SECRET):
    """
    This function logs into TWEEPY API in order to tweet from our BOT user (@CoscuBot)
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET) 
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
    api = tweepy.API(auth)

    return api

def auth_in_gdrive():
    """
    This function logs into DRIVE API in order to interact, in this case, with our DATABASE
    """
    json_creds = json.loads(os.getenv('GOOGLE_SHEETS_CREDS_JSON'))
    with open('gcreds.json', 'w') as fp:
         json.dump(json_creds, fp)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] #Add Endpoint to make it work
    creds = ServiceAccountCredentials.from_json_keyfile_name('gcreds.json', scope)
    client = gspread.authorize(creds)

    return client

def avoid_already_replied_id(db_data, reply_id):
    """
    This function avoid tweets already replied
    """
    already_replied = False
    db_ids = db_data[1:]

    for tw_id in db_ids:
        if reply_id == tw_id:
             print("Tweet ID: ", reply_id, " already replied" )
             already_replied = True

    return already_replied

def avoid_tweets_from_users(current_user, users_to_avoid, reply_id):
    """
    This function avoid tweets from certain users, to prevent shadowban
    """
    avoid_tweet = False

    if current_user in users_to_avoid:
         print("Tweet ID: ", reply_id , "is from user", current_user, " | AVOIDED")
         avoid_tweet = True
   
    return avoid_tweet
    
def reply_to_tweet(tweet_to_tweet, reply_id):
    """
    This function replies with a tweet to a tweet id passed by parameter
    """
    try:
         if api.update_status(status = tweet_to_tweet, in_reply_to_status_id = reply_id) :
             print("Tweet ID: ", reply_id, "tweeted successfuly")
    except tweepy.error.TweepError as e:
         print(e)

def update_excel_db(tweet_to_tweet, reply_id):
    """
    This function updates the excel,adding one new row, used as a DataBase
    """
    row = [reply_id, tweet_to_tweet]
    sheet.append_row(row)

def get_file_data(file_name):
    """
    This function get all de data from a certain file passed by parameter
    """
    with codecs.open(file_name, encoding='ISO-8859-1', errors='ignore') as myfile:    
        data = myfile.readlines()

    myfile.close()   

    return data

def get_last_quote_index():
    """
    This function get last random number from DataBase used to make 
    the last quote reply, in order to avoid duplicate status
    """
    return int(sheet.cell(2, 3).value)

def generate_tweet_reply(quotes, reply_id, last_random_index):
    """
    This function generates a tweet to reply 
    """
    r = random.randint(0, (len(quotes) - 1))

    while(r == last_random_index):
        r = random.randint(0, (len(quotes) - 1))

    sheet.update_acell('C2', r)
    tweet_to_tweet = "@" + username +" "+ quotes[r]

    return tweet_to_tweet

## Logic ##

INTERVAL = 60 * 10 #Ten minutes interval

#Creds to use Tweepy API
CONSUMER_KEY    = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY      = os.getenv('ACCESS_KEY')
ACCESS_SECRET   = os.getenv('ACCESS_SECRET')

api = auth_in_tweepy(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY, ACCESS_SECRET)

#Creds to use Google Drive API (db)
client = auth_in_gdrive()

avoid_users = ['CoscuBot', 'CogeNoCogeBOT', 'BotReunion', 'FacuBanzasBOT']

sheet = client.open("CoscuBot-IdLog").sheet1

while True:

 #Get all tweets that contains "CoscuBot"
 twitter_data = api.search("CoscuBot")

 for tweet in twitter_data:

     #ID of the tweet that contains @CoscuBot TAG
     reply_id_str = tweet.id_str

     #User who mentions @CoscuBot
     username = tweet.user.screen_name

     if avoid_tweets_from_users(username,avoid_users,reply_id_str):
         continue

     db_data = sheet.col_values(1)

     if not avoid_already_replied_id(db_data, reply_id_str):

         quotes = get_file_data('coscuQuotes.txt')

         last_index = get_last_quote_index()

         tweet_to_tweet = generate_tweet_reply(quotes, reply_id_str, last_index)

         reply_to_tweet(tweet_to_tweet, reply_id_str)

         update_excel_db(tweet_to_tweet, reply_id_str)

 time.sleep(INTERVAL)
