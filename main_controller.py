'''
Author : Pavia Bera - University of South Florida
This is a simulator for Domain wall memory (DWM)
DWM leverages the 'shift-register' nature of spintronic domain-wall memory (DWM).
Shift-based scheme utilizes a multi-nanowire approach to ensure that reads and writes
can be more effectively aligned with access ports for simultaneous access in the same cycle.
'''

import numpy as np
# Importing all
import WriteData as adt
import LogicOperation as logicop
import ArithmaticOperation as ao
from fault_modeling import f_percent_model
import config as config

class DBC():
    TRd_size = config.TRd_size
    bit_length = config.bit_length
    memory_size = config.memory_size
    fault_mode = config.fault_mode
    # Initializing single Local Buffer for all DBC's
    Local_row_buffer = [0] * (bit_length)

    def __init__(self, ):
        '''This is a single instance of DBC'''
        # self.fault = 3
        self.bit_length = DBC.bit_length - 1  #511
        self.memory_size = DBC.memory_size #32
        # self.padding_bits = int(self.memory_size / 2)
        self.TRd_head = int(0)
        self.TRd_tail = int(self.TRd_head + DBC.TRd_size - 1)
        # self.memory = [[('0') for _ in range(self.memory_size * 2)]for _ in range(self.bit_length)]

        self.memory = [[('0') for _ in range(self.bit_length+1)] for _ in range(self.memory_size)]




    def controller(self, write_port, instruction, nanowire_num_start_pos, nanowire_num_end_pos, data_hex = None):

        nanowire_num_start_pos = int(nanowire_num_start_pos)
        nanowire_num_end_pos = int(nanowire_num_end_pos)


        perform_param = dict()
        keys = ['write', 'TR_writes', 'read', 'TR_reads', 'shift', 'STORE']
        perform_param = {key: 0 for key in keys}

        row_number = int(write_port)
        # print('prev head, prev tail, row no:', self.TRd_head, self.TRd_tail, write_port)

        # if instruction == 'overwrite' or instruction == 'Read':
        if abs(self.TRd_head - row_number) < abs(self.TRd_tail - row_number) and row_number <= (self.memory_size - self.TRd_size):
            # Move TRd_head
            if self.TRd_head > row_number:
                diff = self.TRd_head - row_number
                self.TRd_head = self.TRd_head - diff
                self.TRd_tail = self.TRd_head + DBC.TRd_size - 1
                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 1 * diff
                perform_param['STORE'] += 0



            elif self.TRd_head < row_number:
                diff = row_number - self.TRd_head
                self.TRd_head = self.TRd_head + diff
                self.TRd_tail = self.TRd_head + DBC.TRd_size - 1
                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 1 * diff
                perform_param['STORE'] += 0

            else:
                self.TRd_head = row_number
                self.TRd_tail = self.TRd_head + DBC.TRd_size - 1
                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 0
                perform_param['STORE'] += 0


            self.TRd_head = int(self.TRd_head)
            self.TRd_tail = int(self.TRd_tail)
            # Call read or write at AP0
            if instruction == 'overwrite':
                instruction = 'W AP0'
            elif type(instruction) == int:
                instruction = str(instruction)
            elif instruction == 'Read':
                instruction = 'R AP0'
            elif 'SHL' in instruction or 'SHR' in instruction:
                instruction = instruction + ' ' +'AP0'
            elif instruction == 'CARRY':
                instruction = 'CARRY_AP0'
            elif instruction == 'CARRYPRIME':
                instruction = 'CARRYPRIME_AP0'




        elif abs(self.TRd_head - row_number) > abs(self.TRd_tail - row_number) and row_number >= (self.TRd_size-1):
            # Move TRd_tail
            if self.TRd_tail > row_number:
                diff = self.TRd_tail - row_number
                self.TRd_tail = self.TRd_tail - diff
                self.TRd_head = self.TRd_tail - DBC.TRd_size + 1

                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 1 * diff
                perform_param['STORE'] += 0

            elif self.TRd_tail < row_number:
                diff = row_number - self.TRd_tail
                self.TRd_tail = self.TRd_tail + diff
                self.TRd_head = self.TRd_tail - DBC.TRd_size + 1

                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 1 * diff
                perform_param['STORE'] += 0

            else:
                self.TRd_tail = row_number
                self.TRd_head = self.TRd_tail - DBC.TRd_size + 1

                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 0
                perform_param['STORE'] += 0


            self.TRd_head = int(self.TRd_head)
            self.TRd_tail = int(self.TRd_tail)
            # Call read or write at AP1
            if instruction == 'overwrite':
                instruction = 'W AP1'
            elif type(instruction) == int:
                instruction = str(instruction)
            elif instruction == 'Read':
                instruction = 'R AP1'
            elif 'SHL' in instruction or 'SHR' in instruction:
                instruction = instruction + ' ' + 'AP1'
            elif instruction == 'CARRY':
                instruction = 'CARRY_AP1'
            elif instruction == 'CARRYPRIME':
                instruction = 'CARRYPRIME_AP1'


        elif abs(self.TRd_head - row_number) == abs(self.TRd_tail - row_number) and row_number <= (self.memory_size - self.TRd_size):
            # if equal distance from AP0 and AP1 choose AP0
            diff = self.TRd_head - row_number
            # Cycles for shift
            cycles = + (diff * 2)
            self.TRd_head = self.TRd_head - diff
            self.TRd_tail = self.TRd_head + DBC.TRd_size - 1

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 1 * diff
            perform_param['STORE'] += 0


            # Call read or write at AP0
            if instruction == 'overwrite':
                instruction = 'W AP0'
            elif instruction == 'Read':
                instruction = 'R AP0'
            elif 'SHL' in instruction or 'SHR' in instruction:
                instruction = instruction + ' ' + 'AP0'
            elif instruction == 'CARRY':
                instruction = 'CARRY_AP0'
            elif instruction == 'CARRYPRIME':
                instruction = 'CARRYPRIME_AP0'

        else:
            if row_number < (self.TRd_size - 1):
                # Move TRd_head
                diff = self.TRd_head - row_number
                self.TRd_head = self.TRd_head - diff
                self.TRd_tail = self.TRd_head + DBC.TRd_size - 1
                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 1 * diff
                perform_param['STORE'] += 0

                self.TRd_head = int(self.TRd_head)
                self.TRd_tail = int(self.TRd_tail)
                # Call read or write at AP0
                if instruction == 'overwrite':
                    instruction = 'W AP0'
                elif type(instruction) == int:
                    instruction = str(instruction)
                elif instruction == 'Read':
                    instruction = 'R AP0'
                elif 'SHL' in instruction or 'SHR' in instruction:
                    instruction = instruction + ' ' + 'AP0'
                elif instruction == 'CARRY':
                    instruction = 'CARRY_AP0'
                elif instruction == 'CARRYPRIME':
                    instruction = 'CARRYPRIME_AP0'

            elif row_number > (self.memory_size - self.TRd_size):
                diff = self.TRd_tail - row_number
                self.TRd_tail = self.TRd_tail - diff
                self.TRd_head = self.TRd_tail - DBC.TRd_size + 1

                ## performance parameters
                perform_param['write'] += 0
                perform_param['TR_writes'] += 0
                perform_param['read'] += 0
                perform_param['TR_reads'] += 0
                perform_param['shift'] += 1 * diff
                perform_param['STORE'] += 0

                self.TRd_head = int(self.TRd_head)
                self.TRd_tail = int(self.TRd_tail)
                # Call read or write at AP1
                if instruction == 'overwrite':
                    instruction = 'W AP1'
                elif type(instruction) == int:
                    instruction = str(instruction)
                elif instruction == 'Read':
                    instruction = 'R AP1'
                elif 'SHL' in instruction or 'SHR' in instruction:
                    instruction = instruction + ' ' + 'AP1'
                elif instruction == 'CARRY':
                    instruction = 'CARRY_AP1'
                elif instruction == 'CARRYPRIME':
                    instruction = 'CARRYPRIME_AP1'


        if data_hex != None:
            # Convert hex data to bin
            data_hex_size = len(data_hex) * 4
            data_bin = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)
            
            for i in range(0, len(data_bin)):
                DBC.Local_row_buffer[i] = data_bin[i]

        # # Write instruction
        if (instruction == '1'):
            self.TRd_head = row_number
            # write at (left) TRd start loc and shift data right within the TRd space
            adt.writezero(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += (1)
            perform_param['read'] += 0
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param

        elif (instruction == '2'):
            self.TRd_head = row_number - DBC.TRd_size
            self.TRd_tail = row_number
            # write at (right) TRd end loc and shift data left within the TRd space.
            adt.writeone(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 1
            perform_param['read'] += 0
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param

        if (instruction == 'W AP0' ):
            # overwrite at left side (TRd start position)

            adt.overwrite_zero(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] = config.bit_length#1
            perform_param['TR_writes'] = 0
            perform_param['read'] = 0
            perform_param['TR_reads'] = 0
            perform_param['shift'] = config.bit_length -1
            perform_param['STORE'] = 0

            return perform_param

        elif (instruction == 'W AP1'):
            # overwrite at right side(TRd end position)
            # print('overwrite', self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            adt.overwrite_one(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] = config.bit_length#1
            perform_param['TR_writes'] = 0
            perform_param['read'] = 0
            perform_param['TR_reads'] = 0
            perform_param['shift'] = (config.bit_length - 1)
            perform_param['STORE'] = 0

            return perform_param

        elif (instruction == '3'):
            adt.writezero_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 1
            perform_param['read'] += 0
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param

        elif (instruction == '4'):
            # write at (left) TRd start and shift data towards the right padding.
            adt.writezero_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += (1)
            perform_param['read'] += 0
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param

        elif (instruction == '5'):
            # write at (right) TRd end and shift data towards left padding.
            adt.writeone_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 1
            perform_param['read'] += 0
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param

        elif (instruction == '6'):
            # write at (right) TRd end and shift data towards right padding.
            adt.writeone_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 1
            perform_param['read'] += 0
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param


        #Logical shift
        elif ('SHL' in instruction):
            command = (instruction.rsplit(' ', 2))
            n = int(command[1])
            local_buffer_count = 0
            if command[-1] == 'AP0':
                for i in range(n, self.bit_length):
                    DBC.Local_row_buffer[local_buffer_count] = self.memory[self.TRd_head][i]
                    local_buffer_count += 1



                for i in range(local_buffer_count, self.bit_length):
                    DBC.Local_row_buffer[i] = '0'

            else:
                for i in range(n, self.bit_length):
                    DBC.Local_row_buffer[local_buffer_count] = self.memory[self.TRd_tail][i]
                    local_buffer_count += 1
                for i in range(local_buffer_count, self.bit_length):
                    DBC.Local_row_buffer[i] = '0'



            # Converting binary data at TRd head to Hex for verification/visualization
            count = 0
            s = ''
            hex_num = '0x'

            for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
                s += str(DBC.Local_row_buffer[i])
                count += 1
                if count == 4:
                    num = int(s, 2)
                    string_hex_num = format(num, 'x')
                    hex_num += (string_hex_num)
                    s = ''
                    count = 0

            # print("local Buffer :", (hex_num))

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 1
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, hex_num




        elif ('SHR' in instruction):
            command = (instruction.rsplit(' ', 2))
            n = int(command[1])
            # print("n",n)
            local_buffer_count = n


            if command[-1] == 'AP0':
                for i in range(0, n):
                    DBC.Local_row_buffer[i] = '0'

                for i in range(0, self.bit_length-n ):
                    DBC.Local_row_buffer[local_buffer_count] = self.memory[self.TRd_head][i]
                    local_buffer_count += 1

            else:
                for i in range(0, n):
                    DBC.Local_row_buffer[i] = '0'

                for i in range(0, self.bit_length - n):
                    DBC.Local_row_buffer[local_buffer_count] = self.memory[self.TRd_tail][i]
                    local_buffer_count += 1

            # Converting binary data at TRd head to Hex for verification/visualization
            count = 0
            s = ''
            hex_num = '0x'
            # print(DBC.Local_row_buffer[i])
            for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
                # print(i)
                s += str(DBC.Local_row_buffer[i])
                count += 1
                if count == 4:
                    num = int(s, 2)
                    string_hex_num = format(num, 'x')
                    hex_num += (string_hex_num)
                    s = ''
                    count = 0
            # print("local Buffer :", hex_num)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 1
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, hex_num



        # # shift Instructions
        # elif (instruction == 'SR'):
        #     self.TRd_head += 1
        #     cycles = + 2
        #
        # elif (instruction == 'SL'):
        #     self.TRd_head -= 1
        #     cycles = + 2

        # Read instruction
        elif (instruction == 'R AP0' ):
            for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
                DBC.Local_row_buffer[i] = self.memory[self.TRd_head][i]

            # converting to Hex
            count = 0
            s = ''
            hex_num = '0x'

            for j in range(nanowire_num_start_pos, nanowire_num_end_pos ):
                s += str(self.memory[self.TRd_head][j])
                count += 1
                if count == 4:
                    num = int(s, 2)
                    string_hex_num = format(num, 'x')
                    hex_num += (string_hex_num)

                    s = ''
                    count = 0

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 1
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0


            return perform_param, hex_num

        elif (instruction == 'R AP1'):
            for i in range(nanowire_num_start_pos, nanowire_num_end_pos):
                DBC.Local_row_buffer[i] = self.memory[self.TRd_tail][i]

            # converting to Hex
            count = 0
            s = ''
            hex_num = '0x'

            for j in range(nanowire_num_start_pos, nanowire_num_end_pos):
                s += str(self.memory[self.TRd_tail][j])
                count += 1
                if count == 4:
                    num = int(s, 2)
                    string_hex_num = format(num, 'x')
                    hex_num += (string_hex_num)

                    s = ''
                    count = 0

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 1
            perform_param['TR_reads'] += 0
            perform_param['shift'] += 0
            perform_param['STORE'] += 0



            return perform_param, hex_num

        # # Counting carry bit's
        elif (instruction == 'CARRY_AP0'):
            Local_buffer = logicop.carry(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += 1
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif (instruction == 'CARRYPRIME_AP0'):
            Local_buffer = logicop.carry_prime(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += 1
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif (instruction == 'CARRY_AP1'):
            Local_buffer = logicop.carry(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += (1)
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif (instruction == 'CARRYPRIME_AP1'):
            Local_buffer = logicop.carry_prime(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += (1)
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        # Logic Operations
        elif (instruction == 'AND'):
            Local_buffer = logicop.And(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            # Modeling fault probabilities
            if config.fault_mode == True:
                # count number if ones between head and tail
                f_percent_model(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += (1)
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif instruction == 'NAND':
            Local_buffer = logicop.Nand(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            # Modeling fault probabilities
            if config.fault_mode == True:
                # count number if ones between head and tail
                f_percent_model(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += (1)
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif instruction == 'XOR':
            Local_buffer = logicop.Xor(self.memory, self.TRd_head,nanowire_num_start_pos, nanowire_num_end_pos)

            # Modeling fault probabilities
            if config.fault_mode == True:
                # count number if ones between head and tail
                f_percent_model(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] = 0
            perform_param['TR_writes'] = 0
            perform_param['read'] = config.bit_length
            # print(perform_param['read'])
            perform_param['TR_reads'] = 0#(1)
            perform_param['shift'] = config.bit_length - 1
            perform_param['STORE'] = 0

            return perform_param, Local_buffer

        elif instruction == 'XNOR':
            Local_buffer = logicop.Xnor(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            # Modeling fault probabilities
            if config.fault_mode == True:
                # count number if ones between head and tail
                f_percent_model(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] = 0
            perform_param['TR_writes'] = 0
            perform_param['read'] = 0
            perform_param['TR_reads'] = (1)
            perform_param['shift'] = 0
            perform_param['STORE'] = 0

            return perform_param, Local_buffer

        elif instruction == 'OR':
            Local_buffer = logicop.Or(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            # Modeling fault probabilities
            if config.fault_mode == True:
                # count number if ones between head and tail
                f_percent_model(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += (1)
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif instruction == 'NOR':
            Local_buffer = logicop.Nor(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            # Modeling fault probabilities
            if config.fault_mode == True:
                # count number if ones between head and tail
                f_percent_model(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += (1)
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif instruction == 'NOT':
            Local_buffer = logicop.Not(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            # Modeling fault probabilities
            if config.fault_mode == True:
                # count number if ones between head and tail
                f_percent_model(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 0
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += (1)
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        # Arithmatic operation (Addition and multiplication)
        elif instruction == 'ADD':
            Local_buffer = ao.addition(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 15
            perform_param['TR_writes'] += 0
            perform_param['read'] += 0
            perform_param['TR_reads'] += 8
            perform_param['shift'] += 0
            perform_param['STORE'] += 0

            return perform_param, Local_buffer

        elif instruction == 'MULT':
            Local_buffer = ao.multiply(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

            ## performance parameters
            perform_param['write'] += 8+4+15
            perform_param['TR_writes'] += 6
            perform_param['read'] += 8+7
            perform_param['TR_reads'] += 3+8
            perform_param['shift'] += 8+9
            perform_param['STORE'] += 0
            # perform_param['write'] += 33
            # perform_param['TR_writes'] += 7
            # perform_param['read'] += 22
            # perform_param['TR_reads'] += 11
            # perform_param['shift'] += 24
            # perform_param['STORE'] += 0

            return perform_param, Local_buffer

        #
        # elif instruction == 'PC':
        #     Local_buffer = sftFlt.parity_checking(self.memory, self.TRd_head,nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #     ## performance parameters
        #     perform_param['write'] += 0
        #     perform_param['TR_writes'] += 0
        #     perform_param['read'] += 0
        #     perform_param['TR_reads'] += (1)
        #     perform_param['shift'] += 0
        #     perform_param['STORE'] += 0
        #
        #     return perform_param, Local_buffer
        #
        #
        # # elif instruction == 'RS':
        # #     None
        # elif instruction == 'CS' or instruction == 'RS':
        #     Local_buffer = sftFlt.corrective_shift(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
        #     ## performance parameters
        #     perform_param['write'] += 0
        #     perform_param['TR_writes'] += 0
        #     perform_param['read'] += 0
        #     perform_param['TR_reads'] += (0)
        #     perform_param['shift'] += 0
        #     perform_param['STORE'] += 0
        #
        #
        #     return perform_param, Local_buffer
        #
