#!/usr/bin/env python
# Author: Imran Akbar (imran@osg.stanford.edu)
# Created: 1/24/2012

'''
Description of Problem:
Print for him a path, consisting of a list of positions, starting anywhere in the nucleus, where:
Each position is empty
Each successive position is only 1 nm away from the one before it
The path passes through each position in the nucleus at most once
The number of positions visited is equal to the length of Danny Dendrite's genome (the starting and ending positions both count).
If no path exists, just print "impossible".
Sample Input file:
5 4 8
oxoo
xoxo
ooxo
xooo
oxox
Sample Output:
1,1
2,1
3,1
3,2
3,3
2,3
1,3
0,3
'''

import sys
# could have used a NumPy matrix here, but for compatibility just use lists
# Grid coords start at 0,0 and follow matrix notation
grid=[]
currentPath = [] # stores row, column of visited nodes

def readFile():
    try:
        file = open('membrane_input.txt','r')
        lines = file.readlines()
        file.close()
        global grid
        arguments = lines.pop(0).strip('\n').split(" ")
        for line in lines:
            grid.append(list(line.strip('\n')))
        return [int(x) for x in arguments] # casts strings to integers
    except:
        print "Error reading from file"

def squareStatus(row,column,state,rows,columns):
    if column>=columns or row>=rows or row<0 or column<0: # out of bounds
        return False
    else:
        if grid[row][column]=="o": # free
            return True if state=="free" else False
        elif grid[row][column]=="x": # occupied
            return False if state=="free" else True
        else: # invalid data
            raise Exception

def traversal(start_row, start_column, rows, columns, length): # tries different starting positions
    while start_column<columns:
        start_row = 0 # reset
        while start_row<rows:
            result = testPosition(start_row,start_column,length,rows,columns)
            if result==True:
                return True
            elif result==False:
                backTrack(start_row,start_column,rows,columns)
            # otherwise, keep searching
            start_row += 1
        start_column += 1
    return False # if done searching, return impossible

def testPosition(row,column,length,rows,columns):
    if squareStatus(row,column,"free",rows,columns): # possible starting point
        currentPath.append([row,column]) # add to path
        grid[row][column] = "x" # mark as visited
        if length==1:
            return True
        else: # start recursion on nearest neighbors
            result = testPosition(row+1,column,length-1,rows,columns)
            if result==True:
                return True
            elif result==False:
                backTrack(row+1,column,rows,columns)
            result = testPosition(row-1,column,length-1,rows,columns)
            if result==True:
                return True
            elif result==False:
                backTrack(row-1,column,rows,columns)
            result = testPosition(row,column+1,length-1,rows,columns)
            if result==True:
                return True
            elif result==False:
                backTrack(row,column+1,rows,columns)
            result = testPosition(row,column-1,length-1,rows,columns)
            if result==True:
                return True
            elif result==False:
                backTrack(row,column-1,rows,columns)
            return False # couldn't find any path
    else: # already occupied or out of bounds
        return "invalid" # different from False, so you know when to backtrack
    
def backTrack(row,column,rows,columns):
    if squareStatus(row,column,"occupied",rows,columns): # is NOT out of bounds, and IS occupied
        currentPath.pop() # remove last visited node from path
        grid[row][column] = "o" # UNmark as visited

def printPath():
    for coord in currentPath:
        print str(coord[0]) + "," + str(coord[1])

def main():
    rows, columns, length = readFile()
    if traversal(0,0,rows, columns, length)==True:
        printPath() 
    else:
        print "impossible"

if __name__ == '__main__':
    main()
    sys.exit()