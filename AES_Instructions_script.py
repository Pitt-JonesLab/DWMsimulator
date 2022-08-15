'''
This is the script that uses the DWM simulator to run the AES algorithm.
'''
import xlrd
from main_controller import controller

class DBC():
    TRd_size = 4

    def __init__(self, ):
        '''This is a single instance of DBC'''
        self.bit_length = 512
        self.memory_size = 32
        self.memory = [[0 for _ in range(self.bit_length)] for _ in range(self.memory_size * 2)]

# Creating 16 DBC objects
dbcs = [DBC() for i in range(16)]

#Reading Instruction of Excel
loc = ("/Users/paviabera/Desktop/instruction set for AES operation.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
# Extracting number of columns and rows
ncol = sheet.ncols
#nrow = sheet.nrows
nrow = 5
total_cycles = 0
for i in range(1, nrow):
    # Reading Excel File with instruction/commands.
    DBC_number = sheet.cell_value(i, 1)
    row_number = sheet.cell_value(i, 2)
    nanowire_num_start_pos = sheet.cell_value(i, 4)
    nanowire_num_end_pos = sheet.cell_value(i, 6)
    operation = sheet.cell_value(i, 8)
    data_hex = sheet.cell_value(i, 9)

    # Calling DBC object for each instruction above
    cycles = 0
    if DBC_number == '0000':
        dbc = dbcs[0]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0001':
        dbc = dbcs[1]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0010':
        dbc = dbcs[2]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0011':
        dbc = dbcs[3]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0100':
        dbc = dbcs[4]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0101':
        dbc = dbcs[5]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0110':
        dbc = dbcs[6]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0111':
        dbc = dbcs[7]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1000':
        dbc = dbcs[8]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0101':
        dbc = dbcs[9]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1010':
        dbc = dbcs[10]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1011':
        dbc = dbcs[11]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1100':
        dbc = dbcs[12]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1101':
        dbc = dbcs[13]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1110':
        dbc = dbcs[14]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1111':
        dbc = dbcs[15]
        cycles = controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles

print("The total number of cycles to run AES is", total_cycles)








