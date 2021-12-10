## Add data to Memory in DWM

import random
from collections import deque
import configuration as cfg

bit_length = cfg.bit_length   # Enter the bit size of the inputs from the following 512, 1024, 2048, 4096
L = cfg.L         # Enter the size of the memory
#memory = []
TRd = cfg.TRd
TRd_start_loc = cfg.TRd_start_loc
TRd_end_loc = TRd_start_loc + TRd - 1



def writezero(writeport, memory, data_in_binary):

    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)
    writeport = int(writeport)
    if (memory[writeport] != None):
        # Shifting data left by 1 position
        for i in range(writeport + TRd - 1, writeport, -1):
            memory[i] = memory[i-1]
        memory[writeport] = data_in_binary
    else:
        memory[writeport] = data_in_binary

    print(writeport)
    print(writeport + TRd - 1)
    #print(memory[writeport :writeport + TRd])
    return memory

def writeone(writeport, memory, data_in_binary):

    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)

    writeport = int(writeport)
    #print(writeport - TRd + 1)
    #print(writeport)
    if (memory[writeport - 1] != None):
        # Shifting data left by 1 position
        for i in range(writeport - 1, writeport - TRd):
            print('memory[{}] = {}'.format(i, memory[i]))
            print('memory[{}] = {}'.format(i-1, memory[i+1]))
            memory[i] = memory[i + 1]
        memory[writeport - 1] = data_in_binary
    else:
        memory[writeport - 1] = data_in_binary

    print(writeport -1)
    print(writeport - TRd)
    # print(memory[writeport - TRd + 1 : writeport + 1])
    #print(memory[writeport : writeport + TRd])
    return memory


def shift_TRd_left():
    shiftposition = int(input("Enter the position to shift to left : "))
    TRd_start_loc = shiftposition
    print(TRd_start_loc)
    print(L/2)

    return TRd_start_loc

def shift_TRd_right():
    shiftposition = int(input("Enter the position to shift to right : "))
    TRd_start_loc = shiftposition

    return TRd_start_loc