from TwitterStore import TweetStore
from couchdb.design import ViewDefinition

DATA_BASE = "cloud_computing"
SERVER = "http://127.0.0.1:5984/"

twitter_store = TweetStore(DATA_BASE, url=SERVER)

db = twitter_store.get_db_reference()
view_map = 'function(doc) { if(doc.bag_of_words) { for (word in doc.bag_of_words) { emit([doc.bag_of_words[word], doc.polarity, doc.suburb],1)}}}'
view_reduce = '_sum'
view = ViewDefinition('scenarios', 'get_polarity_stats', view_map, reduce_fun=view_reduce)
view.sync(db)
