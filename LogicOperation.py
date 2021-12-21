import configuration as cfg
from functools import reduce

TRd = cfg.TRd
L = cfg.L
def And(memory, TRd_start_loc, TRd_end_loc):
    print(memory)
    print(TRd_start_loc)
    print(TRd_end_loc)
    mem = memory[TRd_start_loc:TRd_end_loc]
    print(mem)
    # Bitwise AND of List
    # Using reduce() + lambda + "&" operator
    res = reduce(lambda x, y: (int(x)) & (int (y)), mem)

    return res


def Nand(memory, TRd_start_loc):
    TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Calling and
    Andresult = And(mem)
    res = not (Andresult)  # complementing the and result

    return res


def Xor(memory, TRd_start_loc):
    TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Bitwise XOR of List
    # Using reduce() + lambda + "&" operator
    res = reduce(lambda x, y: x ^ y, mem)

    return res


def Xnor(memory, TRd_start_loc):
    TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Calling Xnor
    Xorresult = Xor(mem)
    res = not (Xorresult)  # complementing the and result

    return res


def Or(memory, TRd_start_loc):
    TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Bitwise OR of List
    # Using reduce() + lambda + "&" operator
    res = reduce(lambda x, y: x | y, mem)

    return res


def Nor(memory, TRd_start_loc):
    TRd_end_loc = TRd_start_loc + TRd - 1
    mem = memory[TRd_start_loc:TRd_end_loc]
    # Calling Nor
    Orresult = Or(mem)
    res = not (Orresult)  # complementing the and result

    return res

def Not(memory):
    None