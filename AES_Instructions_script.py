'''
This is the script that uses the DWM simulator to run the AES algorithm.
'''
import xlrd
from main_controller import DBC




# Creating 16 DBC objects
dbcs = [DBC() for i in range(16)]

#Reading Instruction of Excel
loc = ("/Users/paviabera/Desktop/DWM Simulator/Stephen/instruction set for AES operation-Stephen.xlsx")
# loc = ("/Users/paviabera/Desktop/DWM Simulator/instruction set for AES operation.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
# Extracting number of columns and rows
ncol = sheet.ncols
#nrow = sheet.nrows
nrow = 4
total_cycles = 0
for i in range(1, nrow):
    # Reading Excel File with instruction/commands.
    DBC_number = sheet.cell_value(i, 1)
    row_number = sheet.cell_value(i, 2)
    nanowire_num_start_pos = sheet.cell_value(i, 4)
    nanowire_num_end_pos = sheet.cell_value(i, 6)
    operation = sheet.cell_value(i, 8)
    if sheet.cell_value(i, 9) == '':
        data_hex = None
    else:
        data_hex = sheet.cell_value(i, 9)






    # Calling DBC object for each instruction above
    cycles = 0
    if DBC_number == '0000':
        dbc = dbcs[0]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0001':
        dbc = dbcs[1]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0010':
        dbc = dbcs[2]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0011':
        dbc = dbcs[3]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0100':
        dbc = dbcs[4]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0101':
        dbc = dbcs[5]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0110':
        dbc = dbcs[6]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0111':
        dbc = dbcs[7]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1000':
        dbc = dbcs[8]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '0101':
        dbc = dbcs[9]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1010':
        dbc = dbcs[10]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1011':
        dbc = dbcs[11]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1100':
        dbc = dbcs[12]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1101':
        dbc = dbcs[13]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1110':
        dbc = dbcs[14]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles
    elif DBC_number == '1111':
        dbc = dbcs[15]
        cycles = dbc.controller(dbc.memory, row_number, operation, nanowire_num_start_pos, nanowire_num_end_pos, data_hex)
        total_cycles += cycles

print("The total number of cycles to run AES is", total_cycles)








