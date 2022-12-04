# Imports
import os
import sys
import argparse
import logging
import binascii
import json
import itertools




# Local imports
# (Can't use relative imports because this is a top-level script)
import bitcoin_toolset




# Shortcuts
from os.path import isdir, isfile, join
util = bitcoin_toolset.util
v = util.validate
hexlify = binascii.hexlify
submodules = bitcoin_toolset.submodules




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
  logger_name = 'cli'
  # Configure logger for this module.
  bitcoin_toolset.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = logger_name,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
  deb('Setup complete.')
  # Configure logging levels for bitcoin_toolset package.
  # By default, without setup, it logs at ERROR level.
  # Optionally, the package could be configured here to use a different log level, by e.g. passing in 'error' instead of log_level.
  bitcoin_toolset.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )




def main():

  # Capture and parse command-line arguments.

  parser = argparse.ArgumentParser(
    description='Command-Line Interface (CLI) for using the bitcoin_toolset package.'
  )

  parser.add_argument(
    '-t', '--task', type=str,
    help="Task to perform (default: '%(default)s').",
    default='hello',
  )

  group = parser.add_mutually_exclusive_group()

  group.add_argument(
    '--private-key-hex', dest='private_key_hex', type=str,
    nargs='+', action='append',
    help="A private key in hex string form.",
  )

  group.add_argument(
    '--private-key-file', dest='private_key_file', type=str,
    nargs='+', action='append',
    help="Path to file that contains a private key in hex string form.",
  )

  group.add_argument(
    '--private-key-dir', dest='private_key_dir', type=str,
    help="Path to directory that contains .txt files that each contain a single private key.",
  )

  group.add_argument(
    '--private-key-wif', dest='private_key_wif', type=str,
    help="A private key in WIF (Wallet Import Format).",
  )

  parser.add_argument(
    '--public-key-hex', dest='public_key_hex', type=str,
    help="A public key in hex string form.",
  )

  parser.add_argument(
    '--signature-hex', dest='signature_hex', type=str,
    help="A signature in hex string form.",
  )

  group = parser.add_mutually_exclusive_group()

  group.add_argument(
    '--data', type=str,
    help="Data string.",
  )

  group.add_argument(
    '--data-file', dest='data_file', type=str,
    help="Path to file that contains a data string.",
  )

  parser.add_argument(
    '--input-file', dest='input_file', type=str,
    help="Path to file that contains the available inputs for the transaction.",
  )

  parser.add_argument(
    '--design-file', dest='design_file', type=str,
    help="Path to file that contains the available inputs for the transaction.",
  )

  parser.add_argument(
    '-l', '--log-level', dest='log_level', type=str,
    choices=['debug', 'info', 'warning', 'error'],
    help="Choose logging level (default: '%(default)s').",
    default='error',
  )

  parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help="Sets log level to 'debug'. This overrides --log-level.",
  )

  parser.add_argument(
    '-s', '--log-timestamp', dest='log_timestamp',
    action='store_true',
    help="Choose whether to prepend a timestamp to each log line.",
  )

  parser.add_argument(
    '-x', '--log-to-file', dest='log_to_file',
    action='store_true',
    help="Choose whether to save log output to a file.",
  )

  parser.add_argument(
    '-z', '--log-file', dest='log_file', type=str,
    help="The path to the file that log output will be written to.",
    default='log_bitcoin_toolset.txt',
  )

  a = parser.parse_args()

  print_args = 0
  if print_args:
    print()
    for k in sorted(a.__dict__.keys()):
      print(k, '=', a.__dict__[k])
    print()

  # Check and analyse arguments
  if not a.log_to_file:
    a.log_file = None

  if a.data_file:
    a.data = open(a.data_file).read()

  # Load the private key(s) from the provided source.
  # - Note: Only one source can be supplied.
  a.private_keys_hex = []

  if a.private_key_hex:
    a.private_keys_hex = list(itertools.chain(*a.private_key_hex))

  if a.private_key_file:
    a.private_key_files = list(itertools.chain(*a.private_key_file))
    private_keys_hex = [open(x).read().strip() for x in a.private_key_files]
    a.private_keys_hex.extend(private_keys_hex)

  if a.private_key_dir:
    a.private_key_files = [os.path.join(a.private_key_dir, x) for x in os.listdir(a.private_key_dir) if os.path.splitext(x)[1] == '.txt']
    private_keys_hex = [open(x).read().strip() for x in a.private_key_files]
    a.private_keys_hex.extend(private_keys_hex)

  tasks_single_private_key = [
    'get_private_key_wif',
    'get_public_key',
    'get_address',
    'sign_data',
  ]
  if a.task in tasks_single_private_key:
    assert len(a.private_keys_hex) == 1
    a.private_key_hex = a.private_keys_hex[0]

  tasks_that_require_data = [
    'sign_data',
    'validate_unsigned_transaction_json',
  ]

  if a.task in tasks_that_require_data:
    if not a.data:
      z = '--data <data_string> --data-file <file_path>'
      msg = 'One of these arguments must be supplied: {}'.format(z)
      raise ValueError(msg)

  tasks_that_sign_transactions = [
    'create_unsigned_transaction_json',
    'create_sign_and_verify_transaction_hex',
    'create_transaction',
  ]

  a.inputs = None
  a.design = None
  if a.task in tasks_that_sign_transactions:
    if not a.input_file:
      z = "--input-file '<input_file>'"
      msg = 'This argument must be supplied: {}'.format(z)
      raise ValueError(msg)
    if not a.design_file:
      z = "--design-file '<design_file>'"
      msg = 'This argument must be supplied: {}'.format(z)
      raise ValueError(msg)
    try:
      a.inputs = json.load(open(a.input_file))
    except Exception as e:
      raise e
    try:
      a.design = json.load(open(a.design_file))
    except Exception as e:
      raise e




  # Setup
  setup(
    log_level = a.log_level,
    debug = a.debug,
    log_timestamp = a.log_timestamp,
    log_file = a.log_file,
  )

  # Note: If you add a new task function, then its name must be added to this list.
  tasks = """
hello hello2 get_python_version
get_private_key_wif
private_key_wif_to_hex
get_public_key
get_address
sign_data
verify_data_signature
create_unsigned_transaction_json
validate_unsigned_transaction_json
create_signed_transaction_json
verify_signed_transaction_json
create_signed_transaction_hex
verify_signed_transaction_hex
decode_signed_transaction_hex
create_sign_and_verify_transaction_hex
create_transaction
""".split()
  if a.task not in tasks:
    msg = "Unrecognised task: {}".format(a.task)
    msg += "\nTask list: {}".format(tasks)
    stop(msg)
  if a.task not in globals():
    msg = "Task function '{}' not found.".format(a.task)
    raise NameError(msg)

  # Run top-level function (i.e. the appropriate task).
  globals()[a.task](a)




def hello(a):
  # Confirm:
  # - that we can run a simple task.
  # - that this tool has working logging.
  log('Log statement at INFO level')
  deb('Log statement at DEBUG level')
  print('hello world')




def hello2(a):
  # Confirm:
  # - that we can run a simple task from within the package.
  # - that the package has working logging.
  bitcoin_toolset.code.hello.hello()




def get_python_version(a):
  # Confirm:
  # - that we can run a shell command.
  check = util.misc.shell_tool_exists('python3')
  v.validate_boolean(check)
  if check is not True:
    msg = "Can't find 'python3' tool in bash shell'"
    raise ValueError(msg)
  cmd = 'python3 --version'
  output, exit_code = util.misc.run_local_cmd(cmd)
  if exit_code != 0:
    msg = "Ran command = '{x}', but got exit code = {c}".format(x=cmd, c=exit_code)
    raise ValueError(msg)
  print(output.strip())




def get_private_key_wif(a):
  private_key_wif = bitcoin_toolset.code.basic.private_key_hex_to_wif(a.private_key_hex)
  print(private_key_wif)




def private_key_wif_to_hex(a):
  private_key_hex = bitcoin_toolset.code.basic.private_key_wif_to_hex(a.private_key_wif)
  print(private_key_hex)




def get_public_key(a):
  public_key_hex = bitcoin_toolset.code.basic.private_key_hex_to_public_key_hex(a.private_key_hex)
  print(public_key_hex)




def get_address(a):
  address = bitcoin_toolset.code.basic.private_key_hex_to_address(a.private_key_hex)
  print(address)




def sign_data(a):
  data_ascii = a.data
  v.validate_string_is_printable_ascii(data_ascii)
  data_hex = hexlify(data_ascii.encode()).decode('ascii')
  signature_hex = bitcoin_toolset.code.basic.create_deterministic_signature(a.private_key_hex, data_hex)
  print(signature_hex)
  # Double-check signature by default.
  public_key_hex = bitcoin_toolset.code.basic.private_key_hex_to_public_key_hex(a.private_key_hex)
  valid_signature = bitcoin_toolset.code.basic.verify_signature(public_key_hex, data_hex, signature_hex)
  if not valid_signature:
    raise ValueError("Invalid signature!")




def verify_data_signature(a):
  data_ascii = a.data
  v.validate_string_is_printable_ascii(data_ascii)
  data_hex = hexlify(data_ascii.encode()).decode('ascii')
  valid_signature = bitcoin_toolset.code.basic.verify_signature(a.public_key_hex, data_hex, a.signature_hex)
  if valid_signature:
    print("Valid signature.")
  else:
    print("Invalid signature!")




def create_unsigned_transaction_json(a):
  tx_unsigned = bitcoin_toolset.code.create_transaction.create_transaction(a)
  tx_unsigned_json = tx_unsigned.to_json()
  print(tx_unsigned_json)
  # Validate transaction by default by rebuilding it.
  tx_unsigned_2 = bitcoin_toolset.code.transaction.Transaction.from_json(tx_unsigned_json)




def validate_unsigned_transaction_json(a):
  tx_unsigned_json = a.data
  tx_unsigned = bitcoin_toolset.code.transaction.Transaction.from_json(tx_unsigned_json)
  print("Unsigned transaction data validated.")




def create_signed_transaction_json(a):
  # Note: When the unsigned tx is built from the JSON data, it is validated.
  tx_unsigned_json = a.data
  tx_unsigned = bitcoin_toolset.code.transaction.Transaction.from_json(tx_unsigned_json)
  #deb(tx_unsigned)
  tx_signed = tx_unsigned.sign(a.private_keys_hex)
  #deb(tx_signed.to_json())
  print(tx_signed.to_json())
  valid_signatures = tx_signed.verify()
  plural = 's' if len(tx_signed.inputs) > 1 else ''
  if not valid_signatures:
    msg = "Invalid signature{}!".format(plural)
    raise ValueError(msg)




def verify_signed_transaction_json(a):
  tx_signed_json = a.data
  tx_signed = bitcoin_toolset.code.transaction.Transaction.from_json(tx_signed_json)
  valid_signatures = tx_signed.verify()
  plural = 's' if len(tx_signed.inputs) > 1 else ''
  if valid_signatures:
    msg = "Valid signature{}.".format(plural)
    print(msg)
  else:
    msg = "Invalid signature{}!.".format(plural)
    print(msg)




def create_signed_transaction_hex(a):
  tx_signed_json = a.data
  tx_signed = bitcoin_toolset.code.transaction.Transaction.from_json(tx_signed_json)
  valid_signatures = tx_signed.verify()
  print(tx_signed.to_hex_signed_form())
  plural = 's' if len(tx_signed.inputs) > 1 else ''
  if not valid_signatures:
    msg = "Invalid signature{}!".format(plural)
    raise ValueError(msg)




def decode_signed_transaction_hex(a):
  tx_signed_hex = a.data.strip()
  tx_signed = bitcoin_toolset.code.transaction.Transaction.from_hex_signed(tx_signed_hex)
  valid_signatures = tx_signed.verify()
  print(tx_signed.to_json())
  plural = 's' if len(tx_signed.inputs) > 1 else ''
  if not valid_signatures:
    msg = "Invalid signature{}!".format(plural)
    raise ValueError(msg)




def verify_signed_transaction_hex(a):
  tx_signed_hex = a.data.strip()
  tx_signed = bitcoin_toolset.code.transaction.Transaction.from_hex_signed(tx_signed_hex)
  valid_signatures = tx_signed.verify()
  plural = 's' if len(tx_signed.inputs) > 1 else ''
  if not valid_signatures:
    msg = "Invalid signature{}!".format(plural)
    raise ValueError(msg)
  msg = "Valid signature{}.".format(plural)
  print(msg)




def create_sign_and_verify_transaction_hex(a):
  # - Create tx
  tx_unsigned = bitcoin_toolset.code.create_transaction.create_transaction(a)
  tx_unsigned_json = tx_unsigned.to_json()
  #print(tx_unsigned_json)
  # - Validate tx (by rebuilding it)
  tx_unsigned_2 = bitcoin_toolset.code.transaction.Transaction.from_json(tx_unsigned_json)
  # - Sign tx
  tx_signed = tx_unsigned.sign(a.private_keys_hex)
  #deb(tx_signed.to_json())
  # - Verify tx
  valid_signatures = tx_signed.verify()
  plural = 's' if len(tx_signed.inputs) > 1 else ''
  if not valid_signatures:
    msg = "Invalid signature{}!".format(plural)
    raise ValueError(msg)
  # - Get hex form of signed tx
  tx_signed_hex = tx_signed.to_hex_signed_form()
  # - Decode and verify signed tx hex.
  tx_signed_2 = bitcoin_toolset.code.transaction.Transaction.from_hex_signed(tx_signed_hex)
  valid_signatures_2 = tx_signed_2.verify()
  plural_2 = 's' if len(tx_signed_2.inputs) > 1 else ''
  #print(tx_signed_2.to_json())
  if not valid_signatures_2:
    msg = "Signed tx hex: Invalid signature{}!".format(plural_2)
    raise ValueError(msg)
  # Print the signed tx hex.
  print(tx_signed_hex)




def create_transaction(a):
  return create_sign_and_verify_transaction_hex(a)




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()




if __name__ == '__main__':
  main()

