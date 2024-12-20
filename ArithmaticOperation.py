
import LogicOperation as logicop
import WriteData as wr
from display import display
import config as config

TRd_size = config.TRd_size
# Initializing single Local Buffer for all DBC's
Local_row_buffer = [0] * (512)


def addition(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):

    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    # print(TRd_head, TRd_end_loc)
    display(memory, TRd_head, 'AP0')
    result = ''
    # Fill AP0 and AP1 with 0's
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos ):
        memory[TRd_head][i] = '0'
        memory[TRd_end_loc][i] = '0'

    # display after appending zeros
    # display(memory, 0, 'AP0')

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos - 1):
        carry = carry_add(memory, TRd_head, i, i)
        # write carry at next nanowire at AP1
        memory[TRd_end_loc][i + 1] = carry

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos - 2):

        carry_prime = carry_prime_add(memory, TRd_head, i, i)
        # write carry prime at next to next nanowire at AP0
        memory[TRd_head][i + 2] = carry_prime


    for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
        sum = xor_add(memory, TRd_head, i, i)

        # write sum at the same nanowire at AP0
        memory[TRd_head][i] = sum
        result += sum

    # display(memory, TRd_head, 'AP0')
    # print(result)
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

    return hex_num



def multiply(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    TRd_head = 1
    TRd_end_loc = TRd_head + TRd_size - 1
    # display(memory, TRd_head, 'AP0')

    result = ''
    carry = ''
    carry_prime = ''
    sum = ''
    # call carry, carry prime and xor till three operand
    l = TRd_end_loc + 1
    
    # print(TRd_size - 2,l - TRd_head)
    while (TRd_head)  <= (TRd_end_loc):
        print("c+cp_xor",TRd_head,TRd_end_loc)
        for i in range(0, 511):
            carry = carry + carry_add(memory, TRd_head, i, i)
            
            carry_prime = carry_prime + carry_prime_add(memory, TRd_head, i, i)
            sum = sum + xor_add(memory, TRd_head, i, i)

        display(memory, TRd_head, 'AP0')
        # print("carry",carry)
        # print("carry_prime",carry_prime)
        # print("sum",sum)
        # print("carry,carry_prime,sum=",carry,carry_prime,sum)
        # write c, c' and sum
        for i in range(0, 510):
            memory[l+1][i + 1] = carry[i]
        for i in range(0, 509):
            memory[l + 2][i + 2] = carry_prime[i]
        for i in range(0, 511):
            memory[l + 3][i] = sum[i]
            memory[TRd_end_loc][i] = 0

        # display(memory, TRd_head, 'AP0')

        TRd_head += TRd_size
        l += 3
        

    # Call ADD function
    result = addition(memory, TRd_end_loc, nanowire_num_start_pos, 16)
    # print('result', result)

    # # Converting binary data at TRd head to Hex for verification/visualization
    # count = 0
    # s = ''
    # hex_num = '0x'
    # for i in range(0, len(result)):
    #     s += str(result[i])
    #     count += 1
    #     if count == 4:
    #         num = int(s, 2)
    #         string_hex_num = format(num, 'x')
    #         hex_num += (string_hex_num)
    #         s = ''
    #         count = 0

    return result

# # Initialize A and B as 8-bit binary integers
# A = 0b00011111  # Binary representation of A: 0001 1111
# B = 0b11111111  # Binary representation of B: 1111 1111

# # Store results for each step in a list
# results = []

# # Loop over each bit of B, starting from the least significant bit
# for i in range(8):
#     # Check if B[i] is set (1)
#     if (B >> i) & 1:
#         # If B[i] is 1, shift A to the right by i positions
#         result = A >> i
#     else:
#         # If B[i] is 0, result is 0
#         result = 0b00000000
#     # Append the result in an 8-bit binary format
#     results.append(f"{result:08b}")

# # Print each result
# for i, res in enumerate(results):
#     print(f"Step {i}: {res}")













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