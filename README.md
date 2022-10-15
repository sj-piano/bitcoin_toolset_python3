# Description


A pure Python 3 toolset for various Bitcoin operations.

Examples: Derive an address from a private key, create and sign a transaction.




# Sample commands


```bash

python3 cli.py

python3 cli.py --help

python3 cli.py --task hello

python3 cli.py --task hello --log-level=info

python3 cli.py --task get_python_version

python3 cli.py --task get_private_key_wif --private-key-hex="01"

python3 cli.py --task get_public_key --private-key-hex="01"

python3 cli.py --task get_address --private-key-hex="01"

python3 cli.py --task sign_data --private-key-hex="01" --data="hello world"

python3 cli.py --task verify_signature --public-key-hex="01" --data="hello world" --signature="foo"

python3 cli.py --task create_transaction --utxo-selection-approach="smallest_first, one_address_at_a_time, smallest_address_first" --utxo-file cli_input/utxos.json --output-file cli_input/outputs.json > cli_input/transaction_unsigned.json

python3 cli.py --task sign_transaction --private-key-file cli_input/private_keys.txt --transaction-file cli_input/transaction_unsigned.json > cli_input/transaction_signed.txt

```


Tests:

```bash

# Run all tests, including submodule tests.
pytest3

# Run all tests in a specific test file
pytest3 bitcoin_toolset/test/test_hello.py

# Run tests with relatively little output
pytest3 --quiet bitcoin_toolset/test/test_hello.py

# Run a single test
pytest3 bitcoin_toolset/test/test_hello.py::test_hello

# Print log output in real-time during a single test
pytest3 --capture=no --log-cli-level=INFO bitcoin_toolset/test/test_hello.py::test_hello

# Note: The --capture=no option will also cause print statements within the test code to produce output.

```



Code style:


```bash

pycodestyle bitcoin_toolset/code/hello.py

pycodestyle --filename=*.py

pycodestyle --filename=*.py --statistics

pycodestyle --filename=*.py --exclude bitcoin_toolset/submodules

```

Settings for pycodestyle are stored in the file `tox.ini`.




# Environment


Successfully run under the following environments:

1:  
- Ubuntu 16.04 on WSL (Windows Subsystem for Linux) on Windows 10  
- Python 3.6.15
- pytest 6.1.2  

Recommendation: Use `pyenv` to install these specific versions of `python` and `pytest`.




# Installation


Install & configure `pyenv`.  

https://github.com/pyenv/pyenv-installer

https://github.com/pyenv/pyenv

Result: When you change into the `bitcoin_toolset_python3` directory, the versions of `python` and `pip` change appropriately.


```
git clone --recurse-submodules git@github.com/sj-piano/bitcoin_toolset_python3.git

cd bitcoin_toolset_python3

pyenv install 3.6.15

pyenv local 3.6.15

pip install -r requirements.txt
```








