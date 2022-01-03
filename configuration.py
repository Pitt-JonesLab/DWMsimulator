####### Configuration file for inputs ############

## User Inputs
# TRd = int(input ("Enter the TRd value between 4 and 7: "))
# TRd_start_loc = int(input("Enter the start loc of TRd: "))
# TRd_end_loc = TRd_start_loc + TRd - 1
# operation = input ("Enter the operations from the list: \n 1 : And \n 2 : Nand \n 3 : Xor \n 4 : Xnor \n 5 : Or \n 6 : Nor \n 7 : Not \n")
# bit_length = int(input ("Enter the bit size of the inputs from the following 512, 1024, 2048, 4096 : "))
# L = int(input ("Enter the size of the memory : "))
# memory = []
# addResultposition = input ("Enter the postion to push the result : \n 1 : Top of TRd \n 2 : End of TRd \n 3 : Top of memory \n 4 : End of Memory \n :")




## User Inputs
TRd = 4      # Enter the TRd value between 4 and 7
TRd_start_loc = 4    # Enter the start loc of TRd
TRd_end_loc = TRd_start_loc + TRd - 1
bit_length = 2    # Enter the bit size of the inputs from the following 512, 1024, 2048, 4096
L = 10         # Enter the size of the memory
memory = [None] * (2*L)
operation = 1      # Enter the operations from the list:
                   # 1 : And
                   # 2 : Nand
                   # 3 : Xor
                   # 4 : Xnor
                   # 5 : Or
                   # 6 : Nor
                   # 7 : Not



#addResultposition = 1    # Enter the postion to push the result :
                         # 1 : Top of TRd
                         # 2 : End of TRd
                         # 3 : Top of memory
                         # 4 : End of Memory


# Adding junk to padded bits
import random

def rand_key(p):
    # Variable to store the
    # string
    key1 = ""

    # Loop to find the string
    # of desired length
    for i in range(p):
        # randint function to generate
        # 0, 1 randomly and converting
        # the result into str
        temp = str(random.randint(0, 1))

        # Concatenation the random 0, 1
        # to the final result
        key1 += temp

    return (key1)

#Driver Code
n = bit_length #size of random binary number to be filled before and after the momory in task
for i in range(2*L):
    if ((i <= L/2 - 1) or (i >= L + L/2)):
        str1 = rand_key(n)
        memory[i] = str1
        #memory.append(int(str1))

#print(memory)
