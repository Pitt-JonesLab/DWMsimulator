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
import AddResult as addres

class DBC():
    # Class attributes
    TRd_size = 4
    bit_length = 512
    memory_size = 32
    global memory
    memory = [[0 for _ in range(bit_length)] for _ in range(memory_size*2)]
    Local_row_buffer = [0] * (512)

    def __init__(self):
        '''This is a single instance of DBC'''

    def controller(self, row_number, instruction, nanowire_num_start_pos = 0, nanowire_num_end_pos = 511, data_hex = None):

        if data_hex != None:
            # Convert hex data to bin
            data_hex_size = len(data_hex) * 4
            data_bin = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)
            Local_row_buffer = data_bin


        # Write instruction
        if (instruction == 'W AP0 AP1'):
            # write at (left) TRd start loc and shift data right within the TRd space
            cycles = adt.writezero(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        elif (instruction == 'W AP1 AP0'):
            # write at (right) TRd end loc and shift data left within the TRd space.
            cycles = adt.writeone(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        elif (instruction == 'W AP0'):
            # overwrite at left side (TRd start position)
            cycles = adt.overwriteZero(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        elif (instruction == 'W AP1'):
            # overwrite at right side(TRd end position)
            cycles = adt.overwriteOne(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        elif (instruction == 'W AP0 LE'):
            # write at (left) TRd start and shift data towards the left padding.
            cycles = adt.writezero_shiftLE(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        elif (instruction == 'W AP0 RE'):
            # write at (left) TRd start and shift data towards the right padding.
            cycles = adt.writezero_shiftRE(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        elif (instruction == 'W AP1 LE'):
            # write at (right) TRd end and shift data towards left padding.
            cycles = adt.writeone_shiftLE(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        elif (instruction == 'W AP1 RE'):
            # write at (right) TRd end and shift data towards right padding.
            cycles = adt.writeone_shiftRE(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

        # # shift Instructions
        # elif (instruction == 'SR'):
        #     cycles = 1
        #     self.row_number = self.row_number + 1
        #     self.TRd_end_loc = self.row_number + self.TRd_size - 1

        # elif (instruction == 'SL'):
        #     self.row_number = self.row_number - 1
        #     self.TRd_end_loc = self.row_number + self.TRd_size - 1
        #
        # elif (instruction == 'SU AP0 8'):
        #     for i in range(0,8):
        #         memory[][] =  memory[nanowire_num_start_pos][]
        #
        # elif (instruction == 'SU AP0 32'):
        #     for i in range(0, 32):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SU AP0 88'):
        #     for i in range(0, 88):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SD AP1 8'):
        #     for i in range(0, 8):
        #
        # elif (instruction == 'SD AP1 32'):
        #     for i in range(0, 32):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SD AP1 88'):
        #     for i in range(0, 88):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SU AP0 8'):
        #     for i in range(0, 8):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SU AP0 32'):
        #     for i in range(0, 32):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SU AP0 88'):
        #     for i in range(0, 88):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SD AP1 8'):
        #     for i in range(0, 8):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SD AP1 32'):
        #     for i in range(0, 32):
        #         memory[][] = memory[][]
        #
        # elif (instruction == 'SD AP1 88'):
        #     for i in range(0, 88):
        #         memory[][] = memory[][]
        #
        # # Read instruction
        # elif (instruction == 'R0'):
        #     Local_row_buffer = int(self.row_number)
        #     Local_row_buffer = memory[][]
        #
        #
        # elif (instruction == 'R1'):
        #     self.TRd_end_loc = row_number + self.TRd_size
        #     Local_row_buffer = memory [][]
        #
        # elif (instruction == 'And'):
        #     Local_row_buffer = logicop.And(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
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



