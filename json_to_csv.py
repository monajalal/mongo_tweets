#converting the Twitter json dump in MongoDB to CSV using PyMongo
from pymongo import MongoClient
from operator import itemgetter
import csv
import os

db = MongoClient().usa_db

if os.path.exists('usa_tweets.csv'):
    os.remove('usa_tweets.csv')
with open('usa_tweets.csv', 'w') as outfile:
  field_names = ['text', 'user', 'created_at', 'geo']
  writer = csv.DictWriter(outfile, delimiter=',', fieldnames=field_names)
  writer.writeheader()

  for data in db.usa_tweets_collection.find():
    writer.writerow({
      'text': data['text'],
      'user': data['user'],
      'created_at': data['created_at'],
      'geo': data['geo'],
      'location' : data['location']
    })

  outfile.close()