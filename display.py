from texttable import Texttable
import numpy as np


def display(memory,row_number):
    padding_bit = 16
    nanowire_num_start_pos = 0
    nanowire_num_end_pos = 511

    start = row_number - 4
    stop = start + 8


    t = Texttable()
    hex_memory = []

    # Converting bin to hex
    count = 0
    s = ''
    hex_num = '0x'
    for j in range(start, stop):
        for i in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
            s += str(memory[i][row_number])
            count += 1
            if count == 4:
                num = int(s, 2)
                string_hex_num = format(num, 'x')
                hex_num += (string_hex_num)
                s = ''
                count = 0
    hex_num = (hex_num[2:31])
    print(hex_num)
    # Add to table
    t.add_rows([hex_num])

    # print(t.draw())