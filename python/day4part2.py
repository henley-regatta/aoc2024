#!/usr/bin/python3
# X-MAS Word Search
# Find ALL instances of the X-grid:
#       M.S  S.M  M.M  
#       .A.  .A.  .A.
#       M.S  S.M  S.S
# (and other permutations of M-A-S in an X-shape...)
# within a word grid. 
# There are 9 in the sample data
import os

#datafile="/data/day4test1.txt"
datafile="/data/day4data.txt"
     

#quickscan: eliminate all start positions that are on the boundary of 
#the grid, they cannot be valid (and this simplifies the later match code too)
#-----------------------------------------------------------------------
def filter_bounds(maxX,maxY,cands) :
    stillcands=[]
    for c in cands:
        if c[0]>0 and c[0] < maxY and c[1]>0 and c[1] < maxX :
            stillcands.append(c)
    return stillcands

#The actual matcher. We can split this into 2 independent checks, 1 per 
#diagonal. This works because failure at any check invalidates the whole
#candidate
#-----------------------------------------------------------------------
def validate_candidate(grid,cand) :
    cX = cand[1]
    cY = cand[0]
    #TL-BR diagonal:
    if grid[cY-1][cX-1] != 'M' and grid[cY-1][cX-1] != 'S' :
        return False
    if grid[cY-1][cX-1] == 'M' and grid[cY+1][cX+1] != 'S' :
        return False
    if grid[cY-1][cX-1] == 'S' and grid[cY+1][cX+1] != 'M' :
        return False
    #BL-TR diagonal:
    if grid[cY+1][cX-1] != 'M' and grid[cY+1][cX-1] != 'S' :
        return False
    if grid[cY+1][cX-1] == 'M' and grid[cY-1][cX+1] != 'S' :
        return False
    if grid[cY+1][cX-1] == 'S' and grid[cY-1][cX+1] != 'M' :
        return False
    
    return True
    
    
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #our data structure du jour will be a 2x2 grid of letters. As we 
    #read in, we'll look for the positions of all A's 
    #as these are the possible middle-points of all M-A-S X's
    grid=[]
    Atuples=[]
    mascount=0
    with open(os.getcwd() + datafile, 'r') as n:
        for line in n:
            row=[]
            y = len(grid)
            for x in range(len(line.rstrip())) :
                row.append(line[x])
                if line[x] == 'A' :
                    Atuples.append([y,x])
            grid.append(row)
    print(f"{len(Atuples)} A's in the grid")
    candidates = filter_bounds(len(grid[0])-1,len(grid)-1,Atuples)
    print(f"{len(candidates)} not on grid boundary")
    for cand in candidates :
        if validate_candidate(grid,cand) :
            mascount+=1
    print(f"Found {mascount} total matches")