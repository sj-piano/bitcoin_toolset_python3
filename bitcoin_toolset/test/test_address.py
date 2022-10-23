# Imports
import pytest




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Shortcuts
ecdsa = submodules.ecdsa_python3




# Setup for this file.
@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):
  # If log_level is supplied to pytest in the commandline args, then use it to set up the logging in the application code.
  log_level = pytestconfig.getoption('log_cli_level')
  if log_level is not None:
    log_level = log_level.lower()
    code.setup(log_level = log_level)
    submodules.setup(log_level = log_level)




def test_hello_world():
  private_key_bytes = b'hello_world'
  private_key_hex = private_key_bytes.hex()
  private_key_hex_2 = '00000000000000000000000000000000000000000068656c6c6f5f776f726c64'
  assert ecdsa.ecdsa.code.convenience.format_private_key_hex(private_key_hex) == private_key_hex_2
  x = code.basic.private_key_hex_to_address(private_key_hex)
  assert x == '19VdGCFG8QH3CmYXjMXd3UQCK2HdC3UodP'














