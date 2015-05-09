__author__ = 'cristianmontero'
import tweepy
from TwitterStore import *
from dataPreprocessor import *


class GetTweets(object):

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, database, server):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret

        self.data_server = database
        self.server = server

        # self.consumer_key = 'OvFt3ix2aummG26HtS8sT1MzU'
        # self.consumer_secret = '71tH27a3HljrW1cEOuoFZRPfmnZFqxhf4UXLI13rhgHfUA8mQ0'
        # self.access_key = '128415623-tbIJqZujbYoYP4xsPleUWthHO7W6jnu5LscL6AAA'
        # self.access_secret = 'wSmbC1oRINjcnAvmCzbOABn8lsJ6GOxtZONGe6o80uEtr'
        # self.DATA_BASE = "test"
        # self.SERVER = "http://localhost:5984"

    def get_all_tweets(self, screen_name):
        # Twitter only allows access to a users most recent 3240 tweets with this method

        # authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)
        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        count_tweets = 0
        while len(new_tweets) > 0:
            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            count_tweets += len(new_tweets)
            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

        # print("num tweets: {}".format(str(count_tweets)))
        counter = 0
        twitter_store = TweetStore(self.data_server, url=self.server)
        for tweet in alltweets:
            try:
                tweet = add_columns(tweet)
                counter += twitter_store.save_tweet(tweet)
                counter += twitter_store.save_tweet(tweet)
            except:
                counter += 0
