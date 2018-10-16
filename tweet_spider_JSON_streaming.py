from __future__ import print_function
import tweepy
import json
import os
import time
import re

path = '../JSON_files'
if not os.path.exists(path):
    os.mkdir(path, 0o777)

WORDS = ['#midterm', '#2018midterms', '#election', '#november2018', '#vote2018']
#WORDS = [re.match(r'^#*vote*')]

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



    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        #if (time.time() - self.start_time) < self.time_limit:
        #    print(time.time() - self.start_time)
        try:
            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the 'created_at' data from the Tweet to use for display
            #created_at = datajson['created_at']

            if 'extended_tweet' in datajson:
                print("data is: ", datajson['extended_tweet']['full_text'])

                # print out a message to the screen that we have collected a tweet
                #print("Tweet collected at " + str(created_at))
                self.num_of_tweets += 1
                #print(self.num_of_tweets)
                #print(" re match: ", re.match(r'^#[a-zA-Z0-9_]*vote[a-zA-Z0-9_]*', datajson['extended_tweet']['full_text']))
                #if re.match(r'[a-zA-Z0-9_ ]*#[a-zA-Z0-9_]*vote[a-zA-Z0-9_ ]*', datajson['extended_tweet']['full_text']) is not None:
                with open(path + '/' + str(datajson['id']) + '.json', 'w+') as fh:
                    json.dump(datajson, fh, indent=4)
            else:
                print("data is: ", datajson['text'])

                # print out a message to the screen that we have collected a tweet
                # print("Tweet collected at " + str(created_at))
                self.num_of_tweets += 1
                # print(self.num_of_tweets)
                #print(" re match: ",
                #      re.match(r'^#[a-zA-Z0-9_]*vote[a-zA-Z0-9_]*', datajson['text']))
                #if re.match(r'[a-zA-Z0-9_ ]*#[a-zA-Z0-9_]*vote[a-zA-Z0-9_ ]*', datajson['text']) is not None:
                with open(path + '/' + str(datajson['id']) + '.json', 'w+') as fh:
                    json.dump(datajson, fh, indent=4)
        except Exception as e:
            print("Error")
        #else:
        #    exit()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener, tweet_mode='extended')
#print("Tracking: " + str(WORDS))
streamer.filter(languages=["en"], track=WORDS)