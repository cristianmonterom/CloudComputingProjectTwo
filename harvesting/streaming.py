from __future__ import absolute_import, print_function

__author__ = 'cristianmontero'

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "OvFt3ix2aummG26HtS8sT1MzU"
consumer_secret = "71tH27a3HljrW1cEOuoFZRPfmnZFqxhf4UXLI13rhgHfUA8mQ0"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "128415623-tbIJqZujbYoYP4xsPleUWthHO7W6jnu5LscL6AAA"
access_token_secret = "wSmbC1oRINjcnAvmCzbOABn8lsJ6GOxtZONGe6o80uEtr"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['melbourne'])