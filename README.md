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

### A) Write operations :

#### i) Write: ‘0’ 
is one of the types of write (‘write_op’) operation that will overwrite at the
destination ‘dst’ after the TRd head or tail aligns with the ‘dst’ address. The data from the
local buffer is overwrites the data at the ‘dst’ address and thus any previous information at
‘dst’ will be lost. This instruction is to be used adjoined with other operational instructions such as ‘AND’, ‘SHL’, ADD etc. The result after performing any operations at ‘src’ is stored
in the local buffer temporarily and then overwritten at ‘dst’ according to ’0’.

#### ii) Transverse write at AP0: ‘1’
is a special type of write operation which represents transverse
write at ‘AP 0’. This means that the data present within the TRd is shifted towards ‘AP
1’ by one row and then the shifted data is written at ‘dst’ address. In doing so, the data at
‘AP 1’ will be lost. This instruction is issued when there is a need to shift place data while
keeping the head at the same address or to clear out old data.

#### iii) Transverse write at AP1: ‘2’ 
is a special type of write operation which represents transverse
write at ‘AP 1’. Similar to the above command, except data is shifted into AP1 and the data
at ‘AP 0’ is lost instead.

#### iv) Transverse write at AP0 shift to bottom extremity: ‘3’ 
represents transverse write at ‘AP
0’, but instead of deleting the data at ‘AP 1’, it pushes it down by one row beyond the
TR distance. This means that the entire data starting from ‘AP 0’, is shifted down by one address until the end of the nanowire. In doing so only, the last row of data at the end of
the nanowire (512) will be lost when issued with this command.

#### v) Transverse write at AP1 shift to top extremity: ‘4’
represents transverse write at ‘AP 1’ and
pushes the data at the track beyond the TR distance (above‘AP 0’) towards the top. This
means all addresses beyond the TRd will be shifted up by one, with the top row being
deleted entirely.

#### vi) Transverse write at AP0 shift to top extremity: ‘5’ 
represents transverse write at ‘AP 0’ and
pushes the data up the track (above AP0) by one row. This will result in all data above ‘AP
0’ being shifted up by one, and the data at address 0 is lost.

#### vii) Transverse write at AP1 shift to bottom extremity: ‘6’ 
represents transverse write at ‘AP 1’
and pushes the data towards the bottom of the track below the TRd. This means that the
data below ‘AP 1’ will be shifted downwards. In doing so only, the data at address 32 is
deleted.

### B) Basic Memory Operations :

#### i) ‘STORE’:
When issued with this instruction, the "data" is loaded from the CPU to the local
buffer and then is written according to the write_op (0 - 6) after the TRd AP 0 or AP 1 aligns
with the destination ’dst’ address. The peculiarity of this instruction is that the CPU data to
be loaded can be supplied with the instruction. For example, " cpim $96 0xA24B791CEF6
STORE 512 0 " implies that Data=0xA24B791CEF6 will be written at address $96 after the
closest of the AP’s aligns with $96.

#### ii) ‘COPY’: When issued with this instruction, the closest of the access points will first align
with the source ’src’ address, and then the "data" is read from the source ’src’ address to
the local buffer. The read data in the local buffer is then written according to the write_op
(0 - 6) after the TRd AP 0 or AP 1 aligns with the destination ’dst’ address. The different
types of write_op (0 - 6) will be discussed in more detail in the following paragraphs. The
peculiarity of this instruction is that it reads the ’scr’ first and then writes the read data.
For example, " cpim $96 $12 COPY 512 0 " implies that source address ’scr’ $12 will be
read and transferred to the local buffer. Then it will be written at ’dst’ address $96 after
the closest of the AP’s aligns with the source address $12 and the destination address $96,
respectively.

#### iii) ‘SHL’ (logical shift left)
represents the left shift of each bit at the ‘src’. This instruction
comes in 3 forms: SHL1, SHL8, and SHL32. When issuing any of the above, SPIMulator’s
first step is to read at ‘scr’ address by using the intelligent alignment of the TRd access port
and then the number of shifts required. The data is then read to the row buffer and shifted
by the instructed number. Data at the left extremity is lost, and 0’s are added to the right
extremity. This operation is conducted in the source address, and then the result is stored
temporarily in the local buffer till the write instruction is executed. The write instruction is
always accompanied with ‘SHL’ instruction. An example for this instruction " cpim $32 $0
SHL1 512 0 " will first align either of the AP’s nearest to $0 and data will be left shifted by
1 bit. The shifted data will be in the local buffer before it is overwritten into the destination
address $32.

#### iv) ‘SHR’ (logical shift right)
represents the right shift of each bit at the ‘src’ address. This
instruction comes in 3 forms: SHR1, SHR8, and SHR32. When issuing any of the above,
SPIMulator’s first reads the ‘scr’ address by using the intelligent alignment of the TRd
access port and then determines the amount to be shifted. The data is then read to the local
buffer and shifted by the desired amount. Data at the right extremity is lost, and 0’s are
added to the left extremity. This operation is conducted in the source address, and then
the result is stored temporarily in the local buffer till the write instruction is executed. The write instruction is always accompanied with ‘SHR’ instruction. An example for this
instruction is " cpim $32 $0 SHR8 512 0 " which will first align either of the AP’s nearest
to $0 and data will be right shifted by 8 bits. The shifted data will be in the local buffer
before it is overwritten into the destination address $32.

#### v) ‘R AP0 and R AP1’ 
represents a simple read instruction at the src location after aligning
either ’AP 0’ or ’AP 1’ access port which is the head or tail of TRd with src. Although this
instruction is not mentioned in the cpim instruction set the table, it is important to have
these options so as to issue a simple read command when necessary. An example of this
instruction is " read $12 AP0 ", which will align the access port AP 0 with source address
$12 and then copies the data into the local buffer. These instructions can be helpful when
data is required to be moved out of the Domain Wall Memory to the CPU. 

### C) Logical and Arithmetic Operations :

#### i) {‘AND’, ‘OR’, ‘XOR’, ‘XNOR’, ‘NAND’, ‘NOR’, ‘NOT’} 
represents the logical operation ‘and’,
‘or’, ‘xor’, ‘xnor’, ‘nand’, ‘nor’, ‘not’ individually when issued with the cpim instruction.
The operation takes place among the operands present between the TR distance after
aligning the access port ’AP 0’ with the source address ‘src’. The result of the operation is
temporarily stored in the local buffer till it is written according to the last three bits (0-6)
of the instruction to the destination ‘dst’ address. An example of logical operations is: "
cpim $32 $0 and 511 0 " in which the ‘and’ operation is executed from source address
‘src’ location to the TR size. The result is then stored in the local buffer and overwritten at
the destination address ‘dst’.

#### ii) ‘CARRY’ and ‘CARRYPRIME’
are a special instructions which are required for the ’ADD’
and ‘MULT’ operations. They are normally not called by the users as they are not the part
of the arithmetic operations. But users can still have the option to call these instructions in
SPIMulator if they want to create custom functions that will require ’CARRY’ and ’CARRYPRIME’
calculations. Both ’CARRY’ and ’CARRYPRIME’ operations counts the number
of ones’s within the TRd distance and will output 1 to the local buffer. ’CARRY’ outputs 1 when the number of 1 within the TRd is any of the following 2,3,6,7. ’CARRYPRIME’
outputs 1 when the number of 1 within the TRd is any of the following 4,5,6,7. Example of
carry instruction is " cpim $32 $0 carry 511 1 " which issues a carry operation at source
address $0 and transverse writes at destination address at $0. Example of carryprime " cpim
$32 $0 carryprime 511 0 " which issues a carryprime operation at source address $0 and
overwrites at destination address at $0. The output from these instruction can be written in
any way according to the last ’3 bit’ of the instruction i.e (0-6).

#### iii) ‘ADD’
represents the arithmetic ’addition ’ operation 𝐴 + 𝐵.We will show an example of an
addition operation for five operands in Fig. 5 for TRd = 7. It is important to note that we
can perform addition for (𝑇𝑅𝑑 − 2) bits. Therefore, for our example, we can perform 5-bit
addition for TRd = 7. In step 1, a TR of 𝑑𝑤𝑚0 (first nanowire) is conducted. 𝑆0, which is
XOR of 𝑎0...𝑒0, (5-bit number) is computed by the PIM block, which is the blue bits between
the AP 0 and AP 1 access ports. Simultaneously, carry, 𝐶0, is computed and sent to the
right to the driver (AP 1) for 𝑑𝑤𝑚1 (second nanowire) shown in orange and carry prime
𝐶′
0 is sent to the left of the driver AP 0 for 𝑑𝑤𝑚2 (3rd nanowire), shown in green in fig.
5. In step 2, a similar set of steps occurs, except the operations include 𝐶0 in addition to
𝑎1...𝑒1. Then in step 3, TR is conducted over 𝐶′
0 , 𝑎2...𝑒2,𝐶1, which is seven total elements.
We will continue to compute 𝑆, 𝐶 and 𝐶′ for every nanowire till the 3rd last nanowire (509)
is reached. In the general case, for step k+1 (i.e., 𝑑𝑤𝑚𝑘 ), TR is conducted over 𝐶′
(𝑘 − 2),
𝑎𝑘 ...𝑒𝑘 , 𝐶(𝑘 − 1) with 𝑆𝑘 written to 𝑝𝑜𝑟𝑡𝐿 of 𝑑𝑤𝑚𝑘 , 𝐶𝑘 written to 𝑝𝑜𝑟𝑡𝑅 of 𝑑𝑤𝑚(𝑘 + 1) and
𝐶′
𝑘 written to 𝑝𝑜𝑟𝑡𝐿 of 𝑑𝑤𝑚(𝑘 + 2). Figure 5 is an example of addition for (TRD - 2) numbers
of operands placed in-between the Access Ports.

#### iv) ‘MULT’
represents the arithmetic ‘multiplication’ operation 𝐴 ∗ 𝐵. A foundational method
to compute 𝐴 ∗ 𝐵 is to sum A B times; e.g., for 𝐵 = 3, 𝐴 ∗ 3 can be computed as 𝐴 + 𝐴 + 𝐴.
Thus, we can perform multiplication by making several additions. Even with a 5 operand
add, this method can quickly require many steps. Consider 9𝐴; this can be computed by
computing 5𝐴 in one step and then computing 5𝐴 + 𝐴 + 𝐴 + 𝐴 + 𝐴 in a second step. This
method could be improved by generating 5𝐴 in one additional step, then replicating 5𝐴 and
summing to compute 25𝐴, and so on, but this clearly scales poorly. One method to accelerate
this process is to shift the copies of A, so as to quickly achieve the precise partial products
that, when summed, produce the desired product. We have reserved our last DBC $15 for
the purpose of shifting copies of A and executing carry, carry prime and add operations on
the shifted copies of A. This is the reduction process, as shown in figure 6. One example of
‘multiplication’ is shown in fig. 7. Here, we multiply 0xfe and 0x1f to generate 0x1588.



























