import json
from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from mysqlCnx import MysqlCnx

#open the config file to connect
with open('.config.json') as f:
    config = json.loads(f.read())

cnx = MysqlCnx(**config)

class Tut(BaseModel):
    id: int
    title: str
    author: str
    submission_date: str

#dictionary for the queries from the basics table
basics = {
    1: {"question":"What is the population of Germany?","sql":"SELECT population FROM world WHERE name = 'France'"},
    2: {"question": "Show the population for Sweden, Norway and Denmark", "sql":"SELECT name, population FROM world WHERE name IN ('Sweden', 'Norway', 'Denmark')" },
    3: {"question": "Which countries have an area between 200 000 and 250 000 sq. km.", "sql":"SELECT name, area FROM world WHERE area BETWEEN 200000 AND 250000"}
}

world = {
    1: {"question" :"Show the name, continent and population of all countries", "sql": "SELECT name, continent, population FROM world"},
    2: {"question":"Show the name for the countries that have a population of at least 200 million", "sql":"SELECT name FROM world WHERE population >= 200000000"},
    3: {"question":"Give the name and the per capita GDP for those countries with a population of at least 200 million" , "sql":"SELECT name, gdp/population FROM world WHERE population >= 200000000"},
    4: {"question":"Show the name and population (in millions) for the countries on the continent of South America ", "sql":"SELECT name, population/1000000 FROM world WHERE continent LIKE 'South America'"},
    5: {"question":"Show the name and population for France, Germany, Italy", "sql":"SELECT name, population FROM world WHERE name IN('France','Germany','Italy')"},
    6: {"question":"Show the countries which have a name that includes the word United", "sql":"SELECT name FROM world WHERE name LIKE '%United' or name like 'United%' or name like '%United%'"},
    7: {"question":"Show the name, population and area of countries that are big by area or big by population.", "sql":"SELECT name, population, area FROM world WHERE area > 3000000 OR population > 250000000"},
    8: {"question":"Show name population and area for the countries with an area more than 3 million or population more than 250 million but not both.", "sql":"SELECT name, population, area FROM world WHERE area > 3000000 XOR population > 250000000"},
    9: {"question":"Show the name and population in millions and the GDP in billions for the countries of the continent South America.", "sql":"SELECT name, ROUND(population/1000000,2), ROUND(gdp/1000000000, 2) FROM world WHERE  continent = 'South America'"},
    10: {"question":"Show per-capita GDP for the trillion dollar countries to the nearest $1000.", "sql":"SELECT name , ROUND(gdp/population, -3) FROM world WHERE gdp >= 1000000000000"},
    11: {"question":"Show the name and capital where the name and the capital have the same number of characters.", "sql":"SELECT name, capital FROM world WHERE LENGTH(name) = LENGTH(capital)"},
    12: {"question":"Show the name and the capital where the first letters of each match. Don't include countries where the name and the capital are the same word.", "sql":"SELECT name, capital FROM world WHERE LEFT(name,1) = LEFT(capital,1) AND name <> capital"},
    13: {"question":"Find the country that has all the vowels and no spaces in its name.", "sql":"SELECT name FROM world WHERE name LIKE '%a%' AND name LIKE '%e%' AND name LIKE '%i%' AND name LIKE '%o%' AND name LIKE '%u%' AND name NOT LIKE '% %'"}
    
}

nobel = {
    1: {"question":"Display Nobel prizes for 1950.", "sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1950"},
    2: {"question":"Who won the 1962 Nobel prize for Literature.", "sql":"SELECT winner FROM nobel WHERE yr = 1962 AND subject = 'Literature'"},
    3: {"question":"Show the year and subject that won 'Albert Einstein' his prize.", "sql":"SELECT yr, subject from nobel WHERE winner = 'Albert Einstein'"},
    4: {"question":"What are the names of the 'Peace' winners since the year 2000 inclusive.", "sql":"select winner from nobel WHERE subject like '%Peace%' and yr >= '2000'"},
    5: {"question":"Show all details (yr, subject, winner) of the Literature prize winners for 1980 to 1989 inclusive.", "sql":"SELECT yr, subject, winner FROM nobel WHERE subject = 'Literature' AND yr >= 1980 AND yr <= 1989"},
    6: {"question":"Show all details of the presidential winners: Theodore Roosevelt Woodrow Wilson Jimmy Carter Barack Obama ", "sql":"SELECT * FROM nobel WHERE winner IN ('Theodore Roosevelt','Woodrow Wilson','Jimmy Carter','Barack Obama')"},
    7: {"question":"Show the winners with first name John", "sql":"SELECT winner FROM nobel WHERE winner LIKE 'John%'"},
    8: {"question":"Show the year, subject, and name of Physics winners for 1980 together with the Chemistry winners for 1984.", "sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1980 AND subject = 'Physics' OR yr = 1984 AND subject = 'Chemistry'"},
    9: {"question":"Show the year, subject, and name of winners for 1980 excluding Chemistry and Medicine", "sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1980 AND subject <> 'Medicine' AND subject <> 'Chemistry'"},
    10: {"question":"Show year, subject, and name of people who won a 'Medicine' prize before 1910, not including 1910) and winners of a 'Literature' prize in or after 2004 inclusive.)", "sql":"SELECT yr, subject, winner FROM nobel WHERE subject = 'Medicine' AND yr < 1910 OR subject = 'Literature' AND yr >= 2004"},
    11: {"question":"Find all details of the prize won by PETER GRÜNBERG", "sql":"SELECT yr, subject, winner FROM nobel WHERE winner = 'PETER GRÜNBERG'"},
    12: {"question":"Find all details of the prize won by EUGENE O'NEILL", "sql":"SELECT yr, subject, winner FROM nobel WHERE winner LIKE 'EUGENE O%' and winner LIKE '%NEILL'"},
    13: {"question":"List the winners, year and subject where the winner starts with Sir. Show the the most recent first, then by name order.", "sql":"SELECT winner, yr, subject FROM nobel WHERE winner LIKE 'Sir%' ORDER BY yr DESC, winner ASC"},
    14: {"question":"Show the 1984 winners and subject ordered by subject and winner name; but list Chemistry and Physics last.", "sql":"SELECT winner, subject FROM nobel WHERE yr=1984 ORDER BY CASE WHEN subject IN ('Physics','Chemistry') THEN 1 ELSE 0 END, subject, winner"},
}

selectOper = {
    1: {"question":"List each country name where the population is larger than that of 'Russia'.", "sql":"SELECT name FROM world WHERE population > (SELECT population FROM world WHERE name='Russia')"},
    2: {"question":"Show the countries in Europe with a per capita GDP greater than 'United Kingdom'.", "sql":"SELECT name FROM world WHERE  (gdp/population) > (SELECT (gdp/population) FROM world WHERE name = 'United Kingdom') AND continent = 'Europe'"},
    3: {"question":"List the name and continent of countries in the continents containing either Argentina or Australia. Order by name of the country.", "sql":"SELECT name, continent FROM world WHERE continent IN (SELECT continent FROM world WHERE name IN ('Argentina', 'Australia')) ORDER BY name"},
    4: {"question":" Which country has a population that is more than Canada but less than Poland? Show the name and the population.", "sql":"SELECT name, population FROM world WHERE population > (SELECT population FROM world WHERE name = 'Canada') AND population < (SELECT population FROM world WHERE name = 'Poland')"},
    5: {"question":"Show the name and the population of each country in Europe. Show the population as a percentage of the population of Germany.", "sql":"SELECT name, CONCAT(ROUND(population/(SELECT population FROM world WHERE name = 'Germany')*100), '%') FROM world WHERE continent = 'Europe"},
    6: {"question":"Which countries have a GDP greater than every country in Europe? ", "sql":"SELECT name FROM world WHERE gdp > ALL(SELECT gdp FROM world WHERE gdp > 0 AND continent = 'Europe')"},
    7: {"question":"Find the largest country (by area) in each continent, show the continent, the name and the area", "sql":"SELECT continent, name, area FROM world x WHERE area >= ALL(SELECT area FROM world y WHERE x.continent = y.continent AND y.area>0)"},
    8: {"question":"List each continent and the name of the country that comes first alphabetically.", "sql":"SELECT continent, name, area FROM world x WHERE area >= ALL(SELECT area FROM world y WHERE x.continent = y.continent AND y.area>0)"},
    9: {"question":"Find the continents where all countries have a population <= 25000000. Then find the names of the countries associated with these continents. Show name, continent and population.", "sql":"SELECT name, continent, population FROM world WHERE continent IN (SELECT continent FROM world x WHERE 25000000 >= (SELECT MAX(population) FROM world y WHERE x.continent = y.continent))"},
    10:{"question":"Give the countries and continents that have populations more than three times that of any of their neighbours (in the same continent).", "sql":"SELECT name, continent FROM world x WHERE population > ALL(SELECT 3*population FROM world y WHERE x.continent = y.continent AND x.name <> y.name)"}
}

sumAndCount = {
    1: {"question":"Show the total population of the world.", "sql":"SELECT SUM(population) FROM world"},
    2: {"question":"List all the continents - just once each.", "sql":"SELECT DISTINCT continent FROM world"},
    3: {"question":"Give the total GDP of Africa", "sql":"SELECT SUM(gdp) FROM world WHERE continent = 'Africa'"},
    4: {"question":"How many countries have an area of at least 1000000", "sql":"SELECT COUNT(*) FROM world WHERE area >= 1000000"},
    5: {"question":"What is the total population of ('Estonia', 'Latvia', 'Lithuania')", "sql":"SELECT SUM(population) FROM world WHERE name IN ('Estonia','Latvia','Lithuania')"},
    6: {"question":"For each continent show the continent and number of countries.", "sql":"SELECT continent, COUNT(*) FROM world GROUP BY continent"},
    7: {"question":"For each continent show the continent and number of countries with populations of at least 10 million.", "sql":"SELECT continent, COUNT(*) FROM world WHERE population >= 10000000 GROUP BY continent"},
    8: {"question":"List the continents that have a total population of at least 100 million", "sql":"SELECT continent FROM world x WHERE (SELECT SUM(population) FROM world y WHERE x.continent = y.continent) >= 100000000 GROUP BY continent"}
}

joinOper = {
    1: {"question":"Show the matchid and player name for all goals scored by Germany.", "sql":"SELECT matchid, player FROM goal WHERE teamid = 'GER'"},
    2: {"question":"Show id, stadium, team1, team2 for just game 1012", "sql":"SELECT id, stadium, team1, team2 FROM game WHERE id = 1012"},
    3: {"question":"Show the player, teamid, stadium and mdate for every German goal.", "sql":"SELECT player, teamid, stadium, mdate FROM game JOIN goal ON game.id = goal.matchid WHERE teamid='GER'"},
    4: {"question":"Show the team1, team2 and player for every goal scored by a player called Mario player LIKE 'Mario%'", "sql":"SELECT game.team1, game.team2, goal.player FROM goal JOIN game ON game.id = goal.matchid WHERE goal.player LIKE 'Mario%'"},
    5: {"question":"Show player, teamid, coach, gtime for all goals scored in the first 10 minutes gtime<=10", "sql":"SELECT player, teamid, coach, gtime FROM goal JOIN eteam ON goal.teamid = eteam.id WHERE gtime <= 10"},
    6: {"question":"List the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach.", "sql":"SELECT mdate, teamname FROM eteam JOIN game ON (eteam.id = game.team1) WHERE coach = 'Fernando Santos'"},
    7: {"question":"List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'", "sql":"SELECT player FROM game JOIN goal ON id = matchid WHERE stadium = 'National Stadium, Warsaw'"},
    8: {"question":"Show the name of all players who scored a goal against Germany.", "sql":"SELECT DISTINCT player FROM game JOIN goal ON matchid = id WHERE (team1='GER' OR team2='GER') AND teamid != 'GER'"},
    9: {"question":"Show teamname and the total number of goals scored.", "sql":"SELECT teamname, COUNT(*) FROM goal JOIN eteam ON eteam.id = goal.teamid GROUP BY teamname"},
    10: {"question":"Show the stadium and the number of goals scored in each stadium.", "sql":"SELECT stadium, COUNT(*) FROM goal JOIN game ON matchid = id GROUP BY stadium"},
    11: {"question":"For every match involving 'POL', show the matchid, date and the number of goals scored.", "sql":"SELECT matchid,mdate, COUNT(teamid) FROM game JOIN goal ON matchid = id WHERE (team1 = 'POL' OR team2 = 'POL') GROUP BY gisq.goal.matchid, gisq.game.mdate"},
    12: {"question":"For every match where 'GER' scored, show matchid, match date and the number of goals scored by 'GER'", "sql":"SELECT matchid, mdate, COUNT(*) FROM goal JOIN game ON id = matchid WHERE (team1 = 'GER' OR team2 = 'GER') AND teamid = 'GER' GROUP BY matchid, gisq.game.mdate"},
    13: {"question":"List every match with the goals scored by each team as shown. This will use 'CASE WHEN' which has not been explained in any previous exercises.", "sql":"SELECT game.mdate, game.team1, SUM(CASE WHEN goal.teamid = game.team1 THEN 1 ELSE 0 END) AS score1,game.team2,SUM(CASE WHEN goal.teamid = game.team2 THEN 1 ELSE 0 END) AS score2 FROM game LEFT JOIN goal ON matchid = id GROUP BY game.id,game.mdate, game.team1, game.team2 ORDER BY mdate,matchid,team1,team2"}
}

teacherPostOper = {
    1: {"question":"", "sql":""},
}

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    price: float
    brand: str

class TeachItem(BaseModel):
    id: Optional[int] = None
    dept: str
    name: str
    phone: int
    mobile: int

class WorldItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    continent: Optional[str] = None
    area: Optional[int] = None
    population: Optional[int] = None
    gdp: Optional[int] = None
    capital: Optional[str] = None
    tld: Optional[str] = None
    flag: Optional[str] = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

#route for reading a table from basics
@app.get("/basics/{item_id}")
async def read_item_basics(item_id:int):
    ques = basics[item_id]['question']
    quer = basics[item_id]['sql']
    res = cnx.query(basics[item_id]['sql'])

    response = {
        "Question":ques,
        "Query": quer,
        "Result": res
    }
    return(response)
    

#route for reading World Tutorial
@app.get("/world/{item_id}")
async def read_item_world(item_id:int):
    ques = world[item_id]['question']
    res = cnx.query(world[item_id]['sql'])
    quer = world[item_id]['sql']    

    response = {
        "Question":ques,
        "Query": quer,
        "Result": res
    }
    return(response)

#route for Nobel Tutorial
@app.get("/nobel/{item_id}")
async def read_item_nobel(item_id:int):
    ques = nobel[item_id]['question']
    res = cnx.query(nobel[item_id]['sql'])
    quer = nobel[item_id]['sql']    

    response = {
        "Question":ques,
        "Query": quer,
        "Result": res
    }
    return(response)

#route for Select Within Tutorial
@app.get("/selectOper/{item_id}")
async def read_item_select_Oper(item_id:int):
    ques = selectOper[item_id]['question']
    res = cnx.query(selectOper[item_id]['sql'])
    quer = selectOper[item_id]['sql']    

    response = {
        "Question":ques,
        "Query": quer,
        "Result": res
    }
    return(response)

#route for Sum and Count Tutorial
@app.get("/sumAndCount/{item_id}")
async def read_item_Sum_And_Count(item_id:int):
    ques = sumAndCount[item_id]['question']
    res = cnx.query(sumAndCount[item_id]['sql'])
    quer = sumAndCount[item_id]['sql']    

    response = {
        "Question":ques,
        "Query": quer,
        "Result": res
    }
    return(response)


#route for Join Tutorial
@app.get("/joinOper/{item_id}")
async def read_item_join_Oper(item_id:int):
    ques = joinOper[item_id]['question']
    res = cnx.query(joinOper[item_id]['sql'])
    quer = joinOper[item_id]['sql']    

    response = {
        "Question":ques,
        "Query": quer,
        "Result": res
    }
    return(response)

#route return all the routes
@app.get("/all/")
async def read_item_all(request:Request):
    response = {
        "BASICS": "-----------------------------------",
        basics[1]['question']: request.url_for("read_item_basics", **{"item_id":1}),
        basics[2]['question']:  request.url_for("read_item_basics", **{"item_id":2}),
        basics[3]['question']:  request.url_for("read_item_basics", **{"item_id":3}),
        "WORLD": "-----------------------------------",
        world[1]['question']:  request.url_for("read_item_world", **{"item_id":1}),
        world[2]['question']:  request.url_for("read_item_world", **{"item_id":2}),
        world[3]['question']:  request.url_for("read_item_world", **{"item_id":3}),
        world[4]['question']:  request.url_for("read_item_world", **{"item_id":4}),
        world[5]['question']:  request.url_for("read_item_world", **{"item_id":5}),
        world[6]['question']:  request.url_for("read_item_world", **{"item_id":6}),
        world[7]['question']:  request.url_for("read_item_world", **{"item_id":7}),
        world[8]['question']:  request.url_for("read_item_world", **{"item_id":8}),
        world[9]['question']:  request.url_for("read_item_world", **{"item_id":9}),
        world[10]['question']:  request.url_for("read_item_world", **{"item_id":10}),
        world[11]['question']:  request.url_for("read_item_world", **{"item_id":11}),
        world[12]['question']:  request.url_for("read_item_world", **{"item_id":12}),
        world[13]['question']:  request.url_for("read_item_world", **{"item_id":13}),
        "NOBEL": "-----------------------------------",
        nobel[1]['question']:  request.url_for("read_item_nobel", **{"item_id":1}),
        nobel[2]['question']:  request.url_for("read_item_nobel", **{"item_id":2}),
        nobel[3]['question']:  request.url_for("read_item_nobel", **{"item_id":3}),
        nobel[4]['question']:  request.url_for("read_item_nobel", **{"item_id":4}),
        nobel[5]['question']:  request.url_for("read_item_nobel", **{"item_id":5}),
        nobel[6]['question']:  request.url_for("read_item_nobel", **{"item_id":6}),
        nobel[7]['question']:  request.url_for("read_item_nobel", **{"item_id":7}),
        nobel[8]['question']:  request.url_for("read_item_nobel", **{"item_id":8}),
        nobel[9]['question']:  request.url_for("read_item_nobel", **{"item_id":9}),
        nobel[10]['question']:  request.url_for("read_item_nobel", **{"item_id":10}),
        nobel[11]['question']:  request.url_for("read_item_nobel", **{"item_id":11}),
        nobel[12]['question']:  request.url_for("read_item_nobel", **{"item_id":12}),
        nobel[13]['question']:  request.url_for("read_item_nobel", **{"item_id":13}),
        nobel[14]['question']:  request.url_for("read_item_nobel", **{"item_id":14}),
        "SELECT OPERATION": "-----------------------------------",
        selectOper[1]['question']:  request.url_for("read_item_select_Oper", **{"item_id":1}),
        selectOper[2]['question']:  request.url_for("read_item_select_Oper", **{"item_id":2}),
        selectOper[3]['question']:  request.url_for("read_item_select_Oper", **{"item_id":3}),
        selectOper[4]['question']:  request.url_for("read_item_select_Oper", **{"item_id":4}),
        selectOper[5]['question']:  request.url_for("read_item_select_Oper", **{"item_id":5}),
        selectOper[6]['question']:  request.url_for("read_item_select_Oper", **{"item_id":6}),
        selectOper[7]['question']:  request.url_for("read_item_select_Oper", **{"item_id":7}),
        selectOper[8]['question']:  request.url_for("read_item_select_Oper", **{"item_id":8}),
        selectOper[9]['question']:  request.url_for("read_item_select_Oper", **{"item_id":9}),
        selectOper[10]['question']:  request.url_for("read_item_select_Oper", **{"item_id":10}),
        "SUM AND COUNT": "-----------------------------------",
        sumAndCount[1]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":1}),
        sumAndCount[2]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":2}),
        sumAndCount[3]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":3}),
        sumAndCount[4]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":4}),
        sumAndCount[5]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":5}),
        sumAndCount[6]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":6}),
        sumAndCount[7]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":7}),
        sumAndCount[8]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":8}),
        "JOIN OPERATION": "-----------------------------------",
        joinOper[1]['question']:  request.url_for("read_item_join_Oper", **{"item_id":1}),
        joinOper[2]['question']:  request.url_for("read_item_join_Oper", **{"item_id":2}),
        joinOper[3]['question']:  request.url_for("read_item_join_Oper", **{"item_id":3}),
        joinOper[4]['question']:  request.url_for("read_item_join_Oper", **{"item_id":4}),
        joinOper[5]['question']:  request.url_for("read_item_join_Oper", **{"item_id":5}),
        joinOper[6]['question']:  request.url_for("read_item_join_Oper", **{"item_id":6}),
        joinOper[7]['question']:  request.url_for("read_item_join_Oper", **{"item_id":7}),
        joinOper[8]['question']:  request.url_for("read_item_join_Oper", **{"item_id":8}),
        joinOper[9]['question']:  request.url_for("read_item_join_Oper", **{"item_id":9}),
        joinOper[10]['question']:  request.url_for("read_item_join_Oper", **{"item_id":10}),
        joinOper[11]['question']:  request.url_for("read_item_join_Oper", **{"item_id":11}),
        joinOper[12]['question']:  request.url_for("read_item_join_Oper", **{"item_id":12}),
        joinOper[13]['question']:  request.url_for("read_item_join_Oper", **{"item_id":13})}

    return (response)


#put route for world
@app.put("/world/{world_item}")
async def create_item(worldItem: WorldItem):
    sql = "UPDATE `world` SET WHERE"
    
    if worldItem.name != None:
        sql += f"`name`=`{worldItem.name}`, "
    
    if worldItem.continent !=None: 
        sql += f"`continent`=`{worldItem.continent}`, "
    
    if worldItem.area !=None: 
        sql += f"`area`=`{worldItem.area}`, "
    
    if worldItem.population !=None: 
        sql += f"`population`=`{worldItem.population}`, "

    if worldItem.gdp != None: 
        sql += f"`gdp`= `{worldItem.gdp}`, "
    
    if worldItem.capital != None: 
        sql += f"`capital`=`{worldItem.capital}`, "
    
    if worldItem.tld != None: 
        sql += f"`tld`=`{worldItem.tld}`, "

    if worldItem.flag != None: 
        sql += f"`flag`=`{worldItem.flag}`, "

    sql += f"WHERE `id`=`{worldItem.id}`"
    print(sql)
    res = cnx.query(sql)
    return worldItem



#post data to teachers table
@app.post("/teachItem/")
async def create_item(teachItem: TeachItem):
    sql = f"""
    INSERT INTO 'teacher' (`id`,`dept`, `phone`,`mobile`)
    VALUES ('{teachItem.id}','{teachItem.dept}','{teachItem.phone}','{teachItem.mobile}')
     """       
    res = cnx.query(sql)
    return res


