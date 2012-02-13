#!/usr/bin/env python
# Author: Imran Akbar (imran@osg.stanford.edu)
# Created: 1/25/2012

'''
brute force algorithm would search for the substrings at every character in the source sequence
would have O(mn) complexity
more sophisticated algorithms include Boyer-Moore-Horspool, Boyer-Moore, and Knuth-Morris-Pratt
however, these algorithms work best for a single pattern/matching sequence
whereas we have multiple sequences that we need to match

for multiple sequences that we want to match, we should use one of the Aho-Corasick, Commentz-Walter, or Rabin-Karp algorithms
for better average running time
the existing library for Aho-Corasick won't work with a streaming input file not in memory
and Rabin-Karp is simpler, so let's implement that

adapted from sample implementations here:
http://courses.csail.mit.edu/6.006/spring08/keynotes/rolling_hash.py
https://github.com/laurentluce/python-algorithms/blob/master/algorithms/string_matching.py
'''

import sys
patternsToMatch = []

def readFile():
    try:
        file = open('genome_input.txt','r')
        parameters = map(int, file.readline().strip('\n').split(" ")) # k = number of sequences, m = length of each sequence, n = length genome
        # read in and store each sequence to be matched
        for i in range(parameters[0]):
            patternsToMatch.append(file.readline().strip('\n'))
        return [file, parameters]
    except:
        print "Error reading from file"

def computeHash(string, base):
    # example: if the string = "abc", value = (97 x base^2) + (98 x base^1) + (99 x base^0), where 97 is the ASCII value of a
    value = 0
    p = len(string)-1
    for i in range(p+1):
        value += ord(string[i]) * (base ** p) # ** is exponential (^)
        p -= 1
    return value
    
def stringMatch(pattern,textStream,m,n,hash_base=256):
    matchAtPositions = []
    homePosition = textStream.tell()
    htext = computeHash(textStream.read(m), hash_base) # will read m characters from the beginning of genome stream
    textStream.seek(homePosition) # go back to start of genome stream
    hpattern = computeHash(pattern, hash_base)
    for i in range(n-m+1):
        if htext == hpattern: # the hashes match
            textStream.seek(homePosition + i) # move to position in stream
            if textStream.read(m) == pattern: # verify that strings actually match (instead of a hash collision)
                matchAtPositions.append(i) # add this position to the results
        if i < n-m: # haven't reached the end yet
            textStream.seek(homePosition + i) # move to position in stream
            first_char = textStream.read(1)
            textStream.seek(homePosition + i + m) # move to position in stream
            last_char = textStream.read(1)
            htext = (hash_base * (htext - (ord(first_char) * (hash_base ** (m-1))))) + ord(last_char)
    if len(matchAtPositions)>0:
        print "Found pattern match at position(s):" + str(matchAtPositions)
    else:
        print "No matches found for pattern"
    textStream.seek(homePosition) # go back to start of genome stream, in case any further patterns need to be searched

def main():
    file, parameters = readFile()
    for pattern in patternsToMatch:
        print pattern
        stringMatch(pattern,file,parameters[1],parameters[2])
    file.close()

if __name__ == '__main__':
    main()
    sys.exit()