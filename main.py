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
import AddData as adt
import AddResult as addres

# Function to create the
# random binary string

def main():

    # user input setting
    TRd = cfg.TRd
    #operation = cfg.operation
    L = cfg.L
    memory = cfg.memory
    #addResultposition = cfg.addResultposition
    #print(memory)

    ## Set TRd position
    TRd_start_loc =  cfg.TRd_start_loc
    TRd_end_loc = cfg.TRd_end_loc

    # Setting instruction to something other than 'quit'.
    instruction = ''

    # Starting a loop that will run until the user enters 'quit'.
    while instruction != 'quit':
        # Ask the user for the instruction.
        instruction = input("Please enter the instruction, or enter 'quit': ")

        if (instruction == 'write 0'):
            writeport = TRd_start_loc + (L/2)
            #print(writeport)
            data_in_binary = input("Enter the data to be inserted : ")
            memory = adt.writezero(writeport, memory, data_in_binary)

        elif (instruction == 'write 1'):
            writeport = TRd_start_loc + (L/2) + TRd
            data_in_binary = input("Enter the data to be inserted : ")
            memory = adt.writeone(writeport, memory, data_in_binary)

        elif (instruction == 'Shift TRd left'):
             TRd_start_loc = adt.shift_TRd_left()

        elif (instruction == 'Shift TRd Right'):
             TRd_start_loc = adt.shift_TRd_right()

        elif (instruction == 'operation'):
             operation = input("Enter the operations from the list: \n 1 : And \n 2 : Nand \n 3 : Xor \n 4 : Xnor \n 5 : Or \n 6 : Nor \n 7 : Not \n")
             if operation == '1':
                 result = logicop.And(memory,TRd_start_loc)
                 addres.addResult(result, memory, TRd_start_loc)

             elif operation == '2':
                 result = logicop.Nand(memory,TRd_start_loc)
                 addres.addResult(result, memory, TRd_start_loc)

             elif operation == '3':
                 result = logicop.Xor(memory,TRd_start_loc)
                 addres.addResult(result, memory, TRd_start_loc)

             elif operation == '4':
                 result = logicop.Xnor(memory,TRd_start_loc)
                 addres.addResult(result, memory, TRd_start_loc)

             elif operation == '5':
                 result = logicop.Or(memory,TRd_start_loc)
                 addres.addResult(result, memory, TRd_start_loc)

             elif operation == '6':
                 result = logicop.Nor(memory,TRd_start_loc)
                 addres.addResult(result, memory, TRd_start_loc)

             elif operation == '7':
                 result = logicop.Not(memory,TRd_start_loc)
                 addres.addResult(result, memory, TRd_start_loc)

    print(memory)







if __name__ == '__main__':
    main()


