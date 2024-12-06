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
#
# THREADED approach for some speed up
# BASELINE (unthreaded) version takes 9m47
# ProcessPoolExecutor:
#   SIMPLEX (per-test) threaded with n=32, s=1       takes 1m33s (6.3x speedup)
#   SLICED  (chunked tests) threaded with n=32, s=50 takes 1.29s (6.5x speedup)
# ThreadPoolExecutor:
#   SIMPLEX (per-test) threaded with n=32, s=1       takes 14m47s (0.66x speedup :-()
#   SLICED  (chunked tests) threaded with n=32, s=50 takes 15m32  (0.6x speedup :-()

# NOTE: t'Internets has it that Enum is slow but Sets are fast. Experience removing
#       Enum and replacing with String comparison doesn't bear that out (marginal improvement)

import os
import sys
#from enum import Enum
import copy # bitten in the backside by the difference between shallow/deep copies

import concurrent.futures
numThreads = 32
sliceSize = 50

testfile="/data/day6test1.txt"
datafile="/data/day6data.txt"

#strictly this ain't just direction any more
#but eh
#class direction(Enum) :
#    EMPTY = 0
#    NORTH = 1
#    EAST = 2
#    SOUTH = 4
#    WEST = 8
#    BLOCKED = 16
#    STARTPOINT = 32

#there's a mathematical function for this but I don't brain too good 
#these days so IF statement it is
#-----------------------------------------------------------------------
def rotate90right(idir) : # remember we're using [Y,X]
    if idir == 'N' :
        return 'E'
    elif idir == 'E' :
        return 'S'
    elif idir == 'S' :
        return 'W'
    elif idir == 'W' :
        return 'N'
    else :
        print(f"Invalid original direction {idir}")
        exit()

#need a helper now we're using enums
#-----------------------------------------------------------------------
def nextPosGuard(gpos,gdir) :
    if gdir == 'N' :
        return([gpos[0]-1,gpos[1]])
    elif gdir == 'E' :
        return([gpos[0],gpos[1]+1])
    elif gdir == 'S' :
        return([gpos[0]+1,gpos[1]])
    elif gdir == 'W' :
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
    while inBounds(cPos,gdim) and 'B' in gmap[cPos[0]][cPos[1]]:
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
    notvisited = {'U','B'}
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
            if 'U' in c :
                line += '.'
            elif 'B' in c:
                line += '#'
            elif 'E' not in c and'W' not in c:
                line += '|'
            elif 'N' not in c and 'S' not in c:
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
        wmap[gpos[0]][gpos[1]].discard('U') # don't use REMOVE, it fails if not exists
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

# async thread executor
#-----------------------------------------------------------------------
def checkObstructions(orgmap,mapdim,gpos,gdir,obsList) :
    goodblockers=[]
    for obs in obsList :
        tmap = copy.deepcopy(orgmap)
        tmap[obs[0]][obs[1]].discard('U')
        tmap[obs[0]][obs[1]].add('B')
        (tested,looped) = driveGuardToCompletion(tmap,mapdim,gpos,gdir)
        if looped :
            goodblockers.append(obs)
    return(goodblockers)


#-----------------------------------------------------------------------
if __name__ == "__main__" :
    # Today's data structure is a simple X-by-Y grid, or 2d array if you
    # prefer. Because we need to track metadata about visitation this will
    # be a 2d array of SETs of ENUMs
    guardmap=[]
    #We're told our starting direction is North (-y)
    #NOTE we specify as [Y,X] because that's how the map data looks
    guarddir='N'
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
                    p.add('U')
                elif r == '#' :
                    p.add('B')
                elif r == '^' :
                    #we found the start position
                    p.add('X')
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
 
    # NOW WE GET CLEVER: We need to test for loops by adding obstructions to the original map
    # Naieve = try every point on the map. 
    # Better = try every point VISITED IN THE ORGINAL WALK because we don't have to worry about
    #          combinatorial multi-obstructions, just adding one. RESTRICTION: Not the start point
    # (clearly *not* the "Best" solution, as it still takes ~15 mins to run on the prod. dataset)
    visited = { 'N','E','S','W' }
    foundBlockers = []
    checkedpos = 0
    tocheck = []
    for r in range(len(orgmovements)) :
        for c in range(len(orgmovements[r])) :
            t = orgmovements[r][c]
            if 'X' not in t and not t.isdisjoint(visited) :
                tocheck.append([r,c])
                
    print(f"We have {len(tocheck)} positions to check for looping")
    checkedSlices=[]
    cSCount = 0
    checkSlices=[tocheck[i:i+sliceSize] for i in range(0,len(tocheck),sliceSize)]
    print(f"(checking as {len(checkSlices)} slices of {sliceSize} candidates)")
    with concurrent.futures.ProcessPoolExecutor(max_workers=numThreads) as executor:
        future_to_checkedObs = {executor.submit(checkObstructions,guardmap,mapdim,guardpos,guarddir,obs) : obs for obs in checkSlices}
        for future in concurrent.futures.as_completed(future_to_checkedObs) :
            s = future_to_checkedObs[future]
            cSCount += sliceSize
            try :
                res = future.result()
            except Exception as exc:
                print(f"{s} Something went wrong with threading: {exc}")
                exit()
            else :
                if res is not None and len(res)>0:
                    checkedSlices = checkedSlices + res
                    print(f"{len(res)} blockers in slice ({cSCount / len(tocheck):.1%} complete)")
    #At this point we've got our answer, it's just the length of checkedSlices
    print(f"After all that there were {len(checkedSlices)} blocking positions")
            
    