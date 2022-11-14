''' This file write's data to DWM Memory depending on the write instrucion'''
from display import display

TRd_size = 5

def writezero(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number)
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)


    # Shifting the data within the TRd space to right and writing at the TRd head
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
        for j in range(writeport + TRd_size - 1, writeport, -1):
            memory[i][j] = memory[i][j-1]

    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos):

        memory[i][writeport] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    # Converting bin to hex
    n = memory[:][writeport]
    n = "".join([str(item) for item in n])
    # convert binary to int
    num = int(n, 2)
    # convert int to hexadecimal
    hex_num = hex(num)
    print('TW AP0 =  ', (hex_num))

    return 1, 0.504676821

def writeone(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number) + TRd_size - 1
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)


    # Shifting the data within the TRd space to left and writing at the TRd tail
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        for j in range(writeport - TRd_size + 1, writeport):
            memory[i][j] = memory[i][j+1]

    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        memory[i][writeport] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    # Converting bin to hex
    n = memory[:][writeport]
    n = "".join([str(item) for item in n])
    # convert binary to int
    num = int(n, 2)
    # convert int to hexadecimal
    hex_num = hex(num)
    print('TW AP1 =  ', (hex_num))

    return 1, 0.504676821

def overwrite_zero(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    # print(row_number)
    writeport = int(row_number)
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Overwriting at the TRd head or tail
    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        memory[i][writeport] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    # Converting bin to hex
    count = 0
    s = ''
    hex_num = '0x'
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        s += str(memory[i][writeport])
        count += 1
        if count == 4:
            num = int(s, 2)
            string_hex_num = format(num, 'x')
            hex_num += (string_hex_num)
            s = ''
            count = 0

    # print("Write AP0 =  ", hex_num)
    arr = np.zeros([8, 32], dtype=object)
    hex_num = (hex_num[2:31])
    x = int((row_number - 16)/4 - 1)
    for i in range(0, len(hex_num)):
        arr[0][i] = hex_num[i]

        # arr =  np.array[hex_num]

    print(arr)


    return 1, 0.1

def overwrite_one(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    # print(row_number)
    writeport = int(row_number)
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Overwriting at the TRd head or tail
    local_buff_start = nanowire_num_start_pos
    for i in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
        memory[writeport][i] = Local_row_buffer[local_buff_start]
        local_buff_start += 1

    display(memory,row_number)

    return 1, 0.1


def writezero_shiftLE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (left) TRd start and shift data towards the left padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data left by 1 position towards left extremity
    start = 0
    for i in range(start, writeport):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i + 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821


def writezero_shiftRE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (left) TRd start and shift data towards the right padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data right by 1 position towards the right extremity.
    start = int(2*32)
    for i in range(start, writeport, -1):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i - 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821

def writeone_shiftLE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (right) TRd end and shift data towards left padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data left by 1 position
    start = 0
    for i in range(start, writeport):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i + 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821

def writeone_shiftRE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    #write at (right) TRd end and shift data towards right padding.
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data left by 1 position
    start = int(2*32)
    for i in range(start, writeport, -1):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i - 1][nanowire_num_start_pos:nanowire_num_end_pos]
    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1, 0.504676821

