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






