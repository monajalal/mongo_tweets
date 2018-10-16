# mongo_tweets

tweet_spider.py:
The script is used for searching tweets from last week. 
Just right click the on it and run.
Data will be stored in MongoDB and json files.

pymongo_tweepy.py:
Minor changes to dump json files.

counthash_search.py:
count the hashtags using search api. 
output files:
1. search_result_match.txt: hashtags that has keywords: vote, midterm, election, november
2. search_result_not_match.txt: hashtags that doesn't contain the keywords

counthash_stream.py:
count the hashtags using streaming api. 
output files:
1. stream_result_match.txt: hashtags that has keywords: vote, midterm, election, november
2. stream_result_not_match.txt: hashtags that doesn't contain the keywords
