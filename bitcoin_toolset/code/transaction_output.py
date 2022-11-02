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




class TransactionOutput:


  def __init__(self):
    # Properties that go into the raw transaction:
    self.value = None  # 8 bytes (little-endian)
    self.script_length = None  # var_int
    self.script_length_int = None
    self.script_pub_key = None  # hex bytes
    # Other properties:
    self.address = None  # string
    self.bitcoin_amount = None  # string
    self.satoshi_amount = None  # int


  def __str__(self):
    name = self.__class__.__name__
    ad = self.address
    sa = self.satoshi_amount
    s = "{name}: address={ad}, satoshi_amount={sa}"
    s = s.format(**vars())
    return s


  @classmethod
  def create(cls, address, satoshi_amount):
    value = basic.int_to_hex_le(satoshi_amount)
    value = basic.pad_hex_le(value, n_bytes=8)
    script_pub_key, script_length = basic.address_to_script_pub_key(address)
    script_length_int = basic.var_int_to_int(script_length)
    # Calculate bitcoin amount from satoshi amount. We use this for logging.
    bitcoin_amount = basic.satoshi_to_bitcoin(satoshi_amount)
    # Create the instance and save the instance variables.
    to = TransactionOutput()
    to.value = value
    to.script_pub_key = script_pub_key
    to.script_length = script_length
    to.script_length_int = script_length_int
    to.address = address
    to.bitcoin_amount = bitcoin_amount
    to.satoshi_amount = satoshi_amount
    return to


  @classmethod
  def create_from_signed_tx_data(cls, value, script_length, script_pub_key):
    # This creation method accepts the data available in a signed tx.
    # It allows us to call tx.verify()
    script_length_int = basic.var_int_to_int(script_length)
    address = basic.script_pub_key_to_address(script_pub_key)
    satoshi_amount = basic.hex_le_to_int(value)
    bitcoin_amount = basic.satoshi_to_bitcoin(satoshi_amount)
    # Create the instance and save the instance variables.
    to = TransactionOutput()
    to.value = value
    to.script_pub_key = script_pub_key
    to.script_length = script_length
    to.script_length_int = script_length_int
    to.address = address
    to.satoshi_amount = satoshi_amount
    to.bitcoin_amount = bitcoin_amount
    return to


  def to_dict(self):
    d = OrderedDict()
    d.update({
      'value': self.value,
      'script_length': self.script_length,
      'script_length_int': self.script_length_int,
      'script_pub_key': self.script_pub_key,
      'address': self.address,
      'bitcoin_amount': self.bitcoin_amount,
      'satoshi_amount': self.satoshi_amount,
    })
    return d


  @classmethod
  def from_dict(cls, d):
    expected = '''
value script_length script_length_int script_pub_key
address satoshi_amount bitcoin_amount
  '''
    expected = expected.replace('\n', ' ').split()
    received = list(d.keys())
    v.validate_list_contains_items(received, expected)
    v.validate_hex(d['value'])
    v.validate_hex(d['script_length'])
    v.validate_int(d['script_length_int'])
    v.validate_hex(d['script_pub_key'])
    basic.validate_bitcoin_address(d['address'])
    basic.validate_bitcoin_amount(d['bitcoin_amount'])
    # Cross-checks
    assert d['script_length_int'] == basic.var_int_to_int(d['script_length'])
    bitcoin_amount = basic.satoshi_to_bitcoin(d['satoshi_amount'])
    assert bitcoin_amount == d['bitcoin_amount']
    value = basic.int_to_hex_le(d['satoshi_amount'])
    value = basic.pad_hex_le(value, n_bytes=8)
    assert value == d['value']
    hash_hex = basic.bitcoin_address_to_public_key_hash_hex(d['address'])
    script_pub_key, script_length = basic.public_key_hash_hex_to_script_pub_key(hash_hex)
    assert script_pub_key == d['script_pub_key']
    assert script_length == d['script_length']
    # Create the instance and save the instance variables.
    to = TransactionOutput()
    to.value = d['value']
    to.script_pub_key = d['script_pub_key']
    to.script_length = d['script_length']
    to.script_length_int = d['script_length_int']
    to.address = d['address']
    to.bitcoin_amount = d['bitcoin_amount']
    to.satoshi_amount = d['satoshi_amount']
    return to


  def set_satoshi_amount(self, satoshi_amount):
    v.validate_positive_integer(satoshi_amount)
    value = basic.int_to_hex_le(satoshi_amount)
    value = basic.pad_hex_le(value, n_bytes=8)
    self.value = value
    self.satoshi_amount = satoshi_amount
    self.bitcoin_amount = basic.satoshi_to_bitcoin(satoshi_amount)


  def to_dict_signable_form(self):
    d = OrderedDict()
    d.update({
      'value': self.value,
      'script_length': self.script_length,
      'script_pub_key': self.script_pub_key,
    })
    return d


  def to_dict_signed_form(self):
    return self.to_dict_signable_form()

