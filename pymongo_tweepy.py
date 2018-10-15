from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
import os
import time

path = '../JSON_files'
print(os.path.exists(path))
if not os.path.exists(path):
    os.mkdir(path, 0o777)
path1 = 'google-drive://chaoswjz@bu.edu/1loKGesRIvMtQ5dj49VlSyL3VBeDozM_B'
MONGO_HOST = 'mongodb://localhost/twitterdb'  # assuming you have mongoDB installed locally
# and a database called 'twitterdb'

#WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#deeplearning']
WORDS = ['#midterm', '#2018midterms', '#election', '#november2018', '#vote2018']

keys_file = open("keys.txt")
lines = keys_file.readlines()
consumer_key = lines[0].rstrip()
consumer_secret = lines[1].rstrip()
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()

class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def __init__(self, api):
        self.num_of_tweets = 0
        #self.start_time = time.time()
        #self.time_limit = 15 * 60

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    '''
    def on_status(self, status):
        try:
            client = MongoClient(MONGO_HOST)

            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitterdb

            # Decode the JSON from Twitter
            client = MongoClient(MONGO_HOST)
            db = client.twitterdb
            datajson = json.dumps(status._json)
            jsondata = json.loads(datajson)
            db.twitter_search.insert(jsondata)

            # grab the 'created_at' data from the Tweet to use for display
            created_at = status.created_at
            print("data is: ", status.full_text)

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            self.num_of_tweets += 1
            print(self.num_of_tweets)
            with open(path + '/' + str(datajson['id']) + '.json', 'w+') as fh:
                json.dump(datajson, fh, indent=4)

            # insert the data into the mongoDB into a collection called twitter_search
            # if twitter_search doesn't exist, it will be created.
            db.twitter_search.insert(datajson)
        except Exception as e:
            print(e)
    '''

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        #if (time.time() - self.start_time) < self.time_limit:
        #    print(time.time() - self.start_time)
        try:
            client = MongoClient(MONGO_HOST)

            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitterdb

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']
            print("data is: ", data)

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            self.num_of_tweets += 1
            print(self.num_of_tweets)
            with open(path + '/' + str(datajson['id']) + '.json', 'w+') as fh:
                json.dump(datajson, fh, indent=4)

            # insert the data into the mongoDB into a collection called twitter_search
            # if twitter_search doesn't exist, it will be created.
            db.twitter_search.insert(datajson)
        except Exception as e:
            print(e)
        #else:
        #    exit()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener, tweet_mode='extended')
print("Tracking: " + str(WORDS))
streamer.filter(languages=["en"], track=WORDS)