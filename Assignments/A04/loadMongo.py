myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["moviesDb"]
collection = db["movieNames"]

def loadFile(path, savePath=None):
    name, ext = os.path.splitext(path)
    name = name[len("datasets.imdbws.com/"):]
    print(name)

    return

    f = open(f'{name}.json','w')