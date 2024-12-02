#!/usr/bin/python3
# Given input as a series of rows of columnular data, determine row "safety"
# A row is safe IFF:
#   1) All column values either INCREASE or DECREASE
#   2) Consecutive values within a report differ by 1 <= x <= 3
#   3) Conditions (1) and (2) can be met by removing AT MOST 1 value from the report
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
    #We first have to work out whether we're looking at INCR or DECR
    #for which we need the first two values
    incrRep = True
    v0 = int(reportline[0])
    v = int(reportline[1])
    if (v == v0) or not cromulentAbs(v,v0):
        return False
    elif v < v0 :
        incrRep = False # values must decrement from here on

    v0 = v
    for i in range(2,len(reportline)):
        v = int(reportline[i])
        if incrRep and v < v0 :
            return False
        if not incrRep and v > v0:
            return False
        if not cromulentAbs(v,v0):
            return False
        v0 = v
    
    return True

#-----------------------------------------------------------------------
# See if we can "fix" a report using the Problem Dampener (remove 1 val from report)
# (this is computationally daft BUT the reports are short so it doesn't matter)
def problemDampenerReport(report) :
    if isSafeReport(report) :
        return True
    else :
        # Iterate through the report taking out ONE and ONLY ONE value, then test
        for i in range(len(report)) :
            dList = report.copy()
            dVal = dList.pop(i)
            if isSafeReport(dList) :
                print(f"Passed if element {i} ({dVal}) is removed")
                return True
            
    
    #we tried everything and still failed
    return False
        
        
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    safecount=0
    with open(os.getcwd() + datafile, 'r') as allreports:
        for report in allreports:
            repVals = report.strip().split()
            sc=problemDampenerReport(repVals)
            print(f"{sc} :   {repVals}")
            safecount += sc


    print(f"Safe Report Count:  {safecount}")