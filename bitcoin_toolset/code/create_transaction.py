# Imports
import logging
import argparse
from collections import defaultdict
import math




# Relative imports
from .. import util
from . import basic
from . import transaction
from . import transaction_input
from . import transaction_output




# Shortcuts
Namespace = argparse.Namespace
v = util.validate




# Set up logger for this module. By default, it produces no output.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.ERROR)
log = logger.info
deb = logger.debug




def setup(
    log_level = 'error',
    debug = False,
    log_timestamp = False,
    log_file = None,
    ):
  # Configure logger for this module.
  util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = __name__,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
  deb('Setup complete.')




# This "rocket launch management" function handles many important transaction aspects and decisions that are not part of the transaction object itself but play a role in its creation.
# Examples: fee rate, maximum spend percentage,
# input selection approach, allow_duplicate_output_address
# We also validate all the argument data.

def create_transaction(a):


  # [SECTION]: Validate arguments.
  # Validate argument object.
  if not isinstance(a, Namespace):
    raise TypeError
  expected = '''
inputs design
'''
  expected = expected.replace('\n', ' ').split()
  received = list(vars(a).keys())
  v.validate_list_contains_items(received, expected)

  validate_inputs(a.inputs)
  validate_design(a.design)

  log('All arguments validated. No problems found.')


  # Unpack various arguments.
  design = a.design
  received = list(design.keys())
  a.outputs = design['outputs']
  fee = design['fee'] if 'fee' in received else None
  fee_rate = design['fee_rate'] if 'fee_rate' in received else None
  change_address = design['change_address']
  max_fee = design['max_fee']
  max_spend_percentage = design['max_spend_percentage']
  input_selection_approach = design['input_selection_approach'] if 'input_selection_approach' in received else ["smallest_first"]


  # [SECTION]: Convert various arguments.
  max_spend_percentage = float(max_spend_percentage)
  # fee is an integer.
  # fee_rate is a string - convert it to a float.
  fee_type = 'fee' if fee else 'fee_rate'
  if fee_type == 'fee_rate':
    fee_rate = float(fee_rate)
  # Calculate satoshi amounts from the Bitcoin amounts.
  # - Add these to the original data.
  for x in a.inputs:
    x['satoshi_amount'] = basic.bitcoin_to_satoshi(x['bitcoin_amount'])
  for x in a.outputs:
    x['satoshi_amount'] = basic.bitcoin_to_satoshi(x['bitcoin_amount'])


  # [SECTION]: Report input and output data.
  log("Report input and output data.")
  for i, x in enumerate(a.inputs):
    address = x['address']
    txid = x['transaction_id']
    index = x['previous_output_index']
    ba = x['bitcoin_amount']
    sa = x['satoshi_amount']
    msg = '''
Input {i}:
- address: {address}
- txid: {txid}
- previous_output_index: {index}
- bitcoin_amount: {ba} ({sa} satoshi)
'''.strip().format(**vars())
    log(msg)
  for i, x in enumerate(a.outputs):
    address = x['address']
    ba = x['bitcoin_amount']
    sa = x['satoshi_amount']
    msg = '''
Output {i}:
- address: {address}
- bitcoin_amount: {ba} ({sa} satoshi)
'''.strip().format(**vars())
    log(msg)


  # [SECTION]: Create input and output instances.
  inputs = []  # Note that this is different from a.inputs.
  for x in a.inputs:
    input_ = transaction_input.TransactionInput.create(
      address = x['address'],
      txid = x['transaction_id'],
      previous_output_index_int = x['previous_output_index'],
      satoshi_amount = x['satoshi_amount'],
    )
    inputs.append(input_)
  log("Number of inputs: {}".format(len(inputs)))
  outputs = []  # Note that this is different from a.outputs.
  for x in a.outputs:
    output = transaction_output.TransactionOutput.create(
      address = x['address'],
      satoshi_amount = x['satoshi_amount'],
    )
    outputs.append(output)
  log("Number of outputs: {}".format(len(outputs)))


  # [SECTION]: Report aspects of the inputs and outputs.
  # Report each input address and the total value within it.
  input_addresses = defaultdict(int)
  for input_ in inputs:
    satoshi = input_.satoshi_amount
    address = input_.address
    input_addresses[address] += satoshi
  msg = "Input addresses and the value that they each contain:"
  for address in input_addresses:
    satoshi = input_addresses[address]
    bitcoin = basic.satoshi_to_bitcoin(satoshi)
    count = sum(1 for x in inputs if x.address == address)
    msg += "\n- {}: {} bitcoin ({} satoshi), {} inputs."
    msg = msg.format(address, bitcoin, satoshi, count)
  log(msg)
  # Report each output address and the total value to be sent to each.
  output_addresses = defaultdict(int)
  for output in outputs:
    satoshi = output.satoshi_amount
    address = output.address
    output_addresses[address] += satoshi
  msg = "Output addresses, with total value to be sent to each:"
  for address in output_addresses:
    satoshi = output_addresses[address]
    bitcoin = basic.satoshi_to_bitcoin(satoshi)
    msg += "\n- {}: {} bitcoin ({} satoshi)"
    msg = msg.format(address, bitcoin, satoshi)
  log(msg)
  # Check if multiple outputs use the same address.
  for address in output_addresses:
    count = sum(1 for x in outputs if x.address == address)
    if count > 1:
      msg = "Multiple outputs ({}) send to this address: {}".format(count, address)
      raise ValueError(msg)


  # [SECTION]: Select inputs, using the supplied input_selection_approach(es), until their combined value exceeds the total output value.
  selected_inputs = []
  total_selected_input = 0
  total_input = sum([x.satoshi_amount for x in inputs])
  total_input_bitcoin = basic.satoshi_to_bitcoin(total_input)
  total_output = sum([x.satoshi_amount for x in outputs])
  total_output_bitcoin = basic.satoshi_to_bitcoin(total_output)
  msg = "Total input value: {} bitcoin ({} satoshi)"
  msg = msg.format(total_input_bitcoin, total_input)
  log(msg)
  msg = "Total output value: {} bitcoin ({} satoshi)"
  msg = msg.format(total_output_bitcoin, total_output)
  log(msg)

  if total_input < total_output:
    shortfall = total_output - total_input
    shortfall_bitcoin = basic.satoshi_to_bitcoin(shortfall)
    msg = "Total input value is less than total output value."
    msg += "\n- Shortfall: {} bitcoin ({} satoshi)".format(shortfall_bitcoin, shortfall)
    raise ValueError(msg)
  elif total_input == total_output:
    log("Total input value exactly matches total output value.")
    selected_inputs = inputs
  else:
    surplus = total_input - total_output
    surplus_bitcoin = basic.satoshi_to_bitcoin(surplus)
    msg = "Total input value is greater than total output value."
    msg += "\n- Surplus value: {} bitcoin ({} satoshi)"
    msg = msg.format(surplus_bitcoin, surplus)
    log(msg)
    msg = "Selecting inputs according to input selection approaches {} until [total selected input value] exceeds [total output value]."
    msg = msg.format(input_selection_approach)
    log(msg)
    if len(input_selection_approach) > 1:
      raise NotImplementedError
    approach = input_selection_approach[0]
    # We create a new list of inputs that we can sort.
    # - Note that the dicts inside are not duplicated.
    inputs2 = inputs[:]
    if approach == 'smallest_first':
      inputs2.sort(key=lambda x: x.satoshi_amount)
    else:
      raise NotImplementedError
    for input_ in inputs2:
      total_selected_input += input_.satoshi_amount
      selected_inputs.append(input_)
      if total_selected_input >= total_output:
        break

  total_selected_input = sum([x.satoshi_amount for x in selected_inputs])
  total_selected_input_bitcoin = basic.satoshi_to_bitcoin(total_selected_input)
  msg = "Total selected input value: {} bitcoin ({} satoshi)"
  msg = msg.format(total_selected_input_bitcoin, total_selected_input)
  log(msg)


  # [SECTION]: Handle change.
  # Send any change to the change address. Create a new tx output if necessary.
  if total_selected_input == total_output:
    log("Total selected input value exactly matches total output value.")
  else:
    surplus = total_selected_input - total_output
    surplus_bitcoin = basic.satoshi_to_bitcoin(surplus)
    msg = "Total selected input value is greater than total output value."
    msg += "\n- Surplus value: {} bitcoin ({} satoshi)"
    msg += "\n- This extra value will be sent to the change address."
    msg += "\n- Change address: {}".format(change_address)
    msg = msg.format(surplus_bitcoin, surplus)
    log(msg)
    # Assign any surplus input value to the change address.
    change_output = None
    change_outputs = [x for x in outputs if x.address == change_address]
    if len(change_outputs) > 1:
      raise ValueError
    elif len(change_outputs) == 1:
      change_output = change_outputs[0]
      # Assign the surplus value to the change output.
      old_amount = change_output.satoshi_amount
      new_amount = old_amount + surplus
      change_output.set_satoshi_amount(new_amount)
      old_amount_bitcoin = basic.satoshi_to_bitcoin(old_amount)
      msg = "Change address found within outputs."
      msg += "\n- Old change amount: {} bitcoin ({} satoshi)"
      msg = msg.format(old_amount, old_amount_bitcoin)
      log(msg)
    else:
      # Create a new output for the change address if one doesn't already exist.
      change_output = transaction_output.TransactionOutput.create(
        address = change_address,
        satoshi_amount = surplus,
      )
      # Place change_output at the start of the outputs list.
      outputs.insert(0, change_output)
      msg = "New output created to send change to change address."
      log(msg)
    # Recalculate total_output.
    total_output = sum([x.satoshi_amount for x in outputs])
    total_output_bitcoin = basic.satoshi_to_bitcoin(total_output)
    msg = "New total output value: {} bitcoin ({} satoshi)"
    msg = msg.format(total_output_bitcoin, total_output)
    log(msg)
  # Double-check.
  if total_selected_input != total_output:
    raise ValueError
  change = change_output.satoshi_amount
  change_bitcoin = basic.satoshi_to_bitcoin(change)
  msg = "Change amount: {} bitcoin ({} satoshi)"
  msg = msg.format(change, change_bitcoin)
  log(msg)


  # [SECTION]: Manage spending limit.
  # Confirm that the amount that we are going to spend does not exceed the permitted limit.
  # - Note that the permitted limit is the total available input value, not the total selected input value.
  msg = "Maximum percentage of input value (prior to fee subtraction) that can be spent: {:.2f}%".format(max_spend_percentage)
  msg += '\n- Note: "spend" == send bitcoin to any address that is not the change address.'
  log(msg)
  max_spend = max_spend_percentage / 100 * total_input
  # Round up to the nearest satoshi.
  max_spend = int(math.ceil(max_spend))
  max_spend_bitcoin = basic.satoshi_to_bitcoin(max_spend)
  msg = "Maximum spend amount: {} bitcoin ({} satoshi)"
  msg = msg.format(max_spend_bitcoin, max_spend)
  log(msg)
  change = change_output.satoshi_amount
  spend = total_selected_input - change
  if spend == 0:
    # basic.satoshi_to_bitcoin doesn't accept a 0-value input.
    spend_bitcoin = '0.00000000'
  else:
    spend_bitcoin = basic.satoshi_to_bitcoin(spend)
  msg = "Spend amount: {} bitcoin ({} satoshi)"
  msg = msg.format(spend_bitcoin, spend)
  log(msg)
  spend_percentage = float(spend) / total_input * 100
  msg = "The spend amount is {:.2f}% of the available input value.".format(spend_percentage)
  log(msg)
  if spend > max_spend:
    msg = "Spend amount ({s} bitcoin) is greater than the maximum permitted spend amount ({m} bitcoin)."
    msg = msg.format(s=spend_bitcoin, m=max_spend_bitcoin)
    msg += " To spend this amount, you will need to increase the --max-spend-percentage value from {m:.0f} to {s:.0f}."
    msg = msg.format(m=max_spend_percentage, s=int(spend_percentage)+1)
    raise ValueError(msg)


  # [SECTION]: Manage fee
  n_inputs = len(inputs)
  n_outputs = len(outputs)
  estimated_tx_size = estimate_transaction_size(n_inputs, n_outputs)
  msg = "Estimated transaction size: {} bytes".format(estimated_tx_size)
  log(msg)
  msg = 'Fee type: {}'.format(fee_type)
  log(msg)
  if fee_type == 'fee':
    msg = 'Fee: {} (satoshi)'.format(fee)
  elif fee_type == 'fee_rate':
    msg = 'Fee rate: {} (satoshi/byte)'.format(fee_rate)
  log(msg)
  # Calculate approximate fee.
  final_fee = None
  final_fee_rate = None
  if fee_type == 'fee':
    final_fee = fee
  elif fee_type == 'fee_rate':
    final_fee = estimated_tx_size * fee_rate
    # Round up to the nearest satoshi.
    final_fee = int(math.ceil(float(final_fee)))
  msg = "Transaction fee: {} satoshi".format(final_fee)
  log(msg)
  final_fee_rate = float(final_fee) / estimated_tx_size
  if fee_type == 'fee':
    msg = "Estimated fee rate: {:.4f} satoshi/byte".format(final_fee_rate)
    log(msg)
  # Check whether the fee passes the fee limit.
  msg = "Maximum fee: {} satoshi".format(max_fee)
  log(msg)
  if final_fee > max_fee:
    msg = "The fee ({f} satoshi) is greater than the specified maximum fee ({m} satoshi).".format(f=final_fee, m=max_fee)
    raise ValueError(msg)
  # Check whether there is enough change to pay the fee.
  change = change_output.satoshi_amount
  if final_fee > change:
    difference = final_fee - change
    msg = '''
The fee is greater than the change amount.
- Fee: {} satoshi
- Change amount: {} satoshi
- Difference: {} satoshi
'''.strip().format(final_fee, change, difference)
    raise ValueError(msg)
  # Subtract fee from change amount.
  new_change = change - final_fee
  if new_change == 0:
    # If the fee entirely consumes the change, then we delete the change output.
    outputs = outputs[1:]
    msg = "The fee will use the entire change amount."
    msg += " The change output has been deleted."
    log(msg)
  else:
    change_output.set_satoshi_amount(new_change)
    log("Fee subtracted from change amount.")
    change = change_output.satoshi_amount
    change_bitcoin = basic.satoshi_to_bitcoin(change)
    msg = "New change amount: {} bitcoin ({} satoshi)"
    msg = msg.format(change, change_bitcoin)
    log(msg)


  # [SECTION]: Create transaction
  tx = transaction.Transaction.create(selected_inputs, outputs)
  log("Transaction created.")
  return tx




def estimate_transaction_size(n_inputs, n_outputs):
  # A standard signed transaction contains:
  # - version (4 bytes)
  # - input_count (1-byte var_int) [1 byte if number of inputs is <= 252]
  # - concatenated inputs (with signatures)
  # - output_count (1-byte var_int) [1 byte if number of outputs is <= 252]
  # - concatenated outputs
  # - block lock time (4 bytes)
  # A standard input contains:
  # - previous_output_hash (32 bytes)
  # - previous_output_index (4 bytes)
  # - script_length (1-byte var_int)
  # - scriptSig [approximately 138 bytes]
  # - sequence (4 bytes)
  # A standard output contains:
  # - value (8 bytes)
  # - script_length (1-byte var_int)
  # - scriptPubKey (25 bytes)
  input_count_bytes = basic.hex_len(basic.int_to_var_int(n_inputs))
  inputs_bytes = n_inputs * (32 + 4 + 1 + 138 + 4)
  output_count_bytes = basic.hex_len(basic.int_to_var_int(n_outputs))
  outputs_bytes = n_outputs * (8 + 1 + 25)
  estimated_tx_size = (
    4
    + input_count_bytes
    + inputs_bytes
    + output_count_bytes
    + outputs_bytes
    + 4
  )
  return estimated_tx_size




def validate_inputs(inputs):
  # List of inputs downloaded from the blockchain.
  # - Note that the inputs come from JSON data, so numbers will be integers, not strings.
  # Example:
  # [
  #   {
  #     "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
  #     "transaction_id": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
  #     "previous_output_index": 9,
  #     "bitcoin_amount": "0.002"
  #   }
  # ]
  v.validate_list(inputs)
  for input_ in inputs:
    expected = '''
address transaction_id previous_output_index bitcoin_amount
'''
    expected = expected.replace('\n', ' ').split()
    received = list(input_.keys())
    v.validate_lists_are_identical(received, expected)
    basic.validate_bitcoin_address(input_['address'])
    v.validate_hex_length(input_['transaction_id'], 32)
    v.validate_whole_number(input_['previous_output_index'])
    basic.validate_bitcoin_amount(input_['bitcoin_amount'])



def validate_design(design):
  # JSON data containing the design for a new transaction.
  # Not included: input data.
  # Example:
  # {
  #   "change_address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
  #   "fee": 225,
  #   "max_fee": 250,
  #   "max_spend_percentage": "100.00",
  #   "input_selection_approach": ["smallest_first"],
  #   "outputs": [
  #     {
  #       "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
  #       "bitcoin_amount": "0.00199775"
  #     }
  #   ]
  # }
    expected = '''
change_address max_fee max_spend_percentage outputs
'''
    expected = expected.replace('\n', ' ').split()
    received = list(design.keys())
    v.validate_list_contains_items(received, expected)

    # Unpack values
    change_address = design['change_address']
    fee = design['fee'] if 'fee' in received else None
    fee_rate = design['fee_rate'] if 'fee_rate' in received else None
    max_fee = design['max_fee']
    max_spend_percentage = design['max_spend_percentage']
    input_selection_approach = design['input_selection_approach'] if 'input_selection_approach' in received else None
    outputs = design['outputs']

    # Validate change_address
    basic.validate_bitcoin_address(change_address)

    # Validate max_fee
    v.validate_whole_number(max_fee)

    # Validate max_spend_percentage
    max_spend_percentage = float(max_spend_percentage)
    v.validate_integer_domain(int(max_spend_percentage), min_value=0, max_value=100)

    # Validate outputs
    v.validate_list(outputs)
    for output in outputs:
      expected2 = '''
address bitcoin_amount
'''
      expected2 = expected2.replace('\n', ' ').split()
      received2 = list(output.keys())
      v.validate_lists_are_identical(received2, expected2)
      basic.validate_bitcoin_address(output['address'])
      basic.validate_bitcoin_amount(output['bitcoin_amount'])
      output['bitcoin_amount'] = basic.ensure_8_decimal_places(output['bitcoin_amount'])

    # Validate fee / fee_rate
    flag = 0
    if fee and fee_rate:
      flag = 1
    if fee is None and fee_rate is None:
      flag = 1
    if flag:
      msg = '''
Design must contain exactly one of these keys:
- fee (integer)
- fee_rate (integer or decimal)
'''.strip()
      raise ValueError(msg)

    if fee:
      # Permit 0-satoshi fee.
      v.validate_whole_number(design['fee'])

    if fee_rate:
      v.validate_string_is_whole_number_or_decimal(design['fee_rate'])

    # Validate input_selection_approach
    # - Ensure that conflicting input selection approaches are not used together.
    if input_selection_approach:
      approaches = input_selection_approach
      log(approaches)
      v.validate_list(approaches)
      available_approaches = [
        'smallest_first', 'largest_first',
        'one_address_at_a_time', 'any_address',
        'smallest_address_first', 'largest_address_first',
      ]
      conflicts = [
        ('smallest_first', 'largest_first'),
        ('one_address_at_a_time', 'any_address'),
        ('smallest_address_first', 'largest_address_first'),
      ]
      for c in conflicts:
        x, y = c
        if x in approaches and y in approaches:
          msg = "In the input selection approach list, cannot use both '{}' and '{}' together."
          msg = msg.format(x, y)
          raise ValueError(msg)


