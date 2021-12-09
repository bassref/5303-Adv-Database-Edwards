import redis
import json
import glob
import time
import pickle
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
""" r.set('hello', 'world') # True
# GET hello
world = r.get('hello')
print(world.decode()) 
r.delete('hello')
print(r.get('hello').decode()) """
alllist =[]
timeeach={}
inserts =[5000,10000,50000,100000]
count = len(inserts)
with  open("/var/www/html/Database/Assignment8/All.json", "r") as file1:
    data = json.load(file1)
    c =0
    while(count >0):
        count-=1
        i =0
        currlist =[]
        start_time = time.time()
        for i in range(i,inserts[c]):
            currlist.append(data[i])
        toinsert =pickle.dumps(currlist)
        r.set('some_key', toinsert)
        endtime =(time.time() - start_time)
        """ keyfor = "redis "+ str(inserts[c]) + 'insert'
        timeeach[keyfor] = endtime """
        start_timeSelect = time.time()
        unpacked_object = pickle.loads(r.get('some_key'))
        endtimeselect =(time.time() - start_timeSelect)
        keyforSelect = "redis "+ str(inserts[c]) + 'SelectMany'
        timeeach[keyforSelect] = endtimeselect
        start_timedelete = time.time()
        r.delete('some_key')
        endtimedelete =(time.time() - start_timedelete)
        keyfordelete = "redis "+ str(inserts[c]) + 'delete'
        timeeach[keyfordelete] = endtimedelete
        c+=1
alllist.append(timeeach)
with  open("/var/www/html/Database/Assignment8/timeall.json", "a") as file1:
    file1.write(json.dumps(alllist))