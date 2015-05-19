__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'
from DatabaseHandler import *
import couchdb
import json

'''
    Class to store the username from whom we gathered historic tweets in a different database
'''
class StoreUser(object):

    # function: constructor
    # return: none
    # description: create connection with Twitter API
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, database, server):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret

        self.database = database
        self.server = server
        self.db_users = DatabaseHandler(self.database, self.server)

    # function: save_user
    # return: None
    # description: save new user of update an existing user with the number of gathered tweets
    def save_user(self, username):
        d = '{"_id": "' + username + '", "num_tweets": 1, "harvested": "true" }'
        try:
            user = json.loads(d)
            self.db_users.save(user)
        except couchdb.http.ResourceConflict:
            user = self.db_users.get_row(user['_id'])
            user['num_tweets'] += 1
            self.db_users.save(user)

    # function: exists
    # return: boolean
    # description: Verify if an user exists in database or not
    def exists(self, username):
        try:
            user = self.db_users.get_row(username)
            if user is None:
                return False
            else:
                return True
        except:
            return False