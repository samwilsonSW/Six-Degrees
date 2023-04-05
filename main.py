import json
import re

moviesList = [] #precursor for the list of json objects fetched through other functions
testList = [{"title":"Manhatta","cast":['Morgan Freeman'],"directors":["[[Charles Sheeler]]","[[Paul Strand]]"],"year":1921},
{"title":"something","cast":[],"directors":["[[Charles Sheeler]]","[[Paul Strand]]"],"year":1921},
{"title":"some","cast":[],"directors":["[[Charles Sheeler]]","[[Paul Strand]]"],"year":1921}] #test list to test functions in a smaller way

with open('data.txt') as f:
    for jsonObj in f:
        movieDict = json.loads(jsonObj)  #Makes the json file "data.txt" readable for Python
        moviesList.append(movieDict)     #Appends all json objects to the moviesList array
        
"""
    NAME:       newNode
    PURPOSE:    The newNode class contains all the innerworkings of what a node for a tree needs
    INVARIANTS: A node has data and a pointer to the left and right node
"""

class newNode:
    def __init__(self,data):
        self.data = data
        self.left = self.right = None

"""
    NAME:           userInput
    PARAMETERS:     None
    PURPOSE:        To take an actor's name and return it
    PRECONDITION:   User should run the program
    POSTCONDITION:  Return the user's input
"""
        
def userInput():
    actor = input("Which actor do you want to connect Kevin Bacon to? ")
    return actor

"""
    NAME:           createTree
    PARAMETERS:     arr is an array of all movies and cast members, i is the incrementer of the tree, n is the length of the original array
    PURPOSE:        To create a tree based on an array
    PRECONDITION:   arr should be full of movies from the json file
    POSTCONDITION:  return root, which should contain all of the movies sorted by order of the json file
"""
        
def createTree(arr,i,n):
    root = None

    if i<n:

        root = newNode(arr[i])

        root.left = createTree(arr,2 * i + 1,n)
        
        root.right = createTree(arr,2 * i + 2,n)

    return root

"""
    NAME:           searchTree
    PARAMETERS:     root, the entire tree of all movies. 
                    Actor is the specified actor (Kevin Bacon and the user inputted actor).
                    Arr is the array of movie objects
    PURPOSE:        To search the tree for a valid actor and build an array of the movies the actor is in
    PRECONDITION:   The root should contain the tree, actor should be the specified actor, and array should be empty
    POSTCONDITION:  The arr should be full of all movies of actor
"""

def searchTree(root,actor,arr):
    if(root != None):
        
        for castMember in root.data['cast']:
            castMember = re.sub(r"[\[\]]",'',castMember)
            if(castMember == actor):
                arr.append(root)
        
        searchTree(root.left,actor,arr)
        searchTree(root.right,actor,arr)
    return arr

"""
    NAME:           findHeight
    PARAMETERS:     root, the tree starting at the specified movie
    PURPOSE:        To find the height of said node.
    PRECONDITION:   The root should start on the specified movie of an actor
    POSTCONDITION:  The function should return an integer of the max height between right and left
"""


def findHeight(root):
    if root is None:
        return 0
    leftHeight = findHeight(root.left)
    rightHeight = findHeight(root.right)
    return max(leftHeight,rightHeight) + 1

"""
    NAME:           findHeightOfAllMovies
    PARAMETERS:     arr, list of nodes that contains movies of a certain actor
    PURPOSE:        To return an array of heights of all movies passed by array
    PRECONDITION:   The array should be full of movie nodes 
    POSTCONDITION:  The heightArray should be full of integers representing the heights of certain movies
"""

def findHeightOfAllMovies(arr):
    heightArray = []
    for node in arr:
        root = node
        heightArray.append(findHeight(root))
    return heightArray
        


"""
    AUTHOR:        Jacob Bartlett, Sam Wilson
    FILENAME:      main.py 
    SPECIFICATION: Find distance between two nodes (actors), should return the Bacon number (distance)
    FOR:           CS 3368 Introduction to Artificial Intelligence Section 001
"""

def main():
    root = None
    root = createTree(moviesList,0,len(moviesList))
    actor= userInput()
    arr1 = []
    arr2 = []
    arr1 = searchTree(root,'Kevin Bacon', arr1)
    arr2 = searchTree(root,actor,arr2)

    heightArray = []
    heightArray = findHeightOfAllMovies(arr1)
   
    heightArray2 = []
    heightArray2 = findHeightOfAllMovies(arr2)

    print('Bacon Number = ' + str(min(heightArray) + min(heightArray2)))
    
    

if __name__ == "__main__":
    main()
