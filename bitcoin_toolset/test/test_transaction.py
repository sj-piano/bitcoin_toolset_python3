# Imports
import pytest
from argparse import Namespace




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Shortcuts
ecdsa = submodules.ecdsa_python3
basic = code.basic
transaction = code.transaction
transaction_input = code.transaction_input
transaction_output = code.transaction_output




# Notes
# Source for test transactions:
# http://edgecase.net/articles/bitcoin_transaction_test_set_2




# Setup for this file.
@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):
  # If log_level is supplied to pytest in the commandline args, then use it to set up the logging in the application code.
  log_level = pytestconfig.getoption('log_cli_level')
  if log_level is not None:
    log_level = log_level.lower()
    code.setup(log_level = log_level)
    submodules.setup(log_level = log_level)




# Translation: Turn pasted JSON output into valid Python dict.
null = None
true = True
false = False




def build_tx_inputs_and_outputs(inputs_data, outputs_data):
  inputs = [
    transaction_input.TransactionInput.create(
      address = x['address'],
      txid = x['transaction_id'],
      previous_output_index_int = x['previous_output_index'],
      satoshi_amount = basic.bitcoin_to_satoshi(x['bitcoin_amount']),
    ) for x in inputs_data
  ]
  outputs = [
    transaction_output.TransactionOutput.create(
      address = x['address'],
      satoshi_amount = basic.bitcoin_to_satoshi(x['bitcoin_amount']),
    ) for x in outputs_data
  ]
  return inputs, outputs




def test_tx1():
  # Input data:
  private_keys_hex = [
    '0000000000000000000000007468655f6c6962726172795f6f665f626162656c'
  ]
  random_values_hex = [
    '0072616e646f6d5f627974655f737472696e675f61786178617861735f6d6c6f'
  ]
  inputs_data = [
    {
      "address": "1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ",
      "transaction_id": "8482e48391425d88fe30bd4066957000335f58e83f854f997146f41b9493b4ce",
      "previous_output_index": 9,
      "bitcoin_amount": "0.002"
    }
  ]
  outputs_data = [
    {
      "address": "12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f",
      "bitcoin_amount": "0.00199775"
    }
  ]
  # Expected output data:
  tx_unsigned_expected = {
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
    "signed": false,
    "total_input": {
      "satoshi_amount": 200000,
      "bitcoin_amount": "0.00200000"
    },
    "total_output": {
      "satoshi_amount": 199775,
      "bitcoin_amount": "0.00199775"
    },
    "fee": {
      "satoshi_amount": 225,
      "bitcoin_amount": "0.00000225"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 223,
    "estimated_fee_rate": {
      "satoshi_per_byte": "1.0090",
      "bitcoin_per_byte": "0.00000001"
    },
    "size_bytes": null,
    "fee_rate": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  }
  tx_signed_expected = {
    "version": "01000000",
    "input_count": "01",
    "inputs": [
      {
        "previous_output_hash": "ceb493941bf44671994f853fe8585f330070956640bd30fe885d429183e48284",
        "previous_output_index": "09000000",
        "previous_output_index_int": 9,
        "script_length": "8a",
        "script_length_int": 138,
        "script_sig": "47304402206a2eea0c908efbd780a34c48b48d80946a6e740c272468427bada3ba9773d39a022076017028c4386020b19b7d1f1640558cd902aeffbfbd85f4637a8be0e92ee1de014104e8ade66f2cc0e43073f4ccea47db279bbab1a5e30a6e8ba49f12538b215c5b9e0d28bd080d35fde878081e8f05dbc23eeba02b544fa83e6d13b5f2145681e76d",
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
    "signed": true,
    "total_input": {
      "satoshi_amount": 200000,
      "bitcoin_amount": "0.00200000"
    },
    "total_output": {
      "satoshi_amount": 199775,
      "bitcoin_amount": "0.00199775"
    },
    "fee": {
      "satoshi_amount": 225,
      "bitcoin_amount": "0.00000225"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 223,
    "estimated_fee_rate": {
      "satoshi_per_byte": "1.0090",
      "bitcoin_per_byte": "0.00000001"
    },
    "size_bytes": 223,
    "fee_rate": {
      "satoshi_per_byte": "1.0090",
      "bitcoin_per_byte": "0.00000001"
    }
  }
  tx_signed_hex_expected = """
0100000001ceb493941bf44671994f853fe8585f330070956640bd30fe885d429183e48284090000008a47304402206a2eea0c908efbd780a34c48b48d80946a6e740c272468427bada3ba9773d39a022076017028c4386020b19b7d1f1640558cd902aeffbfbd85f4637a8be0e92ee1de014104e8ade66f2cc0e43073f4ccea47db279bbab1a5e30a6e8ba49f12538b215c5b9e0d28bd080d35fde878081e8f05dbc23eeba02b544fa83e6d13b5f2145681e76dffffffff015f0c0300000000001976a9140f9ee78522f6cc8a88784ae02b0408e452d8025988ac00000000
""".strip()
  txid_expected = '4bdd5f653d0100ea4735953e8e22e92321af9074926b3bd33c279c289f2d975a'
  # Run test
  inputs = [
    transaction_input.TransactionInput.create(
      address = x['address'],
      txid = x['transaction_id'],
      previous_output_index_int = x['previous_output_index'],
      satoshi_amount = basic.bitcoin_to_satoshi(x['bitcoin_amount']),
    ) for x in inputs_data
  ]
  outputs = [
    transaction_output.TransactionOutput.create(
      address = x['address'],
      satoshi_amount = basic.bitcoin_to_satoshi(x['bitcoin_amount']),
    ) for x in outputs_data
  ]
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx2():
  # Input data:
  private_keys_hex = [
    '00000000000000000000007468655f6d6f74655f696e5f676f6427735f657965'
  ]
  random_values_hex = [
    '00000000005468652046616365206f6620476f64206468636d726c636874646a'
  ]
  inputs_data = [
    {
      "address": "138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam",
      "transaction_id": "e4609e0f1ca854b8b07381f32ba31adbad9713205f5a4f3f56a5a32853d47855",
      "previous_output_index": 8,
      "bitcoin_amount": "0.0024200"
    }
  ]
  outputs_data = [
    {
      "address": "13xPBB175FtPbPQ84iB8KuawaVy3mHrady",
      "bitcoin_amount": "0.00241777"
    }
  ]
  tx_unsigned_expected = {
    "version": "01000000",
    "input_count": "01",
    "inputs": [
      {
        "previous_output_hash": "5578d45328a3a5563f4f5a5f201397addb1aa32bf38173b0b854a81c0f9e60e4",
        "previous_output_index": "08000000",
        "previous_output_index_int": 8,
        "script_length": null,
        "script_length_int": null,
        "script_sig": null,
        "sequence": "ffffffff",
        "public_key_hex": null,
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a914176a0e0c2b9b0e77d630712ad301b749102a304488ac",
        "address": "138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam",
        "txid": "e4609e0f1ca854b8b07381f32ba31adbad9713205f5a4f3f56a5a32853d47855",
        "satoshi_amount": 242000,
        "bitcoin_amount": "0.00242000"
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
    "signed": false,
    "total_input": {
      "satoshi_amount": 242000,
      "bitcoin_amount": "0.00242000"
    },
    "total_output": {
      "satoshi_amount": 241777,
      "bitcoin_amount": "0.00241777"
    },
    "fee": {
      "satoshi_amount": 223,
      "bitcoin_amount": "0.00000223"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 223,
    "estimated_fee_rate": {
      "satoshi_per_byte": "1.0000",
      "bitcoin_per_byte": "0.00000001"
    },
    "size_bytes": null,
    "fee_rate": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  }
  tx_signed_expected = {
    "version": "01000000",
    "input_count": "01",
    "inputs": [
      {
        "previous_output_hash": "5578d45328a3a5563f4f5a5f201397addb1aa32bf38173b0b854a81c0f9e60e4",
        "previous_output_index": "08000000",
        "previous_output_index_int": 8,
        "script_length": "8a",
        "script_length_int": 138,
        "script_sig": "473044022017ece35581a034a4838a577fe438f108cf22764927a1ad197ed379460c0764cd022066723723eff05c10bac9a2f63b3e782e24fde290701c9408f3d1054722adad360141041ad06846fd7cf9998a827485d8dd5aaba9eccc385ba7759a6e9055fbdf90d7513c0d11fe5e5dcfcf8d4946c67f6c45f8e7f7d7a9c254ca8ebde1ffd64ab9dd58",
        "sequence": "ffffffff",
        "public_key_hex": "1ad06846fd7cf9998a827485d8dd5aaba9eccc385ba7759a6e9055fbdf90d7513c0d11fe5e5dcfcf8d4946c67f6c45f8e7f7d7a9c254ca8ebde1ffd64ab9dd58",
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a914176a0e0c2b9b0e77d630712ad301b749102a304488ac",
        "address": "138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam",
        "txid": "e4609e0f1ca854b8b07381f32ba31adbad9713205f5a4f3f56a5a32853d47855",
        "satoshi_amount": 242000,
        "bitcoin_amount": "0.00242000"
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
      "satoshi_amount": 242000,
      "bitcoin_amount": "0.00242000"
    },
    "total_output": {
      "satoshi_amount": 241777,
      "bitcoin_amount": "0.00241777"
    },
    "fee": {
      "satoshi_amount": 223,
      "bitcoin_amount": "0.00000223"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 223,
    "estimated_fee_rate": {
      "satoshi_per_byte": "1.0000",
      "bitcoin_per_byte": "0.00000001"
    },
    "size_bytes": 223,
    "fee_rate": {
      "satoshi_per_byte": "1.0000",
      "bitcoin_per_byte": "0.00000001"
    }
  }
  tx_signed_hex_expected = """
01000000015578d45328a3a5563f4f5a5f201397addb1aa32bf38173b0b854a81c0f9e60e4080000008a473044022017ece35581a034a4838a577fe438f108cf22764927a1ad197ed379460c0764cd022066723723eff05c10bac9a2f63b3e782e24fde290701c9408f3d1054722adad360141041ad06846fd7cf9998a827485d8dd5aaba9eccc385ba7759a6e9055fbdf90d7513c0d11fe5e5dcfcf8d4946c67f6c45f8e7f7d7a9c254ca8ebde1ffd64ab9dd58ffffffff0171b00300000000001976a9142069a3fae01db74cef12d1d01811afdf6a3e1c2e88ac00000000
""".strip()
  txid_expected = '745e224ccba0a033c55ea80523f207da18b903418ac1f5d293eed62c19e0334d'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx3():
  # Input data:
  private_keys_hex = [
    '7972b641101c0ad67b0e401b800a9b6f3225c97fc6b8115042cf66968c2fb2e5'
  ]
  random_values_hex = [
    '257c2ff4ac1606d5e42fe152c2624cffac2aa58cdfe8578a69b12beefbce68b9'
  ]
  inputs_data = [
    {
      "address": "16ASCUS3s7D4UQh6J9oHGuT19agPvD3PFj",
      "transaction_id": "f02eca2852bf73f3c722db2d151e7755d853efd8dd6224249b14f8b51dffbc6e",
      "previous_output_index": 12,
      "bitcoin_amount": "0.00600000"
    }
  ]
  outputs_data = [
    {
      "address": "1KHDLNmqBtiBELUsmTCkNASg79jfEVKrig",
      "bitcoin_amount": "0.00300000"
    },
    {
      "address": "1DLg5i1kBjXYXy9f82xZcHokEMC9dtct7P",
      "bitcoin_amount": "0.00299226"
    }
  ]
  tx_unsigned_expected = {
    "version": "01000000",
    "input_count": "01",
    "inputs": [
      {
        "previous_output_hash": "6ebcff1db5f8149b242462ddd8ef53d855771e152ddb22c7f373bf5228ca2ef0",
        "previous_output_index": "0c000000",
        "previous_output_index_int": 12,
        "script_length": null,
        "script_length_int": null,
        "script_sig": null,
        "sequence": "ffffffff",
        "public_key_hex": null,
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a91438a1681a09280ecb20b62cf661913e811eb3c4b188ac",
        "address": "16ASCUS3s7D4UQh6J9oHGuT19agPvD3PFj",
        "txid": "f02eca2852bf73f3c722db2d151e7755d853efd8dd6224249b14f8b51dffbc6e",
        "satoshi_amount": 600000,
        "bitcoin_amount": "0.00600000"
      }
    ],
    "output_count": "02",
    "outputs": [
      {
        "value": "e093040000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a914c8833727be832b6634d8ddf7bfcf51e379b28f6388ac",
        "address": "1KHDLNmqBtiBELUsmTCkNASg79jfEVKrig",
        "bitcoin_amount": "0.00300000",
        "satoshi_amount": 300000
      },
      {
        "value": "da90040000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a914875a093668adff783d0835f4db655c5a47a0ceaa88ac",
        "address": "1DLg5i1kBjXYXy9f82xZcHokEMC9dtct7P",
        "bitcoin_amount": "0.00299226",
        "satoshi_amount": 299226
      }
    ],
    "block_lock_time": "00000000",
    "hash_type_4_byte": "01000000",
    "hash_type_1_byte": "01",
    "signed": false,
    "total_input": {
      "satoshi_amount": 600000,
      "bitcoin_amount": "0.00600000"
    },
    "total_output": {
      "satoshi_amount": 599226,
      "bitcoin_amount": "0.00599226"
    },
    "fee": {
      "satoshi_amount": 774,
      "bitcoin_amount": "0.00000774"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 257,
    "estimated_fee_rate": {
      "satoshi_per_byte": "3.0117",
      "bitcoin_per_byte": "0.00000003"
    },
    "size_bytes": null,
    "fee_rate": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  }
  tx_signed_expected = {
    "version": "01000000",
    "input_count": "01",
    "inputs": [
      {
        "previous_output_hash": "6ebcff1db5f8149b242462ddd8ef53d855771e152ddb22c7f373bf5228ca2ef0",
        "previous_output_index": "0c000000",
        "previous_output_index_int": 12,
        "script_length": "8a",
        "script_length_int": 138,
        "script_sig": "47304402202d8617427fc589848ef2e0481d148e0ce5d60aaa26e466fdfe62890d0d67ca6902200df89728ea73816cecfdfd6a734ca8b70da7000e213b87dcfdc9d48400164fac014104108e1c01a42bbd09b77a26b5f732f10d7108b2fe31cba137e9d15e24c7c30d2515904dfe646f3e94a3aa482afbbe0dc178b9b212154529768e0ba74452df1c2a",
        "sequence": "ffffffff",
        "public_key_hex": "108e1c01a42bbd09b77a26b5f732f10d7108b2fe31cba137e9d15e24c7c30d2515904dfe646f3e94a3aa482afbbe0dc178b9b212154529768e0ba74452df1c2a",
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a91438a1681a09280ecb20b62cf661913e811eb3c4b188ac",
        "address": "16ASCUS3s7D4UQh6J9oHGuT19agPvD3PFj",
        "txid": "f02eca2852bf73f3c722db2d151e7755d853efd8dd6224249b14f8b51dffbc6e",
        "satoshi_amount": 600000,
        "bitcoin_amount": "0.00600000"
      }
    ],
    "output_count": "02",
    "outputs": [
      {
        "value": "e093040000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a914c8833727be832b6634d8ddf7bfcf51e379b28f6388ac",
        "address": "1KHDLNmqBtiBELUsmTCkNASg79jfEVKrig",
        "bitcoin_amount": "0.00300000",
        "satoshi_amount": 300000
      },
      {
        "value": "da90040000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a914875a093668adff783d0835f4db655c5a47a0ceaa88ac",
        "address": "1DLg5i1kBjXYXy9f82xZcHokEMC9dtct7P",
        "bitcoin_amount": "0.00299226",
        "satoshi_amount": 299226
      }
    ],
    "block_lock_time": "00000000",
    "hash_type_4_byte": "01000000",
    "hash_type_1_byte": "01",
    "signed": true,
    "total_input": {
      "satoshi_amount": 600000,
      "bitcoin_amount": "0.00600000"
    },
    "total_output": {
      "satoshi_amount": 599226,
      "bitcoin_amount": "0.00599226"
    },
    "fee": {
      "satoshi_amount": 774,
      "bitcoin_amount": "0.00000774"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 257,
    "estimated_fee_rate": {
      "satoshi_per_byte": "3.0117",
      "bitcoin_per_byte": "0.00000003"
    },
    "size_bytes": 257,
    "fee_rate": {
      "satoshi_per_byte": "3.0117",
      "bitcoin_per_byte": "0.00000003"
    }
  }
  tx_signed_hex_expected = """
01000000016ebcff1db5f8149b242462ddd8ef53d855771e152ddb22c7f373bf5228ca2ef00c0000008a47304402202d8617427fc589848ef2e0481d148e0ce5d60aaa26e466fdfe62890d0d67ca6902200df89728ea73816cecfdfd6a734ca8b70da7000e213b87dcfdc9d48400164fac014104108e1c01a42bbd09b77a26b5f732f10d7108b2fe31cba137e9d15e24c7c30d2515904dfe646f3e94a3aa482afbbe0dc178b9b212154529768e0ba74452df1c2affffffff02e0930400000000001976a914c8833727be832b6634d8ddf7bfcf51e379b28f6388acda900400000000001976a914875a093668adff783d0835f4db655c5a47a0ceaa88ac00000000
""".strip()
  txid_expected = 'db2c3d84708cd9d0e40ae1754021f9146a0d6ab555fc0e1d547d7876c0c092f4'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx4():
  # Input data:
  private_keys_hex = [
    '7a0d11f6015f941ea486922e45310535c5b71c59d8489447648eebdb6a39e2a8'
  ]
  random_values_hex = [
    '84425ee562f20d7493420c97eea153d37891eb63ce51fa24f51bfc7646353d32'
  ]
  inputs_data = [
    {
      "address": "17pNyD9ur28aBgPhHtAFi6fAyrvgshp5yn",
      "transaction_id": "1b1ad779f50b07aac0048471844c0637100561b179457ddd433f1c05adf24a19",
      "previous_output_index": 3,
      "bitcoin_amount": "0.00400000"
    }
  ]
  outputs_data = [
    {
      "address": "1PFw45xp5JUcLZfDQnMpto6yJpcjRLqrJ8",
      "bitcoin_amount": "0.00200000"
    },
    {
      "address": "19u4WSjpp19yoAK9kdRyY9HJ7ad2S8s1E4",
      "bitcoin_amount": "0.00199614"
    }
  ]
  tx_unsigned_expected = {
    "version": "01000000",
    "input_count": "01",
    "inputs": [
      {
        "previous_output_hash": "194af2ad051c3f43dd7d4579b161051037064c84718404c0aa070bf579d71a1b",
        "previous_output_index": "03000000",
        "previous_output_index_int": 3,
        "script_length": null,
        "script_length_int": null,
        "script_sig": null,
        "sequence": "ffffffff",
        "public_key_hex": null,
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a9144ac6a4d0ee2aa064974bf6e571f6f700b7f67ce688ac",
        "address": "17pNyD9ur28aBgPhHtAFi6fAyrvgshp5yn",
        "txid": "1b1ad779f50b07aac0048471844c0637100561b179457ddd433f1c05adf24a19",
        "satoshi_amount": 400000,
        "bitcoin_amount": "0.00400000"
      }
    ],
    "output_count": "02",
    "outputs": [
      {
        "value": "400d030000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a914f425b648af85989c1387d532393938fcb7d7bcbb88ac",
        "address": "1PFw45xp5JUcLZfDQnMpto6yJpcjRLqrJ8",
        "bitcoin_amount": "0.00200000",
        "satoshi_amount": 200000
      },
      {
        "value": "be0b030000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a91461999077782b7298b813d83459a9c944da6460bd88ac",
        "address": "19u4WSjpp19yoAK9kdRyY9HJ7ad2S8s1E4",
        "bitcoin_amount": "0.00199614",
        "satoshi_amount": 199614
      }
    ],
    "block_lock_time": "00000000",
    "hash_type_4_byte": "01000000",
    "hash_type_1_byte": "01",
    "signed": false,
    "total_input": {
      "satoshi_amount": 400000,
      "bitcoin_amount": "0.00400000"
    },
    "total_output": {
      "satoshi_amount": 399614,
      "bitcoin_amount": "0.00399614"
    },
    "fee": {
      "satoshi_amount": 386,
      "bitcoin_amount": "0.00000386"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 257,
    "estimated_fee_rate": {
      "satoshi_per_byte": "1.5019",
      "bitcoin_per_byte": "0.00000002"
    },
    "size_bytes": null,
    "fee_rate": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  }
  tx_signed_expected = {
    "version": "01000000",
    "input_count": "01",
    "inputs": [
      {
        "previous_output_hash": "194af2ad051c3f43dd7d4579b161051037064c84718404c0aa070bf579d71a1b",
        "previous_output_index": "03000000",
        "previous_output_index_int": 3,
        "script_length": "8a",
        "script_length_int": 138,
        "script_sig": "47304402204f38e1194a0f71f4cb03b1a8644dae69c543cab339d19f0412511bed0868904a02201a9356663d0ad3527b5633ced4cbc469f98bccb0940f2583c7c6c0c0868973a3014104c0128d7e4cbfef4e1bae30788b7bd7a4b974027eea5d83c07ac041f194707e8bba70a162c557cdbcb89682a5a310a2d5a722b2d58d18920a00b6b4c7024ce966",
        "sequence": "ffffffff",
        "public_key_hex": "c0128d7e4cbfef4e1bae30788b7bd7a4b974027eea5d83c07ac041f194707e8bba70a162c557cdbcb89682a5a310a2d5a722b2d58d18920a00b6b4c7024ce966",
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a9144ac6a4d0ee2aa064974bf6e571f6f700b7f67ce688ac",
        "address": "17pNyD9ur28aBgPhHtAFi6fAyrvgshp5yn",
        "txid": "1b1ad779f50b07aac0048471844c0637100561b179457ddd433f1c05adf24a19",
        "satoshi_amount": 400000,
        "bitcoin_amount": "0.00400000"
      }
    ],
    "output_count": "02",
    "outputs": [
      {
        "value": "400d030000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a914f425b648af85989c1387d532393938fcb7d7bcbb88ac",
        "address": "1PFw45xp5JUcLZfDQnMpto6yJpcjRLqrJ8",
        "bitcoin_amount": "0.00200000",
        "satoshi_amount": 200000
      },
      {
        "value": "be0b030000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a91461999077782b7298b813d83459a9c944da6460bd88ac",
        "address": "19u4WSjpp19yoAK9kdRyY9HJ7ad2S8s1E4",
        "bitcoin_amount": "0.00199614",
        "satoshi_amount": 199614
      }
    ],
    "block_lock_time": "00000000",
    "hash_type_4_byte": "01000000",
    "hash_type_1_byte": "01",
    "signed": true,
    "total_input": {
      "satoshi_amount": 400000,
      "bitcoin_amount": "0.00400000"
    },
    "total_output": {
      "satoshi_amount": 399614,
      "bitcoin_amount": "0.00399614"
    },
    "fee": {
      "satoshi_amount": 386,
      "bitcoin_amount": "0.00000386"
    },
    "change_address": null,
    "change": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    },
    "estimated_size_bytes": 257,
    "estimated_fee_rate": {
      "satoshi_per_byte": "1.5019",
      "bitcoin_per_byte": "0.00000002"
    },
    "size_bytes": 257,
    "fee_rate": {
      "satoshi_per_byte": "1.5019",
      "bitcoin_per_byte": "0.00000002"
    }
  }
  tx_signed_hex_expected = """
0100000001194af2ad051c3f43dd7d4579b161051037064c84718404c0aa070bf579d71a1b030000008a47304402204f38e1194a0f71f4cb03b1a8644dae69c543cab339d19f0412511bed0868904a02201a9356663d0ad3527b5633ced4cbc469f98bccb0940f2583c7c6c0c0868973a3014104c0128d7e4cbfef4e1bae30788b7bd7a4b974027eea5d83c07ac041f194707e8bba70a162c557cdbcb89682a5a310a2d5a722b2d58d18920a00b6b4c7024ce966ffffffff02400d0300000000001976a914f425b648af85989c1387d532393938fcb7d7bcbb88acbe0b0300000000001976a91461999077782b7298b813d83459a9c944da6460bd88ac00000000
""".strip()
  txid_expected = '8f6318124bdd66f4643ccbfcbcb0a802924833505c015929dc7b1cab2ca02826'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx5():
  # Input data:
  private_keys_hex = [
    'cbac84458fcfbb39f87fca7ab9a9ef2f76812a6f999a75dfa25dbcbb0ee3eb6f',
    '7d37c1a74d3b87d3994ac6db65b4f298f64a8ed6144edfdb2cacea70cf3070af'
  ]
  random_values_hex = [
    '5ab5bbe6fdc861a461a6721b2953d32be23c233e5ad5dc08d7c13daa95adbc17',
    '75fc65686a47326556735be91491a06f380a9db682fe9d50f82ad8d8d8849c2f',
  ]
  inputs_data = [
    {
      "address": "1PFw45xp5JUcLZfDQnMpto6yJpcjRLqrJ8",
      "transaction_id": "8f6318124bdd66f4643ccbfcbcb0a802924833505c015929dc7b1cab2ca02826",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00200000",
    },
    {
      "address": "19u4WSjpp19yoAK9kdRyY9HJ7ad2S8s1E4",
      "transaction_id": "8f6318124bdd66f4643ccbfcbcb0a802924833505c015929dc7b1cab2ca02826",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00199614",
    }
  ]
  outputs_data = [
    {
      "address": "17PZ6uyL59vPirNqqpMnB1kjEXkU7ske7s",
      "bitcoin_amount": "0.00399171",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
01000000022628a02cab1c7bdc2959015c5033489202a8b0bcfccb3c64f466dd4b1218638f000000008b4830450221008d4ecab2a74461cabcd3e5398ca6752594fbd758c3d10ff3a50c5bf45e460a4502206e7607d2f9ff8fa40489c041fdbbcaecfe723caabf28de9451a2be67d8705d1901410426f2ad4968ef7c5412a2cfac85c902f613b7406962477c931d25ddfb2957c494e70f832ac8dd50740c64297038c722542005b0c5191061e444c793b62d9b2aceffffffff2628a02cab1c7bdc2959015c5033489202a8b0bcfccb3c64f466dd4b1218638f010000008a4730440220184f1d7e9cfe7539cd40cae04e71dc21ce05de958620294cb2d490d45356bfc102203f4ae4afe33b93d1cc96c356735d7a4d3b90cfe62cab0d0cf71fd2f7718e99df0141043c8564e9fa9e9530699ffe7c5dd75077698ff96f3786e96bdbb210a109147cedacfdaa784eb4ba538556e8dd70455ba3627fe902f152940d70ffdd55acdb82a9ffffffff0143170600000000001976a9144614b4066faf3ef831a20186f76381c25dd6ea8288ac00000000
""".strip()
  txid_expected = '92616e432f7807bf6d93252fcdca7efb139e56f7aa34835b50670ebc6a4b5649'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 443
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx6():
  # Input data:
  private_keys_hex = [
    'dd23f217012efd9ac3dec71d0c2b42212a58bff75d9e97af900403cf5657bad3',
  ]
  random_values_hex = [
    '706eaef9f357ad6f1ddd0536eaec027a2a218094db8db781601d9ad4e486c61b',
  ]
  inputs_data = [
    {
      "address": "15BLTZb6uQr24MrxqXJaPpRGz1tKrzq7iC",
      "transaction_id": "dd616e2b18e41606e9990b19fa6adb21bb4eacb26c54c141d2b703d7571056a3",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00099442",
    }
  ]
  outputs_data = [
    {
      "address": "1KYtin5SrnZTwKJyRCtjHvzpevjZaGjCg",
      "bitcoin_amount": "0.00098884",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000001a3561057d703b7d241c1546cb2ac4ebb21db6afa190b99e90616e4182b6e61dd000000008b483045022100c317199690d5bf20f90d6a6250f919f27a0767ac6d824451951eb1ff19595d1902205e337c880937833f2feb8887917974c3f96595ce7af000ad2938504bae4e3c540141041cbd3a52ecb96d2e39cb7b85d1b6b3d671e348fbc767a756606fffa69ab6dd3719740c88c0c5893082c15ca9c71c0b17225f0930f3c2b891180372d70aed1cecffffffff0144820100000000001976a91403821bf3afc86ee1590de7c879c3ea5434e6d51d88ac00000000
""".strip()
  txid_expected = '82b4f898b02a557de3f10efee491e3aaff6c461a335a21feec383df749967555'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 558
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx7():
  # Input data:
  private_keys_hex = [
    'f6c8b60b49c35ef5e6e05e9b06aa5b2b28bd28fbfce696dfc2301347d494a22b',
  ]
  random_values_hex = [
    'b28780e24336648daa30a9ce4e3585aa8e45942196f76f6d66e57d82db54a11a',
  ]
  inputs_data = [
    {
      "address": "1BB66Gx4833uKx8Lo2k8Mt4TRk42WTr7cZ",
      "transaction_id": "9d64ba7c5afdb3caa79bb79c35dde09af70b27829241b2823e4ffb918c75d153",
      "previous_output_index": 0,
      "bitcoin_amount": "0.01000000",
    }
  ]
  outputs_data = [
    {
      "address": "12YCFdpsRDvEHNcj5rsmvJ5G2XXkW1icJP",
      "bitcoin_amount": "0.00474300",
    },
    {
      "address": "1H5SUR7Fv7x252WuJPqBjewwpeHuJ218Ky",
      "bitcoin_amount": "0.00500000",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
010000000153d1758c91fb4f3e82b2419282270bf79ae0dd359cb79ba7cab3fd5a7cba649d000000008b483045022100aac4e36174bafa5dd5f2a0b89d306f8bfa302a42e6590f9a654a514a8ea19b1b022047402e5a9c68605d97f0a42e84c940fab10db0138c32f0c8f4dbb196403f5ea50141048b372e0137fbd76f3095098e540f8992febf56c822d023237179e23703d31b6811b21205465d6c0e2cf33c470b1aaa7599200e81a28f546a5afdc0902c03976effffffff02bc3c0700000000001976a91410de69df99d4b834ee6f2bd1466edab556beb7d688ac20a10700000000001976a914b058f09e25382dd3b9339c25a5727085a22c8c6088ac00000000
""".strip()
  txid_expected = '585f054c01139bdae20ff8fa233c4cda47db6d891a387e37dfd56f9cb39d1bea'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 25700
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx8():
  # Input data:
  private_keys_hex = [
    'ecfb8057d4e053dda6849f6a361ca2d6797368651bbb2b52ce4691515a7909e1',
    'fc8c7e92b44fe66f8f20d98a648f659da69461661673e22292a67dc20742ef17',
  ]
  random_values_hex = [
    '0a5a9cc087cf3337bfb0fa12f6fa036d17d6b6dc0e93dfa657c8caca47ad8155',
    '2493ac84058e4f4b79f1bd267c45f52bc7545ef01dd66b8bf077cae86460e954',
  ]
  inputs_data = [
    {
      "address": "12YCFdpsRDvEHNcj5rsmvJ5G2XXkW1icJP",
      "transaction_id": "585f054c01139bdae20ff8fa233c4cda47db6d891a387e37dfd56f9cb39d1bea",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00474300",
    },
    {
      "address": "1H5SUR7Fv7x252WuJPqBjewwpeHuJ218Ky",
      "transaction_id": "585f054c01139bdae20ff8fa233c4cda47db6d891a387e37dfd56f9cb39d1bea",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00500000",
    },
  ]
  outputs_data = [
    {
      "address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
      "bitcoin_amount": "0.00430700",
    },
    {
      "address": "12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ",
      "bitcoin_amount": "0.00500000",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000002ea1b9db39c6fd5df377e381a896ddb47da4c3c23faf80fe2da9b13014c055f58000000008b483045022100d75efc99b640bcc09f569b1b53cb33d407720f9931a719d0ae3212182927cbb802205ea59d7e86f3bdcf7ec5b483a181704909e401cdeb3f8c60172d72aa842ec142014104e5f0aa4e9ee32cc982db529c981f18171cd9d1ccf224a94e4b3c09b51fd3752c6ebf66f0861dc435fee962f995ab9c5346d32332a409c598eb575cec74115180ffffffffea1b9db39c6fd5df377e381a896ddb47da4c3c23faf80fe2da9b13014c055f58010000008b483045022100c70dbea33b9a7d51a9f952a63d65f0572194af68774c09e03d347f65cddd38c3022072e8341e85f5cb6c49be050c862837d451f46a6f5d0f51fa80993a45983cf9d6014104cca91b1ad65fc428789b469f0e030fb2de58132c61f3240f416e3a6eb1963009a359770805e71e9b7c7982da51c2a3209ec908efe71cf5ec8b65f5b9eb05115bffffffff026c920600000000001976a91417091ffac2b6bb51d9fd1d979fac6ec6bf3a2f1e88ac20a10700000000001976a9140f3a634504545b37a97b10214b2f640fb16085e588ac00000000
""".strip()
  txid_expected = '2b0cef7b0abfefeb6c7c6b228930e6218e86e9d8c33f5525d10f34f91cc7bad4'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 43600
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx9():
  # Input data:
  private_keys_hex = [
    'f7def6819cf8efb7c4aeaddecb951688bcda37cee73b92f73a29be076e66579c',
    '11717a85a51ba5cd1711905816a694bdd288d0639f27d8bb113ba94df9da1501',
  ]
  random_values_hex = [
    '2423bd4f4af0c89f5cd4a9116905da27d2b5a6abc2c5e5151106035b02e90076',
    'd79be13627e92605f26ce76e6a6e3cf7943d9a2d161760662fcef47583dc8731',
  ]
  inputs_data = [
    {
      "address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
      "transaction_id": "2b0cef7b0abfefeb6c7c6b228930e6218e86e9d8c33f5525d10f34f91cc7bad4",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00430700",
    },
    {
      "address": "12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ",
      "transaction_id": "2b0cef7b0abfefeb6c7c6b228930e6218e86e9d8c33f5525d10f34f91cc7bad4",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00500000",
    },
  ]
  outputs_data = [
    {
      "address": "1LVenxwqnmvwjjBdyUByWsD7mXNmJJP2ZF",
      "bitcoin_amount": "0.00890500",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000002d4bac71cf9340fd125553fc3d8e9868e21e63089226b7c6cebefbf0a7bef0c2b000000008a47304402202c76a68f7eae79f50034a0a7b3b3dca729f03be1f17c445ad3762ec286a6055402202f8eabbb81a3adc8a6b70ca95dc7972489c6ed28e80be1d8775d00eaf37846640141042d09248cf80095d875561c83adc572f7bae3ff39832f9028b7abd792b4e439b2d522e9b461e8bbaf937c6165a1767b9a105268f013e424e6f7101b042d1dc5edffffffffd4bac71cf9340fd125553fc3d8e9868e21e63089226b7c6cebefbf0a7bef0c2b010000008a47304402205a092cff6c5776e555c4cdbfb8a2dcf696e34fab1202e6d542827b8721c75f56022032b83b3b93f384aaef84b3c0894b5f05917b886ef46f2df61fb5e0c91e62139c0141041489ca134cf898df4e58182cec872126b7a2e635c2db547bda3c27b2b1ea65d145b4563745bac943c8df62be7651a2ec700653c7ebf77d15f8aae48a6e33929fffffffff0184960d00000000001976a914d5d5959ba3035c57b81e9178a8a34e6e7d9580c888ac00000000
""".strip()
  txid_expected = 'b533842c4a338227be180a463eea63df6d85ef0bcc358e84000595980dcc0140'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 40200
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx10():
  # Input data:
  private_keys_hex = [
    'bdd04ba66229d390b565b3aec61ea7aef4863fac98b493d1c6c3e7c6e0d5e391',
  ]
  random_values_hex = [
    '4526f71a88ae5c4e74e930fb5d1988668c37a1f391d1ab37c09fff773b7ffcc6',
  ]
  inputs_data = [
    {
      "address": "1LVenxwqnmvwjjBdyUByWsD7mXNmJJP2ZF",
      "transaction_id": "b533842c4a338227be180a463eea63df6d85ef0bcc358e84000595980dcc0140",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00890500",
    },
  ]
  outputs_data = [
    {
      "address": "1NBXXLc7443x5KFw7k5jbnHBwM1CNGw6ka",
      "bitcoin_amount": "0.00868200",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
01000000014001cc0d98950500848e35cc0bef856ddf63ea3e460a18be2782334a2c8433b5000000008a473044022057fde87fd838bc87d7ebc3f03d379a9dd6e3fd9591e9de65e1403255be3289720220689084c9edba64d620ed8f5773f2ff18745fef3fcff0d609fb18efe375f6a2f40141040476cfff758b2f351a5a70b45b31ae19895ac07ff0ca33cfe5219e99e8ab2f7c6a168916787da0bae89b7a5200e3c1d0c0a6e4c2df82a816fb23862d2345611dffffffff01683f0d00000000001976a914e85847cbba0756cf4b881bd2fc114956fd51b00188ac00000000
""".strip()
  txid_expected = 'aad6d03ab13203ee7bdfb7e747c5aaef5a60f23c46b87e744176ad7955bd8bb6'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 22300
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx11():
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
  ]
  random_values_hex = [
    '9a1f6aec7c093dd63676f18520cab23c989a387a56ce870b1296510d0b11c7a8',
  ]
  inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "dcb76b885dd8130a5e926edde743b8cae969449213686313917eb4ccda6bf3cf",
      "previous_output_index": 0,
      "bitcoin_amount": "0.01000000",
    },
  ]
  outputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "bitcoin_amount": "0.00474300",
    },
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "bitcoin_amount": "0.00500000",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000001cff36bdaccb47e9113636813924469e9cab843e7dd6e925e0a13d85d886bb7dc000000008a47304402207da19140017b49a6bd5dad326d4fe21edc0337ef4d5d1415e6aba1e3419a703702204c6617b87383efc3bab4d3b082a350a72754ecd85c7ed6287923cb862615b88d0141045141d905ca3f3c688bd1fd9b2d91ffeb7c12082dcfe2674ccf0239d75b0456acdf5a53b153907a14712d1c6743a264488e7705c42229fe4d2365bfcd592ab254ffffffff02bc3c0700000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac20a10700000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac00000000
""".strip()
  txid_expected = '674232a1575e618e4755a17c7b0738f33a81fcb63d5db25d41016a3be18db900'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 25700
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx12():
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
  ]
  random_values_hex = [
    'f8a9a797547e67a8999227187f613b089338f79c6d7447bdaed76a706a52c92c',
    '4e2924ecd2302f5b702e93f7cba39082fae7ff2fd1619c3368abf70a9869cdcd',
  ]
  inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "674232a1575e618e4755a17c7b0738f33a81fcb63d5db25d41016a3be18db900",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00474300",
    },
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "674232a1575e618e4755a17c7b0738f33a81fcb63d5db25d41016a3be18db900",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00500000",
    },
  ]
  outputs_data = [
    {
      "address": "1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP",
      "bitcoin_amount": "0.00100000",
    },
    {
      "address": "1B9dT1kcvJqhmF9FpanKbY2vRvNiV6qR2L",
      "bitcoin_amount": "0.00200000",
    },
    {
      "address": "1LgQCG1DPBpk7Avdex5bSGqyKnxWv6spH2",
      "bitcoin_amount": "0.00664900",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
010000000200b98de13b6a01415db25d3db6fc813af338077b7ca155478e615e57a1324267000000008a47304402200bc088521aaba4aa839b34a6f04437a84d16966cdb24c81d72f8279858801bfc022038b0a19f7e65266b3fce2260d07d7d0707e4e2798e6fce7bbed6ddd25fa744f80141045141d905ca3f3c688bd1fd9b2d91ffeb7c12082dcfe2674ccf0239d75b0456acdf5a53b153907a14712d1c6743a264488e7705c42229fe4d2365bfcd592ab254ffffffff00b98de13b6a01415db25d3db6fc813af338077b7ca155478e615e57a1324267010000008b483045022100f879d59fb5e97db6fad01cbc585173801a89e2bc295e67b63e30930e84666137022055bfa081ff5db08bcc2f6dde3df486234f3864767d8af8d5b8c23718dc88750d0141045141d905ca3f3c688bd1fd9b2d91ffeb7c12082dcfe2674ccf0239d75b0456acdf5a53b153907a14712d1c6743a264488e7705c42229fe4d2365bfcd592ab254ffffffff03a0860100000000001976a914898dff254ca0f389679ce68b33ae0c46b992d9f088ac400d0300000000001976a9146f5302de794fa5b6331e7fe95e895ac8bc328ea888ac44250a00000000001976a914d7ddf94fcd3294570e091b84584b6175413b003888ac00000000
""".strip()
  txid_expected = '45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 9400
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx13():
  # Input data:
  private_keys_hex = [
    'ec30b469f5e9b16d565168fbf4c9a60050feab0349ac03ff7611a3a76f2bcd4a',
    '0f1691d20a6ee40f608b46404b9b42d44ee3599f51ebf48ea7439653044fa3f7',
    '9c75fc45b299cf2796809481228d8601dd895f55ffb15f64b583e05bfda3a368',
  ]
  random_values_hex = [
    'fbdfc5a68c8bcb354602ab06d8af7d78a016dc897726cc7499bb77e9be27f9d3',
    '8c5a5c0061ab79d0bb8b918dc521802a6452e861befb307e9a64bc2ed4f3f50e',
    '0b0f60a63f10ed97c95ab56eff70566edb593bbe366d70d50a74555d1030f4c6',
  ]
  inputs_data = [
    {
      "address": "1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00100000",
    },
    {
      "address": "1B9dT1kcvJqhmF9FpanKbY2vRvNiV6qR2L",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00200000",
    },
    {
      "address": "1LgQCG1DPBpk7Avdex5bSGqyKnxWv6spH2",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 2,
      "bitcoin_amount": "0.00664900",
    },
  ]
  outputs_data = [
    {
      "address": "1Fivx1V444aqjY85SxvzsEG5NjYdM6JWib",
      "bitcoin_amount": "0.00300000",
    },
    {
      "address": "1K1zwZscQNA1vsnNzKPdiDpkCmWo4EtWLD",
      "bitcoin_amount": "0.00300000",
    },
    {
      "address": "1ELjTCk6ESp8gydm2KgeyRgBamgrwppTTV",
      "bitcoin_amount": "0.00351920",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
010000000358d1959be4810e3b7850cdb42226383391b449ea2b7d68262834751cab9ea645000000008b48304502210090de75947fea4773c8e5ec2b5f61d6d3b43a8eed88d66e6b36c53dca06c0b6100220483d8fb1b2a5721bdbd35db36b059615cc374856551f56cbd96ac99043f873e7014104c9e9e0bb9a923e815fdef402b23d92fc751d498832fb5a0cbf349e4deba7d4f55d19020b8a7b84c6c8ea03c1635f6dc15be4163a9a914f017d79541a79b2fa8effffffff58d1959be4810e3b7850cdb42226383391b449ea2b7d68262834751cab9ea645010000008b483045022100a7954bb767cf8d86d4b5a6e8462f8aba8b639020ee492c77ad2667051b30793702203c0d7aeb54204bcf93c23b0d164ec642f95264bb810cabc518f1386b8015636f014104d05610a527029d91535c4c9e9861d9783ca5e7967b3cf61600a9b38cedfed0f2a8d2fe7f2e644652078a9a3da9a372323bb3b7530e0b38ec48b34b2924ffdc0effffffff58d1959be4810e3b7850cdb42226383391b449ea2b7d68262834751cab9ea645020000008a473044022040b1cc33f8d2e304dc8b345c5c65e29f871278ff694e201421a72ba3b130b54802207249a48acd592ae095efa911cc770e5ca8e4c69b81cc0c2fbeedd5325346b155014104e89d1048d763532481e7dc3ab86ace305c4114e9ce3dfc30f04bc7a4df97adaee3578197f5e1413f9a99dfc99e425344f7bee317762a680b61292e687c12f399ffffffff03e0930400000000001976a914a17fd96a5a6d76be05542f1a93a263bf02e3b9bc88ace0930400000000001976a914c5a2a172c3d16db0e2e064d182b4ee9fec533bf988acb05e0500000000001976a9149254f9b4af834fbea8773a6138d2d53e471fcfe188ac00000000
""".strip()
  txid_expected = '0a4b990b11185bfa8dfa2f29fe51a619abe89f8a3e527416a0cb40f5cdfc96ff'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 12980
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx14():
  # Input data:
  private_keys_hex = [
    'a99c96b4f983d3d0cee414480578f219995a7d8c7dea40a99d83402421a436f3',
    '2f6356a88c432f0149c877553eed29c1aba597dbf59515724f0e001f1adf1556',
    '153fa0dd919216f4a557d295fb1a8bc3c321ad1492daee35c9eb82227a2d5252',
  ]
  random_values_hex = [
    '63f7432e2224571acfdf233c2fb2523fb3e18108af9b2163b4ddbba7f1126af1',
    'ff458e6414471b906e864cd41b979b653a999d454fb89d2f737cc87cac18c9c0',
    '9c671cdf96db307eca3d9fd6dbe3b4dad38108058cff5efe99bbc3f538372db9',
  ]
  inputs_data = [
    {
      "address": "1Fivx1V444aqjY85SxvzsEG5NjYdM6JWib",
      "transaction_id": "0a4b990b11185bfa8dfa2f29fe51a619abe89f8a3e527416a0cb40f5cdfc96ff",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00300000",
    },
    {
      "address": "1K1zwZscQNA1vsnNzKPdiDpkCmWo4EtWLD",
      "transaction_id": "0a4b990b11185bfa8dfa2f29fe51a619abe89f8a3e527416a0cb40f5cdfc96ff",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00300000",
    },
    {
      "address": "1ELjTCk6ESp8gydm2KgeyRgBamgrwppTTV",
      "transaction_id": "0a4b990b11185bfa8dfa2f29fe51a619abe89f8a3e527416a0cb40f5cdfc96ff",
      "previous_output_index": 2,
      "bitcoin_amount": "0.00351920",
    },
  ]
  outputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "bitcoin_amount": "0.00300000",
    },
    {
      "address": "1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP",
      "bitcoin_amount": "0.00639620",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000003ff96fccdf540cba01674523e8a9fe8ab19a651fe292ffa8dfa5b18110b994b0a000000008b48304502210091c97b0f3195bad52438436f9a41745364f435171f89700a8744b1d120c63ddf022054ca2c65a57076d4563df23e31f7527290c8518c4671a2cd1e81082ad58c2e660141043b0ce517d5e3206e77f6c7f0c6a2ca264c09202cc34a7036adc391434dfad435eb0fdddb7637dae95c24131adfe2e95faa49365bf7eada7e2e25b09a21f5379effffffffff96fccdf540cba01674523e8a9fe8ab19a651fe292ffa8dfa5b18110b994b0a010000008a47304402206231487d016d507ec1373caad8404240737b17b08628ea7396bb230c3b7daf020220637e036bc290834962e284fc81e6176baa890c057f713c7884eef264f1dcfe82014104da0f0a2fb16d1c739e05e9d14a6dbc411bd6c31f3cec812e12d7402f6352cc3dee78882fc83a3bccf087c1224798eaa1fefa19c2150db09e860e290414885666ffffffffff96fccdf540cba01674523e8a9fe8ab19a651fe292ffa8dfa5b18110b994b0a020000008a47304402203311351244e4c4ecaa8cf006f664d7c1beacf6e5b249b9e37b4fe0a0255db97d02205324c9aeb394dd0323c227f523aad0b37c2d9f8110a8c29a45fd5566102628c50141046ca6bcf1a709667ce9c219df51d8cbb4f6c764a4deeac000613d68f62628739c2ac082421ea0bdf28379c58b3be25d4af6c1cd2216fb4061283d20a9de7f9368ffffffff02e0930400000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac84c20900000000001976a914898dff254ca0f389679ce68b33ae0c46b992d9f088ac00000000
""".strip()
  txid_expected = '10f92ae76b7df85ca3a3dc14e9445e68461fe2d2efad28c91000eb0ac6053411'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 12300
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx15():
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
    'ec30b469f5e9b16d565168fbf4c9a60050feab0349ac03ff7611a3a76f2bcd4a',
  ]
  random_values_hex = [
    '2fc30fed4b5e84fed20f4e43d1efc58b2a0970da22e0405690f477f8b9b6d46a','0d1df243ebf5b19ce72e40319a60992d43c96474315244975267d01cbaa060d4',
  ]
  inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "10f92ae76b7df85ca3a3dc14e9445e68461fe2d2efad28c91000eb0ac6053411",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00300000",
    },
    {
      "address": "1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP",
      "transaction_id": "10f92ae76b7df85ca3a3dc14e9445e68461fe2d2efad28c91000eb0ac6053411",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00639620",
    },
  ]
  outputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "bitcoin_amount": "0.00937208",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000002113405c60aeb0010c928adefd2e21f46685e44e914dca3a35cf87d6be72af910000000008b483045022100d7e042d154e661ba62b58454f04ac57b84c93d6df6984c4f814569d5e8d9f87f02203adf0a27a822a55096cb78a8e04ed021796121fddbba63b7686c1c5ebe0daff90141045141d905ca3f3c688bd1fd9b2d91ffeb7c12082dcfe2674ccf0239d75b0456acdf5a53b153907a14712d1c6743a264488e7705c42229fe4d2365bfcd592ab254ffffffff113405c60aeb0010c928adefd2e21f46685e44e914dca3a35cf87d6be72af910010000008a473044022005a57c24dd640ff2f547681872e3f766fd74ee3fa85473443c8a56861945be17022003fd9614906bdf83acfd6a99e8766810d15973398d4d53319c7dc5bf8af48223014104c9e9e0bb9a923e815fdef402b23d92fc751d498832fb5a0cbf349e4deba7d4f55d19020b8a7b84c6c8ea03c1635f6dc15be4163a9a914f017d79541a79b2fa8effffffff01f84c0e00000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac00000000
""".strip()
  txid_expected = '8f23fddd6176059649c4b12eb45d8062748f42dd6b6cab7067aae2cd56776f48'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 2412
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_tx16():
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
  ]
  random_values_hex = [
    '79d93d141305855969f57329fd34173c2546ad9be09f84f458c9d87bbf12b24c',
  ]
  inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "8f23fddd6176059649c4b12eb45d8062748f42dd6b6cab7067aae2cd56776f48",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00937208",
    },
  ]
  outputs_data = [
    {
      "address": "1NBXXLc7443x5KFw7k5jbnHBwM1CNGw6ka",
      "bitcoin_amount": "0.00935870",
    },
  ]
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000001486f7756cde2aa6770ab6c6bdd428f7462805db42eb1c44996057661ddfd238f000000008a4730440220550fa9bc55b09f93770c593f46724b4e604076df8e6be26a06fe240936a4580b0220213ab793d6d1d583aa8794d353b8739729bed96d7127bc08855de9516189c6d50141045141d905ca3f3c688bd1fd9b2d91ffeb7c12082dcfe2674ccf0239d75b0456acdf5a53b153907a14712d1c6743a264488e7705c42229fe4d2365bfcd592ab254ffffffff01be470e00000000001976a914e85847cbba0756cf4b881bd2fc114956fd51b00188ac00000000
""".strip()
  txid_expected = '0999dbd016073b440a190f9e919ae98fb4d6e5b46623d79323ffd6a58881c624'
  inputs, outputs = build_tx_inputs_and_outputs(inputs_data, outputs_data)
  tx_unsigned = transaction.Transaction.create(inputs, outputs)
  assert tx_unsigned.fee == 1338
  #print(tx_unsigned.to_json())
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected



