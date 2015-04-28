__author__ = 'cristianmontero'
import time
import sys
import getopt

import tweepy

from harvesting.TwitterStore import *


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

DATA_BASE = ""
SERVER = ""

# CONSUMER_KEY = 'OvFt3ix2aummG26HtS8sT1MzU'
# CONSUMER_SECRET ='71tH27a3HljrW1cEOuoFZRPfmnZFqxhf4UXLI13rhgHfUA8mQ0'
# OAUTH_TOKEN = '128415623-tbIJqZujbYoYP4xsPleUWthHO7W6jnu5LscL6AAA'
# OAUTH_TOKEN_SECRET = 'wSmbC1oRINjcnAvmCzbOABn8lsJ6GOxtZONGe6o80uEtr'
#
# DATA_BASE = "cloud_computing"
# SERVER = "http://localhost:5984"

def print_help():
    print('python3 TweetsCity.py [-db <database>] -server <url server> -h')

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:d:k:v:t:o:", ["help", "server=", "db=", "consumer_key="
                                                               , "consumer_secret=", "token=", "token_secret="])
    if len(opts) == 0:
        print('If you do need help, please enter: ')
        print('TweetsCity.py [-h | -help]')
        sys.exit(2)
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', "--help"):
        print_help()
        sys.exit()
    elif opt in ("-s", "--server"):
        SERVER = arg
    elif opt in ("-d", "--db"):
        DATA_BASE = arg
    elif opt in ("-k", "--consumer_key"):
        CONSUMER_KEY = arg
    elif opt in ("-v", "--consumer_secret"):
        CONSUMER_SECRET = arg
    elif opt in ("-t", "--token"):
        OAUTH_TOKEN = arg
    elif opt in ("-o", "--token_secret"):
        OAUTH_TOKEN_SECRET = arg

print('CONSUMER_KEY = {}'.format(CONSUMER_KEY))
print('CONSUMER_SECRET = {}'.format(CONSUMER_SECRET))
print('OAUTH_TOKEN = {}'.format(OAUTH_TOKEN))
print('OAUTH_TOKEN_SECRET = {}'.format(OAUTH_TOKEN_SECRET))
print('DATA_BASE = {}'.format(DATA_BASE))
print('SERVER = {}'.format(SERVER))

twitter_store = TweetStore(DATA_BASE, url=SERVER)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)
places = api.geo_search(query="Singapore", granularity="city")
place_id = places[0].id

counter = 0
request_counter = 0
while True:
    try:
        tweets = api.search(q="place:%s" % place_id)
        # tweets = api.search(geocode="{},{},{}".format('1.295853', '103.809934', '10km'))
        request_counter += 1
        for tweet in tweets:
            counter += twitter_store.save_tweet(tweet)

        # print(counter)
        time.sleep(5)
        # print(tweet.user + "|" + tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place")
    except:
        print("request counter: {}".format(request_counter))
        time.sleep(60)
