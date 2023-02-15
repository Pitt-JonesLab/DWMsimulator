# DWMsimulator
## DWM simulatorwas written in python 3.8

# Intro to DWM:































A ‘.txt’ file is loaded into the tool and the tool can translate the text file into PIM readable instructions. The
tool can issue instructions sequentially from a ‘.txt’ file given by the user.

A) Write operations :
i) Overwrite ’0’: is one of the types of write (‘write_op’) operation that will overwrite at the destination ’dst’
after the TRd head or tail aligns with the ’dst’ address. The data from the local buffer is overwritten at
the ’dst’ address and thus any previous information at ’dst’ will be lost. This instruction is to be used
adjoined with other operational instructions such as ’AND’, ’SHL’, ADD etc. The result after performing
any operations at ’src’ is stored in the local buffer temporarily and then overwritten at ’dst’ according to
’0’.
ii) Transverse write at AP0 ’1’: is a special type of write operation which represents transverse write at ’AP
0’. This means that the data present within the TRd is shifted to the right by a bit. In doing so, the data at
’AP 1’ will be lost when issued with this command. This instruction is issued when there is a need to
shift the data to the right by one bit within the designated TR distance.

iii) Transverse write at AP1 ’2’ is a special type of write operation which represents transverse write at ‘AP 1’.
This means that the data present within the TRd is shifted to the left by a bit. In doing so, the data at ‘AP
0’ will be lost when issued with this command. This instruction is issued when there is a need to shift the
data to the left by one bit within the designated TR distance.
iv) Transverse write at AP0 shift to right extremity ’3’ represents transverse write at ’AP 0’ and pushes the
data at the track beyond the TR distance to the right. This means that the entire data starting from the
row number i.e. the source address, is shifted to the right by a bit till the end of the track. In doing so only,
the last bit of data at the end of the track will be lost when issued with this command. This instruction is
issued when there is a need to shift the data to the right by one bit beyond the designated TR distance
into the track and write with AP 0.
v) Transverse write at AP1 shift to left extremity ’4’ represents transverse write at ’AP 1’ and pushes the data
at the track beyond the TR distance to left. This means that the entire data starting from the row number
i.e. the source address, is shifted to the left by a bit till the end of the track. In doing so only, the first bit
of data at the start of the track will be lost when issued with this command. This instruction is issued
when there is a need to shift the data to the left by one bit beyond the designated TR distance into the
track and write with AP 1.
vi) Transverse write at AP0 shift to left extremity ’5’represents transverse write at ’AP 0’ and pushes the data
at the track beyond the TR distance to left. This means that the entire data starting from the row number,
i.e. the source address, is shifted to the left by a bit till the start of the track. In doing so only, the first bit
of data at the start of the track will be lost when issued with this command. This instruction is issued
when there is a need to shift the data to the left by one bit beyond the designated TR distance into the
track and write with AP 0
vii) Transverse write at AP1 shift to right extremity ’6’ represents transverse write at ’AP 1’ and pushes the
data at the track beyond the TR distance to the right. This means that the entire data starting from the
row number, i.e. the source address, is shifted to the right by a bit till the end of the track. In doing so only,
the last bit of data at the end of the track will be lost when issued with this command. This instruction is
issued when there is a need to shift the data to the right by one bit beyond the designated TR distance
into the track and write with AP 1.
B) Basic Memory Operations :
i) ‘STORE’: When issued with this instruction, the "data" is loaded from the CPU to the local buffer and
then is written according to the write_op (0 - 6) after the TRd AP 0 or AP 1 aligns with the destination
’dst’ address. The peculiarity of this instruction is that the CPU data to be loaded can be supplied with the
instruction. For example, " cpim $96 0xA24B791CEF6 STORE 512 0 " implies that Data=0xA24B791CEF6
will be written at address $96 after the closest of the AP’s aligns with $96.
ii) ‘COPY’: When issued with this instruction, the closest of the access points will first align with the source
’src’ address, and then the "data" is read from the source ’src’ address to the local buffer. The read data in
the local buffer is then written according to the write_op (0 - 6) after the TRd AP 0 or AP 1 aligns with
the destination ’dst’ address. The different types of write_op (0 - 6) will be discussed in more detail in the
following paragraphs. The peculiarity of this instruction is that it reads the ’scr’ first and then writes the
read data. For example, " cpim $96 $12 COPY 512 0 " implies that source address ’scr’ $12 will be read
and transferred to the local buffer, and then it will be written at ’dst’ address $96 after the closest of the
AP’s aligns with both the source address $12 and the destination address $96 respectively.
iii) ‘SHL’ (logical shift left) represents clockwise rotation of the given ‘blocksize’ at the ‘src’. When issued
with this command, SPIMulator’s first step is to read at ‘scr’ by using the intelligent alignment of the
TRd access port and then rotate the data so as to have the ‘blocksized’ data placed between ‘nanowire
= ‘blocksized’’ to emph‘nanowire = ’512’’. The nanowires from ’0’ to ‘blocksize’ is substituted with ’bin
zero’. This operation is conducted in the source address and then the result is stored temporarily in the
local buffer till the write instruction is executed. The write instruction is always accompanied with ‘SHL’
instruction. An example for this instruction " cpim $32 $0 SHL 1 0 " will first align the either of the
AP’s nearest to $0 and data will be left shifted by 1 bit. The shifted data will be in the local buffer before
it is overwritten into the destination address $32. The ‘blocksize’ for this instructions can be ∼ [1, 8, 32]
which can left shift the data by 1 or 8 or 32 bits.
iv) ‘SHR’ (logical shift right) represents anti - clockwise rotation of the given ‘blocksize’ at the ‘src’. When
issued with this command, SPIMulator’s first step is to read at ‘scr’ address by using the intelligent
alignment of the TRd access port and then rotate the data so as to have the ‘blocksized’ data placed
between ‘nanowire = 0’ to ‘nanowire = ’‘blocksized’’’. The nanowires from ‘blocksized’ to ’512’ is substituted
with ’bin zero’. This operation is conducted in the source address and then the result is stored temporarily
in the local buffer till the write instruction is executed. The write instruction is always accompanied by
‘SHR’ instruction. An example for this instruction " cpim $32 $0 SHR 8 1 " will first align either of
the APs nearest to $0, and data will be right shifted by 8 bit. The shifted data will be in the local buffer
before it is transversely written into the destination address $32. The ‘blocksize’ for this instruction can
be ∼ [1, 8, 32], which can right shift the data by 1 or 8 or 32 bits.
v) ‘R AP0 and R AP1’ represents a simple read instruction at the src location after aligning either ’AP 0’ or
’AP 1’ access port which is the head or tail of TRd with src. Although this instruction is not mentioned
in the cpim instruction set the table, it is important to have these options so as to issue a simple read
command when necessary. An example of this instruction is " read $12 AP0 ", which will align the
access port AP 0 with source address $12 and then copies the data into the local buffer. These instructions
can be helpful when data is required to be moved out of the Domain Wall Memory to the CPU.
C) Logical Operations and Arithmetic Operation :
i) {‘AND’, ‘OR’, ‘XOR’, ‘XNOR’, ‘NAND’, ‘NOR’, ‘NOT’} represents the logical operation ‘and’, ‘or’, ‘xor’, ‘xnor’,
‘nand’, ‘nor’, ‘not’ individually when issued with the cpim instruction. The operation takes place among
the operands present between the TR distance after intelligently aligning the closest of the access port
with the source address ‘src’. The result of the operation is temporarily stored in the local buffer till it is
written according to the last three bits (0-6) of the instruction to the destination ‘dst’ address. An example
of logical operations is: " cpim $32 $0 and 511 0 " in which the ‘and’ operation is executed from source
address ‘src’ location to the TR size. The result is then stored in the local buffer and overwritten at the
destination address ‘dst’.
ii) ‘CARRY’ and ‘CARRYPRIME’ are a special instructions which are required for the ’ADD’ and ‘MULT’
operations. They are normally not called by the users as they are not the part of the arithmetic operations.
But users can still have the option to call these instructions in SPIMulator if they want to create custom
functions that will require ’CARRY’ and ’CARRYPRIME’ calculations. Both ’CARRY’ and ’CARRYPRIME’
operations counts the number of ones’s within the TRd distance and will output 1 to the local buffer.
’CARRY’ outputs 1 when the number of 1 within the TRd is any of the following 2,3,6,7. ’CARRYPRIME’
outputs 1 when the number of 1 within the TRd is any of the following 4,5,6,7. Example of carry instruction
is " cpim $32 $0 carry 511 1 " which issues a carry operation at source address $0 and transverse writes
at destination address at $0. Example of carryprime " cpim $32 $0 carryprime 511 0 " which issues a
carryprime operation at source address $0 and overwrites at destination address at $0. The output from
these instruction can be written in any way according to the last ’3 bit’ of the instruction i.e (0-6).
iii) ‘ADD’ represents the arithmetic ’addition ’ operation 𝐴 + 𝐵. We will show an example of an addition
operation for five operands in Fig. 5 for TRd = 7. It is important to note that we can perform addition
for (𝑇 𝑅𝑑 − 2) bits. Therefore, for our example, we can perform 5-bit addition for TRd = 7. In step 1, a TR
of 𝑑𝑤𝑚0 (first nanowire) is conducted. 𝑆0, which is XOR of 𝑎0...𝑒0, (5-bit number) is computed by the
PIM block, which is the blue bits between the AP 0 and AP 1 access ports. Simultaneously, carry, 𝐶0, is
computed and sent to the right to the driver (AP 1) for 𝑑𝑤𝑚1 (second nanowire) shown in orange and
carry prime 𝐶′
0 is sent to the left of the driver AP 0 for 𝑑𝑤𝑚2 (3rd nanowire), shown in green in fig. 5.
v) ‘MULT’ represents the arithmetic ‘multiplication’ operation 𝐴 ∗ 𝐵. A foundational method to compute
𝐴 ∗ 𝐵 is to sum A B times; e.g., for 𝐵 = 3, 𝐴 ∗ 3 can be computed as 𝐴 + 𝐴 + 𝐴. Thus, we can perform
multiplication by making several additions. Even with a 5 operand add, this method can quickly require
many steps. Consider 9𝐴; this can be computed by computing 5𝐴 in one step and then computing
5𝐴 + 𝐴 + 𝐴 + 𝐴 + 𝐴 in a second step. This method could be improved by generating 5𝐴 in one additional
step, then replicating 5𝐴 and summing to compute 25𝐴, and so on, but this clearly scales poorly. One
method to accelerate this process is to shift the copies of A, so as to quickly achieve the precise partial
products that, when summed, produce the desired product. We have reserved our last DBC $15 for the
purpose of shifting copies of A and executing carry, carry prime and add operations on the shifted copies
of A. This is the reduction process, as shown
----->  .idea folder contains test files used to create the project. 
They are not required for for the actual implementaion of the project.


