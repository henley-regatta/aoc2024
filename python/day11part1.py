#!/usr/bin/python3
# DAY 11 PART 1 - PLUTONIAN PEBBLES
#
# A series of stones engraved with numbers undergo regular changes:
# - Stones with a 0 become 1
# - Stones with an EVEN NUMBER OF DIGITS become 2 stones. Left stone gets the left half of digits,
#   right stone gets the right half of digits, discarding zeros
# - Otherwise unmatching stones get replaced by one with the original number multiplied by 2024
#
# Stones remain in their existing sequence, when split the two stones occupy the original space. 
#
# nb: for part 1 the output doesn't actually need this condition. Bet it comes back to haunt me
#     in part 2 though
# Count the NUMBER of stones after 25 iterations.

import os
import sys

testfile="/data/day11test1.txt"
datafile="/data/day11data.txt"

#-----------------------------------------------------------------------
def iteratestones(inStones) :
    outStones={}
    for s in inStones:
        #The easy one (turn 0 into 1):
        if s == 0 :
            outStones = addToStones(outStones,1,inStones[s])
        #The hard one (split even-length):
        elif len(str(s)) % 2 == 0 :
            sStr=str(s)
            sLeft=sStr[:len(sStr)//2]
            sRight=sStr[len(sStr)//2:]
            #print(f"{sStr} -> {sLeft}, {sRight}")
            outStones = addToStones(outStones,int(sLeft),inStones[s])
            outStones = addToStones(outStones,int(sRight),inStones[s])
        #the default case
        else :
            outStones = addToStones(outStones,s*2024,inStones[s])
    return outStones

#-----------------------------------------------------------------------
def addToStones(stones,i,j) :
    if i in stones :
        stones[i] += j
    else :
        stones[i] = j
    return stones

#-----------------------------------------------------------------------
def sumStones(stones) :
    sumStones=0
    for s in stones :
        sumStones += stones[s]
    return sumStones

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    
    df = os.getcwd() + testfile
    if len(sys.argv)>1 :
        if sys.argv[1] == 'p' :
            df = os.getcwd() + datafile

    #Today's input is just a series of numbers. A list, if you will
    slist=[]
    with open(df, 'r') as n:
        for l in n:
            l.strip()
            slist=list(map(int,l.split()))
    #PART ONE optimisation: we only need to keep track of unique stone numbers
    # and their counts. So build T[initial]:
    stones={}
    for s in slist:
        stones[s]=1
    for x in range(25) :
        stones=iteratestones(stones)
    print(f"PART ONE ANSWER: {sumStones(stones)}")