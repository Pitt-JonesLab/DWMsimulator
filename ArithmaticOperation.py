
import LogicOperation as logicop
import WriteData as wr
from display import display


TRd_size = 5
# Initializing single Local Buffer for all DBC's
Local_row_buffer = [0] * (512)

def addition(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    cycle = 0
    energy = 0
    result = ''
    # Fill AP0 and AP1 with 0's
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos ):
        memory[TRd_head][i] = '0'
        memory[TRd_end_loc][i] = '0'

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos - 2):

        carry = carry_add(memory, TRd_head, i, i)

        # write carry at next nanowire at AP1
        memory[TRd_end_loc][i+1] = carry
        carry_prime = carry_prime_add(memory, TRd_head, i, i)

        # write carry prime at next to next nanowire at AP0
        memory[TRd_head][i + 2] = carry_prime
        # print(TRd_head)
        sum = xor_add(memory, TRd_head, i, i)

        # write sum at the same nanowire at AP0
        memory[TRd_head][i] = sum
        result += sum

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


    return 1, 1, hex_num



def multiply(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    cycle = 0
    energy = 0
    result = []

    # read AP0 where B is stored
    B = memory[TRd_head][:nanowire_num_end_pos]


    # calculate the length of B

    # read from $480 (DBC 15) where A is stored

    dbc = nanowire_num_start_pos
    A = dbc.controller(row_number, 'read', 0, 8)
    A = memory[TRd_end_loc][:nanowire_num_end_pos]

    # # make (len B) copies of AP0 (X)
    # shifted_A = shifted_by_one(A,nanowire_num_end_pos)

    # for i, l in enumerate(shifted_A):
    #     for j in range(0, ):
    #         if B[i] != '0':
    #             result.append(l)

    # for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
    #     c = 0
    #     for j in range(TRd_head, TRd_end_loc + 1):
    #
    #         if memory[j][i] == '1':
    # xor, carry, carry_prime
    xor = logicop.Xor(result, 0, 0,nanowire_num_end_pos)
    carry = logicop.carry(result, 0, 0,nanowire_num_end_pos)
    carry_prime = logicop.carry_prime(result, 0, 0,nanowire_num_end_pos)
    m = [xor,carry,carry_prime]
    addition(m, 0, 0, nanowire_num_end_pos)




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

    return 1, 1, hex_num

def xor_add(memory, row_number, nanowire_num_start_pos,nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1


    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        c = 0
        for j in range(TRd_head, TRd_end_loc + 1):

            if memory[j][i] == '1':
                c += 1

        if (c % 2 == 0):
            val = '0'
        else:
            val = '1'

    return val

def carry_add(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        c = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '1':
                c += 1

        if (c == 2 or c == 3 or c == 6 or c == 7):
            val = '1'
        else:
            val = '0'

    return val

def carry_prime_add(memory,row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        count = 0
        for j in range(TRd_head, TRd_end_loc + 1):
            if memory[j][i] == '1':
                count += 1

        if (count == 4 or count == 5 or count == 6 or count == 7):
            val = '1'
        else:
            val = '0'

    return val

def shifted_by_one(data, bit_length):

    shifted_A = [[('0') for _ in range(bit_length)] for _ in range(bit_length)]
    output = data

    for i in range(0,bit_length):
        # call  function to shift data by 1
        output = shift(output)
        for j in range(0, bit_length):
            shifted_A[i][j] = output[j]


    return shifted_A

def shift(data):
    bit_length = len(data)
    # Logical shift
    n = 1
    output = [0] * bit_length

    count = 0
    for i in range(n, bit_length):
        output[count] = data[i]
        count += 1

    for i in range(count, bit_length):
        output[i] = '0'

    return output