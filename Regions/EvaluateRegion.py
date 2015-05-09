__author__ = 'santiago_villagomez'
from matplotlib.path import Path
from PlaningAreas import areas_dict

class SG_planning:

    def area_name(self,point):
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


def main_program():
    evaluation_point = (1.242534, 103.832911)
    area_planning = SG_planning()
    result = area_planning.area_name(evaluation_point)
    print(result)

if __name__ == '__main__':
    main_program()
