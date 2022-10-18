# Imports
import os
import sys
import argparse
import logging
import binascii
import json




# Local imports
# (Can't use relative imports because this is a top-level script)
import bitcoin_toolset




# Shortcuts
from os.path import isdir, isfile, join
util = bitcoin_toolset.util
v = util.validate
remove_whitespace = util.misc.remove_whitespace
hexlify = binascii.hexlify
submodules = bitcoin_toolset.submodules
ecdsa_python3 = submodules.ecdsa_python3




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
    '-t', '--task',
    help="Task to perform (default: '%(default)s').",
    default='hello',
  )

  parser.add_argument(
    '--private-key-hex', dest='private_key_hex',
    help="A private key in hex string form.",
  )

  parser.add_argument(
    '--private-keys-file', dest='private_keys_file',
    help="Path to JSON file that contains one or more private keys in hex string form.",
  )

  parser.add_argument(
    '--public-key-hex', dest='public_key_hex',
    help="A public key in hex string form.",
  )

  parser.add_argument(
    '--signature-hex', dest='signature_hex',
    help="A signature in hex string form.",
  )

  parser.add_argument(
    '--data',
    help="Data string.",
  )

  parser.add_argument(
    '--data-file', dest='data_file',
    help="Path to file that contains a data string.",
  )

  parser.add_argument(
    '-l', '--log-level', type=str, dest='log_level',
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
    '-z', '--log-file', dest='log_file',
    help="The path to the file that log output will be written to.",
    default='log_bitcoin_toolset.txt',
  )

  a = parser.parse_args()

  # Check and analyse arguments
  if not a.log_to_file:
    a.log_file = None

  single_private_key_tasks = [
    'get_private_key_wif',
    'get_public_key',
    'get_address',
  ]
  if a.task in single_private_key_tasks:
    msg1 = "One of these arguments must be supplied: --private_key_hex '<string_value>' or --private_keys_file '<file_path>'"
    msg2 = "Either --private_key_hex '<string_value>' or --private_keys_file '<file_path>' must be supplied, but not both."
    if not a.private_key_hex and not a.private_keys_file:
      raise ValueError(msg1)
    if a.private_key_hex and a.private_keys_file:
      raise ValueError(msg2)
    if a.private_keys_file:
      a.private_keys = json.load(a.private_keys_file)

  if a.task == 'sign_data':
    msg1 = "One of these arguments must be supplied: --data '<string_value>' or --data_file '<file_path>'"
    msg2 = "Either --data '<string_value>' or --data_file '<file_path>' must be supplied, but not both."
    if not a.data and not a.data_file:
      raise ValueError(msg1)
    if a.data and a.data_file:
      raise ValueError(msg2)
    if a.data_file:
      a.data = open(a.data_file).read()



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
get_public_key
get_address
sign_data
verify_signature
create_transaction
sign_transaction
verify_signed_transaction
""".split()
  if a.task not in tasks:
    msg = "Unrecognised task: {}".format(a.task)
    msg += "\nTask list: {}".format(tasks)
    stop(msg)

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
  private_key_hex = util.misc.format_private_key_hex(a.private_key_hex)
  private_key_wif = bitcoin_toolset.code.basic.private_key_hex_to_wif(private_key_hex)
  print(private_key_wif)




def get_public_key(a):
  private_key_hex = util.misc.format_private_key_hex(a.private_key_hex)
  public_key_hex = ecdsa_python3.private_key_hex_to_public_key_hex(private_key_hex)
  print(public_key_hex)




def get_address(a):
  private_key_hex = util.misc.format_private_key_hex(a.private_key_hex)
  address = bitcoin_toolset.code.basic.private_key_hex_to_address(private_key_hex)
  print(address)




def sign_data(a):
  data_ascii = a.data
  v.validate_string_is_printable_ascii(data_ascii)
  data_hex = hexlify(data_ascii.encode()).decode('ascii')
  private_key_hex = util.misc.format_private_key_hex(a.private_key_hex)
  signature_hex = ecdsa_python3.create_deterministic_signature(private_key_hex, data_hex)
  print(signature_hex)
  # Double-check signature by default.
  public_key_hex = ecdsa_python3.private_key_hex_to_public_key_hex(private_key_hex)
  valid_signature = ecdsa_python3.verify_signature(public_key_hex, data_hex, signature_hex)
  if not valid_signature:
    raise ValueError("Invalid signature!")




def verify_signature(a):
  data_ascii = a.data
  v.validate_string_is_printable_ascii(data_ascii)
  data_hex = hexlify(data_ascii.encode()).decode('ascii')
  valid_signature = ecdsa_python3.verify_signature(a.public_key_hex, data_hex, a.signature_hex)
  if valid_signature:
    print("Valid signature.")
  else:
    print("Invalid signature!")




def create_transaction(a):
  pass




def sign_transaction(a):
  pass




def verify_signed_transaction(a):
  pass




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()




if __name__ == '__main__':
  main()

