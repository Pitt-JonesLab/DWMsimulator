
import LogicOperation as logicop


TRd_size = 5
# Initializing single Local Buffer for all DBC's
Local_row_buffer = [0] * (512)

def addition(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos):
    TRd_head = int(row_number)
    TRd_end_loc = TRd_head + TRd_size - 1

    mem = []
    sum = ''
    carry = ''
    carry_prime = ''

    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):

            if i == 0:
                cycle, energy, sum =logicop.Xor(memory, TRd_head, 0, 0)
                carry =
                carry_prime =
            if i == 1:
                sum =
                carry =
                carry_prime =
            else:
                # calculate the
                sum =
                carry =
                carry_prime =

                memory[0 ][j] =











    # Converting binary data at TRd head to Hex for verification/visualization
    # count = 0
    # s = ''
    # hex_num = []
    # for i in range(0, len(mem)):
    #     s += str(mem[i])
    #     count += 1
    #     if count == 4:
    #         num = int(s, 2)
    #         hex_num.append(hex(num))
    #         s = ''
    #         count = 0
    # print('AND ', hex_num)

    return 1, mem



def add_xor():

    None
