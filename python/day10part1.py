#!/usr/bin/python3
# DAY 10 PART 1 - HOOF IT
# Given an input map of spot-heights. plot the LONGEST, EVEN, GRADUAL UPHILL hike
#  - Start at 0 
#  - End at 9
#  - Increase Height by 1 per step
#  - Move only Vertically or Horizontally
#
# Trail's score is the number of 9-height positions accessible from a 0-rated start point

import os
import sys

testfile="/data/day10test1.txt"
t2file="/data/day10test2.txt"
t3file="/data/day10test3.txt"
datafile="/data/day10data.txt"


#simple "are we still on the map" check
#-----------------------------------------------------------------------
def inBounds(pos,mapDim) :
    if pos[0]<0 or pos[0]>mapDim[0] :
        return False
    if pos[1]<0 or pos[1]>mapDim[1] :
        return False
    return True

#core of the wotsit here, a recursive algo. Return the sum of the paths
#to 9 from current position, depth-first search
#-----------------------------------------------------------------------
def findPathsFromPosition(topomap,mapDim,pos) :
    pVal = topomap[pos[0]][pos[1]] 
    #print(f"{pos} ({pVal})", end=' ')
    if pVal == 9 :
        #print("summit!")
        return [pos] # we got here!
    #Valid next moves are in-bounds horizontal,vertical where the number
    #increments by one
    up=[pos[0]-1,pos[1]]
    down=[pos[0]+1,pos[1]]
    left=[pos[0],pos[1]-1]
    right=[pos[0],pos[1]+1]
    moves=[up,down,left,right]
    vmoves=[]
    summitsFromHere=[]
    for m in moves:
        if inBounds(m,mapDim) and topomap[m[0]][m[1]] == (pVal+1) :
            vmoves.append(m)
    #print(f"{len(vmoves)} moves ({vmoves})")
    if len(vmoves)==0 :
        #we're stuck
        #print("stuck")
        return None
    else :
        for m in vmoves:
            summits = findPathsFromPosition(topomap,mapDim,m)
            if summits is not None :
                for s in summits :
                    summitsFromHere.append(s)
    return summitsFromHere

#-----------------------------------------------------------------------
def dedupSummits(summits) :
    dedup = []
    for s in summits:
        if s not in dedup :
            dedup.append(s)
    return dedup

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    
    df = os.getcwd() + testfile
    if len(sys.argv)>1 :
        if sys.argv[1] == 'p' :
            df = os.getcwd() + datafile
        elif sys.argv[1] == '2' :
            df = os.getcwd() + t2file
        elif sys.argv[1] == '3' :
            df = os.getcwd() + t3file
            
    # Today's data is a "map" of spot-heights from 0 to 9
    # So our data structure is a 2d list. 
    # To make later scanning easier, as we read in we'll capture all
    # 0-heights as starting points
    topomap=[]
    trailheads=[]
    with open(df, 'r') as n:
        for l in n:
            r=list(l.strip())
            row=[]
            for c in r :
                if c == '.' :
                    v = -1
                else :
                    v=int(c)
                row.append(v)
                if v == 0 :
                    trailheads.append([len(topomap),len(row)-1])
            topomap.append(row)
    print(f"Read a map of {len(topomap[0])} by {len(topomap)} containing {len(trailheads)} trailheads")
    mapDim=[len(topomap)-1, len(topomap[0])-1]
    sumTrails = 0
    for t in trailheads:
        summits = dedupSummits(findPathsFromPosition(topomap,mapDim,t))
        tCount = len(summits)
        print(f"Start point {t} has {tCount} valid trails ending at {summits}")
        sumTrails += tCount
    print(f"PART ONE ANSWER is therefore {sumTrails}")