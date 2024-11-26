from math import comb
import config as config
import LogicOperation as logicop
from ProbCalc import calculate_probability
TRd_size = config.TRd_size
bit_length = config.bit_length
memory_size = config.memory_size
# Initializing single Local Buffer for all DBC's
Local_row_buffer = [0] * (bit_length)
word_size = (bit_length // 8)
n =  word_size + 8
fault_matrix = [0] * bit_length
fault_matrix_word = {}
faultpercent = 10**(-6)

def fault_modeling(faultpercent):
  k1 = 1
  k2 = 2

  ## Probability for 0,1,2, 3 plus bit error:
  p_0 = (1 - faultpercent)**(n)
  p_1 = comb(n, k1)*(faultpercent**k1)
  p_2 = comb(n, k2)*(faultpercent**k2)
  p_3plus = 1 - (p_0 + p_1 + p_2)

#   print('p_0,p_1,p_2,p_3plus',p_0,p_1,p_2,p_3plus)


def f_percent_model(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    # word_size_start = 0
    # word_size_end = word_size
    # while word_size_end  < nanowire_num_end_pos:
        # divide the memory into words
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
        count = 0
        # count no of 1's between TRd heads
        for j in range(row_number, TRd_size + row_number):
            if memory[j][i] == "1":
                count+=1
        fault_matrix[i]  = count

    # divide the memory into words
    word_size_start = 0
    word_size_end = word_size
    k = 0

    while word_size_end  <= nanowire_num_end_pos+1:
        failure_rate_50 = 0
        failure_rate_100 = 0
        p_50_success = 0
        p_100_success = 0
        p_success_word = 0

        for i in range(word_size_start, word_size_end):
            if fault_matrix[i] == config.TRd_size or fault_matrix[i] == 0:
                failure_rate_50 += 1
            else:
                failure_rate_100  += 1

        key_word = 'word_{}'.format(k)
        # p_50_success = (1 - 0.5*faultpercent)**failure_rate_50
        # p_100_success = (1 - faultpercent)**failure_rate_100
        # p_success_word = p_50_success*p_100_success

        E = failure_rate_50
        probabilities = calculate_probability(E)
        fault_matrix_word[key_word] = sum(probabilities[0:3])
        fault_matrix_word[key_word] *= fault_matrix_word[key_word]



        # # Display the probabilities for F=0 to F=max_fault
        # for i, prob in enumerate(probabilities):
        #     print(f"P(F = {i}) = {prob:.5e}")

        word_size_start = word_size_end
        word_size_end = word_size_start + word_size
        k += 1

    print(fault_matrix_word)


def fault_addition(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1

    result = ''
    # Fill AP0 and AP1 with 0's
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
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

def fault_mult():
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1
    # display(memory, TRd_head, 'AP0')

    result = ''
    carry = ''
    carry_prime = ''
    sum = ''
    # call carry, carry prime and xor till three operand
    l = nanowire_num_end_pos
    while (TRd_size - 2) < (l - TRd_head):

        for i in range(0, 511):
            carry += carry_add(memory, TRd_head, i, i)
            carry_prime += carry_prime_add(memory, TRd_head, i, i)
            sum += xor_add(memory, TRd_head, i, i)

        # write c, c' and sum
        for i in range(0, 510):
            memory[l][i + 1] = carry[i]
        for i in range(0, 509):
            memory[l + 1][i + 2] = carry_prime[i]
        for i in range(0, 511):
            memory[l + 2][i] = sum[i]

        # display(memory, TRd_head, 'AP0')

        TRd_head += TRd_size
        l += 3

    # Call ADD function
    result = addition(memory, TRd_head - 1, nanowire_num_start_pos, 16)
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


def xor_add(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
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


def carry_prime_add(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
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

    for i in range(0, bit_length):
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





## Driver Code:
fault_modeling(faultpercent)










'''
# def parity_checking(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos):
#   """
#   Parity checking is a method for detecting errors in data. It works by generating a parity bit,
#   which is a single bit that is calculated from the data. The parity bit is then used to check
#   if there are any errors in the data.
#
#   Args:
#     data: The data to be checked.
#
#   Returns:
#     True if there are no errors in the data, False otherwise.
#   """
#
#
#
#
#
#   # Shifting the data within the TRd space to right and writing at the TRd head
#   for i in range(TRd_head, TRd_head + TRd_size - 1):
#       # Calculate the parity bit.
#       parity_bit = 0
#       for j in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
#         bit = memory[i][j]
#         # parity_bit ^= bit
#         Local_buffer = logicop.Xor(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
#
#       # # Check if the parity bit is 0.
#       # for i in range(0, len(Local_buffer)):
#       #   if i == 0:
#       #     return True
#       # # call reed solomon
#       # #error_correction
#       # # call
#       #   else:
#       #     return False
#
#   return Local_buffer
#
# def reed_solomon(data, k, n):
#   """
#   Reed-Solomon error correction is a method for correcting errors in data. It works by generating a parity code, which is a redundant representation of the data. The parity code is then used to detect and correct errors in the data.
#
#   Args:
#     data: The data to be protected.
#     k: The number of data bits.
#     n: The total number of bits.
#
#   Returns:
#     The corrected data.
#   """
#
#   # Check if the parameters are valid.
#   if k > n:
#     raise ValueError("The number of data bits must be less than or equal to the total number of bits.")
#
#   # Generate the parity code.
#   parity_code = np.zeros(n - k, dtype=int)
#   for i in range(n - k):
#     for j in range(k):
#       parity_code[i] ^= data[j] * (2 ** i)
#
#   # Check if there are any errors in the data.
#   if np.any(data != np.bitwise_xor(data, parity_code)):
#     # There are errors in the data.
#     # Correct the errors using the parity code.
#     for i in range(n - k):
#       if data[i] != np.bitwise_xor(data[i], parity_code[i]):
#         # There is an error in the current bit.
#         # Correct the error by flipping the bit.
#         data[i] = 1 - data[i]
#
#   # Return the corrected data.
#   return data
#
#
# def corrective_shift(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos):
#   """
#   Error correction is a method for correcting errors in data. It works by comparing the data to a known good copy of the data.
#   The errors are then corrected using a variety of techniques, such as majority voting and Reed-Solomon error correction.
#
#   Args:
#     data: The data to be corrected.
#     shift_distance: The distance that the data has been shifted.
#
#   Returns:
#     The corrected data.
#   """
#   # Calling parity checking method to determine single bit error:
#   Local_buffer = parity_checking(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
#   data = memory[TRd_head][:]
#   # # Check if the parity bit is 0.
#   for i in range(0, len(Local_buffer)):
#     if i == 1:
#         # There is an error in the current bit.
#         # Correct the error by flipping the bit.
#         data[i][:] = 1 - data[i][:]
#
#     # Return the corrected data.
#     return data
'''