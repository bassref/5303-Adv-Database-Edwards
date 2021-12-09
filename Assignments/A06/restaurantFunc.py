import pymongo
import pprint
import random
import fastapi
import json

# connect to mongodb
cnx = pymongo.MongoClient("mongodb://localhost:27017/")
# use businessData
db = cnx["restaurantData"]
# choose collection
coll = db['restaurants']


#coll.index_information()
def find_all(page_size, page_num):
        '''
        : @params:
        '''
        skips = page_size * (page_num -1)
        cursor = coll.find({},{"_id":0}).skip(skips).limit(page_size)
        return list(cursor)

def listAllCollections(dbName=None):
    """
    Description:
        lists all collections in a db (just as an example)
    Params:
        dbName (string) : name of database to view collections (optional)
    Returns:
        list
    """
    if dbName:
        collections = cnx[dbName].list_collection_names()
    else:
        collections = db.list_collection_names()

    return collections

def findAllRestaurants():
    """
    Description: 
        Find all restaurants in collection
    Params:
        None
    Returns: 
        dict : {"result":list,"size":int}
    """
    
    res = list(coll.find())
    
    return {"result":res,"count":len(res)}

def findCuisineCounts():
    """
    Description: 
        Count all restaurants that serve a specific cuisine
    Params:
        None
    Returns: 
        list of cuisine counts
    """

    results = db['restaurants'].aggregate([

        # Group the documents and "count" via $sum on the values
        { "$group": 
            {
                "_id": '$cuisine',
                "count": { "$sum": 1 }
            }
        }
    ])

    return list(results)

def findCuisines():
    """
    Description: 
        List all the cuisines available
    Params:
        None
    Returns: 
        list of cuisine options
    """

    results = db['restaurants'].distinct("cuisine")

    return list(results)

def findRestaurantsByCuisine(cuisine=None):
    """
    Description: 
        Find all restaurants that serve a specific cuisine
    Params:
        cuisine (string) : type of restaurant to find
    Returns: 
        list
    """

    if cuisine == None:
        res="No Cuisine selected"
    else: 
        db.restaurants.create_index('cuisine')
        db.restaurants.index_information()
        myquery = {'cuisine':cuisine}       
        res = coll.find(myquery)
    
    return list(res)

def findRestaurantsByZipcode(zipcodes=None):
    '''
    Description: Finds the restaurants in a given zipcode
    Params: 1 or more zipcodes
    Returns: list
    '''
    zipcodes =list(zipcodes)
    if zipcodes == None:
        res = ["None available"]
    else:
        
        res = coll.find({ "address.zipcode": {"$in": zipcodes}})

    return list(res)

def findRestaurantsByGrade(score=None):
    '''
    Description:
    Params:
    Returns: list
    '''
    if score == None:
        res = ["None Available"]
    else:
        res= coll.find({"grades.score":{"$gte":score}})
    
    return (res)

def findRestaurantsByDistance(coords=None):
    '''
    Description: finds restaurants close to a certain parameter
    Params:
    Returns: list
    '''
    
    db.restaurants.createIndex({ coords: "2dsphere" })
    db.restaurants.find({'location': { '$nearSphere': { '$geometry': { type: "Point", coords:coords}, '$maxDistance': 10 } }})


if __name__=='__main__':
    print("\n","="*80,"\n","="*80)
    print("\nList all collections in 'moviesDb':\n")
    res = listAllCollections(dbName='moviesDb')
    print(res)

    print("\n","="*80,"\n","="*80)
    print("\nList counts of all restaurants:\n")
    res = findAllRestaurants()
    print(res["count"])

    print("\n","="*80,"\n","="*80)
    print("\nList counts of all unique cuisines:\n")
    res = findCuisineCounts()
    pprint.pprint(res)

    print("\n","="*80,"\n","="*80)
    print("\nList restaurants by cuisine (no param = random cuisine) and only print 5:\n")
    res = findRestaurantsByCuisine()
    pprint.pprint(res[:5])
