#!/usr/bin/python3
# GUARD PATH
# Given a "sparse" input map consisting of "." space, "#" obstacles and "^" guard start
# position, calculate the number of positions on the map that the guard visits before leaving
# the map completely. This includes the starting position.
# The guard obeys the following behaviour:
#   1) If there is something in front of the guard, turn right 90 degrees
#   2) Otherwise take a step forward.

import os
import sys

testfile="/data/day6test1.txt"
datafile="/data/day6data.txt"



#there's a mathematical function for this but I don't brain too good 
#these days so IF statement it is
#-----------------------------------------------------------------------
def rotate90right(idir) : # remember we're using [Y,X]
    odir=[0,0]
    if idir == [-1,0] : # NORTH, go EAST
        odir = [0,1]
    elif idir == [0,1] : # EAST, go SOUTH
        odir = [1,0]
    elif idir == [1,0] : # SOUTH, go WEST
        odir = [0,-1]
    elif idir == [0,-1] : # WEST, go NORTH
        odir = [-1,0]
    else :
        print(f"Invalid original direction {idir}")
        exit()
    return odir

#core function, like. Move the guard according to the rules. Report new
#position
#-----------------------------------------------------------------------
def moveGuard(gmap,gdim,gpos,gdir) :
    cPos=[gpos[0]+gdir[0], gpos[1]+gdir[1]]
    #Collisions can loop, so we need to adjust accordingly
    #(although to be fair they can only loop twice....)
    while inBounds(cPos,gdim) and gmap[cPos[0]][cPos[1]] == "#" :
        gdir = rotate90right(gdir)
        cPos=[gpos[0]+gdir[0], gpos[1]+gdir[1]]
    return([cPos,gdir])

#we like a utility function
#-----------------------------------------------------------------------
def drawMap(gmap) :
    for r in gmap :
        print(''.join(r))

#just to keep the code clean-ish
#-----------------------------------------------------------------------
def inBounds(gpos,mapDim) :
    if gpos[0] < 0 or gpos[0] > mapDim[0] :
        return False
    elif gpos[1] < 0 or gpos[1] > mapDim[1] :
        return False
    else :
        return True


#there'll be quicker ways to do this I'm sure but this is fun, right?
#-----------------------------------------------------------------------
def countVisited(gmap) :
    v=0
    for r in gmap :
        for c in r:
            if c == "*" :
                v+=1
    return v


#-----------------------------------------------------------------------
if __name__ == "__main__" :
    # Today's data structure is a simple X-by-Y grid, or 2d array if you
    # prefer. For part one we will populate it with "#" for obstacles,
    # "." for unvisited locations and "*" for visited locations. 
    guardmap=[]
    #We're told our starting direction is North (-y)
    #NOTE we specify as [Y,X] because that's how the map data looks
    guarddir=[-1,0]
    guardpos=[-1,-1] #we'll look for this as we read in
    
    df = os.getcwd() + testfile
    if len(sys.argv)>1 and sys.argv[1] == 'p' :
        df = os.getcwd() + datafile
    
    print(df)
    with open(df, 'r') as n:
        for l in n:
            r = list(l.strip())
            #look for starting position in line as special case
            foundStart = l.find("^")
            if foundStart >-1 :
                #found it!
                guardpos=[len(guardmap),foundStart]
                print(f"Found the guard at {guardpos}")
                r[foundStart] = "*" # guard has already been here, after all
            guardmap.append(r)
    mapdim=[len(guardmap)-1,len(guardmap[0])-1] #we'll use this over and over
    print(f"Map is [Y,X] = {mapdim}")
    print(f"Guard starts at {guardpos}")
    drawMap(guardmap)
    mvCount=0
    while inBounds(guardpos,mapdim) :
        mvCount+=1
        guardmap[guardpos[0]][guardpos[1]] = "*" # mark location visited
        [guardpos,guarddir] = moveGuard(guardmap,mapdim,guardpos,guarddir)
        #print(f"{mvCount}, {guardpos}, {guarddir}")
        #drawMap(guardmap)
    
    print(f"Out of bounds after {mvCount} moves, final map:")
    drawMap(guardmap)
    print(f"Total Visited Positions: {countVisited(guardmap)}")
    