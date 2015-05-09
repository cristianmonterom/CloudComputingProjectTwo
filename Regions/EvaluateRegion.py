__author__ = 'santiago_villagomez'
from matplotlib.path import Path
from PlaningAreas import areas_dict
import json

class SG_planning:

    def get_area_name(self,point):
        # point = (latitude, longitude)
        area_found_result = False
        area_name = ""
        for i in areas_dict:
            path = Path(areas_dict[i])

            if path.contains_point(point) == 1:
                area_name = i
                area_found_result = True
                break
        if area_found_result == False:
            area_name = "NO area Found"
        return area_name

class Location:
    def get_tweet_location(self,tweet):
        json_tweet = tweet
        lonlat = json_tweet['coordinates']['coordinates']
        return lonlat

class Region:
    def add_region_field(self,tweet):
        location_handler = Location()
        area_handler = SG_planning()
        lonlat = location_handler.get_tweet_location(tweet)
        point = (lonlat[1],lonlat[0])
        suburb_name = area_handler.get_area_name(point)
        region = {"suburb":suburb_name}
        tweet.update(region)
        return tweet

def main_program():
    evaluation_point = (1.242534, 103.832911)
    area_planning = SG_planning()
    result = area_planning.get_area_name(evaluation_point)
    print(result)

if __name__ == '__main__':
    main_program()
