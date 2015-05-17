__author__ = 'cristianmontero'

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Regions.EvaluateRegion import SG_planning
from dataPreprocessor import *
from TwitterStore import TweetStore

DATA_BASE = "cloud_computing"
SERVER = "http://127.0.0.1:5984/"
DOCS_PER_PAGE = 10000

twitter_store = TweetStore(DATA_BASE, url=SERVER)

db = twitter_store.get_db_reference()
page_number = 1
docs_number = 1
skip = (page_number - 1) * DOCS_PER_PAGE
region_handler = SG_planning()

while skip < docs_number:
    rows = db.view('_all_docs', limit=DOCS_PER_PAGE, skip=0, include_docs=True)
    docs_number = rows.total_rows

    # docs = [row.doc for row in rows]
    for row in rows:
        doc = row.doc
        try:
            # doc.delete[]
            doc.pop('suburb', None)
            # doc['suburb'] = ''
        except:
            print()

        try:
            doc.pop('bag_of_words', None)
            # doc['bag_of_words'] = ''
        except:
            print()

        try:
            doc.pop('polarity', None)
            # doc['polarity'] = ''
        except:
            print()

        # row.doc = doc
        db.save(doc)

    page_number += 1
    skip = (page_number - 1) * DOCS_PER_PAGE


# print(docs)