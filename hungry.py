#!/usr/bin/env python
# Author: Imran Akbar (imran@osg.stanford.edu)
# Created: 1/25/2012

'''
optimization problem (assignment problem)
enter in a sample N*M matrix, where M>N
N engineers, M lunches
values in the matrix correspond to N's enjoyment value M
allocate M to N in order to maximize enjoyment
this implementation uses the Hungarian algorithm (http://en.wikipedia.org/wiki/Hungarian_algorithm)
as implemented by Munkres (http://software.clapper.org/munkres/)
'''

import sys
from munkres import Munkres, print_matrix, make_cost_matrix
matrix = []

def readFile():
    try:
        file = open('hungry_input.txt','r')
        lines = file.readlines()
        file.close()
        # rows are enginers, columns are lunches
        global matrix
        for line in lines:
            row = list(line.strip('\n').split(" "))
            matrix.append([int(x) for x in row]) # casts strings to integers
    except:
        print "Error reading from file"
        
def optimizeMatrix():
    cost_matrix = make_cost_matrix(matrix, lambda cost: sys.maxint - cost)
    m = Munkres()
    indexes = m.compute(cost_matrix)
    return indexes

def printResult(indexes):
    print_matrix(matrix, msg="Optimal allocation of lunches to engineers for this matrix:")
    print "is:"
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        print "Engineer %d chooses Lunch %d with Enjoyment %d" % (row, column, value)
    print "Total enjoyment is %d" % total
    
def main():
    readFile()
    indexes = optimizeMatrix()
    printResult(indexes)

if __name__ == '__main__':
    main()
    sys.exit()