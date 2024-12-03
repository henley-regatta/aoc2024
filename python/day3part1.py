#!/usr/bin/python3
#
# Valid instructions consist ONLY of the sequence "mul(x,y)" where x and y are between 0 and 999
# Given arbitrary text input, extract only valid mul() instructions, execute them and sum the 
# results.
# GOTCHAS: The sample is 1 short-ish string. The Actual data is across 6-7 (long) lines. Betcha
#          there's some otherwise-valid instructions separated by LF chars....
#
import os
import re

#datafile="/data/day3test.txt"
datafile="/data/day3data.txt"

#This matches all valid instructions in a line
insRE = re.compile('mul\(\d{1,3},\d{1,3}\)')

#we'll use this to extract the operands - numbers - from a valid instruction
opRE = re.compile('mul\((\d{1,3}),(\d{1,3})\)')

#-----------------------------------------------------------------------
def do_mult(instr) :
    oper = opRE.match(instr).groups()
    return int(oper[0]) * int(oper[1])

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    bignum = 0
    with open(os.getcwd() + datafile, 'r') as n:
        for line in n:
            instructions = insRE.findall(line)
            for ins in instructions:
                sum = do_mult(ins)
                print(f"{ins} = {sum}")
                bignum += sum
    print(f"SUM OF ALL INSTRUCTIONS:    {bignum}")
                