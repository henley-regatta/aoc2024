#!/usr/bin/python3
# XMAS Word Search
# Find ALL instances of the word XMAS written forwards, backwards, diagonally or vertically within
# a word grid. There are 18 in the sample data
import os

#datafile="/data/day4test1.txt"
datafile="/data/day4data.txt"

#From a given X-pos (start), return only the found valid S-pos
#-----------------------------------------------------------------------
def valid_endpos(grid,Xpos) :
    x = Xpos[1]
    y = Xpos[0]
    maxX=len(grid[0])-1
    maxY=len(grid)-1
    #there can be at most 8 of these
    spos = []
    #made up of these possibilities:
    cpos = [[y-3,x-3],[y-3,x],[y-3,x+3],[y,x-3],[y,x+3],[y+3,x-3],[y+3,x],[y+3,x+3]]
    for c in cpos:
        if c[0] >= 0 and c[0] <= maxY and c[1] >= 0 and c[1] <= maxX :
            if grid[c[0]][c[1]] == 'S' :
                spos.append([Xpos,c])
    return spos        

# Now we validate whether between the X and the S positions is an M and an
# A:
#-----------------------------------------------------------------------
def validate_match(grid,xpos,spos) :
    dX = spos[1] - xpos[1]
    if dX > 0 : 
        dX = 1
    elif dX < 0 :
        dX = -1
    dY = spos[0] - xpos[0]
    if dY > 0 :
        dY = 1
    elif dY < 0 :
        dY = -1
    #NB: the "else" case for both is dX/Y == 0 which is fine
    candMPos = [xpos[0]+dY,xpos[1]+dX]
    candAPos = [spos[0]-dY,spos[1]-dX]
    if (grid[candMPos[0]][candMPos[1]] == 'M' and
       grid[candAPos[0]][candAPos[1]] == 'A') :
           return True
    else :
        return False

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #our data structure du jour will be a 2x2 grid of letters. As we 
    #read in, we'll look for the positions of all X's and all S's
    #as these are the possible START and END points of XMAS
    wordgrid=[]
    xtuples=[]
    stuples=[]
    xmascount=0
    with open(os.getcwd() + datafile, 'r') as n:
        for line in n:
            row=[]
            y = len(wordgrid)
            for x in range(len(line.rstrip())) :
                row.append(line[x])
                if line[x] == 'X' :
                    xtuples.append([y,x])
                if line[x] == 'S' :
                    stuples.append([y,x])
            wordgrid.append(row)
    candidates=[]
    print(f"{len(xtuples)} X's and {len(stuples)} S's in the grid")
    for xcand in xtuples :
        candidates = candidates + valid_endpos(wordgrid,xcand)
    print(f"Checking {len(candidates)} candidate XMASes:")
    for cand in candidates :
        if validate_match(wordgrid,cand[0],cand[1]) :
            xmascount+=1
    print(f"Found {xmascount} total matches")