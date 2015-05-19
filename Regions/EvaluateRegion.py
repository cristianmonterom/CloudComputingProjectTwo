__author__ = 'Group 21 - COMP90024 Cluster and Cloud Computing'

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from matplotlib.path import Path
from Regions.PlaningAreas import areas_dict
import time


class SG_planning:

    def __init__(self):
        self.default_no_suburb = "No suburb found"

    def get_area_name(self,point):
        # the parameter must be like  point = (latitude, longitude)
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

    def get_default_no_area(self):
        return self.default_no_suburb


class Location:
    def get_tweet_location(self, tweet):
        json_tweet = tweet
        lonlat = json_tweet['coordinates']['coordinates']
        return lonlat


class Region:
    def add_region_field(self, tweet):
        location_handler = Location()
        area_handler = SG_planning()
        lonlat = location_handler.get_tweet_location(tweet)
        point = (lonlat[1], lonlat[0])
        suburb_name = area_handler.get_area_name(point)
        region = {"suburb": suburb_name}
        tweet.update(region)
        return tweet


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
