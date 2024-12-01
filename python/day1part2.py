#!/usr/bin/python3
# Given input as 2 columns of numbers, perform an arbitrary "similarity test" by comparing to
# the NUMBER of times left col appears in right col
import os


#datafile="/data/day1test.txt"
datafile="/data/day1data.txt"

#-----------------------------------------------------------------------
# Return the number of times <num> appears in <list>
# (taking advantage of the fact that <list> is sorted)
def occurs(needle, listofnum) :
    count=0
    for haystack in listofnum :
        if needle > haystack :
            continue
        elif needle == haystack :
            count += 1
        else :
            break
    return count

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    lc = []
    rc = []
    with open(os.getcwd() + datafile, 'r') as n:
        for line in n:
            nStr = line.split()
            lc.append(int(nStr[0]))
            rc.append(int(nStr[1]))
    rc.sort()

    # This doesn't scale well but the input's only <=1000 long
    # and I'm running on a 4Ghz machine...
    totalscore = 0
    for v in lc :
        occ = occurs(v,rc)
        score = v * occ
        #print(f"{v} occurs in right column {occ} times, giving a score of {score}")
        totalscore += score
        
    print(f"BIG ANSWER:   {totalscore}")