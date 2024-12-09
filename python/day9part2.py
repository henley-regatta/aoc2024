#!/usr/bin/python3
# DAY 9 PART 2 -DISK DEFRAGMENTER - ACTUAL DEFRAGMENTER NOT ULTRAFRAGMENTER
# INPUT: 
#    A sequence of numbers in format [fileBlocks,freeBlocks]
# (IMPLICIT: Each file (odd-number) has an ID number sequencially incrementing, starting from 0)
# 
# THIS TIME, move the file with the highest ID (i.e. the last) to the leftmost position with 
# sufficient free space. Skip any files that cannot be moved according to this rule. Only whole
# files get moved in 1 fell swoop.
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
        elif dMap[x]>9 :
            d = d + '#'
        else :
            d = d + str(dMap[x])
    print(d)

#
#-----------------------------------------------------------------------
def buildDiskMap(fmap) :
    #Rebuild the disk map based on the new file positions. Note that we can't assume
    #the LAST file in the list has the LARGEST start position....
    maxStart=0
    lastFPos=0
    for f in fmap :
        if f[0]>maxStart :
            maxStart=f[0]
            lastFPos=maxStart+f[1]
    diskMap = array.array('i',(-1 for i in range(0,lastFPos)))
    #initialise the diskMap
    for i in (range(len(fmap))) :
        for x in range(fmap[i][1]) :
            diskMap[fmap[i][0]+x] = i
    return diskMap

# in part 2 we need to check the whole falloc table
#-----------------------------------------------------------------------
def calcChecksum(fmap) :
    cs=0
    for f in range(len(fmap)) :
        s=fmap[f][0]
        for i in range(fmap[f][1]) :
            cs = cs + ((s+i) * f)
    return cs

#-----------------------------------------------------------------------
def checkDiskDisksum(diskMap) :
    cs=0
    for i in range(len(diskMap)) :
        if diskMap[i]>0 :
            cs = cs + (i * diskMap[i])
    return cs

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #today's input is a single line, consisting of pair-sequences, which 
    #we can immediately parse into {id,startpos,length} as long as we track
    #the free space. Luckily everything's single-digit.
    fmap=[]
    smap=[] # part 2 requires us to track free space too.

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
                    smap.append([sBlock,v])
                    inFree=False
                sBlock+=v

    takenSpace=0
    for f in fmap :
        takenSpace += f[1]
    freeSpace=0
    for s in smap :
        freeSpace += s[1]
    #build the initial disk map as empty:
    diskMap = buildDiskMap(fmap)
    print(f"Disk contains {len(fmap)} files taking {takenSpace} over {len(diskMap)} total space, leaving {freeSpace} free")
    if(len(diskMap)<256) :
        drawDisk(diskMap)

    #OK SO HERE WE GO
    #algorithm says take the LAST file and move it to the LEFTMOST free block that can accommodate it.
    #The only real challenge is that we need to upgdate the free space after every file move:
    fPtr = len(fmap)-1 #the file to move
    fFreeBlock = smap[0][0]
    while fPtr >= 0 :
        fLen=fmap[fPtr][1]
        #print(f"Moving file {fPtr} of length {fLen} from start {fmap[fPtr][0]}; {len(smap)} free chunks remain")
        for c in range(0,len(smap)-1) :
            if fLen <= smap[c][1] and smap[c][0] < fmap[fPtr][0]:
                #print(f"moving id {fPtr} to sblock {c} at {smap[c][0]}")
                #change start position for file to start of space block
                fmap[fPtr][0] = smap[c][0]
                #how much free space does that leave?
                sLen = smap[c][1] - fmap[fPtr][1]
                if sLen == 0 :
                    #remove the free block from the list completely
                    del smap[c]
                else :
                    #update start position of free block
                    sStrt = smap[c][0] + fmap[fPtr][1]
                    smap[c][0] = sStrt
                    smap[c][1] = sLen
                break # the file is moved, move on
        #move fFreeBlock position
        fFreeBlock = smap[0][0]
        #and decrement fptr counter:
        fPtr -= 1
        if(len(diskMap)<256) :
            drawDisk(buildDiskMap(fmap))

    #rebuild the disk map
    diskMap = buildDiskMap(fmap)
    drawDisk(diskMap)
    print(f"Part Two Answer is thus: {calcChecksum(fmap)}")
    print(f"Or if you prefer it fully enumerated: {checkDiskDisksum(diskMap)}")