__author__ = 'cristianmontero'

import sys
import getopt
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Regions.EvaluateRegion import SG_planning
from TwitterStore import TweetStore
from dataPreprocessor import *
import couchdb

DATA_BASE = ""
SERVER = ""
DOCS_PER_PAGE = 5

try:
    opts, args = getopt.getopt(sys.argv[1:], "s:d:p:", ["server=", "db=", "page="])
    if len(opts) == 0:
        sys.exit(2)
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-s", "--server"):
        SERVER = arg
    elif opt in ("-d", "--db"):
        DATA_BASE = arg
    elif opt in ("-p", "--page"):
        DOCS_PER_PAGE = arg
                  
db = couchdb.Database(SERVER + DATA_BASE)
page_number = 1
docs_number = 1
skip = (page_number - 1) * int(DOCS_PER_PAGE)
region_handler = SG_planning()

while skip < docs_number:
    rows = db.view('_all_docs', limit=DOCS_PER_PAGE, skip=0, include_docs=True)
    docs_number = int(rows.total_rows)

    # docs = [row.doc for row in rows]
    for row in rows:
        doc = add_columns_doc(row.doc)
        try:
            lonlat_list = doc['coordinates']['coordinates']
            if lonlat_list is not None:
                point = (lonlat_list[1], lonlat_list[0])
                doc['suburb'] = region_handler.get_area_name(point)
            else:
                doc['suburb'] = region_handler.get_default_no_area()
        except:
            doc['suburb'] = region_handler.get_default_no_area()

        db.save(doc)

    page_number += 1
    skip = (page_number - 1) * int(DOCS_PER_PAGE)

# print(docs)