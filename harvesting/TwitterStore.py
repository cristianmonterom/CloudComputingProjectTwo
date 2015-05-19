__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'
import couchdb


class TweetStore(object):

    def __init__(self, dbname, url='http://127.0.0.1:5984/'):
        try:
            self.server = couchdb.Server(url=url)
            self.db = self.server.create(dbname)
        except couchdb.http.PreconditionFailed:
            self.db = self.server[dbname]

    def save_tweet(self, tw):
        try:
            json_str = tw
            json_str['_id'] = json_str['id_str']
            self.db.save(json_str)
            return 1
        except:
            return 0

    def get_db_reference(self):
        return self.db