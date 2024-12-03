#!/usr/bin/python3
# Given input as 2 columns of numbers, sort EACH column smallest-largest, then for each pair calculate
# the difference and then return the SUM of the differences.
import os


#datafile="/data/day1test.txt"
datafile="/data/day1data.txt"


#-----------------------------------------------------------------------
if __name__ == "__main__" :
    lc = []
    rc = []
    with open(os.getcwd() + datafile, 'r') as n:
        for line in n:
            nStr = line.split()
            lc.append(int(nStr[0]))
            rc.append(int(nStr[1]))
    lc.sort()
    rc.sort()
    sumDiff=0
    if len(lc) != len(rc) :
        print(f"Error, lists ain't the same length")
    else :
        print(f"Comparing 2 lists of {len(rc)} numbers...")
    for i in range(len(lc)) :
        d = abs(lc[i] - rc[i])
        #print(f"l: {lc[i]} r: {rc[i]} d: {d}")
        sumDiff += d
    print(f"BIG ANSWER:   {sumDiff}")