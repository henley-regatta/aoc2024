#!/usr/bin/python3
# GUARD PATH - LOOP INDUCEMENT
#
# Find the total number of solutions where adding ONE obstacle causes the guard to loop.
# 
# Given a "sparse" input map consisting of "." space, "#" obstacles and "^" guard start
# position, calculate the number of positions on the map that the guard visits before leaving
# the map completely. This includes the starting position.
# The guard obeys the following behaviour:
#   1) If there is something in front of the guard, turn right 90 degrees
#   2) Otherwise take a step forward.

import os
import sys
from enum import Enum
import copy # bitten in the backside by the difference between shallow/deep copies

testfile="/data/day6test1.txt"
datafile="/data/day6data.txt"

#strictly this ain't just direction any more
#but eh
class direction(Enum) :
    EMPTY = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    BLOCKED = 16
    STARTPOINT = 32

#there's a mathematical function for this but I don't brain too good 
#these days so IF statement it is
#-----------------------------------------------------------------------
def rotate90right(idir) : # remember we're using [Y,X]
    if idir == direction.NORTH :
        return direction.EAST
    elif idir == direction.EAST :
        return direction.SOUTH
    elif idir == direction.SOUTH :
        return direction.WEST
    elif idir == direction.WEST :
        return direction.NORTH
    else :
        print(f"Invalid original direction {idir}")
        exit()

#need a helper now we're using enums
#-----------------------------------------------------------------------
def nextPosGuard(gpos,gdir) :
    if gdir == direction.NORTH :
        return([gpos[0]-1,gpos[1]])
    elif gdir == direction.EAST :
        return([gpos[0],gpos[1]+1])
    elif gdir == direction.SOUTH :
        return([gpos[0]+1,gpos[1]])
    elif gdir == direction.WEST :
        return([gpos[0],gpos[1]-1])
    else :
        print(f"Invalid MOVEMENT direction {gdir}")
        exit()


#core function, like. Move the guard according to the rules. Report new
#position
#-----------------------------------------------------------------------
def moveGuard(gmap,gdim,gpos,gdir) :
    cPos=nextPosGuard(gpos,gdir)
    #Collisions can loop, so we need to adjust accordingly
    #(although to be fair they can only loop twice....)
    while inBounds(cPos,gdim) and direction.BLOCKED in gmap[cPos[0]][cPos[1]]:
        gdir = rotate90right(gdir)
        cPos = nextPosGuard(gpos,gdir)
    return([cPos,gdir])

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
    notvisited = {direction.EMPTY,direction.BLOCKED}
    for r in gmap :
        for c in r:
            if not c.intersection(notvisited) :
                v+=1
    return v


#we like a utility function
#-----------------------------------------------------------------------
def drawMap(gmap) :
    for r in gmap :
        line=''
        for c in r :
            if direction.EMPTY in c :
                line += '.'
            elif direction.BLOCKED in c:
                line += '#'
            elif direction.EAST not in c and direction.WEST not in c:
                line += '|'
            elif direction.NORTH not in c and direction.SOUTH not in c:
                line += '-'
            else :
                line += '+'
        print(line)
        

#drive the map to completion
#-----------------------------------------------------------------------
def driveGuardToCompletion(gmap,gdim,gpos,gdir) :
    mCount = 0
    wmap = copy.deepcopy(gmap)
    while inBounds(gpos,gdim) :
        #add current pos/dir to wmap:
        opos = gpos.copy()
        odir = gdir
        wmap[gpos[0]][gpos[1]].discard(direction.EMPTY) # don't use REMOVE, it fails if not exists
        wmap[gpos[0]][gpos[1]].add(gdir)
        (gpos,gdir) = moveGuard(wmap,gdim,gpos,gdir)
        #if we changed direction, add that to the original position 
        if gdir != odir :
            wmap[opos[0]][opos[1]].add(gdir)
        #check for a loop = we've been here before, in this direction
        if inBounds(gpos,gdim) and gdir in wmap[gpos[0]][gpos[1]] :
            looped = True
            return (wmap,True)

    return(wmap,False)

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    # Today's data structure is a simple X-by-Y grid, or 2d array if you
    # prefer. Because we need to track metadata about visitation this will
    # be a 2d array of SETs of ENUMs
    guardmap=[]
    #We're told our starting direction is North (-y)
    #NOTE we specify as [Y,X] because that's how the map data looks
    guarddir=direction.NORTH
    guardpos=[-1,-1] #we'll look for this as we read in
    
    df = os.getcwd() + testfile
    if len(sys.argv)>1 and sys.argv[1] == 'p' :
        df = os.getcwd() + datafile
    
    #Part 2- our needs are different. 
    with open(df, 'r') as n:
        for l in n:
            rList = list(l.strip())
            #convert each position to set based on read status
            row = []
            for r in rList :
                p = set()
                if r == '.' :
                    p.add(direction.EMPTY)
                elif r == '#' :
                    p.add(direction.BLOCKED)
                elif r == '^' :
                    #we found the start position
                    p.add(direction.STARTPOINT)
                    guardpos=[len(guardmap),len(row)]
                else :
                    print(f"Invalid char in input: {r}")
                row.append(p)
            guardmap.append(row)
    mapdim=[len(guardmap)-1,len(guardmap[0])-1] #we'll use this over and over
    print(f"Map is [Y,X] = {mapdim}")
    print(f"Guard starts at {guardpos}")
    
    #FIRST ITERATION: we need to find all the locations the guard visits, as
    #this constrains the number of positions we COULD place an obstruction
    # HOWEVER - for later loop detection we need to record the DIRECTION
    # the guard was traveling as they visited the square, noting that this
    # could be >1
    (orgmovements,blocked) = driveGuardToCompletion(guardmap,mapdim,guardpos,guarddir)
    if blocked :
        print("error in testing - original check failed with blocked")
    #drawMap(orgmovements)
    #we can't block the origin
    tocheck = countVisited(orgmovements)-1
    print(f"Total Visited Positions to check for adding obstructions: {tocheck}")
    # NOW WE GET CLEVER: We need to test for loops by adding obstructions to the original map
    # Naieve = try every point on the map. 
    # Better = try every point VISITED IN THE ORGINAL WALK because we don't have to worry about
    #          combinatorial multi-obstructions, just adding one. RESTRICTION: Not the start point
    # (clearly *not* the "Best" solution, as it still takes ~15 mins to run on the prod. dataset)
    visited = { direction.NORTH, direction.EAST, direction.SOUTH, direction.WEST}
    foundBlockers = []
    checkedpos = 0
    for r in range(len(orgmovements)) :
        for c in range(len(orgmovements[r])) :
            t = orgmovements[r][c]
            if direction.STARTPOINT not in t and not t.isdisjoint(visited) :
                checkedpos += 1
                tmap = copy.deepcopy(guardmap)
                tmap[r][c].discard(direction.EMPTY)
                tmap[r][c].add(direction.BLOCKED)
                (tested,looped) = driveGuardToCompletion(tmap,mapdim,guardpos,guarddir)
                if looped :
                    foundBlockers.append([r,c])
                    print(f"obstruction at {[r,c]} loops ({checkedpos/tocheck:.1%} complete)")
                     
    print(f"After all that, found {len(foundBlockers)} locations that block guard")
            
    