'''
This is the script that uses the DWM simulator to run differrent algorithm.
'''

from main_controller import DBC


def get_adress(address):

    if address <= 31:
        DBC_number = 0
        row_number = address
    elif address >= 32 and address <= 63:
        DBC_number = 1
        row_number = address - 32
    elif address >= 64 and address <= 95:
        DBC_number = 2
        row_number = address - 64
    elif address >= 96 and address <= 127:
        DBC_number = 3
        row_number = address - 96
    elif address >= 128 and address <= 159:
        DBC_number = 4
        row_number = address - 128
    elif address >= 160 and address <= 191:
        DBC_number = 5
        row_number = address - 160
    elif address >= 192 and address <= 223:
        DBC_number = 6
        row_number = address - 192
    elif address >= 224 and address <= 255:
        DBC_number = 7
        row_number = address - 224
    elif address >= 256 and address <= 287:
        DBC_number = 8
        row_number = address - 256
    elif address >= 288 and address <= 319:
        DBC_number = 9
        row_number = address - 288
    elif address >= 320 and address <= 351:
        DBC_number = 10
        row_number = address - 320
    elif address >= 352 and address <= 383:
        DBC_number = 11
        row_number = address - 352
    elif address >= 384 and address <= 415:
        DBC_number = 12
        row_number = address - 384
    elif address >= 416 and address <= 447:
        DBC_number = 13
        row_number = address - 416
    elif address >= 448 and address <= 479:
        DBC_number = 14
        row_number = address - 448
    elif address >= 478 and address <= 509:
        DBC_number = 15
        row_number = address - 478

    return DBC_number, row_number


def call_DBC(dbc, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, d):
    if operation == 'Read' or 'SHL' in  operation or 'SHR' in operation:
        # Calling DBC object for each instruction above
        cycles, energy, data = dbc.controller(row_number, operation,nanowire_num_start_pos,nanowire_num_end_pos, d)
        return cycles, energy, data
    else:
        cycles, energy = dbc.controller(row_number, operation, nanowire_num_start_pos,nanowire_num_end_pos, d)
        return cycles, energy




# Creating 16 DBC objects
dbcs = [DBC() for i in range(16)]

total_cycles = 0
total_energy = 0

#Reading Instruction of text file
instruction_file = open("/Users/paviabera/Desktop/intruction set/AES/AES_instruction_set.txt", "r")

# Read single line in file
lines = instruction_file.readlines()

# Extracting each instruction from Lines:
for line in lines:
    instruction_line = []
    for word in line.split():
        if word == '#':
            continue
        instruction_line.append(word)
    print('instruction:', instruction_line)
    address_destination = instruction_line[1]
    address_destination = (address_destination.split("$", 1))
    address_destination = int(address_destination[1])
    DBC_number_destinantion, row_number_destination = get_adress(address_destination)


    if '$' in instruction_line[2]:
        address_source = instruction_line[2]
        address_source = (address_source.split("$", 1))
        address_source = (address_source[1])
        address_source = int(address_source)
        DBC_number_source, row_number_source = get_adress(address_source)
        #Calling read function
        cycles, energy, data = call_DBC(dbcs[DBC_number_source], row_number_source, 'Read', 0, 511, None)
        data_hex = data[2:]
        nanowire_num_start_pos = 0
        nanowire_num_end_pos = 511
        total_cycles += cycles
        total_energy += energy

    else:
        data = instruction_line[2]
        data_hex = data[2:]
        nanowire_num_start_pos = 0
        nanowire_num_end_pos = len(data_hex)*4



    # instructions for write operations
    if instruction_line[0] == 'WRITE':
        # Call Write
        cycles, energy = call_DBC(dbcs[DBC_number_destinantion], row_number_destination, 'overwrite', nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
        total_energy += energy


    # instructions for CPIM operations
    elif instruction_line[0] == 'CPIM':
        if instruction_line[3] == 'WRITE':
            # call Transverse Write
            cycles, energy = call_DBC(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5],nanowire_num_start_pos, nanowire_num_end_pos,data_hex)
            total_cycles += cycles
            total_energy += energy

        else:
            if instruction_line[3] == 'SHL' or instruction_line[3] == 'SHR':
                instruction = instruction_line[3] + ' ' + instruction_line[4]
                # call operations
                cycles, energy, data = call_DBC(dbcs[DBC_number_destinantion], row_number_destination, instruction, nanowire_num_start_pos,nanowire_num_end_pos,  data_hex)
                data_hex = data[2:]
                total_cycles += cycles
                total_energy += energy


            # call write function:
            # cycles, energy = call_DBC(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], nanowire_num_start_pos, nanowire_num_end_pos,  data_hex)
            # total_cycles += cycles
            # total_energy += energy
    # Close opened file
    instruction_file.close()

# print('The total_cycles and  total_energy is :',total_cycles, total_energy)
#




