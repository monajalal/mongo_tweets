#create a map of tweets using Folium
#inspired by https://github.com/kimasx/lfc-tweet-analysis


import folium, pandas, ast

# get geo data only from rows with non-empty values
locations = pandas.read_csv('./usa_tweets.csv', usecols=[3]).dropna()

geos = []

for location in locations.values:
  # add to geos array an evaluated python literal syntax of the data
  geos.append(ast.literal_eval(location[0])['coordinates'])

# initialize and create map
tweet_map = folium.Map(location=[39.50, -98.35], tiles='Mapbox Bright', zoom_start=7)


status_geo = []
status_geo_screen_names = []
from pymongo import MongoClient
from operator import itemgetter
import csv
import os

db = MongoClient().usa_db

tweets = db.usa_tweets_collection.find()



#for tweet in tweets:
#  if ('status' in tweet and tweet['status']['geo'] is not None):
#    status_geo.append(tweet['status']['geo'])


print(dir(tweet_map))
# add markers
for geo in geos:
  #tweet_map.CircleMarker(location=geo, radius=250)
  folium.CircleMarker(location=geo, radius=5).add_to(tweet_map)

#tweet_map.create_map(path='map.html')
tweet_map.save('map.html')