import json
import re
from typing import cast
import sys

sys.setrecursionlimit(100000000)

moviesList = []
actorDict = {}
movieDict = {}

testList = [{"title":"The Killer Must Kill Again","cast":["[[George Hilton (actor)|George Hilton]]","[[Antoine Saint-John]]","[[Femi Benussi]]","[[Cristina Galbó]]","[[Eduardo Fajardo]]","[[Tere Velázquez]]","[[Alessio Orano]]"],"directors":["[[Luigi Cozzi]]"],"producers":["Sergio Gobbi","[[Umberto Lenzi]] <small>(as Umberto Linzi)</small>","Giuseppe Tortorella"],"companies":["Albione Cinematografica","Git International Film","Paris-Cannes Productions"],"year":1975},
{"title":"Silent Action","cast":["[[Mel Ferrer]]","[[Brad Pitt]]","[[Tomas Milian]]","[[Luc Merenda]]","[[Michele Gammino]]","[[Paola Tedesco]]","[[Gianfranco Barra]]","Carlo Alighiero","[[Antonio Casale]]","Gianni Di Benedetto","[[Claudio Gora]]","[[Clara Colosimo]]","[[Arturo Dominici]]"],"directors":["[[Sergio Martino]]"],"producers":["[[Luciano Martino]]"],"companies":["Flora Film","Medusa Distribuzione","Medusa"],"year":1975},
{"title":"Manzil (1979 film)","cast":["[[Amitabh Bachchan]]","[[Moushumi Chatterjee]]","[[Rakesh Pandey]]","[[Satyen Kappu]]","[[Urmila Bhatt]]","[[Lalita Pawar]]","[[Shreeram Lagoo]]","[[A. K. Hangal]]","[[C. S. Dubey]]"],"directors":["[[Basu Chatterjee]]"],"producers":["Jai Pawar","Raj Prakash","Rajiv Suri"],"year":1979},
{"title":"Saajan Ki Baahon Mein","cast":["[[Rishi Kapoor]]","Sumeet Saigal","[[Raveena Tandon]]","[[Tabu (actress)|Tabu]]","[[Prem Chopra]]","[[Deven Verma]]","[[Laxmikant Berde]]","[[Pran (actor)|Pran]]","[[Saeed Jaffrey]]"],"directors":["Jay Prakash"],"producers":["Dinesh B. Patel"],"year":1995}]
def load():
    """
    Load given movie data into a list for manipulation
    """
    with open('data.txt') as f:
        for jsonObj in f:
            movieDict = json.loads(jsonObj)
            moviesList.append(movieDict)
    return moviesList

def createMovieDict():
    """
    Create simplified movie dictionary with cast as values 
    for computation in program
    """
    sampleDict = {}

    for movie in moviesList:
        tempList = []
        for i in range(0,len(movie['cast'])):
            actor = re.sub(r"[\[\]]",'',movie['cast'][i])
            tempList.append(actor)
        sampleDict[movie['title']] = tempList
    return sampleDict

def movieCount():
    """
    Get all actors from movies in data.txt file 
    then dump actor dictionary to actor_data.json file
    """
    
    for movie in moviesList:

            for i in range(0,len(movie['cast'])):
                
                actor = re.sub(r"[\[\]]",'',movie['cast'][i])

                if actor in actorDict.keys():
                    actorDict[actor].append(movie['title'])
                else:
                    actorDict[actor] = [movie['title']]

    json.dump(actorDict, open("actor_data.json", 'w'), indent=2)
    return actorDict

def findPath(actorDict,start,target,visited,path, depth=2):
    """
    Attempt at combined DFS and BFS search using depth limiter value - 
    only returns the first and last connection between the two,
    not the entire spanning tree.
    """
    if len(path) > depth:
       del path[:]
       start = og

    visited.append(start)
    for currMovie in actorDict[start]:
        #actors in the cast of the movies start is in
        for actor in movieDict[currMovie]:
            if(actor == target):
                path.append(currMovie)
                print(f"Degrees of separation: {len(path)}")
                print(f"Path Taken:  {path}")
                exit(0)
                
            elif(actor not in visited and currMovie not in path):
                path.append(currMovie)
                findPath(actorDict,actor,target,visited,path)

def findNeighbors(person_id):
    """ 
    Return a list of (movie, person) pairs to represent 
    movies as the edges connecting the actor nodes to each other.
    """
    movies_in = actorDict[person_id]
    neighbors = set()

    for mov in movies_in:
        cast = movieDict[mov]
        for actor in cast:
            neighbors.add((mov, actor))
    print(neighbors)
    return neighbors


def findShortest(current, target):
    """ 
    Proper algorithm to perform breadth first search - 
    Time consuming and costly as degrees of separation increase
    """
    explored = set([])
    frontier = [current]
    parents = {}

    while len(frontier) > 0:
        actor = frontier.pop(0)
        if actor == target:
            break
        explored.add(actor)

        for (m, a) in findNeighbors(actor):
            if not a in frontier and not a in explored:
                frontier.append(actor)
                parents[a] = (m, actor)
                if not target in parents:
                    return None
        if not target in parents:
            return None

def proper():
    """
    Function to run findShortest() with Paul Rudd as target
    """
    path = findShortest(og, target='Paul Rudd')
    if path is None:
        print("Not found")
    else:
        degrees_of_separation = len(path)
        print(f"{degrees_of_separation} degrees of separation.")
        print(path)

moviesList = load()
movieDict = createMovieDict()
actorDict = movieCount()
actorDictLength = (len(actorDict))



og = 'Kevin Bacon'
fg = input("Please enter the name of actor (not Kevin Bacon): ")

print()
print(f"The initial state is {og} and the final state is {fg}")
print()
print(findPath(actorDict,start=og, target=fg,visited=[],path = []))