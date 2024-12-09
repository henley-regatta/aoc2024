#!/usr/bin/python3
# DAY 8 PART 1 - RESONANT COLLINEARITY
#
# Given a map input of antennas at different "frequencies" (a digit or letter), find the
# "antinodes" where:
#   1) Antinodes occur between any 2 occurrences of the same "frequency"
#   2) They occur at a point where 1 antenna is 2x away from the other
#   3) They are constrained to occur only on the map
#
# Calculate the total number of unique positions wthin the bounds of the map containing
# an antinode

import os
import sys

#why write many code when short import work?
import itertools

testfile="/data/day8test1.txt"
t2file="/data/day8test2.txt"
t3file="/data/day8test3.txt"
datafile="/data/day8data.txt"

#by definition each coord pair DOES have an antinode whether it's inbounds or not
#-----------------------------------------------------------------------
def find_antinode(pair) :
    p0 = pair[0]
    p1 = pair[1]
    dX = p1[1] - p0[1]
    dY = p1[0] - p0[0]
    #According to the specification, the antinode is found by adding the deltas
    #to the p1 position
    a = [p1[0]+dY,p1[1]+dX]
    #print(f"p0 = {p0}, p1 = {p1}, delta = {[dY,dX]}, a = {a}")

    return(a)

#-----------------------------------------------------------------------
def inbounds(p,bound) :
    if p[0]<0 or p[0] > bound[0] :
        return False
    if p[1]<0 or p[1] > bound[1] :
        return False
    return True

# Calculate the answer, the sum of unique positions of antinodes on the map
#-----------------------------------------------------------------------
def count_antinodes(antimap) :
    anti=0
    for r in antimap :
        for c in r :
            if c == '#' :
                anti+=1
    return anti
    


# draw the map but preference antinodes over the top
#-----------------------------------------------------------------------
def drawMap(antmap,anti) :
    for r in range(len(antmap)) :
        row=''
        for c in range(len(antmap[r])) :
            if anti[r][c] == '#' :
                row += anti[r][c]
            else :
                row += antmap[r][c]
        print(f"{row}")

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #it's 2-d map time again
    antmap=[]
    #initialise the antinode overlay
    antinodes=[]
 
    #frequencies found and position
    frequencies={}
 
    df = os.getcwd() + testfile
    if len(sys.argv)>1 :
        if sys.argv[1] == 'p' :
            df = os.getcwd() + datafile
        elif sys.argv[1] == '2' :
            df = os.getcwd() + t2file
        elif sys.argv[1] == '3' :
            df = os.getcwd() + t3file
       
    with open(df, 'r') as n:
        for l in n:
            l = l.strip()
            row=[]
            ant=[]
            for c in l :
                row.append(c)
                ant.append('.')
                if c != '.' :
                    cpos=[len(antmap),len(row)-1]
                    if c not in frequencies :
                        frequencies[c] = [cpos]
                    else :
                        frequencies[c].append(cpos)
            antmap.append(row)
            antinodes.append(ant)
    #we'll need this for the constraints on antinodes
    mapDim = [len(antmap)-1,len(antmap[0])-1]
    #drawMap(antmap,antinodes)
    # For each FREQUENCY found, we need to work out the antinodes for
    # each PAIR of occurrences. This is another permutations problem...
    # NOTE: our generator creates both (A,B) and (B,A) which means we 
    #       can simplify our antinode locator to just find the antinode X->Y
    #       since it'll be called again to find Y->X anyway
    for f in frequencies :
        perm = list(itertools.permutations(frequencies[f],2)) # just the 2-pairs
        for p in perm :
            apos = find_antinode(p)
            if inbounds(apos,mapDim) :
                antinodes[apos[0]][apos[1]] = '#'
    drawMap(antmap,antinodes)
    print(f"PART 1 ANSWER IS: {count_antinodes(antinodes)}")