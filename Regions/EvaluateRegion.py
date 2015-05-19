__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from matplotlib.path import Path
from Regions.PlaningAreas import areas_dict
import time


# SG_planning class
# Usage: It is intended for retrieving a name given a latitude and longitude coordinates
class SG_planning:

    def __init__(self):
        self.default_no_suburb = "No suburb found"

    # function: get_area_name
    # description: evaluates a point coordinates and returns a suburb name associated with it.
    #              "No suburb found" if point is does not belong to any suburb
    # return: string name of suburb
    # parameters: tuple "point = (latitude, longitude)"
    def get_area_name(self,point):
        area_found_result = False
        area_name = ""
        for i in areas_dict:
            path = Path(areas_dict[i])

            if path.contains_point(point) == 1:
                area_name = i
                area_found_result = True
                break
        if area_found_result == False:
            area_name = self.default_no_suburb
        return area_name

    # function: get_default_no_area
    # description: it is the getter function for the default name. Used when a point falls
    #              outside Singapore
    # return: string "No suburb found:
    # parameters: None

    def get_default_no_area(self):
        return self.default_no_suburb

# Location: class
# Usage: It is intended for retrieving information regarding a tweet location
class Location:

    # function: get_tweet_location
    # description: access a tweeter coordinates located inside the coordinates field
    # return: a list containing the longitude a latitude values
    # parameters: single tweet
    def get_tweet_location(self, tweet):
        json_tweet = tweet
        lonlat = json_tweet['coordinates']['coordinates']
        return lonlat

# Region: class
# Usage: It is intended for adding the suburb field in a tweet
class Region:
    # function: add_region_field
    # description: add the suburb information taking into account the location values inside a twee
    # return: a tweet with suburb field
    # parameters: single tweet
    def add_region_field(self, tweet):
        location_handler = Location()
        area_handler = SG_planning()
        lonlat = location_handler.get_tweet_location(tweet)
        point = (lonlat[1], lonlat[0])
        suburb_name = area_handler.get_area_name(point)
        region = {"suburb": suburb_name}
        tweet.update(region)
        return tweet

# function: main_program
# description: a function to do some tests if needed. Must be called explicitly by teh user
# return: None
# parameters: None
def main_program():
    evaluation_point = (1.242534, 103.832911)
    area_planning = SG_planning()
    tiempo0 = time.time()
    for i in range (0,10000):
        result = area_planning.get_area_name(evaluation_point)
    print("10000 en :",(time.time() - tiempo0))

    print(result)

if __name__ == '__main__':
    main_program()
