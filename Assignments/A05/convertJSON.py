import json

def convertToGeoJSON():
        '''  
        : @param: None
        : description:
         '''
        restaurantsList = []
        coords = []
        with open('resaurant_updated_coord.json') as file:
            for restaurant in file:
                restDict = json.loads(restaurant)
                coords = restDict["address"]["coord"]
                if coords:
                    restDict["location"] = {
                        "type" : "Point",
                        "coordinates" : coords,
                    }
                    del restDict["address"]["coord"]
                    restaurantsList.append(restDict)
        with open('restaurantData.json', 'w+') as new_file:
            for newRestaurant in restaurantsList:
                rest_obj = json.dump(newRestaurant, new_file)

if __name__=="__main__":
    convertToGeoJSON()