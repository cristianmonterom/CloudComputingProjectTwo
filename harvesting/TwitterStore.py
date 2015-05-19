__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'
import couchdb

'''
    Class to store tweets in database
    create connection and save them
'''
class TweetStore(object):

    # function: constructor
    # return: none
    # description: create a DB if it does not exists and it creates a connection to it
    def __init__(self, dbname, url='http://127.0.0.1:5984/'):
        try:
            self.server = couchdb.Server(url=url)
            self.db = self.server.create(dbname)
        except couchdb.http.PreconditionFailed:
            self.db = self.server[dbname]

    # function: save_tweet
    # return: integer
    # description: save a tweet to the database
    def save_tweet(self, tw):
        try:
            json_str = tw
            json_str['_id'] = json_str['id_str']
            self.db.save(json_str)
            return 1
        except:
            return 0

    # function: get_db_reference
    # return: DB object
    # description: return an instance object of a DB
    def get_db_reference(self):
        return self.db