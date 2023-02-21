# DWM simulator
## A Spintronic Processing-In-Memory Simulator for Racetracks {**SPIMulator**}.



### Project Setup:
* The SPIMulator was written in python version 3.8.
* SPIMulator does not require any exterrnal pip downloads. It can run in itself after download. 
* SPIMulator.py is the main file where we read the intruction(.text) files. So, the instruction files needs to be initialized here every time we run a new algorithm.
* config.py is the congiguration file where we can change the TRd size.

### Domain wall memory 
For this project we have a memory with 32 tracks and 512 nanowires.

### Instruction sets
The general format is "CPIM DST SRC OP BLOCKSIZE WRITE_OPERATION".
Below is the list of operations "OP":
A) Write operations :
i) Write: ‘0’ is one of the types of write (‘write_op’) operation that will overwrite at the
destination ‘dst’ after the TRd head or tail aligns with the ‘dst’ address. The data from the
local buffer is overwrites the data at the ‘dst’ address and thus any previous information at
‘dst’ will be lost. This instruction is to be used adjoined with other operational instructions




























