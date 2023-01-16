# Imports
import logging
import pkgutil




# Relative imports
from .. import util
from .. import submodules




# Shortcuts
v = util.validate
ecdsa = submodules.ecdsa_python3
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




# Notes:
# - This file contains basic functions required for Bitcoin operations.
# - 'x' as an argument indicates a hex string.
# - 's' as an argument indicates a string.
# - 'n' as an argument indicates an integer.
# - 'b' as an argument indicates a byte sequence.

# My working definition of a standard address is: Pay-To-Public-Key-Hash (P2PKH) where the public key was not compressed before being hashed.

# This is my current understanding of a standard scriptPubKey:
#
# scriptPubKey:
# START FORMAT
# - OP_DUP: 76
# - OP_HASH160: a9
# - PUSHDATA: 14
# - [derived property] PUSHDATA decimal value: 20
# - public_key_hash: 20 bytes (big-endian)
# - OP_EQUALVERIFY: 88
# - OP_CHECKSIG: ac
# END FORMAT




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
  # - scriptSig [approximately 138-139 bytes]
  # - sequence (4 bytes)
  # 1 input ~= 180 bytes. So, at 1 sat per byte, if the input contains less than 180 satoshi, you lose money if you spend it. This ignores the basic cost of the transaction.
  # - However, if you're already building a transaction for a separate reason at the low fee rate of 1 sat/byte, it makes sense to tack on any input with > 180 satoshi.
  # A standard output contains:
  # - value (8 bytes)
  # - script_length (1-byte var_int)
  # - scriptPubKey (25 bytes)
  input_count_bytes = hex_len(int_to_var_int(n_inputs))
  inputs_bytes = n_inputs * (32 + 4 + 1 + 138 + 4)
  output_count_bytes = hex_len(int_to_var_int(n_outputs))
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




def signature_from_der(signature_hex):
  v.validate_hex(signature_hex)
  order = None
  signature_bytes = bytes.fromhex(signature_hex)
  r, s = ecdsa.ecdsa.code.utility.sigdecode_der(signature_bytes, order)
  r_hex = int_to_hex(r)
  s_hex = int_to_hex(s)
  # Pad r and s with leading 0 bytes, so that we ensure that they are 32 bytes long.
  r_hex = pad_hex(r_hex, n_bytes=32)
  s_hex = pad_hex(s_hex, n_bytes=32)
  signature_hex = r_hex + s_hex
  msg = "Signature decoded from DER encoding:"
  msg += "\nsignature_hex ({} bytes) = {}".format(hex_len(signature_hex), signature_hex)
  msg += "\nr_hex ({} bytes) = {}".format(hex_len(r_hex), r_hex)
  msg += "\ns_hex ({} bytes) = {}".format(hex_len(s_hex), s_hex)
  deb(msg)
  return signature_hex




def signature_to_der(signature_hex):
  # Convert the signature (r, s) into DER encoding. The Python ECDSA library includes a function for doing this.
  r_hex, s_hex = ecdsa.ecdsa.code.convenience.signature_hex_to_r_and_s_hex(signature_hex)
  r_int = int(r_hex, 16)
  s_int = int(s_hex, 16)
  # order = signing_key.privkey.order
  # sigencode_der doesn't actually use the order argument.
  order = None
  signature_bytes = ecdsa.ecdsa.code.utility.sigencode_der(r_int, s_int, order)
  signature_hex_2 = signature_bytes.hex()
  return signature_hex_2




def verify_signature_digest(public_key_hex, digest_hex, signature_hex):
  v.validate_hex_length(public_key_hex, 64)
  v.validate_hex(digest_hex, 64)
  #v.validate_hex_length(signature_hex, 64)
  valid_signature = ecdsa.verify_signature_digest_low_s(public_key_hex, digest_hex, signature_hex)
  return valid_signature




def verify_signature(public_key_hex, data_hex, signature_hex):
  v.validate_hex_length(public_key_hex, 64)
  v.validate_hex(data_hex)
  v.validate_hex_length(signature_hex, 64)
  valid_signature = ecdsa.verify_signature_low_s(public_key_hex, data_hex, signature_hex)
  return valid_signature




def create_deterministic_signature(private_key_hex, data_hex):
  return ecdsa.create_deterministic_signature_low_s(private_key_hex, data_hex)




def create_deterministic_signature_for_digest(private_key_hex, digest_hex):
  return ecdsa.create_deterministic_signature_for_digest_low_s(private_key_hex, digest_hex)




def create_signature_for_digest(private_key_hex, digest_hex, random_value_hex):
  return ecdsa.create_signature_for_digest_low_s(private_key_hex, digest_hex, random_value_hex)




def script_pub_key_to_address(script_pub_key):
  # Remove first 3 bytes and last 2 bytes.
  hash_hex = script_pub_key[3*2:-2*2]
  address = public_key_hash_hex_to_address(hash_hex)
  return address




def private_key_hex_to_address(private_key_hex):
  private_key_hex = ecdsa.format_private_key_hex(private_key_hex)
  ecdsa.validate_private_key_hex(private_key_hex)
  public_key_hex = ecdsa.private_key_hex_to_public_key_hex(private_key_hex)
  address = public_key_hex_to_address(public_key_hex)
  return address




def public_key_hex_to_address(public_key_hex):
  hash_hex = get_public_key_hash(public_key_hex)
  address = public_key_hash_hex_to_address(hash_hex)
  return address




def public_key_hash_hex_to_address(hash_hex):
  # Add version byte to public key hash ("00" for "main Bitcoin network").
  hash_hex_2 = "00" + hash_hex
  # Convert the public key hash to Base58Check format.
  address = hex_to_base58check(hash_hex_2)
  return address




def public_key_hex_to_script_pub_key(public_key_hex):
  hash_hex = get_public_key_hash(public_key_hex)
  script_pub_key, script_length = public_key_hash_hex_to_script_pub_key(hash_hex)
  return script_pub_key, script_length




def get_public_key_hash(public_key_hex):
  # Add identification byte to public key ("04" for "uncompressed") to get an uncompressed Bitcoin public key
  public_key_hex = "04" + public_key_hex
  public_key_bytes = bytes.fromhex(public_key_hex)
  digest_1 = sha256.digest(public_key_bytes)
  digest_2 = ripemd160.digest(digest_1)
  digest_2_hex = digest_2.hex()
  v.validate_hex_length(digest_2_hex, 20)
  return digest_2_hex




def private_key_hex_to_public_key_hex(private_key_hex):
  private_key_hex = ecdsa.format_private_key_hex(private_key_hex)
  ecdsa.validate_private_key_hex(private_key_hex)
  public_key_hex = ecdsa.private_key_hex_to_public_key_hex(private_key_hex)
  return public_key_hex




def private_key_hex_to_wif(private_key_hex):
  # "WIF" = "Wallet Import Format"
  private_key_hex = ecdsa.format_private_key_hex(private_key_hex)
  ecdsa.validate_private_key_hex(private_key_hex)
  # Add a "80" byte at the front (to indicate Bitcoin "mainnet").
  private_key_hex = "80" + private_key_hex
  private_key_wif = hex_to_base58check(private_key_hex)
  return private_key_wif




def private_key_wif_to_hex(private_key_wif):
  private_key_hex = base58check_to_hex(private_key_wif)
  # Remove "80" byte from the front.
  private_key_hex = private_key_hex[2:]
  ecdsa.validate_private_key_hex(private_key_hex)
  return private_key_hex




def script_sig_to_signature_hex_and_public_key_hex(script_sig):
  v.validate_hex(script_sig)
  b = script_sig[0:2]  # b = byte
  n = var_int_to_int(b)
  m = n*2+2
  signature_hex = script_sig[2:m]
  deb("signature_hex (DER-encoded, 1-byte hash type appended) ({} bytes): {}".format(hex_len(signature_hex), signature_hex))
  b = script_sig[m:m+2]
  n2 = var_int_to_int(b)
  m2 = m+2 + n2*2
  public_key_hex = script_sig[m+2:m2]
  deb("public_key_hex ({} bytes): {}".format(hex_len(public_key_hex), public_key_hex))
  # Check that last byte of signature is "01" (hash_type SIGHASH_ALL as a single byte) and remove it.
  b = signature_hex[-2:]
  msg = "1-byte hash type appended to signature_hex = {}".format(b)
  deb(msg)
  if b != '01':
    raise ValueError
  signature_hex = signature_hex[:-2]
  deb("signature_hex (DER-encoded) ({} bytes): {}".format(hex_len(signature_hex), signature_hex))
  # Check that first byte of public_key is "04" ("uncompressed") and remove it.
  b = public_key_hex[:2]
  msg = "1-byte compression type prepended to public key = {}".format(b)
  deb(msg)
  if b != '04':
    raise ValueError
  public_key_hex = public_key_hex[2:]
  deb("public_key_hex ({} bytes): {}".format(hex_len(public_key_hex), public_key_hex))
  return signature_hex, public_key_hex




def signature_hex_and_public_key_hex_to_script_sig(signature_hex, public_key_hex):
  # This is my current understanding of a standard scriptSig:
  #
  # scriptSig:
  # START FORMAT
  # - PUSHDATA: 47 (approximately)
  # - [derived property] PUSHDATA decimal value: 71 (approximately)
  # - signature_data: 71 bytes (approximately)
  # - PUSHDATA: 41
  # - [derived property] PUSHDATA decimal value: 65
  # - public_key_data: 65 bytes ("04", 32-byte big-endian X value, 32-byte big-endian Y value)
  # END FORMAT
  #
  #deb("public_key_hex: {}".format(public_key_hex))
  v.validate_hex(signature_hex)
  v.validate_hex_length(public_key_hex, 64)
  #deb("signature_hex: {}".format(signature_hex))
  #deb("public_key_hex: {}".format(public_key_hex))
  # Add '04' ("uncompressed") compression type prefix to public_key_hex.
  public_key_hex = '04' + public_key_hex
  msg = "public_key_hex (1-byte compression type prepended) ({} bytes) = {}".format(hex_len(public_key_hex), public_key_hex)
  deb(msg)
  signature_hex_pushdata = int_to_var_int(hex_len(signature_hex))
  public_key_hex_pushdata = int_to_var_int(hex_len(public_key_hex))
  msg = "signature_hex_pushdata ({} bytes) = {}".format(hex_len(signature_hex_pushdata), signature_hex_pushdata)
  deb(msg)
  msg = "public_key_hex_pushdata ({} bytes) = {}".format(hex_len(public_key_hex_pushdata), public_key_hex_pushdata)
  deb(msg)
  script_sig = signature_hex_pushdata + signature_hex + public_key_hex_pushdata + public_key_hex
  script_length = int_to_var_int(hex_len(script_sig))
  msg = "script_sig ({} bytes) = {}".format(hex_len(script_sig), script_sig)
  deb(msg)
  msg = "script_length ({} bytes) = {}".format(hex_len(script_length), script_length)
  deb(msg)
  return script_sig, script_length




def address_to_script_pub_key(address):
  hash_hex = bitcoin_address_to_public_key_hash_hex(address)
  script_pub_key, script_length = public_key_hash_hex_to_script_pub_key(hash_hex)
  return script_pub_key, script_length




def public_key_hash_hex_to_script_pub_key(x):
  # START FORMAT: scriptPubKey
  # - OP_DUP: 76
  # - OP_HASH160: a9
  # - PUSHDATA: 14
  # - [derived property] PUSHDATA decimal value: 20
  # - public_key_hash: 20 bytes (big-endian)
  # - OP_EQUALVERIFY: 88
  # - OP_CHECKSIG: ac
  # END FORMAT
  script_pub_key = "76" + "a9" + "14" + x + "88" + "ac"
  script_length = hex_len(script_pub_key)
  script_length = int_to_var_int(script_length)
  return script_pub_key, script_length




def validate_bitcoin_address(s):
  bitcoin_address_to_public_key_hash_hex(s)




def bitcoin_address_to_public_key_hash_hex(s):
  x = base58check_to_hex(s)
  # Remove version byte ("00" for "main Bitcoin network").
  y = x[:2]
  if y != '00':
    raise ValueError
  x = x[2:]
  # The result should be the public key hash in hex bytes.
  # public key hash = RIPEMD-160(SHA256(public_key)) and should be exactly 20 bytes long.
  v.validate_hex_length(x, 20)
  return x




def base58check_to_hex(s):
  v.validate_string(s)
  # 1) Count the number of leading '1' characters in the address, and remove them.
  s2 = s.lstrip('1')
  count_1 = len(s) - len(s2)
  # 2) Convert the result of step (1) from the Bitcoin base-58 encoding to a base-10 integer.
  s3 = base58_to_int(s2)
  # 3) Convert the result of step (2) from a base-10 integer to a hex byte string.
  s4 = int_to_hex(s3)
  # 4) The last four bytes in the result of step (3) are the checksum. Record the checksum's value and remove it.
  checksum = s4[-8:]
  s5 = s4[:-8]
  # 5) Let the result of step (1) be N. Add N leading zero bytes to the result of step (4).
  s6 = (count_1 * '00') + s5
  # Calculate the checksum and confirm that it matches the recorded value.
  checksum_new = get_double_sha256_checksum(s6)
  analysis = '''
- Input: {s}
- Input hex: {s4}
- Input hex without checksum: {s5}
- Input hex without checksum and with zeroes: {s6}
- Checksum value     : {checksum}
- Calculated checksum: {checksum_new}
'''.format(**vars())
  if checksum != checksum_new:
    msg = "Checksum value does not match calculated checksum." + analysis
    raise ValueError(msg)
  return s6




def hex_to_base58check(x):
  checksum_hex = get_double_sha256_checksum(x)
  x += checksum_hex
  x_base58 = hex_to_base58(x)
  n = count_leading_zero_bytes(x)
  output = '1' * n + x_base58
  return output




def base58_to_int(s):
  # Convert a string from Bitcoin base-58 encoding to a base-10 integer.
  # The string base58_symbols can accessed as a 0-indexed list of characters.
  base58_symbols = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
  n = len(s)
  m = n - 1
  t = 0  # running total
  for i in range(n):
    character = s[i]
    value = base58_symbols.index(character)
    # Multiply the character's value by the power of 58 that corresponds to its position in the string.
    result = value * (58 ** (m - i))
    t += result
  v.validate_positive_integer(t)
  return t




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
    b = x[i:i+2]  # b = byte
    if b == '00':
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
  y = bytes.fromhex(x)
  return sha256.hexdigest(y)




def get_ripemd160(x):
  v.validate_hex(x)
  y = bytes.fromhex(x)
  return ripemd160.hexdigest(y)




def satoshi_to_bitcoin(n):
  # Accepts int, returns bitcoin amount (string).
  # Example: accepts 242000, returns "0.00242".
  max_amount = 21*(10**6)  # 21 million bitcoin
  max_amount_satoshi = max_amount * (10 ** 8)
  v.validate_integer_domain(n, 0, max_amount_satoshi)
  s = str(n)
  p = len(s)  # Number of digits
  if p <= 8:
    # This is less than 1 bitcoin.
    # Left-pad with zeroes to reach 8 decimal places.
    m = 8 - p
    s = '0' * m + s
    # Prefix with '0' and a decimal point.
    s = '0.' + s
  else:  # p > 8
    s1 = s[:-8]  # "Integer part" of bitcoin amount.
    s2 = s[-8:]  # "Fractional part" of bitcoin amount.
    # Insert decimal point.
    s = s1 + '.' + s2
  validate_bitcoin_amount(s)
  return s




def bitcoin_to_satoshi(s):
  # Accepts bitcoin amount (string), returns int.
  # Example: Accepts "0.00242", returns 242000.
  validate_bitcoin_amount(s)
  # Avoid any calculations in floating point.
  if s.count('.') == 0:
    # No decimal component
    output = s + '0' * 8  # Add 8 zeros to get satoshi amount.
  elif s.count('.') == 1:
    # Increase number of decimal places to 8, then remove the decimal point.
    s1, s2 = s.split('.')
    n = len(s2)
    m = 8 - n  # Number of "missing" decimal places.
    output = s.replace('.', '') + '0' * m
  else:
    msg = "Bitcoin amount should contain 0 or 1 decimal points."
    msg += " Amount received: {}".format(s)
    raise ValueError(msg)
  # Remove any leading zeros.
  output = output.lstrip('0')
  # Convert to integer.
  output = int(output)
  v.validate_whole_number(output)
  return output




def validate_positive_bitcoin_amount(s):
  # Doesn't accept zero amount.
  v.validate_string(s)
  if s.replace('.', '').replace('0', '') == '':
    msg = "Amount ('{}') cannot be 0.".format(s)
    raise ValueError(msg)
  validate_bitcoin_amount(s)




def validate_bitcoin_amount(s):
  # Example values:
  # 1, 2, 1.1, 1.0001, 0.00000001, 0.00000000, 0.12345678
  v.validate_string(s)
  max_amount = 21*(10**6)  # 21 million bitcoin
  min_amount = 0.00000000  # 0 satoshi
  # Amount can contain 0 or 1 period.
  if s.count('.') not in [0, 1]:
    msg = "Amount contains {} periods ('.'). It must contain either 1 or 0 periods. Amount: {}".format(s.count('.'), s)
    raise ValueError(msg)
  # Apart from the period, amount can contain only digits.
  s2 = s.replace('.', '')
  if not s2.isdigit():
    msg = "Apart from an optional period ('.'), amount can contain only digits. Amount: {}".format(s)
    raise ValueError(msg)
  # Check whether the amount has too many decimal places.
  if s.count('.') == 1:
    s3 = s.split('.')[1]
    if len(s3) > 8:
      msg = "Amount ({}) has {} decimal places. It can have at most 8 decimal places.".format(s, len(s3))
      raise ValueError(msg)
  # The numerical value must be within the acceptable domain.
  if float(s) < float(min_amount):
    msg = "The minimum possible amount is {:.8f}. Amount: {}".format(min_amount, s)
    raise ValueError(msg)
  elif float(s) > float(max_amount):
    msg = "The maximum possible amount is {:.8f}. Amount: {}".format(max_amount, s)
    raise ValueError(msg)




def ensure_8_decimal_places(s):
  # Input is a string. It can be a number or a decimal.
  if s.count('.') == 0:
    s += '.'
  d = len(s.split('.')[1])
  m = 8 - d
  if m < 0:
    msg = 'String decimal ({}) has {} decimal places.'
    msg = msg.format(s, d)
    raise ValueError(msg)
  s += '0' * m
  return s




def var_int_to_int(x):
  # Currently only handles 1-byte var_ints.
  # A 1-byte var_int can encode values in the domain [0, 252].
  v.validate_hex_length(x, 1)
  if x in 'fd fe ff'.split():
    raise ValueError
  n = int(x, 16)
  v.validate_integer_domain(n, min_value=0, max_value=252)
  return n




def int_to_var_int(n):
  # Currently only handles 1-byte var_ints.
  # A 1-byte var_int can encode values in the domain [0, 252].
  v.validate_integer_domain(n, min_value=0, max_value=252)
  x = int_to_hex(n)
  v.validate_hex(x)
  return x




def pad_hex(x, n_bytes):
  v.validate_hex(x)
  v.validate_integer(n_bytes)
  n = hex_len(x)
  if n_bytes < n:
    msg = "Hex value is already longer than desired padded length. Hex value: {}".format(x)
    raise ValueError(msg)
  m = n_bytes - n
  if m > 0:
    # Add leading zero hex bytes at the left-hand side.
    x = '00' * m + x
  return x




def pad_hex_le(x, n_bytes):
  # Used for padding hex in little-endian format.
  v.validate_hex(x)
  v.validate_integer(n_bytes)
  n = hex_len(x)
  if n_bytes < n:
    msg = "Hex value is already longer than desired padded length. Hex value: {}".format(x)
    raise ValueError(msg)
  m = n_bytes - n
  if m > 0:
    # Add leading zero hex bytes at the right-hand side.
    x += '00' * m
  return x




def hex_le_to_int(x_le):
  # Accepts hex string in little-endian format, returns integer.
  x = reverse_hex_order(x_le)
  n = hex_to_int(x)
  return n




def int_to_hex_le(n):
  # Accepts integer, returns hex string in little-endian format.
  x = int_to_hex(n)
  x_le = reverse_hex_order(x)
  return x_le




def hex_to_int(x):
  return int(x, 16)




def int_to_hex(n):
  # Accepts integer, returns hex string.
  v.validate_integer(n)
  x = hex(n)
  x = x[2:]  # Remove '0x' prefix.
  # Python-specific issue: Remove 'L' suffix if it exists.
  if x[-1] == "L":
    x = x[:-1]
  # Ensure an even number of characters.
  # 1 byte == 2 hex characters. An extra hex character by itself is a half-byte.
  if len(x) % 2 == 1:
    # Add a leading 0 (a single empty half-byte in hex).
    x = '0' + x
  v.validate_hex(x)
  return x




def reverse_hex_order(x):
  v.validate_hex(x)
  n = 2  # Number of hex characters per byte
  output = [x[i:i+n] for i in range(0, len(x), n)]
  output.reverse()
  output = ''.join(output)
  v.validate_hex(output)
  return output




def hex_len(x):
  # Divide hex length by 2 to get hex length in bytes.
  v.validate_hex(x)
  n = len(x) // 2
  return n



