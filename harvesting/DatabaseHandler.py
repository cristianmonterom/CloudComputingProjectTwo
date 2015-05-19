__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import couchdb


class DatabaseHandler(object):

    def __init__(self, dbname, url='http://127.0.0.1:5984/'):
        try:
            self.server = couchdb.Server(url=url)
            self.db = self.server.create(dbname)
        except couchdb.http.PreconditionFailed:
            self.db = self.server[dbname]

    def save(self, document):
        try:
            self.db.save(document)
            return 1
        
        except couchdb.http.ResourceConflict:
            raise couchdb.http.ResourceConflict("repeated doc")
            # return 0

    def read_from_view(self, view):
        """

        :rtype : object
        """
        results = self.db.view(view)
        return results

    def update(self, document):
        pass
    
    def get_row(self, id):
        return self.db.get(id)