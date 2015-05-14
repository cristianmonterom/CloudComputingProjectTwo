__author__ = 'santiago_villagomez'

import sys
import getopt
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Regions.EvaluateRegion import SG_planning
from TwitterStore import TweetStore

DATA_BASE = ""
SERVER = ""
PAGE = ""

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
        PAGE = arg


class SuburbDbUpdater:
    def __init__(self, db_direct_ref, page):
        self.DBRef = db_direct_ref
        self.pagination = int(page)

    def update(self):
        doc_ids_no_suburb = self._get_doc_ids_without_suburb()
        # all_ids = self._get_doc_ids()
        # ids_Yes_suburb = self._getDocIdsWithSuburb()
        # print("TO DO .. everything")
        # print("tatal without suburb field: ",len(doc_ids_no_suburb))
        # print("total with suburb field: ",len(ids_Yes_suburb))
        # print("total documents: ",len(all_ids))
        self._bulk_update(doc_ids_no_suburb)

    def _get_doc_ids(self):
        ids_list = []
        print("TO DO.. get all documents ids.. docs without region field")
        for _id in self.DBRef:
            ids_list.append(_id)
        return ids_list

    def _get_doc_ids_without_suburb(self):
        ids_list = []
        for _id in self.DBRef:
            doc = self.DBRef[_id]
            try:
                result = doc['suburb']
            except:
                ids_list.append(_id)
        return ids_list

    def _get_doc_ids_with_suburb(self):
        ids_list = []
        for _id in self.DBRef:
            doc = self.DBRef[_id]
            try:
                result = doc['suburb']
                ids_list.append(_id)
            except:
                pass
        return ids_list

    def _bulk_update(self, ids_to_update):
        if not ids_to_update:
            return
        region_handler = SG_planning()
        for several_ids in self._chunk_id_list(ids_to_update, self.pagination):
            docs = []
            for id in several_ids:
                doc = self.DBRef[id]
                try:
                    lonlat_list = doc['coordinates']['coordinates']
                    if lonlat_list is not None:
                        point = (lonlat_list[1], lonlat_list[0])
                        doc['suburb'] = region_handler.get_area_name(point)
                    else:
                        doc['suburb'] = region_handler.get_default_no_area()
                except:
                    doc['suburb'] = region_handler.get_default_no_area()
                docs.append(doc)
            self.DBRef.update(docs)

    def _chunk_id_list(self, ids, n=1000):
        i = 0
        while True:
            ret_val = []
            ret_val = ids[i:i+n]
            i+=n
            if len(ret_val) == 0:
                break
            yield ret_val


def update_main():
    twitter_store = TweetStore(DATA_BASE, url=SERVER)
    updater = SuburbDbUpdater(twitter_store.get_db_reference(), PAGE)
    updater.update()

if __name__ == '__main__':
    update_main()
    # TO DO : include code if needed