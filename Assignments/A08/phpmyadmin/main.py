import json
from mysqlCnx import MysqlCnx
import glob
import time


with open('/var/www/html/Database/Assignment8/phpmyadmin/.config.json') as f:
    config = json.loads(f.read())
cnx = MysqlCnx(**config)
#insert,update,delete
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
        """ start_time = time.time() """ 
        for i in range(i,inserts[c]):
            toinsert =str(json.dumps(data[i]))
            sql ="INSERT INTO `Speed` (`testdata`, `1d`) VALUES('{datas}',{id})".format(datas=toinsert,id='NULL')
            cnx.query(sql)
        """ endtime =(time.time() - start_time)
        keyfor = "MYSQL "+ str(inserts[c]) + 'insert'
        timeeach[keyfor] = endtime  """

        #select Multiple
        start_timeSS = time.time()   
        sql2 ='SELECT * FROM `Speed` WHERE JSON_EXTRACT(testdata , "$.id") >1'
        cnx.query(sql2)
        endtimeSS =(time.time() - start_timeSS)
        keyforSS = "MYSQL "+ str(inserts[c]) + 'selectMultiple'
        timeeach[keyforSS] = endtimeSS
        #select single
        start_timeSS1 = time.time()   
        sql3 ='SELECT * FROM `Speed` WHERE JSON_EXTRACT(testdata , "$.id") =1'
        cnx.query(sql3)
        endtimeSS1 =(time.time() - start_timeSS1)
        keyforSS1 = "MYSQL "+ str(inserts[c]) + 'selectSingle'
        timeeach[keyforSS1] = endtimeSS1
        start_timeupdate = time.time()   
        for i in range(i,inserts[c]):
            update ="UPDATE `Speed` SET `testdata`= JSON_SET(testdata, '$.Car', 'Mazda') where 1d > 1"
            cnx.query(update)
        endtimeupdate =(time.time() - start_timeupdate)
        keyforupdate = "MYSQL "+ str(inserts[c]) + 'update'
        timeeach[keyforupdate] = endtimeupdate

        start_timdelete = time.time()   
        for i in range(i,inserts[c]):
            delete ='DELETE FROM `Speed` WHERE testdata->"$.id" > 1;'
            cnx.query(delete)
        endtimedelete =(time.time() - start_timdelete)
        keyfordelete= "MYSQL "+ str(inserts[c]) + 'Delete'
        timeeach[keyfordelete] = endtimedelete
        delete = "TRUNCATE TABLE Speed"
        cnx.query(delete)
        print(timeeach)
        c+=1
alllist.append(timeeach)
with  open("/var/www/html/Database/Assignment8/timeall.json", "a") as file1:
    file1.write(json.dumps(alllist))
#selectSingle