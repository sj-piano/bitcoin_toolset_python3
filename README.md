# Description


A pure Python 3 toolset for various Bitcoin operations.

Examples: Derive an address from a private key, create and sign a transaction.




# Sample commands


```bash

python cli.py

python cli.py --help

python cli.py --task hello

python cli.py --task hello --log-level=info

python cli.py --task get_python_version



python cli.py --task get_private_key_wif --private-key-hex="01"

# result:
# 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf



python cli.py --task get_public_key --private-key-hex="01"

# result:
# 79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8


python cli.py --task get_address --private-key-hex="01"

# result:
# 1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm



python cli.py --task sign_data --private-key-hex="01" --data="hello world"

# result:
# 50abcc1d060f40ca0049124dadc0977ecca7a0ed05a32a1dae0a5178cf8ca28827f4d877497750ce5079f48a1beb4aa590110f165de67cd2c439fd2a3d91927e




PUBLIC_KEY="79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8"

SIGNATURE="50abcc1d060f40ca0049124dadc0977ecca7a0ed05a32a1dae0a5178cf8ca28827f4d877497750ce5079f48a1beb4aa590110f165de67cd2c439fd2a3d91927e"

python cli.py --task verify_data_signature --public-key-hex=$PUBLIC_KEY --data="hello world" --signature-hex=$SIGNATURE

# result:
# Valid signature.

```




The next set of sample commands require a list of available inputs, stored in `inputs.json`, and a set of design details for a new transaction, stored in `design.json`.

To create a valid new transaction, `inputs.json` must of course contain inputs that are currently available on the blockchain for spending. However, for testing, we can use test inputs that don't exist or have already been spent.

Sample `inputs.json`:

```json
[
  {
    "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
    "transaction_id": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
    "previous_output_index": 9,
    "bitcoin_amount": "0.002"
  }
]
```

Sample `design.json`:

```json
{
  "change_address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
  "fee": 225,
  "max_fee": 250,
  "max_spend_percentage": "100.00",
  "outputs": [
    {
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775"
    }
  ]
}
```

Private keys are stored as text files in their own directory. Each private key file contains the key in hex form on a single line.

```bash
stjohn@judgement:bitcoin_toolset_python3$ tail -n +1 ../bitcoin_private_keys_test/*
==> ../bitcoin_private_keys_test/private_key_1.txt <==
0000000000000000000000007468655f6c6962726172795f6f665f626162656c

==> ../bitcoin_private_keys_test/private_key_2.txt <==
00000000000000000000007468655f6d6f74655f696e5f676f6427735f657965
```


In this sequence, we go through all the possible steps of creating a new transaction. Creation, validation, signing, verification, rendering into hex, and decoding.


```bash

python cli.py --task create_unsigned_transaction_json --input-file cli_input/inputs.json --design-file cli_input/design.json > cli_output/tx_unsigned.json


python cli.py --task validate_unsigned_transaction_json --data-file cli_output/tx_unsigned.json


python cli.py --task create_signed_transaction_json --private-key-dir ../bitcoin_private_keys_test --data-file cli_output/tx_unsigned.json > cli_output/tx_signed.json


python cli.py --task verify_signed_transaction_json --data-file cli_output/tx_signed.json


python cli.py --task create_signed_transaction_hex --data-file cli_output/tx_signed.json


python cli.py --task verify_signed_transaction_hex --data-file cli_output/tx_signed.txt


python cli.py --task decode_signed_transaction_hex --data-file cli_output/tx_signed.txt

```




We can also perform all the steps in a single command.

```bash

python cli.py --task create_sign_and_verify_transaction_hex --private-key-dir ../bitcoin_private_keys_test --input-file cli_input/inputs.json --design-file cli_input/design.json


We can also use a shorter task name (`create_transaction`) that is easier to remember:

```bash

python cli.py --task create_transaction --private-key-dir ../bitcoin_private_keys_test --input-file cli_input/inputs.json --design-file cli_input/design.json

```




Tests:

```bash

# Run all tests, including submodule tests.
pytest

# Run all tests, excluding submodule tests.
pytest --ignore=bitcoin_toolset/submodules

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



# Guidance for `design.json`


Sample `design.json`:

```json
{
  "change_address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
  "fee": 225,
  "max_fee": 250,
  "max_spend_percentage": "100.00",
  "outputs": [
    {
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775"
    }
  ]
}
```

Obligatory arguments:  
- change_address  
- fee or fee_rate  
- max_fee  
- max_spend_percentage  


change_address: Inputs will be selected from the available list until their combined value exceeds the total output value + the fee value. Any surplus value will be sent to the change address.

fee: The transaction fee in satoshi. Can be integer or string.

fee_rate: An alternative option to `fee`. The transaction fee rate in satoshi/byte. Can be integer or string. If string, can be a float value.

max_fee: The maximum fee in satoshi that is permitted in the transaction. Can be integer or string.

max_spend_percentage: Maximum percentage of total available input value that may be spent in the transaction. Can be integer or string. If string, can be a float value.




# Example transaction creation (fast)


`inputs.json`:

```json
[
  {
    "address": "138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam",
    "transaction_id": "e4609e0f1ca854b8b07381f32ba31adbad9713205f5a4f3f56a5a32853d47855",
    "previous_output_index": 8,
    "bitcoin_amount": "0.00242"
  }
]
```


`design.json`:

```json
{
  "change_address": "138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam",
  "fee_rate": 1,
  "max_fee": 250,
  "max_spend_percentage": "100.00",
  "outputs": [
    {
      "address": "13xPBB175FtPbPQ84iB8KuawaVy3mHrady",
      "bitcoin_amount": "0.00241777"
    }
  ]
}
```

`../bitcoin_private_keys_test/private_key_2.txt`:

```
00000000000000000000007468655f6d6f74655f696e5f676f6427735f657965
```


```bash
stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task create_transaction --private-key-dir ../bitcoin_private_keys_test --input-file cli_input/inputs.json --design-file cli_input/design.json > cli_output/tx_signed.txt


stjohn@judgement:bitcoin_toolset_python3$ cat cli_output/tx_signed.txt
01000000015578d45328a3a5563f4f5a5f201397addb1aa32bf38173b0b854a81c0f9e60e4080000008b483045022100ee18501fbcf2543ee8ffb5f9c12b65181960345014856b5f639e2f98f70c001b02203af10ddcedd833781628b144d1201d2369dbf7f99d0a9fb955da63d4881186320141041ad06846fd7cf9998a827485d8dd5aaba9eccc385ba7759a6e9055fbdf90d7513c0d11fe5e5dcfcf8d4946c67f6c45f8e7f7d7a9c254ca8ebde1ffd64ab9dd58ffffffff0171b00300000000001976a9142069a3fae01db74cef12d1d01811afdf6a3e1c2e88ac00000000
```


The signed transaction hex is ready for broadcast. However, it is recommended to decode it first and double-check its output addresses and values. Note that the signed transaction does not include input values or fee information.


```
stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task decode_signed_transaction_hex --data-file cli_output/tx_signed.txt
{
  "version": "01000000",
  "input_count": "01",
  "inputs": [
    {
      "previous_output_hash": "5578d45328a3a5563f4f5a5f201397addb1aa32bf38173b0b854a81c0f9e60e4",
      "previous_output_index": "08000000",
      "previous_output_index_int": 8,
      "script_length": "8b",
      "script_length_int": 139,
      "script_sig": "483045022100ee18501fbcf2543ee8ffb5f9c12b65181960345014856b5f639e2f98f70c001b02203af10ddcedd833781628b144d1201d2369dbf7f99d0a9fb955da63d4881186320141041ad06846fd7cf9998a827485d8dd5aaba9eccc385ba7759a6e9055fbdf90d7513c0d11fe5e5dcfcf8d4946c67f6c45f8e7f7d7a9c254ca8ebde1ffd64ab9dd58",
      "sequence": "ffffffff",
      "public_key_hex": "1ad06846fd7cf9998a827485d8dd5aaba9eccc385ba7759a6e9055fbdf90d7513c0d11fe5e5dcfcf8d4946c67f6c45f8e7f7d7a9c254ca8ebde1ffd64ab9dd58",
      "script_pub_key_length": "19",
      "script_pub_key_length_int": 25,
      "script_pub_key": "76a914176a0e0c2b9b0e77d630712ad301b749102a304488ac",
      "address": "138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam",
      "txid": "e4609e0f1ca854b8b07381f32ba31adbad9713205f5a4f3f56a5a32853d47855",
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  ],
  "output_count": "01",
  "outputs": [
    {
      "value": "71b0030000000000",
      "script_length": "19",
      "script_length_int": 25,
      "script_pub_key": "76a9142069a3fae01db74cef12d1d01811afdf6a3e1c2e88ac",
      "address": "13xPBB175FtPbPQ84iB8KuawaVy3mHrady",
      "bitcoin_amount": "0.00241777",
      "satoshi_amount": 241777
    }
  ],
  "block_lock_time": "00000000",
  "hash_type_4_byte": "01000000",
  "hash_type_1_byte": "01",
  "signed": true,
  "total_input": {
    "satoshi_amount": null,
    "bitcoin_amount": null
  },
  "total_output": {
    "satoshi_amount": 241777,
    "bitcoin_amount": "0.00241777"
  },
  "fee": {
    "satoshi_amount": null,
    "bitcoin_amount": null
  },
  "change_address": null,
  "change": {
    "satoshi_amount": null,
    "bitcoin_amount": null
  },
  "estimated_size_bytes": 223,
  "estimated_fee_rate": {
    "satoshi_per_byte": null,
    "bitcoin_per_byte": null
  },
  "size_bytes": 224,
  "fee_rate": {
    "satoshi_amount": null,
    "bitcoin_amount": null
  }
}
```




# Example transaction creation (slow, detailed, step-by-step)


`inputs.json`:

```json
[
  {
    "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
    "transaction_id": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
    "previous_output_index": 9,
    "bitcoin_amount": "0.002"
  }
]
```


`design.json`:

```json
{
  "change_address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
  "fee": 225,
  "max_fee": 250,
  "max_spend_percentage": "100.00",
  "outputs": [
    {
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775"
    }
  ]
}
```

`../bitcoin_private_keys_test/private_key_1.txt`:

```
0000000000000000000000007468655f6c6962726172795f6f665f626162656c
```



```bash


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task create_unsigned_transaction_json --input-file cli_input/inputs.json --design-file cli_input/design.json
{
  "version": "01000000",
  "input_count": "01",
  "inputs": [
    {
      "previous_output_hash": "ceb493941bf44671994f853fe8585f330070956640bd30fe885d429183e48284",
      "previous_output_index": "09000000",
      "previous_output_index_int": 9,
      "script_length": null,
      "script_length_int": null,
      "script_sig": null,
      "sequence": "ffffffff",
      "public_key_hex": null,
      "script_pub_key_length": "19",
      "script_pub_key_length_int": 25,
      "script_pub_key": "76a9147dc03dfbe8c62821bcd1ab95446b88ed7008a76e88ac",
      "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
      "txid": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
      "satoshi_amount": 200000,
      "bitcoin_amount": "0.00200000"
    }
  ],
  "output_count": "01",
  "outputs": [
    {
      "value": "5f0c030000000000",
      "script_length": "19",
      "script_length_int": 25,
      "script_pub_key": "76a9140f9ee78522f6cc8a88784ae02b0408e452d8025988ac",
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775",
      "satoshi_amount": 199775
    }
  ],
  "block_lock_time": "00000000",
  "hash_type_4_byte": "01000000",
  "hash_type_1_byte": "01",
  "signed": false
}




# We can set log-level to 'info' to see the construction decisions in detail.


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task create_unsigned_transaction_json --input-file cli_input/inputs.json --design-file cli_input/design.json --log-level=info
INFO     [bitcoin_toolset.code.create_transaction: 79 (create_transaction)] All arguments validated. No problems found.
INFO     [bitcoin_toolset.code.create_transaction: 110 (create_transaction)] Report input and output data.
INFO     [bitcoin_toolset.code.create_transaction: 124 (create_transaction)] Input 0:
- address: 1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ
- txid: 8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce
- previous_output_index: 9
- bitcoin_amount: 0.002 (200000 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 134 (create_transaction)] Output 0:
- address: 12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f
- bitcoin_amount: 0.00199775 (199775 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 147 (create_transaction)] Number of inputs: 1
INFO     [bitcoin_toolset.code.create_transaction: 155 (create_transaction)] Number of outputs: 1
INFO     [bitcoin_toolset.code.create_transaction: 172 (create_transaction)] Input addresses and the value that they each contain:
- 1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ: 0.00200000 bitcoin (200000 satoshi), 1 inputs.
INFO     [bitcoin_toolset.code.create_transaction: 185 (create_transaction)] Output addresses, with total value to be sent to each:
- 12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f: 0.00199775 bitcoin (199775 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 203 (create_transaction)] Total input value: 0.00200000 bitcoin (200000 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 206 (create_transaction)] Total output value: 0.00199775 bitcoin (199775 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 223 (create_transaction)] Total input value is greater than total output value.
- Surplus value: 0.00000225 bitcoin (225 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 226 (create_transaction)] Selecting inputs according to input selection approaches ['smallest_first'] until [total selected input value] exceeds [total output value].
INFO     [bitcoin_toolset.code.create_transaction: 247 (create_transaction)] Total selected input value: 0.00200000 bitcoin (200000 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 262 (create_transaction)] Total selected input value is greater than total output value.
- Surplus value: 0.00000225 bitcoin (225 satoshi)
- This extra value will be sent to the change address.
- Change address: 1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ
INFO     [bitcoin_toolset.code.create_transaction: 288 (create_transaction)] New output created to send change to change address.
INFO     [bitcoin_toolset.code.create_transaction: 294 (create_transaction)] New total output value: 0.00200000 bitcoin (200000 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 302 (create_transaction)] Change amount: 225 bitcoin (0.00000225 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 310 (create_transaction)] Maximum percentage of input value (prior to fee subtraction) that can be spent: 100.00%
- Note: "spend" == send bitcoin to any address that is not the change address.
INFO     [bitcoin_toolset.code.create_transaction: 317 (create_transaction)] Maximum spend amount: 0.00200000 bitcoin (200000 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 327 (create_transaction)] Spend amount: 0.00199775 bitcoin (199775 satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 330 (create_transaction)] The spend amount is 99.89% of the available input value.
INFO     [bitcoin_toolset.code.create_transaction: 344 (create_transaction)] Estimated transaction size: 257 bytes
INFO     [bitcoin_toolset.code.create_transaction: 346 (create_transaction)] Fee type: fee
INFO     [bitcoin_toolset.code.create_transaction: 351 (create_transaction)] Fee: 225 (satoshi)
INFO     [bitcoin_toolset.code.create_transaction: 362 (create_transaction)] Transaction fee: 225 satoshi
INFO     [bitcoin_toolset.code.create_transaction: 366 (create_transaction)] Estimated fee rate: 0.8755 satoshi/byte
INFO     [bitcoin_toolset.code.create_transaction: 369 (create_transaction)] Maximum fee: 250 satoshi
INFO     [bitcoin_toolset.code.create_transaction: 391 (create_transaction)] The fee will use the entire change amount. The change output has been deleted.
INFO     [bitcoin_toolset.code.create_transaction: 404 (create_transaction)] Transaction created.
{
  "version": "01000000",
  "input_count": "01",
  "inputs": [
    {
      "previous_output_hash": "ceb493941bf44671994f853fe8585f330070956640bd30fe885d429183e48284",
      "previous_output_index": "09000000",
      "previous_output_index_int": 9,
      "script_length": null,
      "script_length_int": null,
      "script_sig": null,
      "sequence": "ffffffff",
      "public_key_hex": null,
      "script_pub_key_length": "19",
      "script_pub_key_length_int": 25,
      "script_pub_key": "76a9147dc03dfbe8c62821bcd1ab95446b88ed7008a76e88ac",
      "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
      "txid": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
      "satoshi_amount": 200000,
      "bitcoin_amount": "0.00200000"
    }
  ],
  "output_count": "01",
  "outputs": [
    {
      "value": "5f0c030000000000",
      "script_length": "19",
      "script_length_int": 25,
      "script_pub_key": "76a9140f9ee78522f6cc8a88784ae02b0408e452d8025988ac",
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775",
      "satoshi_amount": 199775
    }
  ],
  "block_lock_time": "00000000",
  "hash_type_4_byte": "01000000",
  "hash_type_1_byte": "01",
  "signed": false
}




# Sign the transaction.


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task create_unsigned_transaction_json --input-file cli_input/inputs.json --design-file cli_input/design.json > cli_output/tx_unsigned.json


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task validate_unsigned_transaction_json --data-file cli_output/tx_unsigned.json
Unsigned transaction data validated.


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task create_signed_transaction_json --private-key-file ../bitcoin_private_keys_test/private_key_1.txt --data-file cli_output/tx_unsigned.json
{
  "version": "01000000",
  "input_count": "01",
  "inputs": [
    {
      "previous_output_hash": "ceb493941bf44671994f853fe8585f330070956640bd30fe885d429183e48284",
      "previous_output_index": "09000000",
      "previous_output_index_int": 9,
      "script_length": "8a",
      "script_length_int": 138,
      "script_sig": "483045022100e516545b7d5ec7222c11421da59171ce7fa1237723146ca82e0a90e1d160321302207fcfad1c1734f6f5af208e2f8f43842ac01fc9b8b93d803d11c0f27fc9b749f70140e8ade66f2cc0e43073f4ccea47db279bbab1a5e30a6e8ba49f12538b215c5b9e0d28bd080d35fde878081e8f05dbc23eeba02b544fa83e6d13b5f2145681e76d",
      "sequence": "ffffffff",
      "public_key_hex": "e8ade66f2cc0e43073f4ccea47db279bbab1a5e30a6e8ba49f12538b215c5b9e0d28bd080d35fde878081e8f05dbc23eeba02b544fa83e6d13b5f2145681e76d",
      "script_pub_key_length": "19",
      "script_pub_key_length_int": 25,
      "script_pub_key": "76a9147dc03dfbe8c62821bcd1ab95446b88ed7008a76e88ac",
      "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
      "txid": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
      "satoshi_amount": 200000,
      "bitcoin_amount": "0.00200000"
    }
  ],
  "output_count": "01",
  "outputs": [
    {
      "value": "5f0c030000000000",
      "script_length": "19",
      "script_length_int": 25,
      "script_pub_key": "76a9140f9ee78522f6cc8a88784ae02b0408e452d8025988ac",
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775",
      "satoshi_amount": 199775
    }
  ],
  "block_lock_time": "00000000",
  "hash_type_4_byte": "01000000",
  "hash_type_1_byte": "01",
  "signed": true
}


# What has changed: Each input now contains values for `public_key_hex` and for `script_sig`.


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task verify_signed_transaction_json --data-file cli_output/tx_signed.json
Valid signature(s).


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task create_signed_transaction_hex --data-file cli_output/tx_signed.json
0100000001ceb493941bf44671994f853fe8585f330070956640bd30fe885d429183e48284090000008a483045022100e516545b7d5ec7222c11421da59171ce7fa1237723146ca82e0a90e1d160321302207fcfad1c1734f6f5af208e2f8f43842ac01fc9b8b93d803d11c0f27fc9b749f70140e8ade66f2cc0e43073f4ccea47db279bbab1a5e30a6e8ba49f12538b215c5b9e0d28bd080d35fde878081e8f05dbc23eeba02b544fa83e6d13b5f2145681e76dffffffff015f0c0300000000001976a9140f9ee78522f6cc8a88784ae02b0408e452d8025988ac0000000001000000


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task create_signed_transaction_hex --data-file cli_output/tx_signed.json > tx_signed.txt


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task verify_signed_transaction_hex --data-file cli_output/tx_signed.txt
Valid signature(s).


stjohn@judgement:bitcoin_toolset_python3$ python cli.py --task decode_signed_transaction_hex --data-file cli_output/tx_signed.txt
{
  "version": "01000000",
  "input_count": "01",
  "inputs": [
    {
      "previous_output_hash": "ceb493941bf44671994f853fe8585f330070956640bd30fe885d429183e48284",
      "previous_output_index": "09000000",
      "previous_output_index_int": 9,
      "script_length": "8a",
      "script_length_int": 138,
      "script_sig": "483045022100e516545b7d5ec7222c11421da59171ce7fa1237723146ca82e0a90e1d160321302207fcfad1c1734f6f5af208e2f8f43842ac01fc9b8b93d803d11c0f27fc9b749f70140e8ade66f2cc0e43073f4ccea47db279bbab1a5e30a6e8ba49f12538b215c5b9e0d28bd080d35fde878081e8f05dbc23eeba02b544fa83e6d13b5f2145681e76d",
      "sequence": "ffffffff",
      "public_key_hex": "e8ade66f2cc0e43073f4ccea47db279bbab1a5e30a6e8ba49f12538b215c5b9e0d28bd080d35fde878081e8f05dbc23eeba02b544fa83e6d13b5f2145681e76d",
      "script_pub_key_length": "19",
      "script_pub_key_length_int": 25,
      "script_pub_key": "76a9147dc03dfbe8c62821bcd1ab95446b88ed7008a76e88ac",
      "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
      "txid": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  ],
  "output_count": "01",
  "outputs": [
    {
      "value": "5f0c030000000000",
      "script_length": "19",
      "script_length_int": 25,
      "script_pub_key": "76a9140f9ee78522f6cc8a88784ae02b0408e452d8025988ac",
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775",
      "satoshi_amount": 199775
    }
  ],
  "block_lock_time": "00000000",
  "hash_type_4_byte": "01000000",
  "hash_type_1_byte": "01",
  "signed": true
}


# Note: When decoding a signed tx from its hex form, we can't know the value contained in each input.


```






