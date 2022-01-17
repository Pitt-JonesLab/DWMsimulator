import configuration as cfg
from functools import reduce

TRd = cfg.TRd
L = cfg.L

def And(memory, TRd_start_loc, TRd_end_loc):
    # print(memory)
    # print(TRd_start_loc)
    # print(TRd_end_loc)
    TRd_start_loc = int(TRd_start_loc)
    TRd_end_loc = int(TRd_end_loc)
    mem = memory[TRd_start_loc:TRd_end_loc+1]
    #print(mem)
    # Bitwise AND of List
    # Using reduce() + lambda + "&" operator
    res = reduce(lambda x, y: x and y, mem)

    return res


def Nand(memory, TRd_start_loc, TRd_end_loc):
    TRd_start_loc = int(TRd_start_loc)
    TRd_end_loc = int(TRd_end_loc)
    #TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Calling and
    Andresult = And(mem,TRd_start_loc,TRd_end_loc)
    res = not (Andresult)  # complementing the and result

    return res


def Xor(memory, TRd_start_loc, TRd_end_loc):
    TRd_start_loc = int(TRd_start_loc)
    TRd_end_loc = int(TRd_end_loc)
    #TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Bitwise XOR of List
    # Using reduce() + lambda + "&" operator
    res = reduce(lambda x, y: x ^ y, mem)

    return res


def Xnor(memory, TRd_start_loc, TRd_end_loc):
    TRd_start_loc = int(TRd_start_loc)
    TRd_end_loc = int(TRd_end_loc)
    #TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Calling Xnor
    Xorresult = Xor(mem,TRd_start_loc, TRd_end_loc)
    res = not (Xorresult)  # complementing the and result

    return res


def Or(memory, TRd_start_loc, TRd_end_loc):
    TRd_start_loc = int(TRd_start_loc)
    TRd_end_loc = int(TRd_end_loc)
    #TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Bitwise OR of List
    # Using reduce() + lambda + "&" operator
    res = reduce(lambda x, y: x or y, mem)

    return res


def Nor(memory, TRd_start_loc, TRd_end_loc):
    TRd_start_loc = int(TRd_start_loc)
    TRd_end_loc = int(TRd_end_loc)
    #TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Calling Nor
    Orresult = Or(mem,TRd_start_loc,TRd_end_loc)
    res = not (Orresult)  # complementing the and result

    return res

# def Not(memory, TRd_start_loc, TRd_end_loc):
#     TRd_start_loc = int(TRd_start_loc)
#     TRd_end_loc = int(TRd_end_loc)
#     mem = memory[TRd_start_loc:TRd_end_loc]
#     for i in range(0, (len(mem))):
#         print(i)
#         temp = mem[i]
#         mem[i] = not (temp)
#
#     return mem




##DRIVER CODE for debugging this file logicOperation.py:
bit_length = 512
## Five Inputs of 512 bits
import random

def rand_key(p):
    # Variable to store the
    # string
    key1 = ""

    # Loop to find the string
    # of desired length
    for i in range(p):
        # randint function to generate
        # 0, 1 randomly and converting
        # the result into str
        temp = str(random.randint(0, 1))

        # Concatenation the random 0, 1
        # to the final result
        key1 += temp

    return (key1)

n = bit_length #size of random binary number to be filled before and after the momory in task
#str1 = rand_key(n)
#data_in_binary = ''.join(format(ord(x), 'b') for x in str1)
data = []
for i in range(0, 5):
    str1 = rand_key(n)
    data_in_binary = ''.join(format(ord(x), 'b') for x in str1)
    #data_in_binary = ''.join(format(ord(x), 'b') for x in str1)
    #print(len(data_in_binary))
    #print(type(str1))

    data.append(data_in_binary)


memory = [1,1,1,1,1,None,None,data[0],data[1],data[2],data[3],data[4],None,None,None,0,0,0,0,0]
TRd_start_loc = 7
TRd_end_loc = 11
#res = Xor(memory,TRd_start_loc, TRd_end_loc)
#print("The result is : ", type(memory[0]))