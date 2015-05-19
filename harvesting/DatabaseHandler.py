__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import couchdb

'''
    Class for database handling, open connection as well as reading documents
'''

class DatabaseHandler(object):

    # function: constructor
    # return: None
    # description: create a db if it does not exists and create a connection to it
    def __init__(self, dbname, url='http://127.0.0.1:5984/'):
        try:
            self.server = couchdb.Server(url=url)
            self.db = self.server.create(dbname)
        except couchdb.http.PreconditionFailed:
            self.db = self.server[dbname]

    # function: save
    # return: 1 if document was saved. Exception otherwise
    # Description: Function to save a document into the database
    def save(self, document):
        try:
            self.db.save(document)
            return 1
        except couchdb.http.ResourceConflict:
            raise couchdb.http.ResourceConflict("repeated doc")

    # function: read_from_view
    # return: documents from database
    # description: Read documents from a view
    def read_from_view(self, view):
        """

        :rtype : object
        """
        results = self.db.view(view)
        return results

    # function: get_row
    # return: document
    # description: get a document from DB using document id
    def get_row(self, doc_id):
        return self.db.get(doc_id)