#!/usr/bin/python3
# Given input as a series of rows of columnular data, determine row "safety"
# A row is safe IFF:
#   1) All column values either INCREASE or DECREASE
#   2) Consecutive values within a report differ by 1 <= x <= 3
import os

#datafile="/data/day2test.txt"
datafile="/data/day2data.txt"


#-----------------------------------------------------------------------
def cromulentAbs(x,y) :
    diff = abs(x-y)
    if diff > 0 and diff < 4 :
        return True
    else :
        return False

#-----------------------------------------------------------------------
def isSafeReport(reportline) :
    repval = reportline.split()
        
    #We first have to work out whether we're looking at INCR or DECR
    #for which we need the first two values
    incrRep = True
    v0 = int(repval.pop(0))
    v = int(repval.pop(0))
    if (v == v0) or not cromulentAbs(v,v0) :
        return False # Values can't be the same OR differ by more than the max delta
    elif v < v0 :
        incrRep = False # values must decrement from here on
    
    v0 = v
    for v in repval:
        v = int(v)
        if incrRep and v < v0:
            return False
        if not incrRep and v > v0:
            return False
        if not cromulentAbs(v,v0):
            return False
        v0 = v
    
    return True


#-----------------------------------------------------------------------
if __name__ == "__main__" :
    safecount=0
    with open(os.getcwd() + datafile, 'r') as allreports:
        for report in allreports:
            sc=isSafeReport(report.strip())
            print(f"{sc} :   {report.strip()}")
            safecount += sc


    print(f"Safe Report Count:  {safecount}")