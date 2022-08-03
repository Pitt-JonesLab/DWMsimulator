'''
Author : Pavia Bera - University of South Florida

This is a simulator for Domain wall memory (DWM)
DWM leverages the 'shift-register' nature of spintronic domain-wall memory (DWM).
Shift-based scheme utilizes a multi-nanowire approach to ensure that reads and writes
can be more effectively aligned with access ports for simultaneous access in the same cycle.
'''

import sys
from functools import reduce
from collections import deque
import configuration as cfg
import LogicOperation as logicop
import WriteData as adt
import AddResult as addres
from AWS_Encryption import *


# Function to create the
# random binary string


# user input setting
TRd = cfg.TRd
#operation = cfg.operation
L = cfg.L
memory = cfg.memory
# print(memory)
#addResultposition = cfg.addResultposition


## Set TRd position
TRd_start_loc =  cfg.TRd_start_loc + (L/2) - 1
#print(TRd_start_loc)
TRd_end_loc = cfg.TRd_end_loc + (L/2) - 1
#print(TRd_end_loc)

def controller_write(data, instruction):


    # # user input setting
    # TRd = cfg.TRd
    # #operation = cfg.operation
    # L = cfg.L
    # memory = cfg.memory
    # # print(memory)
    # #addResultposition = cfg.addResultposition
    #
    #
    # ## Set TRd position
    # TRd_start_loc =  cfg.TRd_start_loc + (L/2) - 1
    # #print(TRd_start_loc)
    # TRd_end_loc = cfg.TRd_end_loc + (L/2) - 1
    # #print(TRd_end_loc)

    global TRd_start_loc
    global memory
    global TRd_end_loc


    # Starting a loop that will run until the user enters 'quit'.
    # while instruction != 'quit':
    #     # Ask the user for the instruction.

    if (instruction == 'AP0 AP1'):
        #write at (left) TRd start and shift data right
        writeport = TRd_start_loc

        memory = adt.writezero(writeport, memory, data)

    elif (instruction == 'AP1 AP0'):
        #write at (right) TRd end and shift data left.
        writeport = TRd_end_loc

        memory = adt.writeone(writeport, memory, data)

    elif (instruction == 'write at Address 0'):
        #write at (right) TRd end and shift data left.

        memory = adt.shift_writezero(memory, data)
        TRd_start_loc = int(L / 2 )
        TRd_end_loc = TRd + TRd_start_loc


    elif (instruction == 'write at Address 1'):
        #write at (right) TRd end and shift data left.

        memory = adt.shift_writeone(memory, data)
        TRd_start_loc = int(L/2 + L)
        TRd_end_loc = TRd + TRd_start_loc


    elif (instruction == 'AP0'):
        #overwrite at left side (TRd start position)
        writeport = TRd_start_loc

        memory = adt.overwriteZero(writeport, memory, data)

    elif (instruction == 'AP1'):
        #overwrite at right side(TRd end position)
        writeport = TRd_end_loc

        memory = adt.overwriteOne(writeport, memory, data)

    elif (instruction == 'AP0 LE'):
        #write at (left) TRd start and shift data towards the left padding.
        writeport = TRd_start_loc

        memory = adt.writezero_shiftLE(writeport, memory, data)

    elif (instruction == 'AP0 RE'):
        #write at (left) TRd start and shift data towards the right padding.
        writeport = TRd_end_loc

        memory = adt.writezero_shiftRE(writeport, memory, data)

    elif (instruction == 'AP1 LE'):
        #write at (right) TRd end and shift data towards left padding.
        writeport = TRd_end_loc

        memory = adt.writeone_shiftLE(writeport, memory, data)

    elif (instruction == 'AP1 RE'):
        #write at (right) TRd end and shift data towards right padding.
        writeport = TRd_end_loc

        memory = adt.writeone_shiftRE(writeport, memory, data)


def controller_shift(instruction):

    global TRd_start_loc
    global memory
    global TRd_end_loc

    if (instruction == 'Shift Right'):
         TRd_start_loc = TRd_start_loc + 1
         TRd_end_loc = TRd_start_loc + TRd - 1

    elif (instruction == 'Shift Left'):
         TRd_start_loc = TRd_start_loc - 1
         TRd_end_loc = TRd_start_loc + TRd - 1

def controller_read(instruction):

    global TRd_start_loc
    global memory
    global TRd_end_loc

    if (instruction == 'Read 0'):
        TRd_start_loc = int(TRd_start_loc)


    elif(instruction == 'Read 1'):
        TRd_end_loc = int(TRd_end_loc)

def controller_operation(operation, source, sink):

    global TRd_start_loc
    global memory
    global TRd_end_loc
    # memory = [1, 1, 1, 1, 1, None, None, None, 1, 1, 1, 0, None, None, None, 0, 0, 0, 0, 0]
    # operation = input("Enter the operations from the list: \n 1 : And \n 2 : Nand \n 3 : Xor \n 4 : Xnor \n 5 : Or \n 6 : Nor \n 7 : Not \n")
    # source = input("Enter the source from the list : \n 1 : AP0 \n 2: AP1 \n")
    # sink = input("Enter the sink from the list : \n 0: Overwrite \n 1 : AP0 \n 2: AP1 \n 3: LE \n 4: RE \n")
    if (operation == '1'):
         result = logicop.And(memory,TRd_start_loc, TRd_end_loc)
         addres.addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink)

    elif operation == '2':
         result = logicop.Nand(memory,TRd_start_loc, TRd_end_loc)
         addres.addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink)

    elif operation == '3':
         result = logicop.Xor(memory,TRd_start_loc, TRd_end_loc)
         addres.addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink)

    elif operation == '4':
         result = logicop.Xnor(memory,TRd_start_loc, TRd_end_loc)
         addres.addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink)

    elif operation == '5':
         result = logicop.Or(memory,TRd_start_loc, TRd_end_loc)
         addres.addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink)

    elif operation == '6':
         result = logicop.Nor(memory,TRd_start_loc,TRd_end_loc)
         addres.addResult(result, memory, TRd_start_loc,TRd_end_loc, source, sink)

         # elif operation == '7':
         #     result = logicop.Not(memory,TRd_start_loc, TRd_end_loc)
         #     addres.addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink)









