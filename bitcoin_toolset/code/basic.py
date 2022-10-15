# Notes:
# - This file contains basic functions required for Bitcoin operations.
# - 'x' as an argument indicates a hex data string.




# Imports
import logging
import pkgutil




# Relative imports
from .. import util
from .. import submodules




# Shortcuts
v = util.validate
ripemd160 = submodules.ripemd160_python3
sha256 = submodules.sha256_python3




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




def private_key_hex_to_wif(private_key_hex):
  # add a "80" byte at the front (to indicate Bitcoin "mainnet").
  private_key_hex = "80" + private_key_hex
  private_key_wif = hex_to_base58check(private_key_hex)
  return private_key_wif




def hex_to_base58check(x):
  checksum_hex = get_double_sha256_checksum(x)
  x += checksum_hex
  x_base58 = hex_to_base58(x)
  n = count_leading_zero_bytes(x)
  output = n * '1' + x_base58
  return output




def hex_to_base58(x):
	v.validate_hex(x)
	y = int(x, 16)  # Convert from hex to integer.
	# The string base58_symbols can accessed as a 0-indexed list of characters.
	base58_symbols = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	output = ''
	y2 = y
	while y2 > 0:
		y2, remainder = divmod(y2, 58)
		# Use remainder as index for accessing the corresponding base58 symbol.
		output += base58_symbols[remainder]
	output = ''.join(reversed(output))
	return output




def count_leading_zero_bytes(x):
	count = 0
	for i in range(0, len(x), 2):
		byte = x[i:i+2]
		if byte == '00':
			count += 1
		else:
			break
	return count




def get_double_sha256_checksum(x):
  y = get_double_sha256(x)
  checksum_hex = y[:8]  # Select first 4 bytes
  return checksum_hex




def get_double_sha256(x):
  y = get_sha256(x)
  z = get_sha256(y)
  return z




def get_sha256(x):
  v.validate_hex(x)
  return sha256.hexdigest(x)




def get_ripemd160(x):
  v.validate_hex(x)
  return ripemd160.hexdigest(x)



