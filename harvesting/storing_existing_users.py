from harvesting.DatabaseHandler import DatabaseHandler
import couchdb

__author__ = 'cristianmontero'

DATA_BASE = "cloud_computing"
SERVER = "http://localhost:5984"
VIEW = "_design/user_tweets/_view/user_tweets"

DATA_BASE_DEST = "users_test"
SERVER_DEST = "http://localhost:5984"

db_origin = DatabaseHandler(DATA_BASE, SERVER)
db_dest = DatabaseHandler(DATA_BASE_DEST, SERVER_DEST)

users = db_origin.read_from_view(VIEW)
counter = 0
for user in users:
    try:
        user['_id'] = str(user['key'])
        del user['key']
        del user['id']
        user['harvested'] = 'false'
        user['num_tweets'] = 1
        counter += db_dest.save(user)
    except couchdb.http.ResourceConflict:
        user = db_dest.get_row(user['_id'])
        user['num_tweets'] += 1
        db_dest.save(user)

print("count: {}".format(counter))
