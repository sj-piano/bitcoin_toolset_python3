# Imports
import logging
from collections import OrderedDict
import json
from decimal import Decimal




# Relative imports
from .. import util
from . import basic
from . import transaction_input
from . import transaction_output




# Shortcuts
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




# My working definition of a standard transaction:
# - It has at least one input and at least one output.
# - All input and output addresses are Pay-To-Public-Key-Hash (P2PKH).
# - All input scriptSigs contain uncompressed public keys.




# This is my current working definition of the raw format of a standard Bitcoin transaction:
#
# Standard transaction:
# START FORMAT
# - version: 4 bytes (little-endian)
# - input_count: (var_int)
# - [for each input:]
# -- previous_output_hash: 32 bytes (big-endian). When little-endian, it is the "txid".
# -- previous_output_index: 4 bytes (little-endian)
# -- script_length: (var_int)
# -- scriptSig [see below]
# -- sequence: 4 bytes (little-endian)
# - output_count: (var_int)
# - [for each output:]
# -- value: 8 bytes (little-endian)
# -- script_length: (var_int)
# -- scriptPubKey [see below]
# - block lock time: 4 bytes
# END FORMAT
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
#
# Notes:
# - var_int = (variable-length byte sequence)
# - The version is always hardcoded as '1' for the main Bitcoin network. In 4 little-endian hex bytes, this is 0x01 00 00 00.
# - Sequence can always be set to 0xff ff ff ff. It is a nonfunctional legacy feature that was designed to allow multiple signers to agree to update a transaction.
# - Block lock time can always be set to 0x00 00 00 00. It was designed to ask miners not to mine a transaction until a specified block height is reached. A block lock time of 0x00 00 00 00 specifies that the transaction can be mined at any block height after 0.
# - The previous_output_hash is:
# -- the hash of the previous transaction that:
# --- contains the unspent output that:
# ---- will be used as an input in this new transaction
# - The hash type (SIGHASH_ALL) is 1. As 1 byte, this is 0x01. As 4 bytes (little-endian), this is 0x01 00 00 00. The 4-byte version is appended to the transaction-in-signable-form before signing. The 1-byte version is appended to the signature_data after signing.
#
#
# This is my current working definition of the raw format of a standard Bitcoin transaction-in-signable-form:
#
# START FORMAT
# - version: 4 bytes (little-endian)
# - input_count: (var_int)
# - [for each input:]
# -- previous_output_hash: 32 bytes (big-endian)
# -- previous_output_index: 4 bytes (little-endian)
# -- script_length: (var_int)
# -- scriptPubKey of relevant unspent output from previous transaction [same format as scriptPubKey - see below]
# -- sequence: 4 bytes (little-endian)
# - output_count: (var_int)
# - [for each output:]
# -- value: 8 bytes (little-endian)
# -- script_length: (var_int)
# -- scriptPubKey [see below]
# - block lock time: 4 bytes
# - hash type: 4 bytes (little-endian)
# END FORMAT
#
# scriptPubKey (standard form):
# START FORMAT
# - OP_DUP: 76
# - OP_HASH160: a9
# - PUSHDATA: 14
# - [derived property] PUSHDATA decimal value: 20
# - public_key_hash: 20 bytes (big-endian)
# - OP_EQUALVERIFY: 88
# - OP_CHECKSIG: ac
# END FORMAT
#
# Note: In the {scriptPubKey of relevant unspent output from previous transaction}, the unspent output is associated with a particular address, the private key of which is to be used to sign this particular transaction-in-signable-form in order to create a single scriptSig.




# var_int = "variable length integer"








class Transaction:


  def __init__(self):
    # Default properties:
    self.version = "01000000"
    self.input_count = None  # var_int
    self.inputs = []
    self.output_count = None  # var_int
    self.outputs = []
    self.block_lock_time = "00000000"
    # Properties that go into the transaction-in-signable-form:
    self.hash_type_4_byte = "01000000"  # 4 bytes (little-endian)
    # Properties that go into the signed transaction:
    self.hash_type_1_byte = "01"
    self.change_address = None


  def __str__(self):
    name = self.__class__.__name__
    n_inputs = len(self.inputs)
    n_outputs = len(self.outputs)
    i_plural = 's' if n_inputs > 1 else ''
    o_plural = 's' if n_outputs > 1 else ''
    signed = ' (unsigned)' if not self.signed else ' (signed)'
    s = "{name}{signed}: {n_inputs} input{i_plural}, {n_outputs} output{o_plural}"
    s = s.format(**vars())
    return s


  @classmethod
  def create(cls, inputs, outputs):
    t = Transaction()
    t.input_count = basic.int_to_var_int(len(inputs))
    t.inputs = inputs
    t.output_count = basic.int_to_var_int(len(outputs))
    t.outputs = outputs
    return t


  @property
  def signed(self):
    signed = all(x.signed for x in self.inputs)
    return signed


  @property
  def input_values_known(self):
    return all(x.satoshi_amount is not None for x in self.inputs)

  @property
  def total_input(self):
    if not self.input_values_known:
      return None
    return sum([x.satoshi_amount for x in self.inputs])


  @property
  def total_output(self):
    return sum([x.satoshi_amount for x in self.outputs])


  @property
  def fee(self):
    if not self.input_values_known:
      return None
    return self.total_input - self.total_output


  @property
  def change(self):
    if not self.change_address:
      return None
    change = sum([x.satoshi_amount for x in self.outputs if x.address == self.change_address])
    return change


  def to_dict(self):

    n_inputs = len(self.inputs)
    n_outputs = len(self.outputs)
    estimated_size_bytes = basic.estimate_transaction_size(n_inputs, n_outputs)

    def fee_rate_satoshi_to_bitcoin(fee_rate_satoshi):
      fee_rate_bitcoin = Decimal(fee_rate_satoshi) / (10 ** 8)
      EIGHT_PLACES = Decimal('0.00000001')
      fee_rate_bitcoin = fee_rate_bitcoin.quantize(EIGHT_PLACES)
      fee_rate_bitcoin = '{:8f}'.format(fee_rate_bitcoin)
      return fee_rate_bitcoin

    # Default values.
    total_input_bitcoin = None
    fee_bitcoin = None
    estimated_fee_rate_satoshi = None
    estimated_fee_rate_bitcoin = None

    # If input values are known, we can calculate these derivative values.
    if self.input_values_known:
      total_input_bitcoin = basic.satoshi_to_bitcoin(self.total_input)
      fee_bitcoin = basic.satoshi_to_bitcoin(self.fee)
      estimated_fee_rate = Decimal(self.fee) / estimated_size_bytes
      estimated_fee_rate_satoshi = '{:.4f}'.format(estimated_fee_rate)
      estimated_fee_rate_bitcoin = fee_rate_satoshi_to_bitcoin(estimated_fee_rate_satoshi)

    d = OrderedDict({
      'version': self.version,
      'input_count': self.input_count,
      'inputs': [x.to_dict() for x in self.inputs],
      'output_count': self.output_count,
      'outputs': [x.to_dict() for x in self.outputs],
      'block_lock_time': self.block_lock_time,
      'hash_type_4_byte': self.hash_type_4_byte,
      'hash_type_1_byte': self.hash_type_1_byte,
      'signed': self.signed,
      'total_input': {
        'satoshi_amount': self.total_input,
        'bitcoin_amount': total_input_bitcoin,
      },
      'total_output': {
        'satoshi_amount': self.total_output,
        'bitcoin_amount': basic.satoshi_to_bitcoin(self.total_output),
      },
      'fee': {
        'satoshi_amount': self.fee,
        'bitcoin_amount': fee_bitcoin,
      },
      'change_address': self.change_address,
      'change': {
        'satoshi_amount': None,
        'bitcoin_amount': None,
      },
      'estimated_size_bytes': estimated_size_bytes,
      'estimated_fee_rate': {
        'satoshi_per_byte': estimated_fee_rate_satoshi,
        'bitcoin_per_byte': estimated_fee_rate_bitcoin,
      },
      'size_bytes': None,
      'fee_rate': {
        'satoshi_amount': None,
        'bitcoin_amount': None,
      },
    })
    # Change address is known only when we use create_transaction.py.
    if self.change_address:
      d['change'] = {
        'satoshi_amount': self.change,
        'bitcoin_amount': basic.satoshi_to_bitcoin(self.change),
      }
    if self.signed:
      size_bytes = basic.hex_len(self.to_hex_signed_form())
      d['size_bytes'] = size_bytes
      if self.fee is not None:
        fee_rate = Decimal(self.fee) / size_bytes
        fee_rate_satoshi = '{:.4f}'.format(fee_rate)
        fee_rate_bitcoin = fee_rate_satoshi_to_bitcoin(fee_rate_satoshi)
        d['fee_rate'] = {
          'satoshi_per_byte': fee_rate_satoshi,
          'bitcoin_per_byte': fee_rate_bitcoin,
        }
    return d


  def to_json(self):
    d = self.to_dict()
    s = json.dumps(d, indent=2)
    return s


  @classmethod
  def from_json(cls, s):
    # Notes:
    # - This is used to load (and validate) both unsigned and signed tx JSON data.
    # 1) Check that the JSON data has a particular structure.
    # 2) Validate the format of the values, as much as is feasible.
    # 3) Check that the total output value is less than or equal to the total input value.
    d = json.loads(s)
    expected = '''
version input_count inputs output_count outputs
block_lock_time hash_type_4_byte hash_type_1_byte signed
  '''
    expected = expected.replace('\n', ' ').split()
    received = list(d.keys())
    v.validate_list_contains_items(received, expected)
    v.validate_hex(d['input_count'])
    v.validate_list(d['inputs'])
    v.validate_list(d['outputs'])
    input_count = basic.var_int_to_int(d['input_count'])
    assert input_count == len(d['inputs'])
    output_count = basic.var_int_to_int(d['output_count'])
    assert output_count == len(d['outputs'])
    inputs = []
    for x in d['inputs']:
      input_ = transaction_input.TransactionInput.from_dict(x)
      inputs.append(input_)
    outputs = []
    for x in d['outputs']:
      output = transaction_output.TransactionOutput.from_dict(x)
      outputs.append(output)
    assert d['block_lock_time'] == '00000000'
    assert d['hash_type_4_byte'] == '01000000'
    assert d['hash_type_1_byte'] == '01'
    v.validate_boolean(d['signed'])
    total_input = sum([x.satoshi_amount for x in inputs])
    total_output = sum([x.satoshi_amount for x in outputs])
    assert total_output <= total_input
    # Create the instance and save the instance variables.
    t = Transaction()
    t.input_count = basic.int_to_var_int(len(inputs))
    t.inputs = inputs
    t.output_count = basic.int_to_var_int(len(outputs))
    t.outputs = outputs
    if d['signed'] is True:
      assert t.signed is True
    return t


  def sign(self, private_keys_hex, random_values_hex=None):
    # We create a signature for each input, using the private key that corresponds to that input.
    # The signature is stored in the input.
    # The transaction form is a little different for each input signing process. It must be altered carefully into the right format.
    # Regarding random_values_hex:
    # - We usually create deterministic signatures.
    # - However, in the test set there are legacy transactions that used random values that were generated separately.
    if random_values_hex:
      if len(random_values_hex) != len(set(random_values_hex)):
        raise ValueError
      if len(random_values_hex) != len(private_keys_hex):
        raise ValueError
    map_address_to_private_key_hex = {}
    for private_key_hex in private_keys_hex:
      v.validate_hex_length(private_key_hex, 32)
      address = basic.private_key_hex_to_address(private_key_hex)
      map_address_to_private_key_hex[address] = private_key_hex
    known_addresses = sorted(map_address_to_private_key_hex.keys())
    for input_index, input_ in enumerate(self.inputs):
      random_value_hex = random_values_hex[input_index] if random_values_hex else None
      address = input_.address
      if address not in known_addresses:
        raise ValueError
      private_key_hex = map_address_to_private_key_hex[address]
      # Derive the public_key_hex from the private_key. This will be included in the scriptSig.
      input_.public_key_hex = basic.private_key_hex_to_public_key_hex(private_key_hex)
      signature_hex = self.create_signature_for_one_input(input_index, private_key_hex, random_value_hex)
      # Convert the signature to DER encoding.
      signature_hex = basic.signature_to_der(signature_hex)
      # Append hash_type SIGHASH_ALL (as a single byte) "01" to DER-encoded signature.
      signature_hex += self.hash_type_1_byte
      script_sig, script_length = basic.signature_hex_and_public_key_hex_to_script_sig(signature_hex, input_.public_key_hex)
      script_length_int = basic.var_int_to_int(script_length)
      # Storing the scriptSig and its script_length in the input-used-for-signing, for every input, completes the sign() process.
      input_.script_length = script_length
      input_.script_length_int = script_length_int
      input_.script_sig = script_sig
    return self


  def create_signature_for_one_input(self, input_index, private_key_hex, random_value_hex=None):
    input_ = self.inputs[input_index]
    # Get the transaction-in-signable-form for this input.
    #deb(self.to_json_signable_form(input_index))
    signable_form_hex = self.to_hex_signable_form(input_index)
    #deb(signable_form_hex)
    digest_hex = basic.get_double_sha256(signable_form_hex)
    #deb(digest_hex)
    v.validate_hex_length(digest_hex, 32)
    if not random_value_hex:
      signature_hex = basic.create_deterministic_signature_for_digest(private_key_hex, digest_hex)
    else:
      signature_hex = basic.create_signature_for_digest(private_key_hex, digest_hex, random_value_hex)
    #deb("signature_hex: {}".format(signature_hex))
    return signature_hex


  def to_hex_signable_form(self, input_index):
    d = self.to_dict_signable_form(input_index)
    s = ''
    for k, v in d.items():
      if k in 'inputs outputs'.split():
        # These are lists of ordered dicts.
        for x in v:
          for k2, v2 in x.items():
            s += v2
      else:
        # Add the stored hex value to the hex result.
        s += v
    return s


  def to_json_signable_form(self, input_index):
    d = self.to_dict_signable_form(input_index)
    s = json.dumps(d, indent=2)
    return s


  def to_dict_signable_form(self, input_index):
    # Iterate over the inputs, converting the relevant input into the non-empty signable form.
    inputs = []
    for i, input_ in enumerate(self.inputs):
      if i == input_index:
        inputs.append(input_.to_dict_signable_form())
      else:
        inputs.append(input_.to_dict_signable_form_empty())
    d = OrderedDict()
    d.update({
      'version': self.version,
      'input_count': self.input_count,
      'inputs': inputs,
      'output_count': self.output_count,
      'outputs': [x.to_dict_signable_form() for x in self.outputs],
      'block_lock_time': self.block_lock_time,
      'hash_type_4_byte': self.hash_type_4_byte,
    })
    return d


  def verify(self):
    for input_index, input_ in enumerate(self.inputs):
      script_sig = input_.script_sig
      if script_sig is None:
        raise ValueError
      signature_hex, public_key_hex = basic.script_sig_to_signature_hex_and_public_key_hex(script_sig)
      # Convert DER-encoded signature to concatenated r & s.
      signature_hex = basic.signature_from_der(signature_hex)
      valid_signature = self.verify_signature_for_one_input(input_index, public_key_hex, signature_hex)
      if not valid_signature:
        return False
    return True


  def verify_signature_for_one_input(self, input_index, public_key_hex, signature_hex):
    input_ = self.inputs[input_index]
    # Get the transaction-in-signable-form for this input.
    #deb(self.to_json_signable_form(input_index))
    signable_form_hex = self.to_hex_signable_form(input_index)
    #deb(signable_form_hex)
    digest_hex = basic.get_double_sha256(signable_form_hex)
    #deb(digest_hex)
    v.validate_hex_length(digest_hex, 32)
    valid_signature = basic.verify_signature_digest(public_key_hex, digest_hex, signature_hex)
    return valid_signature


  def to_hex_signed_form(self):
    d = self.to_dict_signed_form()
    s = ''
    for k, v in d.items():
      if k in 'inputs outputs'.split():
        # These are lists of ordered dicts.
        for x in v:
          for k2, v2 in x.items():
            s += v2
      else:
        # Add the stored hex value to the hex result.
        s += v
    return s


  def to_json_signed_form(self):
    d = self.to_dict_signed_form()
    s = json.dumps(d, indent=2)
    return s


  def to_dict_signed_form(self):
    inputs = []
    for i, input_ in enumerate(self.inputs):
      inputs.append(input_.to_dict_signed_form())
    d = OrderedDict()
    d.update({
      'version': self.version,
      'input_count': self.input_count,
      'inputs': inputs,
      'output_count': self.output_count,
      'outputs': [x.to_dict_signed_form() for x in self.outputs],
      'block_lock_time': self.block_lock_time,
    })
    return d


  @classmethod
  def from_hex_signed(cls, s):
    # Notes:
    # - This is used to load (and validate) signed tx hex data.
    # - We build and return a tx instance, so that we can call tx.verify().
    # -- We only the need to store the information returned in to_dict_signable_form().
    deb(s)
    n = basic.hex_len(s)
    deb('hex length: {}'.format(n))
    hex_bytes = [s[i:i+2] for i in range(0, len(s), 2)]
    version = ''.join(hex_bytes[0:4])
    i = 4  # current index
    if version != '01000000':
      raise ValueError
    deb('version: {}'.format(version))
    input_count = hex_bytes[i]
    i += 1

    deb('input_count: {}'.format(input_count))
    input_count_int = basic.var_int_to_int(input_count)
    deb('input_count_int: {}'.format(input_count_int))
    inputs = []
    for x in range(input_count_int):
      deb('input {}:'.format(x))
      previous_output_hash = ''.join(hex_bytes[i:i+32])
      i += 32
      deb('- previous_output_hash: {}'.format(previous_output_hash))
      previous_output_index = ''.join(hex_bytes[i:i+4])
      i += 4
      deb('- previous_output_index: {}'.format(previous_output_index))
      script_length = ''.join(hex_bytes[i])
      deb('- script_length: {}'.format(script_length))
      script_length_int = basic.var_int_to_int(script_length)
      i += 1
      deb('- script_length_int: {}'.format(script_length_int))
      script_sig = ''.join(hex_bytes[i:i+script_length_int])
      i += script_length_int
      deb('- script_sig: {}'.format(script_sig))
      signature_hex, public_key_hex = basic.script_sig_to_signature_hex_and_public_key_hex(script_sig)
      deb('- signature_hex: {}'.format(signature_hex))
      deb('- public_key_hex: {}'.format(public_key_hex))
      sequence = ''.join(hex_bytes[i:i+4])
      i += 4
      deb('- sequence: {}'.format(sequence))
      if sequence != 'ffffffff':
        raise ValueError
      input_ = transaction_input.TransactionInput.create_from_signed_tx_data(public_key_hex, previous_output_hash, previous_output_index, script_length, script_sig)
      inputs.append(input_)

    output_count = hex_bytes[i]
    i += 1
    deb('output_count: {}'.format(output_count))
    output_count_int = basic.var_int_to_int(output_count)
    deb('output_count_int: {}'.format(output_count_int))
    outputs = []
    for x in range(output_count_int):
      deb('output {}:'.format(x))
      value = ''.join(hex_bytes[i:i+8])
      i += 8
      deb('- value: {}'.format(value))
      script_length = ''.join(hex_bytes[i])
      i += 1
      deb('- script_length: {}'.format(script_length))
      script_length_int = basic.var_int_to_int(script_length)
      deb('- script_length_int: {}'.format(script_length_int))
      script_pub_key = ''.join(hex_bytes[i:i+script_length_int])
      i += script_length_int
      deb('- script_pub_key: {}'.format(script_pub_key))
      output = transaction_output.TransactionOutput.create_from_signed_tx_data(value, script_length, script_pub_key)
      outputs.append(output)

    block_lock_time = ''.join(hex_bytes[i:i+4])
    deb('- block_lock_time: {}'.format(block_lock_time))
    if block_lock_time != '00000000':
      raise ValueError

    # Create the instance and save the instance variables.
    t = Transaction()
    t.input_count = basic.int_to_var_int(len(inputs))
    t.inputs = inputs
    t.output_count = basic.int_to_var_int(len(outputs))
    t.outputs = outputs
    return t


  def calculate_txid(self):
    # The txid is calculated by applying the SHA256 hash algorithm twice to the signed transaction binary data, and then converting the result to little-endian.
    if not self.signed:
      raise ValueError
    tx_signed_hex = self.to_hex_signed_form()
    hash_hex = basic.get_double_sha256(tx_signed_hex)
    txid = basic.reverse_hex_order(hash_hex)
    return txid



