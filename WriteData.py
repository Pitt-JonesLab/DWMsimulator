''' This file write's data to DWM Memory depending on the write instrucion'''

TRd_size = 4

def writezero(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    for i in range(writeport + TRd_size - 1, writeport, -1):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i - 1][nanowire_num_start_pos:nanowire_num_end_pos]

    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1

def writeone(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    # Shifting data left by 1 position
    for i in range(writeport - TRd_size + 1, writeport):
        memory[i][nanowire_num_start_pos:nanowire_num_end_pos] = memory[i + 1][nanowire_num_start_pos:nanowire_num_end_pos]

    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1

def overwrite(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer):
    writeport = int(row_number) + 16
    nanowire_num_start_pos = int(nanowire_num_start_pos)
    nanowire_num_end_pos = int(nanowire_num_end_pos)

    memory[writeport][nanowire_num_start_pos:nanowire_num_end_pos] = Local_row_buffer[nanowire_num_start_pos:nanowire_num_end_pos]

    return 1



# def shift_writezero(memory, data_in_binary):
#     # write at (right) TRd end and shift data towards right padding.
#     # data_in_binary = ''.join(format(ord(x), 'b') for x in data)
#
#     writeport = int(L/2)
#     memory[writeport] = data_in_binary
#
#     return 1
#
# def shift_writeone(memory, data_in_binary):
#     # write at (right) TRd end and shift data towards right padding.
#     # data_in_binary = ''.join(format(ord(x), 'b') for x in data)
#
#     writeport = int(L + L/2)
#     memory[writeport] = data_in_binary
#
#     print(memory)
#
#     return 1



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

    return 1


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

    return 1

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

    return 1

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

    return 1

