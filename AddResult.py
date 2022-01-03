import configuration as cfg
import AddData as addData
TRd = cfg.TRd
L = cfg.L


def addResult(result, memory, TRd_start_loc, TRd_end_loc, source, sink):
    #TRd_end_loc = TRd_start_loc + TRd - 1
   #Resultposition = input ("Enter the postion to push the result : \n 1 : Top of TRd \n 2 : End of TRd \n 3 : Top of memory \n 4 : End of Memory \n :")
    if (source == '1') and (sink == '2'):
        # Add result at (left) TRd start and shift data right.
        addData.writezero(TRd_start_loc, memory, result)

    elif (source == '2') and (sink == '1'):
        # Add result at (right) TRd end and shift data left.
        addData.writeone(TRd_end_loc, memory, result)

    elif (source == '1') and (sink == '3'):
        # Add result at (left) TRd start and shift data towards the left padding.
        addData.writezero_shiftLE(TRd_start_loc, memory, result)

    elif (source == '1') and (sink == '4'):
        # Add result at (left) TRd start and shift data towards the right padding.
        addData.writezero_shiftRE(TRd_start_loc, memory, result)

    elif (source == '2') and (sink == '3'):
        # Add result at (right) TRd end and shift data towards left padding.
        addData.writeone_shiftLE(TRd_end_loc, memory, result)

    elif (source == '2') and (sink == '4'):
        # Add result at (right) TRd end and shift data towards right padding.
        addData.writeone_shiftRE(TRd_end_loc, memory, result)

    elif (source == '1') and (sink == '0'):
        # Add result at (right) TRd end and shift data towards right padding.
        addData.overwriteZero(TRd_start_loc, memory, result)

    elif (source == '2') and (sink == '0'):
        # Add result at (right) TRd end and shift data towards right padding.
        addData.overwriteOne(TRd_end_loc, memory, result)

    
    ## printing the final memory
    print('This is the memory after the adding the result', memory)
