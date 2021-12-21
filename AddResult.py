import configuration as cfg
import AddData as addData
TRd = cfg.TRd
L = cfg.L


def addResult(result , memory, TRd_start_loc, source, sink):
    TRd_end_loc = TRd_start_loc + TRd - 1
   #Resultposition = input ("Enter the postion to push the result : \n 1 : Top of TRd \n 2 : End of TRd \n 3 : Top of memory \n 4 : End of Memory \n :")
    if (source == 'AP0') and (sink == 'AP1'):
        addData.writezero(TRd_start_loc, memory, result)

    elif (source == 'AP0') and (sink == 'AP1'):
        addData.writeone(TRd_start_loc, memory, result)

    elif (source == 'AP0') and (sink == 'AP1'):
        # Add result to top of memory and shift data to right
        None

    elif (source == 'AP0') and (sink == 'AP1'):
        # Add result to end of memory and shift data to left
        None
    
    
    ## printing the final memory
    print('This is the memory after the adding the result', memory)
