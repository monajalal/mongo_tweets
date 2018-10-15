import tweepy
import json
from pymongo import MongoClient
import os
import datetime as DT
from datetime import date
#from geopy.geocoders import Nominatim
#from geopy.exc import GeocoderTimedOut
import time

json_path = '../JSON_files'

#google_path = 'google-drive://chaoswjz@bu.edu/1loKGesRIvMtQ5dj49VlSyL3VBeDozM_B'

MONGO_HOST = 'mongodb://localhost/twitterdb'

#keywords
WORDS = ['#midterm', '#2018midterms', '#election', '#november2018', '#vote2018']

ERROR_LIMIT = 5

'''
def getLocation(address):
    geolocator = Nominatim(user_agent='tweet_spider')
    try:
        return geolocator.geocode(address, addressdetails=True, timeout=10)
    except GeocoderTimedOut:
        return getLocation(address)
'''

def setupTweeepy(f):
    #set up tweepy
    keys_file = open(f)
    lines = keys_file.readlines()
    consumer_key = lines[0].rstrip()
    consumer_secret = lines[1].rstrip()
    access_token = lines[2].rstrip()
    access_token_secret = lines[3].rstrip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

def searchTweets(api):
    num_of_tweets = 0
    error_counter = 0
    today = str(date.today())
    week_ago = str(date.today() - DT.timedelta(days=7))
    while(True):
        try:
            for tweet in tweepy.Cursor(api.search, q='#midterm OR #2018midterms OR #election OR #november2018 OR #vote2018 '
                                                     '-filter:retweets',
                                       since=week_ago, until=today, lang='en', tweet_mode='extended').items():
                #location = getLocation(tweet.user.location)

                error_counter = 0

                client = MongoClient(MONGO_HOST)
                db = client.twitterdb
                datajson = json.dumps(tweet._json)
                jsondata = json.loads(datajson)
                db.twitter_search.insert(jsondata)

                #save the json file
                with open(json_path + '/{0}.json'.format(tweet.id), 'a+') as f:
                    json.dump(tweet._json, f, indent=4)
                num_of_tweets += 1
                #with open('../data_samples.txt', 'a+') as file:
                #    file.write('tweet text:\n' + tweet.full_text + '\n\n')
                print('get {0} tweet(s)'.format(num_of_tweets), '\n', tweet.full_text, '\n\n', 'created at',
                      tweet.created_at, '\t', tweet.user.location, '\n\n')

        except tweepy.TweepError as e:
            print('Error occurs:', e.reason)
            error_counter += 1
            if e.api_code == 429:
                time.sleep(15*60)
                continue
            if error_counter > ERROR_LIMIT:
                break
            else:
                continue

        '''
        if location is not None:
            if 'country' in location.raw['address']:
                if location.raw['address']['country'] == 'United States of America':
                    print(tweet.user.location)
                    print(tweet.id, '\n---------------------------------\n',
                          tweet.full_text, '\n---------------------------------------\n'
                          , tweet.created_at, '\t',
                          tweet.user.location, '\n\n')
                    if 'state' in location.raw['address']:
                        state = location.raw['address']['state']
                    num_of_tweets += 1
                    print('number of tweets:\t', num_of_tweets)
        '''

def main():
    # set up the file path to store json file
    # don't push to the github
    if not os.path.exists(json_path):
        os.mkdir(json_path, 0o777)

    api = setupTweeepy('keys.txt')
    searchTweets(api)


if __name__ == '__main__':
    main()