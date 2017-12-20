from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient


#the name of the MongoDB database 'twitterdb' we save the data into
mongo_host= 'mongodb://localhost/twitterdb'

#select the keywords interested to mine real-time tweets from
search_keys = ['#deeplearning', '#computervision', '#datascience', '#bigdata']

#read the keys.txt file and extract the consumer_key,
#cosumer_secret, access_token and access_token_secret from it
keys_file = open("keys.txt")
lines = keys_file.readlines()
consumer_key = lines[0].rstrip()
consumer_secret = lines[1].rstrip()
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()

class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(mongo_host)

            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitterdb

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']
            if datajson['coordinates'] is not None:
                # print out a message to the screen that we have collected a tweet
                for word in search_keys:
                    if word in datajson['text']:
                        print("found the search key {0} in tweet's text {1}"
                              .format(word, datajson['text'] ))
                print("Tweet collected at " + str(created_at))

                # insert the data into the mongoDB into a collection called twitter_search
                # if twitter_search doesn't exist, it will be created.
                db.twitter_search.insert(datajson)
        except Exception as e:
            print(e)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#you might get 420 error here if you hit the rate limit
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Currently tracking: " + str(search_keys))
streamer.filter(track=search_keys)