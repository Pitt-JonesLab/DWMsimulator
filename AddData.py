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
    #print(writeport)
    #print(writeport + TRd)
    if (memory[writeport] != None):

        for i in range(writeport + TRd - 1 , writeport, -1):
            #print('writeport = ',writeport)
            # print('memory[{}] = {}'.format(i, memory[i]))
            # print('memory[{}] = {}'.format(i-1, memory[i-1]))
            memory[i] = memory[i - 1]
        memory[writeport] = data_in_binary
    else:
        memory[writeport] = data_in_binary

    print(memory)

    return memory

def writeone(writeport, memory, data_in_binary):

    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)

    writeport = int(writeport)
    if (memory[writeport] != None):
        # Shifting data left by 1 position
        for i in range(writeport - TRd + 1, writeport):
            memory[i] = memory[i + 1]
        memory[writeport] = data_in_binary

    else:
        memory[writeport] = data_in_binary

    print(memory)

    return memory

def overwriteZero(writeport, memory, data_in_binary):
    #overwrite at left side (TRd start position
    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)
    writeport = int(writeport)
    memory[writeport] = data_in_binary
    print(memory)

    return memory

def overwriteOne(writeport, memory, data_in_binary):
    #overwrite at right side(TRd end position)
    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)
    writeport = int(writeport)
    memory[writeport] = data_in_binary

    print(memory)

    return memory

def writezero_shiftLE(writeport, memory, data_in_binary):
    #write at (left) TRd start and shift data towards the left padding.
    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)
    writeport = int(writeport)
    if (memory[writeport] != None):
        # Shifting data left by 1 position towards left extremity
        #print(range((L/2 - 1), writeport))
        start = int(L/2 - 1)
        for i in range(start, writeport):
            memory[i] = memory[i + 1]
        memory[writeport] = data_in_binary

    else:
        memory[writeport] = data_in_binary

    print(memory)

    return memory


def writezero_shiftRE(writeport, memory, data_in_binary):
    #write at (left) TRd start and shift data towards the right padding.
    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)
    writeport = int(writeport)

    if (memory[writeport] != None):
        # Shifting data right by 1 position towards the right extremity.
        start = int(L + L/2 - 1)
        for i in range(start, writeport, -1):
            memory[i] = memory[i - 1]
        memory[writeport] = data_in_binary

    else:
        memory[writeport] = data_in_binary

    print(memory)

    return memory

def writeone_shiftLE(writeport, memory, data_in_binary):
    #write at (right) TRd end and shift data towards left padding.
    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)
    writeport = int(writeport)

    if (memory[writeport] != None):
        # Shifting data left by 1 position
        start = int(L/2 - 1)
        for i in range(start, writeport):
            memory[i] = memory[i + 1]
        memory[writeport] = data_in_binary

    else:
        memory[writeport] = data_in_binary

    print(memory)

    return memory

def writeone_shiftRE(writeport, memory, data_in_binary):
    #write at (right) TRd end and shift data towards right padding.
    #data_in_binary = ''.join(format(ord(x), 'b') for x in data)

    writeport = int(writeport)

    if (memory[writeport] != None):
        # Shifting data left by 1 position
        start = int(L + L/2 - 1)
        for i in range(start, writeport, -1):
            memory[i] = memory[i - 1]
        memory[writeport] = data_in_binary

    else:
        memory[writeport] = data_in_binary

    print(memory)

    return memory