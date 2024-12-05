#!/usr/bin/python3
# PRINT QUEUE
# Given input of two types: 
#   1) A set of instructions of the form X|Y where X and Y are numbers
#   2) A set of number sequences
#
# Use the instructions to ensure each number sequence conforms to specification.
# For each sequence that DOES conform, extract the MIDDLE number. 
# The output is the SUM of conforming sequence's middle numbers
#
import os

#datafile="/data/day5test1.txt"
datafile="/data/day5data.txt"

#This is where the code makes or breaks...
#-----------------------------------------------------------------------
def complies_with_instructions(sequence,specifications) :
    #check each element...
    for i in range(len(sequence)) :
        #...against every spec
        for spec in specifications :
            #ignore if page isn't subject
            if sequence[i] == spec[0] :
                #non compliant IFF dest page is in list AND dest page preceeds subject page
                try :
                    if sequence.index(spec[1]) < i :
                        #print(f"{sequence} failed at {i} because of {spec}")
                        return False
                except ValueError :
                    continue # dest wasn't in list, instruction doesn't apply
    return True

#-----------------------------------------------------------------------
def midpoint(list) :
    if len(list) % 2 == 0 :
        print(f"list is even, no midpoint")
        exit()
    else :
        #handily because zero index, the floor number is already the +1
        return list[len(list)//2]

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #Today our data consists of two data structures, firstly
    #a set of instruction tuples with a "|" seperator
    #then a blank line
    #then a list of page specifications with a "," separator
    specs=[]
    updates=[]
    with open(os.getcwd() + datafile, 'r') as n:
        for l in n:
            #good enough
            l = l.strip()
            if l.find("|")>0 :
                spec=list(map(int,l.split("|")))
                specs.append(spec)
            elif l.find(",")>0 :
                update=list(map(int,l.split(",")))
                updates.append(update)
    print(f"Read {len(specs)} specifications, applying to {len(updates)} update lists")
    midsum=0
    compliant=0
    for update in updates :
        if complies_with_instructions(update,specs) :
            compliant += 1
            midsum += midpoint(update)
    
    print(f"{compliant} updates were compliant")
    print(f"SUM OF MIDDLE PAGES = {midsum}")