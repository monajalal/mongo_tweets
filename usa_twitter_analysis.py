#inspired by https://brendansudol.com/writing/united-statemojis
from pymongo import MongoClient
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import re
from emoji import UNICODE_EMOJI
from pprint import pprint

from collections import defaultdict
#from util.misc import CARTOGRAM, SKIN_TONES, STATE_LOOKUP, STATES
import operator


state_cts, emoji_cts = defaultdict(int), defaultdict(int)
state_emoji_cts = defaultdict(lambda: defaultdict(int))
emoji_state_cts = defaultdict(lambda: defaultdict(int))


def tweet_emojis(tweet):
    return [e for e in tweet if e in UNICODE_EMOJI]

def sort_values(data):
    return sorted(data.items(), key=lambda x: x[1], reverse=True)

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    if tweet_analysis.polarity > 0:
        return 'positive'
    elif tweet_analysis.polarity == 0:
        return 'neutral'
    else:
        return 'positive'

client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']
tweets_iterator = collection.find()

print(tweets_iterator.count())


#find all the data related tweets (case insensitive)
#data_related_tweets = collection.find({'text': {'$regex': '.*data.*', '$options' : 'i'}})
#data_unrelated_tweets = collection.find({'text': {'$regex': '^((?!data).)*$', '$options': 'i'}})
#print(data_unrelated_tweets.count())
tweets = collection.find()
count = 0
print(tweets.count())
print(tweets[0]['place']['full_name'][-2:])
print(tweets[0]['user']['geo_enabled'])

print(tweets[0]['created_at'])
print(tweets[0]['coordinates'])
'''for tweet in data_related_tweets:
    #if tweet['user']['geo_enabled']:
    if tweet['coordinates'] is None:
        print(tweet['coordinates'])'''

print(tweets[10]['text'])
print('***')
print(clean_tweet(tweets[10]['text']))

for tweet in tweets:
    if len(tweet_emojis(tweet['text'])) > 0:

        #print(tweet_sentiment(tweet['text']), " sentiment for the tweet: ", tweet['text'])
        #print(tweet['place']['full_name'][-2:])
        state = tweet['place']['full_name'][-2:]
        #print(extract_emojis(tweet['text']))
        emoji_list = tweet_emojis(tweet['text'])
        state_cts[state] += 1
        #for e in tweet['emojis_names']:
        for e in emoji_list:
            #if e not in SKIN_TONES:
            emoji_cts[e] += 1
            state_emoji_cts[state][e] += 1
            emoji_state_cts[e][state] += 1


#pprint(dict(state_emoji_cts))
pprint(sorted(emoji_state_cts.items(), key=lambda k_v: k_v[1][2], reverse=True))
print(sort_values(emoji_cts)[:20])
#pprint(sorted(dict(emoji_state_cts), key = lambda s:s[0]))
#print(count)
#print(data_related_tweets[0]['coordinates']['coordinates'][0])
print(tweets[0]['geo'])
for tweet in tweets:
    if tweet['geo_enabled'] != "true":
        tweet_id = tweet['_id']
        try:
            del tweet['_id']
        except KeyError:
            pass
        tweet['geometry'] = {'type': 'Point',
                             'coordinates': [float(tweet['coordinates_coordinates_longitude']),
                                             float(tweet['coordinates_coordinates_latitude'])]}
        print(tweet['geometry'])

'''for tweet in tweets_iterator:
  print('tweet text: ',tweet['text'])
  print('user\'s screen name: ',tweet['user']['screen_name'])
  print('user\'s name: ',tweet['user']['name'])
  try:
    print('retweet count: ',tweet['retweeted_status']['retweet_count'])
    print('retweeter\'s name: ', tweet['retweeted_status']['user']['name'])
    print('retweeted\'s screen name: ', tweet['retweeted_status']['user']['screen_name'])
  except KeyError:
      pass'''
