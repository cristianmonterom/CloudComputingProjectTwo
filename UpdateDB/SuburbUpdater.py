__author__ = 'santiago_villagomez'

import sys
import getopt
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Regions.EvaluateRegion import SG_planning
from TwitterStore import TweetStore
from dataPreprocessor import *
DATA_BASE = ""
SERVER = ""
PAGE = ""
import time
from threading import Thread

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
        # doc_ids_no_suburb = self._get_doc_ids_without_suburb()
        # all_ids = self._get_doc_ids()
        # ids_Yes_suburb = self._getDocIdsWithSuburb()
        # print("TO DO .. everything")
        # print("tatal without suburb field: ",len(doc_ids_no_suburb))
        # print("total with suburb field: ",len(ids_Yes_suburb))
        # print("total documents: ",len(all_ids))
        self._bulk_update()

    def _get_doc_ids(self):
        ids_list = []
        print("TO DO.. get all documents ids.. docs without region field")
        for _id in self.DBRef:
            ids_list.append(_id)
        return ids_list

    def _get_doc_ids_without_suburb(self):
        ids_list = []
        rows = self.DBRef.view('_all_docs')
        ids_list = [row.id for row in rows ]
        # for _id in self.DBRef:
        #     doc = self.DBRef[_id]
        #     try:
        #         result = doc['suburb']
        #     except:
        #         try:
        #             if not doc['views']:
        #                 ids_list.append(_id)
        #         except:
        #                 ids_list.append(_id)

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

    # def update_task(self,chuck_ids):
    #     docs = []
    #     region_handler = SG_planning()
    #     classifier = Classifier()
    #     for id in chuck_ids:
    #         doc = self.DBRef[id]
    #         try:
    #
    #             # doc = add_columns_doc(doc)
    #             doc = classifier.add_bag_and_polarity(doc)
    #         except:
    #             print(doc)
    #         try:
    #             lonlat_list = doc['coordinates']['coordinates']
    #             if lonlat_list is not None:
    #                 point = (lonlat_list[1], lonlat_list[0])
    #                 doc['suburb'] = region_handler.get_area_name(point)
    #             else:
    #                 doc['suburb'] = region_handler.get_default_no_area()
    #         except:
    #             doc['suburb'] = region_handler.get_default_no_area()
    #         docs.append(doc)
    #     self.DBRef.update(docs)

    def update_task(self,chunk_docs):
        docs = []
        region_handler = SG_planning()
        classifier = Classifier()
        for row in chunk_docs:
            doc = row
            # doc = classifier.add_bag_and_polarity(row)
            # doc = self.DBRef[id]
            try:

                # doc = add_columns_doc(doc)
                doc = classifier.add_bag_and_polarity(doc)
            except:
                # print(doc)
                pass
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


    # def _bulk_update(self, ids_to_update):
    #     if not ids_to_update:
    #         return
    #     number_of_threads = 8
    #     for several_ids in self._chunk_id_list(ids_to_update, self.pagination):
    #         time0 = time.time()
    #         chunks=[several_ids[x:x+int(self.pagination/number_of_threads)] for x in range(0, len(several_ids), int(self.pagination/number_of_threads))]
    #         my_threads = []
    #         for i in range(0,number_of_threads):
    #             t= Thread(target=self.update_task,args=(chunks[i],))
    #             t.start()
    #             my_threads.append(t)
    #         ans = True
    #         while ans == True:
    #             for t in my_threads:
    #                 if t.isAlive():
    #                     break
    #                 ans = False
    #         print("procesados=",(len(several_ids)))
    #         print("tiempo procesando %f = %f sec"%(self.pagination,(time.time()-time0)))
    #
    #
    #
    #
    #
    #         # time_0 = time.time()
    #         # docs = []
    #         # for id in several_ids:
    #         #     doc = self.DBRef[id]
    #         #     try:
    #         #
    #         #         doc = add_columns_doc(doc)
    #         #     except:
    #         #         print(doc)
    #         #     try:
    #         #         lonlat_list = doc['coordinates']['coordinates']
    #         #         if lonlat_list is not None:
    #         #             point = (lonlat_list[1], lonlat_list[0])
    #         #             doc['suburb'] = region_handler.get_area_name(point)
    #         #         else:
    #         #             doc['suburb'] = region_handler.get_default_no_area()
    #         #     except:
    #         #         doc['suburb'] = region_handler.get_default_no_area()
    #         #     docs.append(doc)
    #         # self.DBRef.update(docs)
    #         # print("polling=",(time.time()-time_0))

    def _bulk_update(self):
        # time_init = time.time()
        log_file =  open('log_update.txt','a')

        number_of_threads = 8
        page_number = 1
        docs_number = 1
        skip = (page_number - 1) * int(self.pagination)
        total_processed = 0;
        while skip < docs_number:
            time0 = time.time()
            rows = self.DBRef.view('_all_docs', limit=self.pagination, skip=skip, include_docs=True)
            docs_number = int(rows.total_rows)
            docs = [row.doc for row in rows]
            # for several_docs in self._chunk_doc_list(docs, self.pagination):
            #     time0 = time.time()
            chunks=[docs[x:x+int(self.pagination/number_of_threads)] for x in range(0, len(docs), int(len(docs)/number_of_threads))]
            my_threads = []
            for i in range(0,number_of_threads):
                t= Thread(target=self.update_task,args=(chunks[i],))
                t.start()
                my_threads.append(t)
            ans = True
            while ans == True:
                for t in my_threads:
                    if t.isAlive():
                        break
                    ans = False
            total_processed += len(docs)
            # print("processed=",(total_processed))
            # print("time for processing bulk %f = %f sec"%(self.pagination,(time.time()-time0)))

            log_file.write("page {}: {} \n".format(page_number,(time.time()-time0)))
            page_number += 1
            skip = (page_number - 1) * int(self.pagination)
        log_file.close()
        # print("total time = ",(time.time()-time_init))
    # def _chunk_id_list(self, ids, n=1000):
    #     i = 0
    #     while True:
    #         ret_val = []
    #         ret_val = ids[i:i+n]
    #         i += n
    #         if len(ret_val) == 0:
    #             break
    #         yield ret_val

    def _chunk_doc_list(self, docs, n=1000):
        i = 0
        while True:
            ret_val = []
            ret_val = docs[i:i+n]
            i += n
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