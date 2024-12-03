#!/usr/bin/python3
#
# Valid instructions consist of the sequence "mul(x,y)" where x and y are between 0 and 999
# HOWEVER, they can be "switched on and off" by the presence of "do()" and "dont()" instructions
# within the sequence. State is global; we start in do() (enabled) state.
#
# Given arbitrary text input, extract only valid mul() instructions, execute them and sum the 
# results.
# GOTCHAS: The sample is 1 short-ish string. The Actual data is across 6-7 (long) lines. Betcha
#          there's some otherwise-valid instructions separated by LF chars....
#
import os
import re

#datafile="/data/day3test2.txt"
datafile="/data/day3data.txt"

#This matches all valid instructions in a line
#curse them for making single-quote valid
insRE = re.compile(r"do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\)")

#we'll use this to extract the operands - numbers - from a valid instruction
opRE = re.compile('mul\((\d{1,3}),(\d{1,3})\)')

#-----------------------------------------------------------------------
def do_mult(instr) :
    oper = opRE.match(instr).groups()
    return int(oper[0]) * int(oper[1])

#-----------------------------------------------------------------------
if __name__ == "__main__" :
    bignum = 0
    enabled = True
    with open(os.getcwd() + datafile, 'r') as n:
        for line in n:
            instructions = insRE.findall(line)
            for ins in instructions:
                if ins == "do()" :
                    enabled = True
                elif ins == "don't()" :
                    enabled = False
                else :
                    if enabled :
                        sum = do_mult(ins)
                        print(f"{ins} = {sum}")
                        bignum += sum
                    else :
                        print(f"DISABLED: {ins}")
    print(f"SUM OF ALL INSTRUCTIONS:    {bignum}")
                