import tweepy
import json
from pymongo import MongoClient
import os
import datetime as DT
from datetime import date
#from geopy.geocoders import Nominatim
#from geopy.exc import GeocoderTimedOut
import time
import collections

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
            for tweet in tweepy.Cursor(api.search, q='#midterm OR #2018midterms OR #election OR #november2018 OR '
                                                     '#vote2018 OR #midterms OR #midterms2018 OR #election2018'
                                                     '#2018election OR #november OR #vote',
                                       since=week_ago, until=today, lang='en', tweet_mode='extended').items():

                #location = getLocation(tweet.user.location)

                error_counter = 0

                #client = MongoClient(MONGO_HOST)
                #db = client.twitterdb
                datajson = json.dumps(tweet._json)
                jsondata = json.loads(datajson)
                rt_num_hashtags = 0
                en_num_hashtags = 0
                ex_num_hashtags = 0
                #db.twitter_search.insert(jsondata)

                with open(json_path + '/{0}.json'.format(tweet.id), 'a+') as f:
                    json.dump(tweet._json, f, indent=4)


                if 'retweeted_status' in jsondata:
                    if 'extended_tweet' in jsondata['retweeted_status']:
                        if 'entities' in jsondata['retweeted_status']['extended_tweet']:
                            if 'hashtags' in jsondata['retweeted_status']['extended_tweet']['entities']:
                                rt_num_hashtags = len(
                                    jsondata['retweeted_status']['extended_tweet']['entities']['hashtags'])
                                print(str(jsondata['id']) + '\nin retweeted_status found hashtags: ', rt_num_hashtags)
                                if rt_num_hashtags != 0:
                                    for i in range(rt_num_hashtags):
                                        with open('../hashtags_search.txt', 'a+') as f:
                                            f.write(
                                                jsondata['retweeted_status']['extended_tweet']['entities']['hashtags'][
                                                    i]['text'] + '\n')
                    elif 'entities' in jsondata['retweeted_status']:
                            if 'hashtags' in jsondata['retweeted_status']['entities']:
                                rt_num_hashtags = len(
                                    jsondata['retweeted_status']['entities']['hashtags'])
                                print(str(jsondata['id']) + '\nin retweeted_status found hashtags: ', rt_num_hashtags)
                                if rt_num_hashtags != 0:
                                    for i in range(rt_num_hashtags):
                                        with open('../hashtags_search.txt', 'a+') as f:
                                            f.write(
                                                jsondata['retweeted_status']['entities']['hashtags'][
                                                    i]['text'] + '\n')

                if rt_num_hashtags == 0:
                    if 'entities' in jsondata:
                        if 'hashtags' in jsondata['entities']:
                            en_num_hashtags = len(jsondata['entities']['hashtags'])
                            print(str(jsondata['id']) + '\nin entities found hashtags: ', en_num_hashtags)
                            if en_num_hashtags != 0:
                                for i in range(en_num_hashtags):
                                    with open('../hashtags_search.txt', 'a+') as f:
                                        f.write(jsondata['entities']['hashtags'][i]['text'] + '\n')

                if rt_num_hashtags == 0 and en_num_hashtags == 0:
                    if 'extended_tweet' in jsondata:
                        if 'entities' in jsondata['extended_tweet']:
                            if 'hashtags' in jsondata['extended_tweet']['entities']:
                                ex_num_hashtags = len(jsondata['extended_tweet']['entities']['hashtags'])
                                print(str(jsondata['id']) + '\nin extended_tweet found hashtags: ', ex_num_hashtags)
                                if ex_num_hashtags != 0:
                                    for i in range(ex_num_hashtags):
                                        with open('../hashtags_search.txt', 'a+') as f:
                                            f.write(
                                                datajson['extended_tweet']['entities']['hashtags'][i]['text'] + '\n')

                if rt_num_hashtags == 0 and en_num_hashtags == 0 and ex_num_hashtags == 0:
                    print('no hashtags')

                if os.path.exists('../hashtags_search.txt'):
                    with open('../hashtags_search.txt', 'r') as readfile:
                        res1 = readfile.read().split('\n')

                    res = map(lambda x:x.lower(), res1)

                    writefile = open('../search_result.txt', 'w')

                    writefile.close()

                    mycounter = collections.Counter(res)

                    for k, v in mycounter.most_common():
                        with open('../search_result.txt', 'a+') as outfile:
                            outfile.write('#{0:30}\t{1:7}'.format(k, v)+'\n')

                #save the json file

                #with open(json_path + '/{0}.json'.format(tweet.id), 'a+') as f:
                #    json.dump(tweet._json, f, indent=4)
                #num_of_tweets += 1
                #with open('../data_samples.txt', 'a+') as file:
                #    file.write('tweet text:\n' + tweet.full_text + '\n\n')
                #print('get {0} tweet(s)'.format(num_of_tweets), '\n', tweet.full_text, '\n\n', 'created at',
                #      tweet.created_at, '\t', tweet.user.location, '\n\n')


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