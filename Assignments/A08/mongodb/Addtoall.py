import glob
import json
addtofile =[]

i =1
count =0
filecount =0
with  open("/var/www/html/Database/Assignment8/All.json", "a") as file1:
    for name in glob.glob('/var/www/html/Database/Assignment8/data/*.json'):
        f = open(name)
        print(name)
        filecount+=1
        data = json.load(f)
        for dat in data:
            dat['id'] = i
            i+=1
            addtofile.append(dat)
            count+=1
        print(i)
    file1.write(json.dumps(addtofile))
print(count)
print(len(addtofile))
print(filecount)







        
    
