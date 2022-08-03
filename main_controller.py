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
    TRd_head = 0
    TRd_end_loc = TRd_head + TRd_size - 1
    memory = [None] * (2 * memory_size)
    Local_row_buffer = [0] * (512)

    def __init__(self, instruction, data):
        self.instruction = instruction
        self.data = data


    def controller(self):
        if (self.instruction == 'W AP0 AP1'):
            # write at (left) TRd start loc and shift data right within the TRd space
            self.memory = adt.writezero(self.TRd_head, self.memory, self.data)

        elif (self.instruction == ' W AP1 AP0'):
            # write at (right) TRd end loc and shift data left within the TRd space.
            self.memory = adt.writeone(self.TRd_head, self.memory, self.data)

        # elif (self.instruction == 'write at Address 0'):
        #     # write at (right) TRd end and shift data left.
        #
        #     memory = adt.shift_writezero(memory, data)
        #     TRd_start_loc = int(L / 2)
        #     TRd_end_loc = TRd + TRd_start_loc
        #
        #
        # elif (instruction == 'write at Address 1'):
        #     # write at (right) TRd end and shift data left.
        #
        #     memory = adt.shift_writeone(memory, data)
        #     TRd_start_loc = int(L / 2 + L)
        #     TRd_end_loc = TRd + TRd_start_loc


        elif (self.instruction == 'W AP0'):
            # overwrite at left side (TRd start position)
            self.memory = adt.overwriteZero(self.TRd_head, self.memory, self.data)

        elif (self.instruction == 'W AP1'):
            # overwrite at right side(TRd end position)
            self.memory = adt.overwriteOne(self.writeport, self.memory, self.data)

        elif (self.instruction == 'W AP0 LE'):
            # write at (left) TRd start and shift data towards the left padding.
            self.memory = adt.writezero_shiftLE(self.TRd_head, self.memory, self.data)

        elif (self.instruction == 'W AP0 RE'):
            # write at (left) TRd start and shift data towards the right padding.
            self.memory = adt.writezero_shiftRE(self.TRd_head, self.memory, self.data)

        elif (self.instruction == 'W AP1 LE'):
            # write at (right) TRd end and shift data towards left padding.
            self.memory = adt.writeone_shiftLE(self.TRd_head, self.memory, self.data)

        elif (self.instruction == 'W AP1 RE'):
            # write at (right) TRd end and shift data towards right padding.
            self.memory = adt.writeone_shiftRE(self.TRd_head, self.memory, self.data)


        elif (self.instruction == 'SR'):
            self.TRd_head = self.TRd_head + 1
            self.TRd_end_loc = self.TRd_start_loc + self.TRd_size - 1

        elif (self.instruction == 'SL'):
            self.TRd_head = self.TRd_head - 1
            self.TRd_end_loc = self.TRd_start_loc + self.TRd_size - 1


        elif (self.instruction == 'R0'):
            self.TRd_head = int(self.TRd_head)


        elif (self.instruction == 'R1'):
            self.TRd_end_loc = int(self.TRd_end_loc)

        # source = input("Enter the source from the list : \n 1 : AP0 \n 2: AP1 \n")
        # sink = input("Enter the sink from the list : \n 0: Overwrite \n 1 : AP0 \n 2: AP1 \n 3: LE \n 4: RE \n")
        elif (self.instruction == 'And'):
            result = logicop.And(self.memory, self.TRd_head, self.TRd_end_loc)
            addres.addResult(result, self.memory, self.TRd_head, self.TRd_end_loc, self.source, sink)

        elif self.instruction == 'Nand':
            result = logicop.Nand(memory, TRd_head, TRd_end_loc)
            addres.addResult(result, memory, TRd_head, TRd_end_loc, source, sink)

        elif self.instruction == 'Xor':
            result = logicop.Xor(memory, TRd_head, TRd_end_loc)
            addres.addResult(result, memory, TRd_head, TRd_end_loc, source, sink)

        elif self.instruction == 'Xnor':
            result = logicop.Xnor(memory, TRd_head, TRd_end_loc)
            addres.addResult(result, memory, TRd_head, TRd_end_loc, source, sink)

        elif self.instruction == 'Or':
            result = logicop.Or(memory, TRd_head, TRd_end_loc)
            addres.addResult(result, memory, TRd_head, TRd_end_loc, source, sink)

        elif self.instruction == 'Nor':
            result = logicop.Nor(memory, TRd_head, TRd_end_loc)
            addres.addResult(result, memory, TRd_head, TRd_end_loc, source, sink)

            # elif operation == '7':
            #     result = logicop.Not(memory,TRd_start_loc, TRd_end_loc)
            #     addres.addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink)


