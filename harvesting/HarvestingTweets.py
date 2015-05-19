__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'
import tweepy
from TwitterStore import *
from dataPreprocessor import *

'''
    Class which gather historic tweets from a user
    * Twitter only allows access to a users most recent 3240 tweets with this method
'''
class GetTweets(object):

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, database, server):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret

        self.data_server = database
        self.server = server

    # function: get_all_tweets
    # return: None
    # description: gather tweets from a specific user
    def get_all_tweets(self, screen_name):

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

        counter = 0
        twitter_store = TweetStore(self.data_server, url=self.server)
        for tweet in alltweets:
            try:
                # add bag of words and polarity fields to the tweet
                tweet = add_columns(tweet)
                counter += twitter_store.save_tweet(tweet)
            except:
                counter += 0
