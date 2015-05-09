__author__ = 'cristianmontero'
from DatabaseHandler import *
import couchdb
import json


class StoreUser(object):

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, database, server):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret

        self.database = database
        self.server = server
        self.db_users = DatabaseHandler(self.database, self.server)

# DATA_BASE = "cloud_computing"
# SERVER = "http://localhost:5984"
# VIEW = "_design/user_tweets/_view/user_tweets"
#
# DATA_BASE_DEST = "users_test"
# SERVER_DEST = "http://localhost:5984"

    def save_user(self, username):
        d = '{"_id": "' + username + '", "num_tweets": 1, "harvested": "true" }'
        try:
            user = json.loads(d)
            # user['_id'] = username
            # user['harvested'] = 'false'
            # user['num_tweets'] = 1
            self.db_users.save(user)
        except couchdb.http.ResourceConflict:
            user = self.db_users.get_row(user['_id'])
            user['num_tweets'] += 1
            self.db_users.save(user)

    def exists(self, username):
        try:
            user = self.db_users.get_row(username)
            if user == None:
                return False
            else:
                return True
        except:
            return False