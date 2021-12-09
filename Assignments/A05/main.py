import json
import fastapi
import uvicorn
import restaurantFunc
from pprint import pprint
from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
#open the config file to connect


app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World. this is a Restaurant Search"}

@app.get('/restaurants/{page_size}/{page_num}')
async def get_all(page_size, page_num):
    results =  restaurantFunc.find_all(int(page_size), int(page_num))
    pprint(results)
    return results

#route for finding the unique restaurant categories
@app.get("/uniqueRestaurants")
async def get_unique_category():
    queryResults = restaurantFunc.findCuisines()    
    return(queryResults)
    
#route for getting a restaurant by category
@app.get("/restaurantCategory/{item_name}")
async def get_restaurant_by_category(item_name):
    queryResults = restaurantFunc.findRestaurantsByCuisine(item_name)    
    return(queryResults)

#route for getting a restaurant by category
@app.get("/restaurantZipcode/{item_name}")
async def get_restaurant_by_zipcode(item_name: str):
    queryResults = restaurantFunc.findRestaurantsByZipcode(item_name)    
    return(queryResults)

@app.get("/restaurantGrade/{item_name}")
async def get_restaurant_by_Grade(item_name):
    queryResults = restaurantFunc.findRestaurantsByGrade(item_name)    
    return(queryResults)


if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, log_level="info")
    #