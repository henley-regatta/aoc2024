#!/usr/bin/python3
# DAY 8 PART 2 - RESONANT COLLINEARITY - RESONANT HARMONICS
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

#p2: we'll iterate over the deltas, just gimme the deltas
#-----------------------------------------------------------------------
def deltas(pair) :
    p0 = pair[0]
    p1 = pair[1]
    return([p1[0]-p0[0],p1[1]-p0[1]])
    
#-----------------------------------------------------------------------
def inbounds(p,bound) :
    if p[0]<0 or p[0] > bound[0] :
        return False
    if p[1]<0 or p[1] > bound[1] :
        return False
    return True

#iterate over the antinodes my dude
#-----------------------------------------------------------------------
def all_antinodes(antimap,mapdim,pair) :
    delta = deltas(pair)
    anode = pair[1]
    while inbounds(anode,mapdim) :
        antimap[anode[0]][anode[1]] = '#'
        anode = [anode[0]+delta[0], anode[1]+delta[1]]
    return(antimap)

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
            antinodes = all_antinodes(antinodes,mapDim,p)
    drawMap(antmap,antinodes)
    print(f"PART 2 ANSWER IS: {count_antinodes(antinodes)}")