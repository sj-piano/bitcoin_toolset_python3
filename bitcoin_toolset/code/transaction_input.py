# Imports
import logging
from collections import OrderedDict




# Relative imports
from .. import util
from . import basic




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




# Notes:
# - "txid" = "transaction ID"




class TransactionInput:


  def __init__(self):
    # Properties that go into the raw transaction:
    self.previous_output_hash = None  # 32 bytes (big-endian)
    # - When previous_output_hash is little-endian, it is the "txid".
    self.previous_output_index = None  # 4 bytes (little-endian)
    self.previous_output_index_int = None  # string
    self.sequence = "ffffffff"  # 4 bytes
    # Properties that are needed for signing the raw transaction:
    self.public_key_hex = None  # Included in the scriptSig.
    # - Used when validating transaction signatures.
    self.script_pub_key_length = None  # var_int
    self.script_pub_key_length_int = None
    self.script_pub_key = None
    # - The "scriptPubKey of relevant unspent output from previous transaction" (~= the address from which this input originates) is included in the signable form of a transaction, when signing that transaction with that particular input.
    # Properties that go into the signed transaction:
    # - Note: script_length_int doesn't go in, it's just helpful.
    self.script_length = None
    self.script_length_int = None
    self.script_sig = None
    # Other properties:
    self.address = None
    self.txid = None  # little-endian form of previous_output_hash
    self.satoshi_amount = None  # int
    self.bitcoin_amount = None  # string


  def __str__(self):
    name = self.__class__.__name__
    txid = self.txid[:4] + '...' + self.txid[-4:]
    ad = self.address
    d = self.previous_output_index_int
    sa = self.satoshi_amount
    signed = ' (unsigned)' if not self.signed else ' (signed)'
    s = "{name}{signed}: address={ad}, txid={txid}, index={d}, satoshi_amount={sa}"
    s = s.format(**vars())
    return s


  # This method constructs the basic Input instance from the information that is publically available on the Bitcoin blockchain.
  # Later, when a transaction is signed using this input, the private key will be supplied, and various information will be generated from it.
  # The address will be generated from the private key, and the address supplied here will be compared with it, in order to match the correct private key to this input.


  @classmethod
  def create(cls, address, txid, previous_output_index_int, satoshi_amount):
    basic.validate_bitcoin_address(address)
    v.validate_hex_length(txid, 32)
    previous_output_hash = basic.reverse_hex_order(txid)
    # previous_output_index is an integer. Convert it to 4 hex bytes (little endian).
    v.validate_integer(previous_output_index_int)
    previous_output_index = basic.int_to_hex_le(previous_output_index_int)
    previous_output_index = basic.pad_hex_le(previous_output_index, n_bytes=4)
    # Derive scriptPubKey from the address. This is used during the signing process.
    script_pub_key, script_pub_key_length = basic.address_to_script_pub_key(address)
    script_pub_key_length_int = basic.var_int_to_int(script_pub_key_length)
    # Calculate bitcoin amount from satoshi amount. We use this for logging.
    bitcoin_amount = basic.satoshi_to_bitcoin(satoshi_amount)
    # Create the instance and save the instance variables.
    ti = TransactionInput()
    ti.previous_output_hash = previous_output_hash
    ti.previous_output_index = previous_output_index
    ti.previous_output_index_int = previous_output_index_int
    ti.script_pub_key_length = script_pub_key_length
    ti.script_pub_key = script_pub_key
    ti.script_pub_key_length_int = script_pub_key_length_int
    ti.address = address
    ti.txid = txid
    ti.satoshi_amount = satoshi_amount
    ti.bitcoin_amount = bitcoin_amount
    return ti


  @classmethod
  def create_from_signed_tx_data(cls, public_key_hex, previous_output_hash, previous_output_index, script_length, script_sig):
    # This is a more limited creation function.
    # It handles only the data available in a signed tx.
    # It allows us to call tx.verify(), but we can't produce much else without e.g. the source address and stored value for each input.
    # - tx.verify() requires that tx_input.to_dict_signable_form() works.
    v.validate_hex_length(public_key_hex, 64)
    v.validate_hex_length(previous_output_hash, 32)
    v.validate_hex_length(previous_output_index, 4)
    v.validate_hex(script_length)
    v.validate_hex(script_sig)
    script_length_int = basic.var_int_to_int(script_length)
    script_pub_key, script_pub_key_length = basic.public_key_hex_to_script_pub_key(public_key_hex)
    script_pub_key_length_int = basic.var_int_to_int(script_pub_key_length)
    address = basic.script_pub_key_to_address(script_pub_key)
    previous_output_index_int = basic.hex_le_to_int(previous_output_index)
    txid = basic.reverse_hex_order(previous_output_hash)
    # Create the instance and save the instance variables.
    ti = TransactionInput()
    ti.previous_output_hash = previous_output_hash
    ti.previous_output_index = previous_output_index
    ti.previous_output_index_int = previous_output_index_int
    ti.public_key_hex = public_key_hex
    ti.script_pub_key_length = script_pub_key_length
    ti.script_pub_key_length_int = script_pub_key_length_int
    ti.script_pub_key = script_pub_key
    ti.script_length = script_length
    ti.script_length_int = script_length_int
    ti.script_sig = script_sig
    ti.address = address
    ti.txid = txid
    return ti


  @property
  def signed(self):
    signed = self.script_length is not None and self.script_sig is not None
    return signed


  def to_dict(self):
    d = OrderedDict()
    d.update({
      'previous_output_hash': self.previous_output_hash,
      'previous_output_index': self.previous_output_index,
      'previous_output_index_int': self.previous_output_index_int,
      'script_length': self.script_length,
      'script_length_int': self.script_length_int,
      'script_sig': self.script_sig,
      'sequence': self.sequence,
      'public_key_hex': self.public_key_hex,
      'script_pub_key_length': self.script_pub_key_length,
      'script_pub_key_length_int': self.script_pub_key_length_int,
      'script_pub_key': self.script_pub_key,
      'address': self.address,
      'txid': self.txid,
      'satoshi_amount': self.satoshi_amount,
      'bitcoin_amount': self.bitcoin_amount,
    })
    return d


  @classmethod
  def from_dict(cls, d):
    # Note: This is used to load (and validate) both unsigned and signed inputs.
    expected = '''
previous_output_hash previous_output_index previous_output_index_int
script_length script_length_int script_sig sequence
public_key_hex script_pub_key_length script_pub_key_length_int script_pub_key
address txid satoshi_amount bitcoin_amount
  '''
    expected = expected.replace('\n', ' ').split()
    received = list(d.keys())
    v.validate_list_contains_items(received, expected)
    v.validate_hex_length(d['previous_output_hash'], 32)
    v.validate_hex(d['previous_output_index'])
    v.validate_integer(d['previous_output_index_int'])
    # Cross-checks
    previous_output_index = basic.int_to_hex_le(d['previous_output_index_int'])
    previous_output_index = basic.pad_hex_le(previous_output_index, n_bytes=4)
    assert previous_output_index == d['previous_output_index']
    if d['script_length'] is not None:
      v.validate_hex(d['script_length'])
      assert d['script_length_int'] == basic.var_int_to_int(d['script_length'])
    if d['script_sig'] is not None:
      v.validate_hex(d['script_sig'])
      script_length = basic.var_int_to_int(d['script_length'])
      script_length_2 = basic.hex_len(d['script_sig'])
      if (script_length != script_length_2):
        msg = "Script length value ({}) != calculated hex byte length of script_sig value ({})."
        msg = msg.format(script_length, script_length_2)
        raise ValueError(msg)
    assert d['sequence'] == 'ffffffff'
    if d['public_key_hex'] is not None:
      v.validate_hex_length(d['public_key_hex'], 64)
    if d['script_pub_key_length'] is not None:
      v.validate_hex(d['script_pub_key_length'])
      assert d['script_pub_key_length_int'] == basic.var_int_to_int(d['script_pub_key_length'])
    if d['script_pub_key'] is not None:
      v.validate_hex(d['script_pub_key'])
      script_pub_key_length = basic.var_int_to_int(d['script_pub_key_length'])
      assert script_pub_key_length == basic.hex_len(d['script_pub_key'])
    basic.validate_bitcoin_address(d['address'])
    previous_output_hash = basic.reverse_hex_order(d['txid'])
    assert previous_output_hash == d['previous_output_hash']
    v.validate_integer(d['satoshi_amount'])
    basic.validate_positive_bitcoin_amount(d['bitcoin_amount'])
    bitcoin_amount = basic.satoshi_to_bitcoin(d['satoshi_amount'])
    assert bitcoin_amount == d['bitcoin_amount']
    # Create the instance and save the instance variables.
    ti = TransactionInput()
    ti.previous_output_hash = d['previous_output_hash']
    ti.previous_output_index = d['previous_output_index']
    ti.previous_output_index_int = d['previous_output_index_int']
    ti.script_length = d['script_length']
    ti.script_length_int = d['script_length_int']
    ti.script_sig = d['script_sig']
    ti.script_pub_key_length = d['script_pub_key_length']
    ti.script_pub_key_length_int = d['script_pub_key_length_int']
    ti.script_pub_key = d['script_pub_key']
    ti.address = d['address']
    ti.txid = d['txid']
    ti.satoshi_amount = d['satoshi_amount']
    ti.bitcoin_amount = d['bitcoin_amount']
    return ti


  def to_dict_signable_form(self):
    d = OrderedDict()
    d.update({
      'previous_output_hash': self.previous_output_hash,
      'previous_output_index': self.previous_output_index,
      'script_pub_key_length': self.script_pub_key_length,
      'script_pub_key': self.script_pub_key,
      'sequence': self.sequence,
    })
    return d


  def to_dict_signable_form_empty(self):
    # A script_length of 0 that indicates that no script is included.
    d = OrderedDict()
    d.update({
      'previous_output_hash': self.previous_output_hash,
      'previous_output_index': self.previous_output_index,
      'script_pub_key_length': '00',
      'sequence': self.sequence,
    })
    return d


  def to_dict_signed_form(self):
    d = OrderedDict()
    d.update({
      'previous_output_hash': self.previous_output_hash,
      'previous_output_index': self.previous_output_index,
      'script_length': self.script_length,
      'script_sig': self.script_sig,
      'sequence': self.sequence,
    })
    return d



