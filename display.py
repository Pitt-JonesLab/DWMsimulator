from tabulate import tabulate
import config as config

TRd_size = config.TRd_size
bit_length = config.bit_length
memory_size = config.memory_size
row_before_head = config.display_row_before_head
row_after_tail =  config.display_row_after_tail

def display(memory,row_number, s):

    TRd_pos = (s)
    nanowire_num_start_pos = 0
    nanowire_num_end_pos = bit_length

    table = [['TRd', 'Row', 'Hex Data']]

    start = 0
    stop = 0
    TRd_head = row_number
    TRd_tail = TRd_head + TRd_size - 1
    

    if TRd_pos == 'AP0':
        start = row_number + row_before_head
        stop = start + TRd_size + row_after_tail
        # if row_number == 0 :
        #     start = row_number
        #     stop = row_number + 8
        #     TRd_head = row_number
        #     TRd_tail = row_number + TRd_size - 1
        # elif row_number == 1:
        #     start = row_number - 1
        #     stop = row_number + 7
        #     TRd_head = row_number
        #     TRd_tail = row_number + TRd_size - 1
        # elif row_number >= 2:
        #     start = row_number - 2
        #     stop = row_number + 6
        #     TRd_head = row_number
        #     TRd_tail = row_number + TRd_size - 1
        # elif row_number == 0 :
        #     start = row_number
        #     stop = start + TRd_size
        #     TRd_head = row_number
        #     TRd_tail = row_number + TRd_size - 1



    elif TRd_pos == 'AP1' :
        start = row_number - TRd_size + row_before_head
        stop = start + TRd_size + row_after_tail
        # if row_number == 31:
        #     start = row_number - 8
        #     stop = row_number
        #     TRd_head = row_number - TRd_size + 1
        #     TRd_tail = row_number
        # elif row_number == 30:
        #     start = row_number - 7
        #     stop = row_number + 1
        #     TRd_head = row_number - TRd_size + 1
        #     TRd_tail = row_number
        # elif row_number <= 29 and row_number >= 5:
        #     start = row_number - 6
        #     stop = row_number + 2
        #     TRd_head = row_number - TRd_size + 1
        #     TRd_tail = row_number
        # elif row_number <= 5:
        #     start = 0
        #     stop = row_number + 2
        #     TRd_head = row_number - TRd_size + 1
        #     TRd_tail = row_number
        #
        #
        # elif row_number == 0 and bit_length <= 5:
        #     start = row_number
        #     stop = start + TRd_size
        #     TRd_head = row_number

    # print(start, stop+1,TRd_pos)
    # print(start, stop, bit_length)
    # Converting bin to hex
    for i in range(start, stop+1):

        t = []
        count = 0
        s = ''
        hex_num = '0x'

        for j in range(0, bit_length):
            s += str(memory[i][j])
            count += 1
            if count == 4:
                num = int(s, 2)
                string_hex_num = format(num, 'x')
                hex_num += (string_hex_num)

                s = ''
                count = 0
        # for j in range(44 + 1, nanowire_num_end_pos):
        #     hex_num += ('-')

        
        # Add to table
        if i == TRd_head:
            t = ['AP0', i, hex_num]
        elif i == TRd_tail:
            t = ['AP1', i, hex_num]
        else:
            t = [' ', i, hex_num]

        table.append(t)


    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
