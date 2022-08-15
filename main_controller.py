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



def controller(memory, row_number, instruction, nanowire_num_start_pos = 0, nanowire_num_end_pos = 511, data_hex = None):
    # Initializing Local Buffer for all DBC's
    Local_row_buffer = [0] * (512)
    cycles = 0
    if data_hex != None:
        # Convert hex data to bin
        data_hex_size = len(data_hex) * 4
        data_bin = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)
        for i in range(0, len(data_bin)):
            Local_row_buffer[i] = data_bin[i]

    # Write instruction
    if (instruction == 'W AP0 AP1'):
        # write at (left) TRd start loc and shift data right within the TRd space
        cycles = adt.writezero(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    elif (instruction == 'W AP1 AP0'):
        # write at (right) TRd end loc and shift data left within the TRd space.
        cycles = adt.writeone(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    elif (instruction == 'W AP0'):
        # overwrite at left side (TRd start position)
        cycles = adt.overwrite(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    elif (instruction == 'W AP1'):
        # overwrite at right side(TRd end position)
        cycles = adt.overwrite(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    elif (instruction == 'W AP0 LE'):
        # write at (left) TRd start and shift data towards the left padding.
        cycles = adt.writezero_shiftLE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    elif (instruction == 'W AP0 RE'):
        # write at (left) TRd start and shift data towards the right padding.
        cycles = adt.writezero_shiftRE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    elif (instruction == 'W AP1 LE'):
        # write at (right) TRd end and shift data towards left padding.
        cycles = adt.writeone_shiftLE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    elif (instruction == 'W AP1 RE'):
        # write at (right) TRd end and shift data towards right padding.
        cycles = adt.writeone_shiftRE(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos, Local_row_buffer)

    # shift Instructions
    elif (instruction == 'SR'):
        row_number += 1
        cycles = 1

    elif (instruction == 'SL'):
        row_number -= 1
        cycles = 1


    # Read instruction
    elif (instruction == 'R0'):
        Local_row_buffer[:] = memory[row_number][:]
        cycles = 1

    elif (instruction == 'R1'):
        Local_row_buffer[:] = memory[row_number][:]
        cycles = 1

    elif (instruction == 'And'):
        Local_row_buffer[:] = logicop.And(memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)

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


