from pymongo import MongoClient
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import re

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
db = client['twitterdb']
collection = db['twitter_search']
tweets_iterator = collection.find()

print(tweets_iterator.count())


#find all the data related tweets (case insensitive)
data_related_tweets = collection.find({'text': {'$regex': '.*data.*', '$options' : 'i'}})
#data_unrelated_tweets = collection.find({'text': {'$regex': '^((?!data).)*$', '$options': 'i'}})
#print(data_unrelated_tweets.count())
print(data_related_tweets.count())
print(data_related_tweets[0]['user']['geo_enabled'])
print(data_related_tweets[0]['created_at'])
print(data_related_tweets[0]['coordinates'])
'''for tweet in data_related_tweets:
    #if tweet['user']['geo_enabled']:
    if tweet['coordinates'] is None:
        print(tweet['coordinates'])'''

print(data_related_tweets[10]['text'])
print('***')
print(clean_tweet(data_related_tweets[10]['text']))

#for tweet in data_related_tweets:
#    print(tweet_sentiment(tweet['text']), " sentiment for the tweet: ", tweet['text'])
#print(data_related_tweets[0]['coordinates']['coordinates'][0])

count_geo = 0
for tweet in data_related_tweets:
    if tweet['user']['geo_enabled'] is True:
        #or if tweet['user']['geo_enabled'] is True:

        count_geo += 1

        '''tweet_id = tweet['_id']
        try:
            del tweet['_id']
        except KeyError:
            pass
        tweet['geometry'] = {'type': 'Point',
                             'coordinates': [float(tweet['coordinates_coordinates_longitude']),
                                             float(tweet['coordinates_coordinates_latitude'])]}'''

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

print(count_geo)