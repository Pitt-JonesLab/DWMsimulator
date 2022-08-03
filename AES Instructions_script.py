'''
This is the script that uses the DWM simulator to run the AES algorithm.

'''




from controller import *












def readdata():
    cycles = 0
    # Reads the text file and extracts 128 bits
    # master_key = 0x2b7e151628aed2a6abf7158809cf4f3c

    # #Read Text file and conver to Binary
    # filename = "articles-multistream-index.txt"
    #
    # # read file as string:
    # f = open(filename, 'r')
    # mytext = f.read()
    #
    # # change text into binary mode:
    # binarytxt = str.encode(mytext)
    #
    # # save the bytes object
    # with open('filename_bytes.txt', 'wb') as fbinary:
    #     fbinary.write(binarytxt)

    # Read 128 bits from a file
    master_key = "2b7e151628aed2a6abf7158809cf4f3c"
    plaintext = "3243f6a8885a308d313198a2e0370734"

    ## Convert hex to bits

    # master_key_hex = (bin(int(master_key, scale))[2:].zfill(num_of_bits))
    # plaintext_hex = (bin(int(plaintext, scale))[2:].zfill(num_of_bits))
    plaintext_size = len(plaintext) * 4
    master_key_size = len(master_key) * 4

    master_key_bin = (bin(int(master_key, 16))[2:]).zfill(master_key_size)
    plaintext_bin = (bin(int(plaintext, 16))[2:]).zfill(plaintext_size)
    master_key_bin = master_key_bin.ljust(512,"0")
    plaintext_bin = plaintext_bin.ljust(512,"0")
    dataplacement(master_key_bin, plaintext_bin)

    # data = [plaintext_hex, master_key_hex]



    # instruction = 'AP0 AP1'
    # instruction = ''
    # controller(data[0], instruction)
    # cycles  = cycles + 1
    # print(cycles, 'cycles')
    # controller(data[1], instruction)
    # cycles = cycles + 1
    # print(cycles, 'cycles')


def dataplacement(master_key, plaintext_bin):

    controller_write(master_key, 'AP0 AP1' )
    controller_write(plaintext_bin,'AP0 AP1')

    #Creating junk data to fill the other TRd postions
    zero = '0'
    data1 = zero.ljust(512,'0')
    data2 = zero.ljust(512,'0')

    controller_write(data1, 'AP0 AP1')
    controller_write(data2, 'AP0 AP1')




def AES_Script():
    readdata()
    # step 1: Derive the set of round keys from the cipher key.


    # step 2: Initialize the state array with the block data (plaintext).

    # step 3: Add the initial round key to the starting state array.
    '''
     This is the first step of AES algorithm; add round key operation, and this is simply
     XOR operation.We have 128 - bit length plaintext and 128 - bit length key so XOR
     operate bit by bit.
    '''

    operation = '3'
    source = '1'
    sink = '0'
    controller_operation(operation, source, sink)







AES_Script()