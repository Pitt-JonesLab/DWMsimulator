from display import display

TRd_size = 5

def And(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    result = ''

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        c = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '1':
                c += 1

        if (c == TRd_size):
            val = '1'
        else:
            val = '0'
        result += val

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(0, len(result)):
        s += str(result[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0

    return 1, 0.000958797, hex_num


def Nand(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1

    mem = []
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        count = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[i][j] == '1':
                count += 1

        if (count == TRd_size):
            val = '0'
        else:
            val = '1'
        mem.append(val)

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = []
    for i in range(0, len(mem)):
        s += str(mem[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            hex_num.append(hex(num))
            s = ''
            count = 0
    print('NAND ', hex_num)

    return 1,0.000958797,  mem

def Xor(memory, row_number, nanowire_num_start_pos,nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    result = ''

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
        c = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '1':
                c += 1

        if (c % 2 == 0):
            val = '0'
        else:
            val = '1'
        result += val

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(0, len(result)):
        s += str(result[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0
    print('XOR ', hex_num)

    return 1, 0.000958797, hex_num


def Xnor(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    result = ''

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        c = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[J][I] == '1':
                c += 1

        if (c % 2 == 0):
            val = '1'
        else:
            val = '0'
        result += val

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(0, len(result)):
        s += str(result[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0
    print('XNOR ', hex_num)

    return 1, 0.000958797, hex_num

def Or(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    result = ''

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        c = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '0':
                c += 1

        if (c == TRd_size):
            val = '0'
        else:
            val = '1'
        result += val

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(0, len(result)):
        s += str(result[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0


    return 1, 0.000958797, hex_num


def Nor(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1

    result = ''
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        count = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '0':
                count += 1

        if (count == TRd_size):
            val = '1'
        else:
            val = '0'
        result += val

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(0, len(result)):
        s += str(result[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0


    return 1, 0.000958797, hex_num

def Not(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1

    mem = []
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        count = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[i][j] == '0':
                count += 1

        if (count == TRd_size):
            val = '1'
        else:
            val = '0'
        mem.append(val)

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = []
    for i in range(0, len(mem)):
        s += str(mem[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            hex_num.append(hex(num))
            s = ''
            count = 0
    print('NOR ', hex_num)

    return 1, 0.000958797, mem

def carry(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    result = ''

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        c = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '1':
                c += 1

        if (c == 2 or c == 3 or c == 6 or c == 7):
            val = '1'
        else:
            val = '0'
        result += val

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(0, len(result)):
        s += str(result[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0

    return 1, 0.000958797, hex_num

def carry_prime(memory,row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    result = ''

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        count = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '1':
                count += 1

        if (count == 4 or count == 5 or count == 6 or count == 7):
            val = '1'
        else:
            val = '0'
        result += val

    # Converting binary data at TRd head to Hex for verification/visualization
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(0, len(result)):
        s += str(result[i])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0

    return 1, 0.000958797, hex_num

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