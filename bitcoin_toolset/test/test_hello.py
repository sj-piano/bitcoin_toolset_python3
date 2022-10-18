# Imports
import pytest
import pkgutil




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Setup for this file.
@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):
  # If log_level is supplied to pytest in the commandline args, then use it to set up the logging in the application code.
  log_level = pytestconfig.getoption('log_cli_level')
  if log_level is not None:
    log_level = log_level.lower()
    code.setup(log_level = log_level)
    submodules.setup(log_level = log_level)




# Notes:
# - The command { pytest bitcoin_toolset/test/test_hello.py }
# in the package directory should load and run the tests in this file.
# - Run a specific test:
# -- pytest bitcoin_toolset/test/test_hello.py::test_hello
# - Note: Using { pytest } will cause submodule tests to run as well, and these will fail.
# - Run quietly:
# -- [all tests] pytest --quiet bitcoin_toolset/test
# -- pytest --quiet bitcoin_toolset/test/test_hello.py
# - Print log output in real-time during a single test:
# -- pytest --capture=no --log-cli-level=INFO bitcoin_toolset/test/test_hello.py::test_hello
# --- Note the use of the pytest --capture=no option. This will also cause print statements in the test code itself to produce output.








# ### SECTION
# Basic checks.


def test_hello():
  x = code.hello.hello()
  print(x)
  assert x == 'hello world'


def test_hello_data():
  data_file = '../data/data1.txt'
  data = pkgutil.get_data(__name__, data_file).decode('ascii').strip()
  assert data == 'hello world'

