__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'

import sys
import getopt
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Regions.EvaluateRegion import SG_planning
from harvesting.TwitterStore import TweetStore
from dataPreprocessor import *
DATA_BASE = ""
SERVER = ""
PAGE = ""
import time
from threading import Thread


# code:
# description: initial code fro parameter handling
# sets: SERVER (server address), DATA_BASE(database name), PAGE (number of records to be updated at once)
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

# SuburbDbUpdater: class
# Usage: It is intended for update the db by adding the suburb name, polarity and bag of words
class SuburbDbUpdater:
    # constructor: SuburbDbUpdater constructor
    # description: set up the instance variables to be used in the methods
    # return: None
    # parameters: db_direct_ref -> reference to the database
    #             page -> the number of documents to update at every iteration
    def __init__(self, db_direct_ref, page):
        self.DBRef = db_direct_ref
        self.pagination = int(page)

    # function: update
    # description: method that performs the update
    # return: None
    # parameters: None
    def update(self):
        self._bulk_update()

    # function: _get_doc_ids
    # description: method that returns all the documents ids
    # return: list containing ids
    # parameters: None
    # comments: not in use
    def _get_doc_ids(self):
        ids_list = []
        print("TO DO.. get all documents ids.. docs without region field")
        for _id in self.DBRef:
            ids_list.append(_id)
        return ids_list

    # function: _get_doc_ids
    # description: method that returns all the documents ids that don't include a suburb field
    # return: list containing ids
    # parameters: None
    # comments: not in use
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

    # function: update_task
    # description: this method will add the suburb, polarity and bag of words for every document passed as parameter
    # return: None
    # parameters: s set of documents. each document is actually a tweet.
    def update_task(self,chunk_docs):
        docs = []
        region_handler = SG_planning()
        classifier = Classifier()
        for row in chunk_docs:
            doc = row
            try:
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

    # function: _bulk_update
    # description: this method is managing the update to add suburb, polarity and bag of words.
    #              it creates a log to keep track of the update progress.
    #              it chunk and performs a multithreading update operations aided by update_task
    # return: None
    # parameters: None
    def _bulk_update(self):
        # time_init = time.time()
        number_of_threads = 8
        num_records_so_far = 0
        try:
            # read the log file
            log_file =  open('log_update.txt','r')
            line_list = log_file.readlines()
            log_file.close()
            # access the contents of the las line in the log file
            last_line_items = line_list[len(line_list)-1].split()
            # initilize the parameters with those inside the log file
            num_records_so_far = int(last_line_items[len(last_line_items)-1])
            total_processed = num_records_so_far
            ## fool the process before start
            docs_number = num_records_so_far + 1
            skip = num_records_so_far
            page_number = int(last_line_items[1][:-1])
        except:
            # set up default values
            page_number = 1
            docs_number = 1
            skip = 0
            total_processed = 0

        while skip < docs_number:
            log_file =  open('log_update.txt','a')
            time0 = time.time()
            # retrive as many documents specified by self.pagination, skipping as many as specified by skip
            rows = self.DBRef.view('_all_docs', limit=self.pagination, skip=skip, include_docs=True)
            docs_number = int(rows.total_rows)
            docs = [row.doc for row in rows]
            if(len(docs)==0):
                break
            # for several_docs in self._chunk_doc_list(docs, self.pagination):
            #     time0 = time.time()

            # divide the documents in equal size chunks
            chunks=[docs[x:x+int(self.pagination/number_of_threads)] for x in range(0, len(docs), int(len(docs)/number_of_threads))]

            # assing each thread a bulk/set of documents
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

            # update statistics
            total_processed += len(docs)
            num_records_so_far += len(docs)
            # print("processed=",(total_processed))
            # print("time for processing bulk %f = %f sec"%(self.pagination,(time.time()-time0)))

            # save statistics into file before updating and go for another iteration
            log_file.write("page {}: {} remaining {} records {} \n".format(page_number,(time.time()-time0),  docs_number- skip,total_processed))
            page_number += 1
            skip = num_records_so_far
            log_file.close()

    # function: _chunk_doc_list
    # description: method that chunks a set of documents and return a set of size n.
    #              it keeps records of variables until the "docs" list is empty
    # return: a n-size set of documents. Subset of 'docs'
    # parameters: set of documents docs
    # comments: not in use
    def _chunk_doc_list(self, docs, n=1000):
        i = 0
        while True:
            ret_val = []
            ret_val = docs[i:i+n]
            i += n
            if len(ret_val) == 0:
                break
            yield ret_val

# function: update_main
# description: main method that access a couchdb db and performs the update
# return: None
# parameters: None
def update_main():
    twitter_store = TweetStore(DATA_BASE, url=SERVER)
    updater = SuburbDbUpdater(twitter_store.get_db_reference(), PAGE)
    updater.update()

if __name__ == '__main__':
    update_main()
    # TO DO : include code if needed