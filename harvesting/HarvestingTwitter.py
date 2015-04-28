__author__ = 'cristianmontero'

import tweepy

CONSUMER_KEY = 'OvFt3ix2aummG26HtS8sT1MzU'
CONSUMER_SECRET ='71tH27a3HljrW1cEOuoFZRPfmnZFqxhf4UXLI13rhgHfUA8mQ0'
OAUTH_TOKEN = '128415623-tbIJqZujbYoYP4xsPleUWthHO7W6jnu5LscL6AAA'
OAUTH_TOKEN_SECRET = 'wSmbC1oRINjcnAvmCzbOABn8lsJ6GOxtZONGe6o80uEtr'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# user = tweepy.api.get_user('twitter')
user = api.get_user('twitter')
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
   print(friend.screen_name)