

files = glob.glob('datasets.imdbws.com/*.tsv')

    for file in files:
        print(file)
        if file == 'datasets.imdbws.com/title.basics.tsv':

            categories = {}
            years = {}
            res = cnx.query("truncate movie;")

            cols = ('mid','title','adult','released','runTime')

            with open(file, newLine='\n',encoding='utf-8') as tsvfile:
                movieData = csv.reader(tsvfile, delimiter='\t')
                next(movieData) #get rid of headers
                movieCount = 0
                allCount = 0
                for row in movieData:
                    genre = None
                    catefory = row[1]
                    year = row[5]
                    if not category in categories:
                        categories[category] = 0
                    
                    if not year in years:
                        years[year] = 0
                    
                    categories[category] +=1