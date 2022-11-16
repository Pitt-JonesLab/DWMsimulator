from tabulate import tabulate

TRd_size = 5
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
        start = row_number - 2
        stop = row_number + 7
        TRd_head = row_number
        TRd_tail = row_number + TRd_size

    elif TRd_pos == 'AP1':
        start = row_number - 7
        stop = row_number + 2
        TRd_head = row_number - TRd_size
        TRd_tail = row_number

    # Converting bin to hex
    for i in range(start, stop):
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


        # Add to table
        if i == TRd_head:
            t = ['AP0', i-16, hex_num]
        elif i == TRd_tail:
            t = ['AP1', i-16, hex_num]
        else:
            t = [' ', i-16, hex_num]

        table.append(t)


    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
