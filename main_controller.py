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
    TRd_size = 6
    # Initializing single Local Buffer for all DBC's
    Local_row_buffer = [0] * (512)
    def __init__(self, ):
        '''This is a single instance of DBC'''
        self.TRd_head = 0
        self.TRd_tail = self.TRd_head + DBC.TRd_size
        self.bit_length = 512
        self.memory_size = 32
        self.padding_bits = self.memory_size / 2
        self.memory = [[(0) for _ in range(self.memory_size * 2)]for _ in range(self.bit_length)]



    def controller(self, memory, write_port, instruction, nanowire_num_start_pos = 0, nanowire_num_end_pos = 511, data_hex = None):
        nanowire_num_start_pos = int(nanowire_num_start_pos)
        nanowire_num_end_pos = int(nanowire_num_end_pos)
        cycles = 0
        diff = 0
        row_number = write_port + self.padding_bits
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

        self.TRd_head = int(self.TRd_head)



        if data_hex != None:
            # Convert hex data to bin
            data_hex_size = len(data_hex) * 4
            data_bin = (bin(int(data_hex, 16))[2:]).zfill(data_hex_size)
            for i in range(0, len(data_bin)):
                DBC.Local_row_buffer[i] = data_bin[i]

        # Local_row_buffer_hex = []
        # for element in data_hex:
        #     Local_row_buffer_hex.append(element)
        #
        # print("Data in local Buffer in hex", Local_row_buffer_hex)

        # Write instruction
        if (instruction == 'W AP0 AP1'):
            # write at (left) TRd start loc and shift data right within the TRd space
            cycle = adt.writezero(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1 AP0'):
            # write at (right) TRd end loc and shift data left within the TRd space.
            cycle = adt.writeone(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP0'):
            # overwrite at left side (TRd start position)
            cycle = adt.overwrite(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1'):
            # overwrite at right side(TRd end position)
            cycle = adt.overwrite(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP0 LE'):
            # write at (left) TRd start and shift data towards the left padding.
            cycle = adt.writezero_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP0 RE'):
            # write at (left) TRd start and shift data towards the right padding.
            cycle = adt.writezero_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1 LE'):
            # write at (right) TRd end and shift data towards left padding.
            cycle = adt.writeone_shiftLE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles = + cycle

        elif (instruction == 'W AP1 RE'):
            # write at (right) TRd end and shift data towards right padding.
            cycle = adt.writeone_shiftRE(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos, DBC.Local_row_buffer)
            cycles =+ cycle

        # Logical shift


        elif ('LS L AP0' in instruction or 'LS L AP1' in instruction):
            command = (instruction.rsplit(' ', 1))
            n = int(command[-1])
            local_buffer_count = 0
            for i in range(n, self.bit_length):
                DBC.Local_row_buffer[local_buffer_count] = self.memory[i][self.TRd_head]
                local_buffer_count += 1
            cycles = + 1
            # Converting binary data at TRd head to Hex for verification/visualization
            count = 0
            s = ''
            hex_num = []
            for i in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
                s += str(DBC.Local_row_buffer[i])
                count += 1
                if count == 4:
                    num = int(s, 2)
                    hex_num.append(hex(num))
                    s = ''
                    count = 0
            print("Data in local Buffer in hex after logical shift", hex_num)

        elif ('LS R AP0' in instruction or 'LS R AP1' in instruction):
            command = (instruction.rsplit(' ', 1))
            n = int(command[-1])
            local_buffer_count = 0
            for i in range(n, self.bit_length):
                DBC.Local_row_buffer[local_buffer_count] = self.memory[i][self.TRd_head]
                local_buffer_count += 1
            cycles = + 1


        elif (instruction == 'LS R AP0' or instruction == 'LS R AP1'):
            local_buffer_count = 0
            for i in range(0, nanowire_num_end_pos):
                DBC.Local_row_buffer[local_buffer_count] = self.memory[i][self.TRd_head]
                local_buffer_count += 1
            cycles = + 1

        # shift Instructions
        elif (instruction == 'SR'):
            self.TRd_head += 1
            cycles = + 1

        elif (instruction == 'SL'):
            self.TRd_head -= 1
            cycles = + 1

        # Read instruction
        elif (instruction == 'R AP0' or instruction == 'R AP1'):
            for i in range(nanowire_num_start_pos, nanowire_num_end_pos+1):
                DBC.Local_row_buffer[i] = self.memory[i][self.TRd_head]

            cycles = + 1



        # Counting carry bit's
        elif (instruction == 'carry'):
            DBC.Local_row_buffer[:] = logicop.carry(self.memory, self.TRd_head)

        elif (instruction == 'carry prime'):
            DBC.Local_row_buffer[:] = logicop.carry_prime(self.memory, self.TRd_head)



        # elif (instruction == 'And'):
        #     Local_row_buffer[:] = logicop.And(self.memory, self.TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

        # elif instruction == 'Nand':
        #     Local_row_buffer = logicop.Nand(self.memory, row_number, nanowire_num_start_pos, nanowire_num_end_pos)
        #
        #
        elif instruction == 'xor':
            cycle, DBC.Local_row_buffer = logicop.Xor(self.memory, self.TRd_head,nanowire_num_start_pos, nanowire_num_end_pos)
            cycles = + cycle

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


