'''
Author : Pavia Bera - University of South Florida

This is a simulator for Domain wall memory (DWM)
DWM leverages the 'shift-register' nature of spintronic domain-wall memory (DWM).
Shift-based scheme utilizes a multi-nanowire approach to ensure that reads and writes
can be more effectively aligned with access ports for simultaneous access in the same cycle.

'''

# Importing all
import WriteData as adt
import LogicOperation as logicop


class DBC():
    TRd_size = 4

    def __init__(self, ):
        '''This is a single instance of DBC'''
        self.TRd_head = 0
        self.TRd_tail = self.TRd_head + DBC.TRd_size
        self.bit_length = 512
        self.memory_size = 32
        self.memory = [[0 for _ in range(self.bit_length)] for _ in range(self.memory_size * 2)]


    def controller(self, memory, row_number, instruction, nanowire_num_start_pos = 0, nanowire_num_end_pos = 511, data_hex = None):
        cycles = 0
        diff = 0

        if self.TRd_head > row_number:
            diff = self.TRd_head - row_number
            # Cycles for shift
            cycles = + diff
            self.TRd_head = self.TRd_head - diff
            self.TRd_tail = self.TRd_head + DBC.TRd_size
        elif self.TRd_head < row_number:
            diff = row_number - self.TRd_head
            # Cycles for shift
            cycles = + diff
            self.TRd_head = self.TRd_head + diff
            self.TRd_tail = self.TRd_head + DBC.TRd_size
        else:
            self.TRd_head = row_number
            self.TRd_tail = self.TRd_head + DBC.TRd_size



        # Initializing Local Buffer for all DBC's
        Local_row_buffer = [0] * (512)

        if data_hex != None:
            # Convert hex data to bin
            data_hex_size = len(data_hex) * 4
            data_bin = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)
            for i in range(0, len(data_bin)):
                Local_row_buffer[i] = data_bin[i]

        # Write instruction
        if (instruction == 'W AP0 AP1'):
            # write at (left) TRd start loc and shift data right within the TRd space
            cycle = adt.writezero(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1 AP0'):
            # write at (right) TRd end loc and shift data left within the TRd space.
            cycle = adt.writeone(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP0'):
            # overwrite at left side (TRd start position)
            cycle = adt.overwrite(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1'):
            # overwrite at right side(TRd end position)
            cycle = adt.overwrite(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP0 LE'):
            # write at (left) TRd start and shift data towards the left padding.
            cycle = adt.writezero_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP0 RE'):
            # write at (left) TRd start and shift data towards the right padding.
            cycle = adt.writezero_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1 LE'):
            # write at (right) TRd end and shift data towards left padding.
            cycle = adt.writeone_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1 RE'):
            # write at (right) TRd end and shift data towards right padding.
            cycle = adt.writeone_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)
            cycles =+ cycle

        # Logical shift
        elif (instruction == 'LS R AP0'):
            for i in range(0,504):
                Local_row_buffer[i] = self.memory[self.TRd_head][i+8]

        elif (instruction == 'LS R AP1'):
            for i in range(0, 504):
                Local_row_buffer[i] = self.memory[self.TRd_tail][i + 8]

        elif (instruction == 'LS L AP0'):
            for i in range(0, 504):
                Local_row_buffer[i+8] = self.memory[self.TRd_head][i]

        elif (instruction == 'LS L AP1'):
            for i in range(0, 504):
                Local_row_buffer[i+8] = self.memory[self.TRd_tail][i]

        # shift Instructions
        elif (instruction == 'SR'):
            row_number += 1
            cycles = + 1

        elif (instruction == 'SL'):
            row_number -= 1
            cycles = + 1

        # Read instruction
        elif (instruction == 'R AP0'):
            Local_row_buffer[:] = memory[self.TRd_head][:]
            cycles = + 1

        elif (instruction == 'R AP1'):
            Local_row_buffer[:] = memory[self.TRd_head][:]
            cycles = + 1

        elif (instruction == 'And'):
            Local_row_buffer[:] = logicop.And(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

        # elif instruction == 'Nand':
        #     Local_row_buffer = logicop.Nand(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
        # elif instruction == 'Xor':
        #     Local_row_buffer = logicop.Xor(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
        # elif instruction == 'Xnor':
        #     Local_row_buffer = logicop.Xnor(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
        # elif instruction == 'Or':
        #     Local_row_buffer = logicop.Or(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
        # elif instruction == 'Nor':
        #     Local_row_buffer = logicop.Nor(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
        # elif instruction == 'Not':
        #     Local_row_buffer = logicop.Not(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
        #
        return cycles


