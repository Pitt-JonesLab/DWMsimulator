'''
This is the script that uses the DWM simulator to run differrent algorithm.
'''
import SubByte as SB
from main_controller import DBC
# Calculate Cycle and Energy
total_energy = 0
total_cycles = 0
import config as config
TRd_size = config.TRd_size
bit_length = config.bit_length
memory_size = config.memory_size


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
    elif address >= 480 and address <= 511:
        DBC_number = 15
        row_number = address - 480

    return DBC_number, row_number


def call_DBC(dbc, row_number, operation, nanowire_start_pos, nanowire_end_pos, d=None):

    if operation == 'overwrite':
        param = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos, d)
        return param
    elif operation == 1 or operation == 2 or operation == 3 or operation == 4 or operation == 5 or operation == 6:
        param = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos, d)
        return param
    # elif operation == 'MULT':
    #     param, r = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos)
    #     return param, r
    else:
        # Calling DBC object for each instruction above
       
        param, data = dbc.controller(row_number, operation, nanowire_start_pos, nanowire_end_pos)
        return param, data


def write_type(dbcs, row_number_destination, write_type, nanowire_num_start_pos, nanowire_num_end_pos, data_hex):
    # print('write_type',write_type, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
    write_type = int(write_type)
    if write_type == 0:
        # Type 0: Write back normally
        # Call Write
     
        param = call_DBC(dbcs, row_number_destination, 'overwrite',  nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
    elif write_type >= 1 and  write_type <= 6:
        # Type 1: Transverse writes
        param = call_DBC(dbcs, row_number_destination, write_type, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)

    elif write_type == 7:
        raise Exception("Sorry, no operation for seven")


    return  param





##############################################################################################################################################################################################################################

# Parameter Table
perform_param = dict()
keys = ['write','TR_writes', 'read', 'TR_reads', 'shift', 'STORE']
perform_param = {key: 0 for key in keys}


# Creating 16 DBC objects
dbcs = [DBC() for i in range(16)]

#Reading Instruction of text file
instruction_file = open("Instruction Sets/test_mult.txt", "r")

# Read single line in file
lines = instruction_file.readlines()

# Extracting each instruction from Lines:
break_out_flag = False
stop_chars = [' #', '//']
for line in lines:
    if line.strip():
        instruction_line = []
        if line.startswith("//") or line.startswith("#"):
            continue  # Skip the line and move to the next iteration of the loop

        for word in line.split():
            if "//" in word or "#" in word:
                break
            else:
                instruction_line.append(word)


        # if instruction_line[0] == '#':
        #     continue
        print('instruction:', instruction_line)
        address_destination = instruction_line[1]
        address_destination = (address_destination.split("$", 1))
        address_destination = int(address_destination[1])
        DBC_number_destinantion, row_number_destination = get_adress(address_destination)
        print('Destinantion DBC No:', DBC_number_destinantion)
        print('Destinantion Row No:', row_number_destination)


        if '$' in instruction_line[2]:
            address_source = instruction_line[2]
            address_source = (address_source.split("$", 1))
            address_source = (address_source[1])
            address_source = int(address_source)
            DBC_number_source, row_number_source = get_adress(address_source)
            print('Source DBC No:', DBC_number_source)
            print('Source Row No:', row_number_source)

            # if instruction_line[0] == 'WRITE':
            # Calling read functionx
            param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, 'Read', 0, bit_length, None)
            # perform_param['write'] += param_table['write']
            # perform_param['TR_writes'] += param_table['TR_writes']
            # print('here', perform_param['read'])
            # perform_param['read'] += param_table['read']
            # print('here', perform_param['read'])
            # perform_param['TR_reads'] += param_table['TR_reads']
            # perform_param['shift'] += param_table['shift']
            # perform_param['STORE'] += param_table['STORE']

            data_hex = data[2:]
            nanowire_num_start_pos = 0
            nanowire_num_end_pos = bit_length


        else:
            data = instruction_line[2]
            data_hex = data[2:]
            nanowire_num_start_pos = 0
            nanowire_num_end_pos = bit_length


        # append trailing zeros
        if (len(data_hex) != (memory_size)//4):
        # mask data_hex with zeros:
            N = ((memory_size)//2) - len(data_hex)
            data_hex = data_hex.ljust(N + len(data_hex), '0')


        
        # instructions for CPIM operations
        if instruction_line[0] == 'CPIM':
            if instruction_line[3] == 'COPY':
                # call Transverse Write
                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, bit_length, data_hex)

                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

            elif instruction_line[3] == 'STORE':
                # call read and then write
                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, bit_length, data_hex)

                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += (param_table['STORE'] + 1)


            elif 'SHL' in instruction_line[3] or 'SHR' in instruction_line[3]:
                i = instruction_line[3]
                instruction = ''
                instruction = i[:3] + ' ' + i[3:]
                # call operations
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                data_hex = data[2:]
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']



                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, bit_length, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

            elif instruction_line[3] == 'CARRY' or instruction_line[3] == 'CARRYPRIME':
                # call operations
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction_line[3], 0, bit_length)
                data_hex = data[2:]
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']


                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, bit_length, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']


            elif instruction_line[3] == 'ADD':
                bit_no = instruction_line[4]
                # call operations
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction_line[3], 0, instruction_line[4])
                data_hex = data[2:]
                total_energy += 512*(0.504676821+0.000958797)+512*0.1+(512-64)*0.1+(512-128)*0.1
                total_cycles += (8*((9+4+4)) + 8*(9+4+4+4) + 7*(9+4+4+4))
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']
                # print(perform_param)


                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, bit_length, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

                
            elif instruction_line[3] == 'MULT':
                
                A_zeros = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                # Read B at location instruction_line[3]

                # shift A for length of A
                bit_no = int(instruction_line[4])

                #read the locations provided and move data to DBC 15(dedicted for multiplication) at row 481.
                # write instruction are clubed read and writes
                # [CPIM $481 source address STORE 512 0] 
                # param_table = write_type(dbcs[15], 1, 0, 0, bit_length, data_hex)
                # print(data_hex)

                # Read parameter A in DBC 15
                #Calling read functionx
                # assuming data is stored in DBC 15
                DBC_number_mult = 15
                row_number_mult = 0
                param_table, B = call_DBC(dbcs[DBC_number_mult], row_number_mult, 'Read', 0, bit_length, None)
                B = B[2:]
                # Convert hex data to bin
                data_hex_size = int(bit_no/4)
                B = (bin(int(B, 16))[2:]).zfill(data_hex_size)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']

                

                # Convert hex data to bin
                # data_hex_size = int(bit_no/4)
                # A = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)
                # print(len(A))
                A = data_hex
               
                # for i in range(0, int(bit_no)):
                if (int(B[0]) == 1):
                    # write A with no shift
                    DBC_number_mult = 15
                    row_number_mult = 1
                    
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                else:
                    # Put A = 00000000
                    
                    DBC_number_mult = 15
                    row_number_mult = 1
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A_zeros)
                    
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                if (int(B[1]) == 1):
                    # write A with SHR1
                    # shift A SHR1
                    DBC_number_mult = 15
                    row_number_mult = 2
                    instruction = ''
                    instruction = 'SHR' + ' ' + '1'
                    # call operations
                    param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                    data_hex = data[2:]
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                    # write shifted A
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                else:
                    # Put A = 00000000
                    
                    DBC_number_mult = 15
                    row_number_mult = 2
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A_zeros)
                    
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']




                if (int(B[2]) == 1):
                    # write A with SHR2
                    # shift A SHR2
                    DBC_number_mult = 15
                    row_number_mult = 3
                    instruction = ''
                    instruction = 'SHR' + ' ' + '2'
                    # call operations
                    param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                    data_hex = data[2:]
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                    # write shifted A
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                else:
                    # Put A = 00000000
                    
                    
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A_zeros)
                   
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                if (int(B[3]) == 1):
                    # write A with SHR3
                    # shift A SHR3
                    DBC_number_mult = 15
                    row_number_mult = 4
                    instruction = ''
                    instruction = 'SHR' + ' ' + '3'
                    # call operations
                    param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                    data_hex = data[2:]
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                    # write shifted A
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']
                else:
                    # Put A = 00000000
                    DBC_number_mult = 15
                    row_number_mult = 4
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A_zeros)
                    
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                if (int(B[4]) == 1):
                    # write A with SHR4
                    # shift A SHR4
                    instruction = ''
                    instruction = 'SHR' + ' ' + '4'
                    # call operations
                    param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                    data_hex = data[2:]
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                    # write shifted A
                    DBC_number_mult = 15
                    row_number_mult = 5
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']
                else:
                    # Put A = 00000000
                    DBC_number_mult = 15
                    row_number_mult = 5
                    param_table = write_type(dbcs[15], 1, 0, 0, bit_length, A)
                    param_table = write_type(dbcs[15], i, 0, 0, bit_length, mask_zeros)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                if (int(B[5]) == 1):
                    ## write A with SHR5
                    # shift A SHR5
                    instruction = ''
                    instruction = 'SHR' + ' ' + '5'
                    # call operations
                    param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                    data_hex = data[2:]
                    # print("shifted hex data SH5 = ",data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                    # write shifted A
                    DBC_number_mult = 15
                    row_number_mult = 6
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                else:
                    # Put A = 00000000
                    # write shifted A
                    DBC_number_mult = 15
                    row_number_mult = 6
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A_zeros)
                    
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                if (int(B[6]) == 1):
                    # write A with SHR5
                    # shift A SHR5
                    instruction = ''
                    instruction = 'SHR' + ' ' + '6'
                    # call operations
                    param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                    data_hex = data[2:]
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                    # write shifted A
                    DBC_number_mult = 15
                    row_number_mult = 7
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']
                
                else:
                    # Put A = 00000000
                     # write shifted A
                    DBC_number_mult = 15
                    row_number_mult = 7
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A_zeros)
                    
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                if (int(B[7]) == 1):
                    # write A with SHR5
                    # shift A SHR5
                    instruction = ''
                    instruction = 'SHR' + ' ' + '7'
                    # call operations
                    param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction, 0, bit_length)
                    data_hex = data[2:]
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']


                    # write shifted A
                    DBC_number_mult = 15
                    row_number_mult = 8
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, data_hex)
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']
                else:
                    # Put A = 00000000
                    DBC_number_mult = 15
                    row_number_mult = 8
                    param_table = write_type(dbcs[DBC_number_mult], row_number_mult, 0, 0, bit_length, A_zeros)
                    
                    perform_param['write'] += param_table['write']
                    perform_param['TR_writes'] += param_table['TR_writes']
                    perform_param['read'] += param_table['read']
                    perform_param['TR_reads'] += param_table['TR_reads']
                    perform_param['shift'] += param_table['shift']
                    perform_param['STORE'] += param_table['STORE']

                   

                # call mult operations
                param_table, data = call_DBC(dbcs[15], 0, instruction_line[3], 0, instruction_line[4])
                data_hex = data[2:]
                
                total_energy += (512 * (0.504676821 + 0.000958797) + 512 * 0.1 + (512 - 64) * 0.1 + (512 - 128) * 0.1) +  512*(6*(0.3) + 8*(0.1) + 8*(0.7) + 8*(0.3) + 7*(0.3) + 3*(0.504676821) + 3*(0.1) + 2*(0.3) + 3*(0.7) + 3*(0.3) + 1*(0.3) + 4*(0.3) + 4*(0.7))
                total_cycles += (8*((9+4+4)) + 8*(9+4+4+4) + 7*(9+4+4+4)) + 6*(2) + 8*(9+4+4+4) + 8*(9+4+4) + 8*(2) + 7*(2) + 3*(9+4+4) + 3*(9+4+4+4) + 2*(2) + 3*(9+4+4) + 3*(9+4+4+4+2) + 1*(2) + 4*(9+4+4+4+2) + 4*(9+4+4)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']
                
                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, bit_length, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']



            # ## Calculating shifting faults
            # elif instruction_line[3] == 'PC':
            #     # call operations
            #     param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, 'PC', 0, bit_length)
            #     data_hex = data[2:]
            #     perform_param['write'] += param_table['write']
            #     perform_param['TR_writes'] += param_table['TR_writes']
            #     perform_param['read'] += param_table['read']
            #     perform_param['TR_reads'] += param_table['TR_reads']
            #     perform_param['shift'] += param_table['shift']
            #     perform_param['STORE'] += param_table['STORE']
            #
            #     param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0,
            #                              bit_length,
            #                              data_hex)
            #     perform_param['write'] += param_table['write']
            #     perform_param['TR_writes'] += param_table['TR_writes']
            #     perform_param['read'] += param_table['read']
            #     perform_param['TR_reads'] += param_table['TR_reads']
            #     perform_param['shift'] += param_table['shift']
            #     perform_param['STORE'] += param_table['STORE']
            #
            # elif instruction_line[3] == 'RS':
            #     None
            # elif instruction_line[3] == 'CS':
            #     # call operations
            #     param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, 'CS', 0, bit_length)
            #     data_hex = data[2:]
            #     perform_param['write'] += param_table['write']
            #     perform_param['TR_writes'] += param_table['TR_writes']
            #     perform_param['read'] += param_table['read']
            #     perform_param['TR_reads'] += param_table['TR_reads']
            #     perform_param['shift'] += param_table['shift']
            #     perform_param['STORE'] += param_table['STORE']
            #
            #     param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0,
            #                              bit_length,
            #                              data_hex)
            #     perform_param['write'] += param_table['write']
            #     perform_param['TR_writes'] += param_table['TR_writes']
            #     perform_param['read'] += param_table['read']
            #     perform_param['TR_reads'] += param_table['TR_reads']
            #     perform_param['shift'] += param_table['shift']
            #     perform_param['STORE'] += param_table['STORE']

            else:
                # call operations for logic operands
                param_table, data = call_DBC(dbcs[DBC_number_source], row_number_source, instruction_line[3], 0, bit_length - 1)
                data_hex = data[2:]
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']


                # call write function:
                param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[5], 0, bit_length, data_hex)
                perform_param['write'] += param_table['write']
                perform_param['TR_writes'] += param_table['TR_writes']
                perform_param['read'] += param_table['read']
                perform_param['TR_reads'] += param_table['TR_reads']
                perform_param['shift'] += param_table['shift']
                perform_param['STORE'] += param_table['STORE']






        elif  instruction_line[0] == 'SubByte':
            # read bits
            read_bits = ''
            for i in range(2,int(instruction_line[3]) + 2, 2):
                dec = (data_hex[i-2:i])
                dec = int(dec,16)
                sbox_val = SB.subBytes(dec)
                # convert to decimal number
                hex_data = hex(sbox_val)
                read_bits += (str(hex_data[2:]).zfill(2))


            # mask data_hex with zeros:
            N = 128 - len(read_bits)
            read_bits = read_bits.ljust(N + len(read_bits), '0')
            param_table = write_type(dbcs[DBC_number_destinantion], row_number_destination, instruction_line[4], 0, 4*int(instruction_line[3]), read_bits)

            perform_param['write'] += param_table['write']
            perform_param['TR_writes'] += param_table['TR_writes']
            perform_param['read'] += param_table['read']
            perform_param['TR_reads'] += param_table['TR_reads']
            perform_param['shift'] += param_table['shift']
            perform_param['STORE'] += param_table['STORE']









        # Close opened file
        instruction_file.close()


total_energy += perform_param['write'] * (bit_length)* 0.1
total_energy += perform_param['TR_writes'] * 0.3 *(bit_length)
total_energy += perform_param['read'] * 0.7 * (bit_length)
total_energy += perform_param['TR_reads'] * 0.504676821*bit_length
total_energy += perform_param['shift'] * 0.3 * (bit_length)
total_energy += perform_param['STORE'] * 0
total_energy += perform_param['TR_reads'] * 0.000958797 * (bit_length) #TODO: check pim energy


total_cycles += perform_param['write'] * (9+4+4+4)
total_cycles += perform_param['TR_writes'] * (2+9+4+4+4)
total_cycles += perform_param['read'] * (9+4+4)
total_cycles += perform_param['TR_reads'] * (9+4+4)
total_cycles += perform_param['shift'] * 2
total_cycles += perform_param['STORE'] * (10) #TODO: check STORE cycles



print(perform_param)

print('The total_cycles and  total_energy is :',total_cycles,'and', total_energy)




