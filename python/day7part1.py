#!/usr/bin/python3
# DAY 7 PART 1 - BRIDGE REPAIR
#
# Given a sequence consisting of :
#  RESULT: [operand] [operand] ...
#
# ...Determine the + or * operators that can go between the operands to produce the RESULT
# noting that only RESULTS that _can_ be derived from the rules above count, and the 
# output value is the SUM of the RESULTS that can be obtained.
#
# Note that normal operator precedence is rescinded: operators ALWAYS evaluate left->right

import os
import sys

#why write many code when short import work?
import itertools

testfile="/data/day7test1.txt"
datafile="/data/day7data.txt"

#the guts of the part1 problem: can you get to RESULT by interpolating +/*
#between the operands? Multiple solutions may be possible, we only need
#the first to prove the result
# we just need to permute the +/* operators between operands and bang
# out after first success
#-----------------------------------------------------------------------
def canconstruct(res,op) :
    numop = len(op) - 1
    permutations = list(itertools.product('+*',repeat=numop))
    for p in permutations:
        if evaluate(op,p) == res :
            return True
        
    #if we get here we've failed
    return False


#here's how we test:
#-----------------------------------------------------------------------
def evaluate(operands,operators) :
    sum = operands[0]
    for i in range(1,len(operands)) :
        if operators[i-1] == '+' :
            sum = sum + operands[i]
        else :
            sum = sum * operands[i]
    return sum
    

#-----------------------------------------------------------------------
if __name__ == "__main__" :
 
    #Our Part-1 data can be read in STREAM form as we're only interested
    #in true/false condition matching per evaluation.    
    df = os.getcwd() + testfile
    if len(sys.argv)>1 and sys.argv[1] == 'p' :
        df = os.getcwd() + datafile
       
    sumoftrueresults = 0 
    with open(df, 'r') as n:
        for l in n:
            rp = l.split(':')
            result = int(rp[0])
            oper = list(map(int,rp[1].split()))
            if canconstruct(result,oper) :
                sumoftrueresults += result
    print(f"PART 1 ANSWER: {sumoftrueresults}")
   