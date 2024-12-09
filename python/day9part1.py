#!/usr/bin/python3
# DAY 9 PART 1 -DISK DEFRAGMENTER
# INPUT: 
#    A sequence of numbers in format [fileBlocks,freeBlocks]
# (IMPLICIT: Each file (odd-number) has an ID number sequencially incrementing, starting from 0)
# 
# Disk Defragmentation takes place by moving the RIGHTMOST file block to the LEFTMOST free space.
# This repeats until there is 1 long block of files with no space.
#
# After compaction, calculate the checksum by multiplying the POSITION by the FILEID and summing
# for each occupied block

import os
import sys

# look the disk is an array of integer ids why not use that ds?
import array

testfile="/data/day9test1.txt"
t2file  ="/data/day9test2.txt"
datafile="/data/day9data.txt"

#
#-----------------------------------------------------------------------
def drawDisk(dMap) :
    d=''
    for x in range(len(dMap)) :
        if dMap[x] == -1 :
            d = d + '.'
        else :
            d = d + str(dMap[x])
    print(d)


#
#-----------------------------------------------------------------------
def calcChecksum(diskMap,fullPtr) :
    cs=0
    for i in range(fullPtr) :
        cs = cs + (i * diskMap[i])
    return cs

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #today's input is a single line, consisting of pair-sequences, which 
    #we can immediately parse into {id,startpos,length} as long as we track
    #the free space. Luckily everything's single-digit.
    fmap=[]
    
    df = os.getcwd() + testfile
    if len(sys.argv)>1 :
        if sys.argv[1] == 'p' :
            df = os.getcwd() + datafile
        elif sys.argv[1] == '2' :
            df = os.getcwd() + t2file
   
    with open(df, 'r') as n:
        for l in n:
            l = l.strip();
            inFree=False
            sBlock=0
            for v in l :
                v = int(v)
                if not inFree :
                    fmap.append([sBlock,v])
                    inFree=True
                else :
                    inFree=False
                sBlock+=v

    takenSpace=0
    for f in fmap :
        takenSpace += f[1]
    #build the initial disk map as empty:
    diskMap = array.array('i',(-1 for i in range(0,fmap[len(fmap)-1][0]+fmap[len(fmap)-1][1])))
    #initialise the diskMap
    for i in (range(len(fmap))) :
        for x in range(fmap[i][1]) :
            diskMap[fmap[i][0]+x] = i
    
    print(f"Disk contains {len(fmap)} files taking {takenSpace} over {len(diskMap)} total space")
    if(len(diskMap)<256) :
        drawDisk(diskMap)

    #Bookkeepers:
    firstFree=fmap[0][1]
    lastTaken=fmap[len(fmap)-1][0]+fmap[len(fmap)-1][1]-1
    
    #now iterate over the diskmap until firstFree = takenSpace (i.e. we've compacted everything)
    iterCount=0
    while firstFree < takenSpace :
        diskMap[firstFree] = diskMap[lastTaken]
        diskMap[lastTaken] = -1
        #move lastTaken pointer back to next taken space
        lastTaken += -1
        while diskMap[lastTaken] == -1 :
            lastTaken +=  -1
        #move firstFree pointer forward to next free space
        firstFree += 1
        while diskMap[firstFree] != -1 :
            firstFree += 1
        if(len(diskMap)<256) :
            drawDisk(diskMap)
        iterCount += 1
    print(f"Compaction took {iterCount} iterations")
    print(f"Part One Answer is thus: {calcChecksum(diskMap,takenSpace)}")