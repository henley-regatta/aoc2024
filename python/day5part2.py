#!/usr/bin/python3
# PRINT QUEUE
# Given input of two types: 
#   1) A set of instructions of the form X|Y where X and Y are numbers
#   2) A set of number sequences
#
# Use the instructions to ensure each number sequence conforms to specification.
# For each sequence that DOES NOT CONFORM,
# re-order the pages according to the rules
# then return the sum of the mid points OF THE ORIGINALLY FAILING SEQUENCES ONLY
#
# NOTE: The brain trap to avoid is thinking that all of the "instructions" have to be
#       globally consistent. THEY DON'T. Only the subset of instructions that apply to  
#       a given input number sequence has to be locally consistent. Solutions that proceed
#       with the assumption of global consistency a) are going to be overcomplicated b)
#       may not work out.
# (this is an argument for my rather brutish approach to the solution :-) )
import os
import sys

testfile="/data/day5test1.txt"
datafile="/data/day5data.txt"
    
# Modified to return the instruction a sequence fails on, or None
#-----------------------------------------------------------------------
def failing_instruction(sequence,specifications) :
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
                        return spec
                except ValueError :
                    continue # dest wasn't in list, instruction doesn't apply
    return None

#-----------------------------------------------------------------------
def reorderToSpec(sequence,specifications) :
    fspec = failing_instruction(sequence,specifications)
    permutations=0
    orgseq = sequence.copy()
    while fspec != None :
        permutations += 1
        #print(f"failing at {fspec} : {sequence}")
        #swap the positions of the failing before,after 
        #and try again
        sequence[sequence.index(fspec[0])], sequence[sequence.index(fspec[1])] = fspec[1], fspec[0]
        fspec = failing_instruction(sequence,specifications)
    print(f"{permutations} permutations required to transform {orgseq} -> {sequence}")
    return sequence

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
    df = os.getcwd() + testfile

    if len(sys.argv)>1 and sys.argv[1] == 'p' :
        df = os.getcwd() + datafile
    
    with open(df, 'r') as n:
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
    midsum = 0
    neededwork=0
    requiresReordering = []
    for update in updates :
        if failing_instruction(update,specs) != None:
            neededwork += 1
            reordered = reorderToSpec(update,specs)
            midsum += midpoint(reordered)
    
    print(f"{neededwork} updates needed reordering")
    print(f"SUM OF MIDDLE PAGES = {midsum}")