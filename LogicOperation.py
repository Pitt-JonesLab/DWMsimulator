from functools import reduce
TRd_size = 5
# def And(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos):
#     TRd_head = int(TRd_head)
#     TRd_tail = TRd_head + 4
#
#     mem = memory[TRd_head:TRd_tail+1]
#     #print(mem)
#     # Bitwise AND of List
#     # Using reduce() + lambda + "&" operator
#     res = reduce(lambda x, y: x & y, mem)
#
#
#     return res


# def Nand(memory, TRd_start_loc, TRd_end_loc):
#     TRd_start_loc = int(TRd_start_loc)
#     TRd_end_loc = int(TRd_end_loc)
#     #TRd_end_loc = TRd_start_loc + TRd - 1
#     mem = memory[TRd_start_loc:TRd_end_loc]
#     # Calling and
#     Andresult = And(mem,TRd_start_loc,TRd_end_loc)
#     res = not (Andresult)  # complementing the and result
#
#     return res

def Xor(memory, row_number, nanowire_num_start_pos,nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size
    mem = []
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
        count = 0
        for j in range(TRd_head, TRd_end_loc):
            if memory[i][j] == bin(1):
                count += 1

        if (count % 2 == 0):
            val = bin(0)
        else:
            val = bin(1)
        mem.append(val)

    return 1, mem


    # Bitwise XOR of List
    # Using reduce() + lambda + "&" operator
    # for i in range()
    # res = reduce(lambda x, y: x ^ y, mem)
    # res = ''
    # if TRd == 4:
    #     for m in zip(mem[0], mem[1], mem[2], mem[3]):
    #         count = m.count('1')
    #
    #         if (count % 2 == 0):
    #             res += '0'
    #         else:
    #             res += '1'


    return 1, mem


# def Xnor(memory, TRd_start_loc, TRd_end_loc):
#     TRd_start_loc = int(TRd_start_loc)
#     TRd_end_loc = int(TRd_end_loc)
#     #TRd_end_loc = TRd_start_loc + TRd - 1
#     mem = memory[TRd_start_loc:TRd_end_loc]
#     # Calling Xnor
#     Xorresult = Xor(mem,TRd_start_loc, TRd_end_loc)
#     res = not (Xorresult)  # complementing the and result
#
#     return res
#
#
# def Or(memory, TRd_start_loc, TRd_end_loc):
#     TRd_start_loc = int(TRd_start_loc)
#     TRd_end_loc = int(TRd_end_loc)
#     #TRd_end_loc = TRd_start_loc + TRd - 1
#     mem = memory[TRd_start_loc:TRd_end_loc]
#     # Bitwise OR of List
#     # Using reduce() + lambda + "&" operator
#     res = reduce(lambda x, y: x | y, mem)
#
#     return res
#
#
# def Nor(memory, TRd_start_loc, TRd_end_loc):
#     TRd_start_loc = int(TRd_start_loc)
#     TRd_end_loc = int(TRd_end_loc)
#     #TRd_end_loc = TRd_start_loc + TRd - 1
#     mem = memory[TRd_start_loc:TRd_end_loc]
#     # Calling Nor
#     Orresult = Or(mem,TRd_start_loc,TRd_end_loc)
#     res = Not(Orresult)  # complementing the and result
#
#     return res
#
# def Not(res):
#     result = []
#     for i in res:
#        if i == '1':
#            result.append(0)
#        else:
#            result.append(1)
#
#
#     return result
#
def carry(memory,row_number):
    TRd_start_loc = int(row_number)
    TRd_size = 4
    TRd_end_loc = int(TRd_start_loc) + TRd_size
    mem = memory[TRd_start_loc:TRd_end_loc + 1]

def carry_prime(memory,row_number):
    TRd_start_loc = int(row_number)
    TRd_size = 4
    TRd_end_loc = int(TRd_start_loc) + TRd_size
    mem = memory[TRd_start_loc:TRd_end_loc + 1]
    # for i in range(0, len(mem)):

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

# data0 = bin(9)
# data1 = bin(14)
# data2 = bin(12)
# data3 =bin(14)


# memory = ['0b1111','0b1111','0b1111','0b1111','0b1111',None,None,None,data0,data1,data2,data3,None,None,None, '0b1110','0b1110','0b1110','0b1110','0b1110']
# print(memory)
# print(data0)
# print(data1)
# print(data2)
# print(data3)

# TRd_start_loc = 8
# TRd_end_loc = 11
# res = Xor(memory,TRd_start_loc, TRd_end_loc)
# res = Not(12)
# print("The result of XOR operation is : ", (res))