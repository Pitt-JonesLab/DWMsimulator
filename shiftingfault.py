
import config as config
import LogicOperation as logicop

TRd_size = config.TRd_size
# Initializing single Local Buffer for all DBC's
Local_row_buffer = [0] * (512)

def parity_checking(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos):
  """
  Parity checking is a method for detecting errors in data. It works by generating a parity bit,
  which is a single bit that is calculated from the data. The parity bit is then used to check
  if there are any errors in the data.

  Args:
    data: The data to be checked.

  Returns:
    True if there are no errors in the data, False otherwise.
  """





  # Shifting the data within the TRd space to right and writing at the TRd head
  for i in range(TRd_head, TRd_head + TRd_size - 1):
      # Calculate the parity bit.
      parity_bit = 0
      for j in range(nanowire_num_start_pos, nanowire_num_end_pos + 1):
        bit = memory[i][j]
        # parity_bit ^= bit
        Local_buffer = logicop.Xor(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)

      # # Check if the parity bit is 0.
      # for i in range(0, len(Local_buffer)):
      #   if i == 0:
      #     return True
      # # call reed solomon
      # #error_correction
      # # call
      #   else:
      #     return False

  return Local_buffer

def reed_solomon(data, k, n):
  """
  Reed-Solomon error correction is a method for correcting errors in data. It works by generating a parity code, which is a redundant representation of the data. The parity code is then used to detect and correct errors in the data.

  Args:
    data: The data to be protected.
    k: The number of data bits.
    n: The total number of bits.

  Returns:
    The corrected data.
  """

  # Check if the parameters are valid.
  if k > n:
    raise ValueError("The number of data bits must be less than or equal to the total number of bits.")

  # Generate the parity code.
  parity_code = np.zeros(n - k, dtype=int)
  for i in range(n - k):
    for j in range(k):
      parity_code[i] ^= data[j] * (2 ** i)

  # Check if there are any errors in the data.
  if np.any(data != np.bitwise_xor(data, parity_code)):
    # There are errors in the data.
    # Correct the errors using the parity code.
    for i in range(n - k):
      if data[i] != np.bitwise_xor(data[i], parity_code[i]):
        # There is an error in the current bit.
        # Correct the error by flipping the bit.
        data[i] = 1 - data[i]

  # Return the corrected data.
  return data


def corrective_shift(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos):
  """
  Error correction is a method for correcting errors in data. It works by comparing the data to a known good copy of the data.
  The errors are then corrected using a variety of techniques, such as majority voting and Reed-Solomon error correction.

  Args:
    data: The data to be corrected.
    shift_distance: The distance that the data has been shifted.

  Returns:
    The corrected data.
  """
  # Calling parity checking method to determine single bit error:
  Local_buffer = parity_checking(memory, TRd_head, nanowire_num_start_pos, nanowire_num_end_pos)
  data = memory[TRd_head][:]
  # # Check if the parity bit is 0.
  for i in range(0, len(Local_buffer)):
    if i == 1:
        # There is an error in the current bit.
        # Correct the error by flipping the bit.
        data[i][:] = 1 - data[i][:]

    # Return the corrected data.
    return data
