from __future__ import print_function
import tweepy
import json
import os
import collections
import time
import re
import csv
from shutil import move
import urllib3

path = '../JSON_files'
if not os.path.exists(path):
    os.mkdir(path, 0o777)

unique_hashtags = []
if os.path.exists('./unique_hashtags.txt'):
    with open('./unique_hashtags.txt', 'r') as readfile:
        res1 = readfile.read().split('\n')
        for str1 in res1:
            unique_hashtags.append(str1.strip())
print(unique_hashtags)
print(len(unique_hashtags))

'''
WORDS = ['#midterm', '#2018midterms', '#election', '#november2018',
                                                     '#vote2018', '#midterms', '#midterms2018', '#election2018',
                                                     '#2018election', '#november', '#vote', '#MidtermMlections2018',
         '#RockTheVote', '#GoVote', '#WhenWeAllVote', '#NovemberIsComing', '#VoteBlue', '#VoteThemOut', '#November6'
         '#VoteBlueToSaveAmerica', '#midterms', '#RegisterToVote', '#YourVoteCounts', '#PostcardsToVoters', '#WomenVoters',
         '#VoteBlueAndBringAFriend', '#VoteEarly', '#NativeVote', '#PAvotesBlue', '#GALationaVote', '#voteRed', '#rednovember',
         '#bluenovember', '#voteredmidterm2018', '#voteredmidterms2018', '#voteRedToSaveAmerica2018', '#VoteTed', '#VoteGOP',
         '#VoteRed2018', '#VoteBlue2018', '#iwillvote', '#VotingRights', '#VoteRepublican', '#VoteNovember6th', '#ElectionDay',
         '#NovemberElection', '#voting', '#voters']
'''
#WORDS = [re.match(r'^#*vote*')]

keys_file = open("keys.txt")
lines = keys_file.readlines()
consumer_key = lines[0].rstrip()
consumer_secret = lines[1].rstrip()
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()

'''
if os.path.exists('../hashtags_stream_match.csv'):
    with open('../hashtags_stream_match.csv', 'r') as readfile:
        res1 = readfile.read().split('\n')
'''

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
        rt_num_hashtags = 0
        en_num_hashtags = 0
        ex_num_hashtags = 0
        try:
            # Decode the JSON from Twitter
            datajson = json.loads(data)

            with open(path + '/' + str(datajson['id']) + '.json', 'w+') as fh:
                json.dump(datajson, fh, indent=4)

            if 'retweeted_status' in datajson:
                if 'extended_tweet' in datajson['retweeted_status']:
                    if 'entities' in datajson['retweeted_status']['extended_tweet']:
                        if 'hashtags' in datajson['retweeted_status']['extended_tweet']['entities']:
                            rt_num_hashtags = len(
                                datajson['retweeted_status']['extended_tweet']['entities']['hashtags'])
                            print(str(datajson['id']) + '\nin retweeted_status found hashtags: ', rt_num_hashtags)
                            if rt_num_hashtags != 0:
                                for i in range(rt_num_hashtags):
                                    if re.match(r'.*(vote|midterm|november|election).*',
                                                datajson['retweeted_status']['extended_tweet']['entities']['hashtags'][
                                                    i]['text'].lower()) is not None:
                                        with open('../hashtags_stream_match.csv', 'a+') as f:
                                            csv_writer =csv.writer(f, delimiter = ',')
                                            csv_writer.writerow([
                                                datajson['retweeted_status']['extended_tweet']['entities']['hashtags'][
                                                    i]['text'].encode('utf-8')])
                                    else:
                                        with open('../hashtags_stream_not_match.csv', 'a+') as f:
                                            csv_writer = csv.writer(f, delimiter=',')
                                            csv_writer.writerow([
                                            datajson['retweeted_status']['extended_tweet']['entities']['hashtags'][
                                                i]['text'].encode('utf-8')])

                elif 'entities' in datajson['retweeted_status']:
                    if 'hashtags' in datajson['retweeted_status']['entities']:
                        rt_num_hashtags = len(
                            datajson['retweeted_status']['entities']['hashtags'])
                        print(str(datajson['id']) + '\nin retweeted_status found hashtags: ', rt_num_hashtags)
                        if rt_num_hashtags != 0:
                            for i in range(rt_num_hashtags):
                                if re.match(r'.*(vote|midterm|november|election).*',
                                            datajson['retweeted_status']['entities']['hashtags'][
                                                i]['text'].lower()) is not None:
                                    with open('../hashtags_stream_match.csv', 'a+') as f:
                                        csv_writer = csv.writer(f, delimiter = ',')
                                        csv_writer.writerow([
                                        datajson['retweeted_status']['entities']['hashtags'][
                                            i]['text'].encode('utf-8')])
                                else:
                                    with open('../hashtags_stream_not_match.csv', 'a+') as f:
                                        csv_writer = csv.writer(f, delimiter = ',')
                                        csv_writer.writerow([
                                        datajson['retweeted_status']['entities']['hashtags'][
                                            i]['text'].encode('utf-8')])

            if rt_num_hashtags == 0:
                if 'entities' in datajson:
                    if 'hashtags' in datajson['entities']:
                        en_num_hashtags = len(datajson['entities']['hashtags'])
                        print(str(datajson['id']) + '\nin entities found hashtags: ', en_num_hashtags)
                        if en_num_hashtags != 0:
                            for i in range(en_num_hashtags):
                                if re.match(r'.*(vote|midterm|november|election).*',
                                            datajson['entities']['hashtags'][
                                                i]['text'].lower()) is not None:
                                    with open('../hashtags_stream_match.csv', 'a+') as f:
                                        csv_writer = csv.writer(f, delimiter=',')
                                        csv_writer.writerow([
                                            datajson['entities']['hashtags'][
                                                i]['text'].encode('utf-8')])
                                else:
                                    with open('../hashtags_stream_not_match.csv', 'a+') as f:
                                        csv_writer = csv.writer(f, delimiter=',')
                                        csv_writer.writerow([
                                            datajson['entities']['hashtags'][
                                                i]['text'].encode('utf-8')])

            if rt_num_hashtags == 0 and en_num_hashtags == 0:
                if 'extended_tweet' in datajson:
                    if 'entities' in datajson['extended_tweet']:
                        if 'hashtags' in datajson['extended_tweet']['entities']:
                            ex_num_hashtags = len(datajson['extended_tweet']['entities']['hashtags'])
                            print(str(datajson['id']) + '\nin extended_tweet found hashtags: ', ex_num_hashtags)
                            if ex_num_hashtags != 0:
                                for i in range(ex_num_hashtags):
                                    if re.match(r'.*(vote|midterm|november|election).*',
                                                datajson['extended_tweet']['entities']['hashtags'][
                                                    i]['text']) is not None:
                                        with open('../hashtags_stream_match.csv', 'a+') as f:
                                            csv_writer = csv.writer(f, delimiter = ',')
                                            csv_writer.writerow([
                                                datajson['extended_tweet']['entities']['hashtags'][
                                                    i]['text'].encode('utf-8')])
                                    else:
                                        with open('../hashtags_stream_not_match.csv', 'a+') as f:
                                            csv_writer = csv.writer(f, delimiter = ',')
                                            csv_writer.writerow([
                                                datajson['extended_tweet']['entities']['hashtags'][
                                                    i]['text'].encode('utf-8')])

            if rt_num_hashtags == 0 and en_num_hashtags == 0 and ex_num_hashtags == 0:
                print('no hashtags')

            if os.path.exists('../hashtags_stream_match.csv'):
                with open('../hashtags_stream_match.csv', 'r') as readfile:
                    res1 = readfile.read().split('\n')

                mres = map(lambda x: x.lower(), res1)

                #writefile = open('../stream_result_match.txt', 'w')

                #writefile.close()

                mycounter = collections.Counter(mres)

                for k, v in mycounter.most_common():
                    with open('../stream_result_matchtmp.csv', 'a+') as outfile:
                        csvWriter = csv.writer(outfile, delimiter = ',')
                        csvWriter.writerow([k.encode('utf-8'),v])
                move('../stream_result_matchtmp.csv', '../stream_result_match.csv')

            if os.path.exists('../hashtags_stream_not_match.csv'):
                with open('../hashtags_stream_not_match.csv', 'r') as readfile:
                    res2 = readfile.read().split('\n')

                nmres = map(lambda x: x.lower(), res2)

                #writefile = open('../stream_result_not_match.txt', 'w')

                #writefile.close()

                mycounter = collections.Counter(nmres)

                for k, v in mycounter.most_common():
                    with open('../stream_result_not_matchtmp.csv', 'a+') as outfile:
                        csvWriter = csv.writer(outfile, delimiter = ',')
                        csvWriter.writerow([k.encode('utf-8'),v])
                move('../stream_result_not_matchtmp.csv', '../stream_result_not_match.csv')

        except tweepy.TweepError as e:
            print("Tweepy Error is: ", e.reason)

        except UnicodeEncodeError as e:
            print("Unicode error is: ", e)
            pass

        except urllib3.exceptions.ProtocolError as e:
            print("url exception is:", e)
            pass
        except UnicodeDecodeError as e:
            pass
        #else:
        #    exit()


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener, tweet_mode='extended')
#print("Tracking: " + str(WORDS))
streamer.filter(languages=["en"], track=unique_hashtags[:400])
