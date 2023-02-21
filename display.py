from tabulate import tabulate
import config as config

TRd_size = config.TRd_size
def display(memory,row_number, s):
    TRd_pos = (s)
    nanowire_num_start_pos = 0
    nanowire_num_end_pos = 511

    table = [['TRd', 'Row', 'Hex Data']]

    start = 0
    stop = 0
    TRd_head = 0
    TRd_tail = 0

    if TRd_pos == 'AP0':
        if row_number == 0:
            start = row_number
            stop = row_number + 8
            TRd_head = row_number
            TRd_tail = row_number + TRd_size - 1
        elif row_number == 1:
            start = row_number - 1
            stop = row_number + 7
            TRd_head = row_number
            TRd_tail = row_number + TRd_size - 1
        elif row_number >= 2:
            start = row_number - 2
            stop = row_number + 6
            TRd_head = row_number
            TRd_tail = row_number + TRd_size - 1


    elif TRd_pos == 'AP1' :
        if row_number == 31:
            start = row_number - 8
            stop = row_number
            TRd_head = row_number - TRd_size + 1
            TRd_tail = row_number
        elif row_number == 30:
            start = row_number - 7
            stop = row_number + 1
            TRd_head = row_number - TRd_size + 1
            TRd_tail = row_number
        elif row_number <= 29 and row_number >= 5:
            start = row_number - 6
            stop = row_number + 2
            TRd_head = row_number - TRd_size + 1
            TRd_tail = row_number
        elif row_number <= 5:
            start = 0
            stop = row_number + 2
            TRd_head = row_number - TRd_size + 1
            TRd_tail = row_number


    # print(start, stop+1,TRd_pos)

    # Converting bin to hex
    for i in range(start-1, stop+1  ):
        t = []
        count = 0
        s = ''
        hex_num = '0x'

        for j in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
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
