import configuration as cfg
from functools import reduce


TRd = cfg.TRd
L = cfg.L
bit_length = cfg.bit_length

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
    res = reduce(lambda x, y: x & y, mem)


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
    res = reduce(lambda x, y: x | y, mem)

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

# def Not(res):
#     # Loop to find the string
#     # of desired length
#     for i in range(bit_length):
#         # randint function to generate
#         # 0, 1 randomly and converting
#         # the result into str
#         temp = str(1)
#
#         # Concatenation the random 0, 1
#         # to the final result
#         key1 += temp
#
#
#     return result




##DRIVER CODE for debugging this file logicOperation.py:
# bit_length = 512
# ## Five Inputs of 512 bits
# import random
#
# def rand_key(p):
#     # Variable to store the
#     # string
#     key1 = ""
#
#     # Loop to find the string
#     # of desired length
#     for i in range(p):
#         # randint function to generate
#         # 0, 1 randomly and converting
#         # the result into str
#         temp = str(random.randint(0, 1))
#
#         # Concatenation the random 0, 1
#         # to the final result
#         key1 += temp
#
#     return (key1)

# n = bit_length #size of random binary number to be filled before and after the momory in task
# #str1 = rand_key(n)
# #data_in_binary = ''.join(format(ord(x), 'b') for x in str1)
# data = []
# for i in range(0, 5):
#     str1 = rand_key(n)
#     data_in_binary = ''.join(format(ord(x), 'b') for x in str1)
#     #data_in_binary = ''.join(format(ord(x), 'b') for x in str1)
#     #print(len(data_in_binary))
#     #print(type(str1))
#
#     data.append(data_in_binary)

data0 = bin(9)
data1 = bin(14)
data2 = bin(12)
data3 =bin(14)


memory = ['0b1111','0b1111','0b1111','0b1111','0b1111',None,None,None,9,14,12,14,None,None,None, '0b1110','0b1110','0b1110','0b1110','0b1110']
print(memory)
print(data0)
print(data1)
print(data2)
print(data3)

TRd_start_loc = 8
TRd_end_loc = 11
res = Xor(memory,TRd_start_loc, TRd_end_loc)
# res = Not(12)
print("The result of XOR operation is : ", bin(res))