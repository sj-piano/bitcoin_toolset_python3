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

PUBLIC_KEY="79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8"

python3 cli.py --task get_address --private-key-hex="01"

ADDRESS="1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm" 

python3 cli.py --task sign_data --private-key-hex="01" --data="hello world"

SIGNATURE="50abcc1d060f40ca0049124dadc0977ecca7a0ed05a32a1dae0a5178cf8ca28827f4d877497750ce5079f48a1beb4aa590110f165de67cd2c439fd2a3d91927e"

python3 cli.py --task verify_signature --public-key-hex=$PUBLIC_KEY --data="hello world" --signature-hex=$SIGNATURE

CHANGE_ADDRESS=$ADDRESS

python3 cli.py --task create_transaction --change-address=$CHANGE_ADDRESS --utxo-selection-approach="smallest_first, one_address_at_a_time, smallest_address_first" --utxo-file cli_input/utxos.json --output-file cli_input/outputs.json > cli_input/transaction_unsigned.json

python3 cli.py --task sign_transaction --private-key-file cli_input/private_keys.json --transaction-file cli_input/transaction_unsigned.json > cli_input/transaction_signed.txt

python3 cli.py --task verify_signed_transaction --public-key-file cli_input/public_keys.json --utxo-file cli_input/utxos.json --signed-transaction-file cli_input/transaction_signed.txt

```


Tests:

```bash

# Run all tests, including submodule tests.
pytest

# Run all tests in a specific test file
pytest bitcoin_toolset/test/test_hello.py

# Run tests with relatively little output
pytest --quiet bitcoin_toolset/test/test_hello.py

# Run a single test
pytest bitcoin_toolset/test/test_hello.py::test_hello

# Print log output in real-time during a single test
pytest --capture=no --log-cli-level=INFO bitcoin_toolset/test/test_hello.py::test_hello

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








