from tabulate import tabulate


def display(memory,row_number):

    nanowire_num_start_pos = 0
    nanowire_num_end_pos = 511

    table = [['Row', 'Hex Data']]

    # Converting bin to hex
    for i in range(row_number-4, row_number+3):
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
        t = [i-16, hex_num]
        table.append(t)

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
