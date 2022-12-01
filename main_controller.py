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


class DBC():
    TRd_size = 5
    # Initializing single Local Buffer for all DBC's
    Local_row_buffer = [0] * (512)

    def __init__(self, ):
        '''This is a single instance of DBC'''
        self.bit_length = 512
        self.memory_size = 32
        # self.padding_bits = int(self.memory_size / 2)
        self.TRd_head = int(0)
        self.TRd_tail = int(self.TRd_head + DBC.TRd_size - 1)
        # self.memory = [[('0') for _ in range(self.memory_size * 2)]for _ in range(self.bit_length)]

        self.memory = [[('0') for _ in range(self.bit_length)] for _ in range(self.memory_size)]



    def controller(self, write_port, instruction, nanowire_num_start_pos = 0, nanowire_num_end_pos = 511, data_hex = None):
        nanowire_num_start_pos = int(nanowire_num_start_pos)
        nanowire_num_end_pos = int(nanowire_num_end_pos)

        energies = 0
        cycles = 0

        row_number = int(write_port)
        print('prev head, prev tail, row no:', self.TRd_head, self.TRd_tail, write_port)

        # if instruction == 'overwrite' or instruction == 'Read':
        if abs(self.TRd_head - row_number) < abs(self.TRd_tail - row_number) and self.TRd_head <= (self.memory_size - self.TRd_size):
            # Move TRd_head
            if self.TRd_head > row_number:
                diff = self.TRd_head - row_number
                # Cycles for shift
                cycles = + (diff * 2)
                self.TRd_head = self.TRd_head - diff
                self.TRd_tail = self.TRd_head + DBC.TRd_size - 1
            elif self.TRd_head < row_number:
                diff = row_number - self.TRd_head
                # Cycles for shift
                cycles = + (diff * 2)
                self.TRd_head = self.TRd_head + diff
                self.TRd_tail = self.TRd_head + DBC.TRd_size - 1
            else:
                self.TRd_head = row_number
                self.TRd_tail = self.TRd_head + DBC.TRd_size - 1

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




        elif abs(self.TRd_head - row_number) > abs(self.TRd_tail - row_number) and self.TRd_tail >= (self.TRd_size-1):
            # Move TRd_tail
            if self.TRd_tail > row_number:
                diff = self.TRd_tail - row_number
                # Cycles for shift
                cycles = + (diff * 2)
                self.TRd_tail = self.TRd_tail - diff
                self.TRd_head = self.TRd_tail - DBC.TRd_size + 1

            elif self.TRd_tail < row_number:
                diff = row_number - self.TRd_tail
                # Cycles for shift
                cycles = + (diff * 2)
                self.TRd_tail = self.TRd_tail + diff
                self.TRd_head = self.TRd_tail - DBC.TRd_size + 1

            else:
                self.TRd_tail = row_number
                self.TRd_head = self.TRd_tail - DBC.TRd_size + 1


            self.TRd_head = int(self.TRd_head)
            self.TRd_tail = int(self.TRd_tail)
            # Call read or write at AP1
            if instruction == 'overwrite':
                instruction = 'W AP1'
            elif type(instruction) == int:
                instruction = str(instruction)
            elif instruction == 'Read':
                instruction = 'R AP1'
            elif 'SHL' or 'SHR' in instruction:
                instruction = instruction + ' ' + 'AP1'
            elif instruction == 'CARRY':
                instruction = 'CARRY_AP1'
            elif instruction == 'CARRYPRIME':
                instruction = 'CARRYPRIME_AP1'


        elif abs(self.TRd_head - row_number) == abs(self.TRd_tail - row_number):
            # if equal distance from AP0 and AP1 choose AP0
            diff = self.TRd_head - row_number
            # Cycles for shift
            cycles = + (diff * 2)
            self.TRd_head = self.TRd_head - diff
            self.TRd_tail = self.TRd_head + DBC.TRd_size - 1
            # Call read or write at AP0
            if instruction == 'overwrite':
                instruction = 'W AP0'
            elif instruction == 'Read':
                instruction = 'R AP0'
            elif 'SHL' or 'SHR' in instruction:
                instruction = instruction + ' ' + 'AP0'
            elif instruction == 'CARRY':
                instruction = 'CARRY_AP0'
            elif instruction == 'CARRYPRIME':
                instruction = 'CARRYPRIME_AP0'



        if data_hex != None:
            # Convert hex data to bin
            data_hex_size = len(data_hex) * 4
            data_bin = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)


            # DBC.Local_row_buffer = list(DBC.Local_row_buffer)
            # # s[1] = "_"
            # # s = "".join(s)
            # print(len(data_bin), len(DBC.Local_row_buffer))
            for i in range(0, len(data_bin)):
                DBC.Local_row_buffer[i] = data_bin[i]



            # for idx, item in enumerate(data_bin):
            #     DBC.Local_row_buffer[idx] = item
            # print(DBC.Local_row_buffer)

        # print('TRd_head', self.TRd_head)
        # print('TRd_tail', self.TRd_tail)

        # # Write instruction
        if (instruction == '1'):
            self.TRd_head = row_number
            # write at (left) TRd start loc and shift data right within the TRd space
            cycle, energy = adt.writezero(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle
            energies = + energy
            return cycles, energies

        elif (instruction == '2'):
            self.TRd_head = row_number - DBC.TRd_size
            self.TRd_tail = row_number
            # write at (right) TRd end loc and shift data left within the TRd space.
            cycle, energy = adt.writeone(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle
            energies = + energy
            return cycles, energies

        if (instruction == 'W AP0' ):
            # overwrite at left side (TRd start position)
            cycle, energy = adt.overwrite_zero(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle
            energies = + energy
            return cycles, energies

        elif (instruction == 'W AP1'):
            # overwrite at right side(TRd end position)
            cycle, energy = adt.overwrite_one(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle
            energies = + energy
            return cycles, energies

        # elif (instruction == '3'):
        #     # write at (left) TRd start and shift data towards the left padding.
        #     cycle,energy = adt.writezero_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
        #     cycles = + cycle
        #     energies = + energy
        #     return cycles, energies
        # elif (instruction == '4'):
        #     # write at (left) TRd start and shift data towards the right padding.
        #     cycle, energy = adt.writezero_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
        #     cycles = + cycle
        #     energies = + energy
        #     return cycles, energies
        # elif (instruction == '5'):
        #     # write at (right) TRd end and shift data towards left padding.
        #     cycle, energy = adt.writeone_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
        #     cycles = + cycle
        #     energies = + energy
        #     return cycles, energies
        # elif (instruction == '6'):
        #     # write at (right) TRd end and shift data towards right padding.
        #     cycle,energy = adt.writeone_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
        #     cycles =+ cycle
        #     energies = + energy
        #     return cycles, energies


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


            cycles = + 1
            energies = + 1
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

            print("local Buffer :", (hex_num))
            return cycles, energies, hex_num




        elif ('SHR' in instruction):
            command = (instruction.rsplit(' ', 2))
            n = int(command[1])
            local_buffer_count = n

            if command[-1] == 'AP0':
                for i in range(0, n):
                    DBC.Local_row_buffer[i] = '0'
                print(local_buffer_count, self.bit_length)
                for i in range(0, self.bit_length-n):
                    DBC.Local_row_buffer[local_buffer_count] = self.memory[self.TRd_head][i]
                    local_buffer_count += 1

            else:
                for i in range(0, n):
                    DBC.Local_row_buffer[i] = '0'

                for i in range(0, self.bit_length - n):
                    DBC.Local_row_buffer[local_buffer_count] = self.memory[self.TRd_tail][i]
                    local_buffer_count += 1
            cycles = + 1
            energies = + 1
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
            print("local Buffer :", hex_num)
            return cycles, energies, hex_num



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
            for i in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
                DBC.Local_row_buffer[i] = self.memory[self.TRd_head][i]

            cycles = + 1
            energies = + 1

            # converting to Hex
            count = 0
            s = ''
            hex_num = '0x'

            for j in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
                s += str(self.memory[self.TRd_head][j])
                count += 1
                if count == 4:
                    num = int(s, 2)
                    string_hex_num = format(num, 'x')
                    hex_num += (string_hex_num)

                    s = ''
                    count = 0

            # print('Read AP0=  ', (hex_num))

            return cycles, energies, hex_num

        elif (instruction == 'R AP1'):
            for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
                DBC.Local_row_buffer[i] = self.memory[self.TRd_tail][i]

            cycles = + 1
            energies = + 1



            # n = DBC.Local_row_buffer[:]
            # n = "".join([str(item) for item in n])
            # # convert binary to int
            # num = int(n, 2)
            # # convert int to hexadecimal
            # hex_num = hex(num)
            #
            # n = []
            # for i in range (2, len(hex_num)):
            #     n += (hex_num[i])

            # converting to Hex
            count = 0
            s = ''
            hex_num = '0x'

            for j in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
                s += str(self.memory[self.TRd_tail][j])
                count += 1
                if count == 4:
                    num = int(s, 2)
                    string_hex_num = format(num, 'x')
                    hex_num += (string_hex_num)

                    s = ''
                    count = 0

            print('Read AP1=  ', (hex_num))

            return cycles, energies, hex_num

        # # Counting carry bit's
        elif (instruction == 'CARRY_AP0'):
            cycle, energy, Local_buffer = logicop.carry(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            energies = + energy
            return cycles, energies, Local_buffer

        elif (instruction == 'CARRYPRIME_AP0'):
            cycle, energy, Local_buffer = logicop.carry_prime(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            energies = + energy
            return cycles, energies, Local_buffer
        elif (instruction == 'CARRY_AP1'):
            cycle, energy, Local_buffer = logicop.carry(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos)
            energies = + energy
            return cycles, energies, Local_buffer

        elif (instruction == 'CARRYPRIME_AP1'):
            cycle, energy, Local_buffer = logicop.carry_prime(self.memory, self.TRd_tail, nanowire_num_start_pos, nanowire_num_end_pos)
            energies = + energy
            return cycles, energies, Local_buffer
        # Logic Operations
        elif (instruction == 'AND'):
            cycle, energies, Local_buffer = logicop.And(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycles, energies, Local_buffer

        elif instruction == 'NAND':
            cycle, energies, Local_buffer = logicop.Nand(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycle, energies, Local_buffer

        elif instruction == 'XOR':
            cycle, energies, Local_buffer = logicop.Xor(self.memory, self.TRd_head,nanowire_num_start_pos, nanowire_num_end_pos)
            cycles = + cycle
            return cycle, energies, Local_buffer

        elif instruction == 'XNOR':
            cycle, energies, Local_buffer = logicop.Xnor(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycle, energies, Local_buffer

        elif instruction == 'OR':
            cycle, energies, Local_buffer = logicop.Or(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycle, energies, Local_buffer

        elif instruction == 'NOR':
            cycle, energies, Local_buffer = logicop.Nor(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycle, energies, Local_buffer

        elif instruction == 'NOT':
            cycle, energies, Local_buffer = logicop.Not(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycle, energies, Local_buffer

        # Arithmatic operation (Addition and multiplication)
        elif instruction == 'ADD':
            cycle, energies, Local_buffer = ao.addition(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycle, energies, Local_buffer

        elif instruction == 'MULT':
            cycle, energies, Local_buffer = ao.multuply(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
            return cycle, energies, Local_buffer







