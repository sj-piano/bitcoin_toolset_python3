# Imports
import pytest




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Shortcuts
ecdsa = submodules.ecdsa_python3
format_private_key_hex = ecdsa.format_private_key_hex
validate_private_key_hex = ecdsa.validate_private_key_hex
private_key_hex_to_wif = code.basic.private_key_hex_to_wif
private_key_wif_to_hex = code.basic.private_key_wif_to_hex




# Setup for this file.
@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):
  # If log_level is supplied to pytest in the commandline args, then use it to set up the logging in the application code.
  log_level = pytestconfig.getoption('log_cli_level')
  if log_level is not None:
    log_level = log_level.lower()
    code.setup(log_level = log_level)
    submodules.setup(log_level = log_level)




def test_p1():
  private_key_hex = '01'
  private_key_hex_2 = '0000000000000000000000000000000000000000000000000000000000000001'
  assert format_private_key_hex(private_key_hex) == private_key_hex_2
  x = private_key_hex_to_wif(private_key_hex)
  assert x == '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf'




def test_p1_reverse():
  private_key_wif = '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf'
  x = private_key_wif_to_hex(private_key_wif)
  assert x == '0000000000000000000000000000000000000000000000000000000000000001'




def test_p2():
  # This is the private key of checkpoint 1 in Edgecase Datafeed.
  private_key_hex = "62b0d5ec1efa901eca870b75f743b12061f85b9e687d2a8a2393712363268fd2"
  validate_private_key_hex(private_key_hex)
  x = private_key_hex_to_wif(private_key_hex)
  assert x == '5JZkWDonArJN8T8Uaz8br4uCd7jCFDv8cJLQMSNo5q8M9JAVHkY'




def test_p2_reverse():
  private_key_wif = '5JZkWDonArJN8T8Uaz8br4uCd7jCFDv8cJLQMSNo5q8M9JAVHkY'
  x = private_key_wif_to_hex(private_key_wif)
  assert x == '62b0d5ec1efa901eca870b75f743b12061f85b9e687d2a8a2393712363268fd2'




def test_p3():
  # This is the private key of checkpoint 2 in Edgecase Datafeed.
  private_key_hex = "484b9d5bbf3050047c340998704a6e786310a3676f74052ea09856bd6b2436cd"
  validate_private_key_hex(private_key_hex)
  x = private_key_hex_to_wif(private_key_hex)
  assert x == '5JN8GbXdZ8kF3fdxQWeRo438GwMXmFWeaaoASuat57L7fsEv9UU'




def test_p3_reverse():
  private_key_wif = '5JN8GbXdZ8kF3fdxQWeRo438GwMXmFWeaaoASuat57L7fsEv9UU'
  x = private_key_wif_to_hex(private_key_wif)
  assert x == '484b9d5bbf3050047c340998704a6e786310a3676f74052ea09856bd6b2436cd'



