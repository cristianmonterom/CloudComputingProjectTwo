__author__ = 'cristianmontero'

import sys
import getopt
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Regions.EvaluateRegion import SG_planning
from dataPreprocessor import *
import couchdb
import time

DATA_BASE = ""
SERVER = ""
DOCS_PER_PAGE = 5
START_PAGE = 1

try:
    opts, args = getopt.getopt(sys.argv[1:], "s:d:p:k", ["server=", "db=", "page=", "start-page="])
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
    elif opt in ("-k", "--start-page"):
        START_PAGE = arg

db = couchdb.Database(SERVER + DATA_BASE)
page_number = int(START_PAGE)
docs_number = 1
skip = (page_number - 1) * int(DOCS_PER_PAGE)
region_handler = SG_planning()
total_time = 0.0
f = open('add.txt', 'a')

while skip < docs_number:
    time_0 = time.time()
    rows = db.view('_all_docs', limit=DOCS_PER_PAGE, skip=skip, include_docs=True)
    docs_number = int(rows.total_rows)

    for row in rows.rows:
        # if doc['polarity'] is None:
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
    time_1 = time.time() - time_0
    f.write("page {}: {} \n".format(page_number, time_1))
    # print("page {}: {}".format(page_number, time_1))

    total_time += time_1

    page_number += 1
    skip = (page_number - 1) * int(DOCS_PER_PAGE)

f.write("total time: {} \n".format(total_time))
f.close()