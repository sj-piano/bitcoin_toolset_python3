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
create_transaction = code.create_transaction




# Error shortcuts
OutputValueNotCovered = create_transaction.OutputValueNotCovered
OutputAndFeeValueNotCovered = create_transaction.OutputAndFeeValueNotCovered
DuplicateOutputAddressError = create_transaction.DuplicateOutputAddressError




# Notes
# - Most transactions here are taken directly from test_transaction.py, although some values have been altered.




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




def test_output_shortfall():
  # Situation:
  # - Input value does not cover output value.
  # Input data:
  private_keys_hex = [
    'ecfb8057d4e053dda6849f6a361ca2d6797368651bbb2b52ce4691515a7909e1',
    'fc8c7e92b44fe66f8f20d98a648f659da69461661673e22292a67dc20742ef17',
  ]
  available_inputs_data = [
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
  design = {
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "fee": 225,
    "max_fee": 250,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ",
        "bitcoin_amount": "0.00974301",
      },
    ]
  }
  a = Namespace(
    inputs = available_inputs_data,
    design = design
  )
  with pytest.raises(OutputValueNotCovered):
    tx_unsigned = code.create_transaction.create_transaction(a)




def test_fee_shortfall():
  # Situation:
  # - Input value covers output value but not the fee.
  # Input data:
  private_keys_hex = [
    'ecfb8057d4e053dda6849f6a361ca2d6797368651bbb2b52ce4691515a7909e1',
    'fc8c7e92b44fe66f8f20d98a648f659da69461661673e22292a67dc20742ef17',
  ]
  available_inputs_data = [
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
  design = {
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "fee": 225,
    "max_fee": 250,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ",
        "bitcoin_amount": "0.00974300",
      },
    ]
  }
  a = Namespace(
    inputs = available_inputs_data,
    design = design
  )
  #tx_unsigned = code.create_transaction.create_transaction(a)
  with pytest.raises(OutputAndFeeValueNotCovered):
    tx_unsigned = code.create_transaction.create_transaction(a)




def test_add_input_to_pay_fee():
  # Situation:
  # - We've added enough inputs from the available list to send the specified amounts to the output addresses.
  # - However, the change is too small to pay the specified fee.
  # - So: The create_transaction function should add another input, using the input selection approach.
  # Note that the designed output value exactly equals the first input value. So, in order to pay the fee, the second input must be added to the transaction.
  # Input data:
  private_keys_hex = [
    'ecfb8057d4e053dda6849f6a361ca2d6797368651bbb2b52ce4691515a7909e1',
    'fc8c7e92b44fe66f8f20d98a648f659da69461661673e22292a67dc20742ef17',
  ]
  available_inputs_data = [
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
  design = {
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "fee": 225,
    "max_fee": 250,
    "max_spend_percentage": "100.00",
    "input_selection_approach": ["smallest_first"],
    "outputs": [
      {
        "address": "12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ",
        "bitcoin_amount": "0.00474300",
      },
    ]
  }
  tx_unsigned_expected = {
    "version": "01000000",
    "input_count": "02",
    "inputs": [
      {
        "previous_output_hash": "ea1b9db39c6fd5df377e381a896ddb47da4c3c23faf80fe2da9b13014c055f58",
        "previous_output_index": "00000000",
        "previous_output_index_int": 0,
        "script_length": null,
        "script_length_int": null,
        "script_sig": null,
        "sequence": "ffffffff",
        "public_key_hex": null,
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a91410de69df99d4b834ee6f2bd1466edab556beb7d688ac",
        "address": "12YCFdpsRDvEHNcj5rsmvJ5G2XXkW1icJP",
        "txid": "585f054c01139bdae20ff8fa233c4cda47db6d891a387e37dfd56f9cb39d1bea",
        "satoshi_amount": 474300,
        "bitcoin_amount": "0.00474300"
      },
      {
        "previous_output_hash": "ea1b9db39c6fd5df377e381a896ddb47da4c3c23faf80fe2da9b13014c055f58",
        "previous_output_index": "01000000",
        "previous_output_index_int": 1,
        "script_length": null,
        "script_length_int": null,
        "script_sig": null,
        "sequence": "ffffffff",
        "public_key_hex": null,
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a914b058f09e25382dd3b9339c25a5727085a22c8c6088ac",
        "address": "1H5SUR7Fv7x252WuJPqBjewwpeHuJ218Ky",
        "txid": "585f054c01139bdae20ff8fa233c4cda47db6d891a387e37dfd56f9cb39d1bea",
        "satoshi_amount": 500000,
        "bitcoin_amount": "0.00500000"
      }
    ],
    "output_count": "02",
    "outputs": [
      {
        "value": "3fa0070000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a91417091ffac2b6bb51d9fd1d979fac6ec6bf3a2f1e88ac",
        "address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
        "bitcoin_amount": "0.00499775",
        "satoshi_amount": 499775
      },
      {
        "value": "bc3c070000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a9140f3a634504545b37a97b10214b2f640fb16085e588ac",
        "address": "12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ",
        "bitcoin_amount": "0.00474300",
        "satoshi_amount": 474300
      }
    ],
    "block_lock_time": "00000000",
    "hash_type_4_byte": "01000000",
    "hash_type_1_byte": "01",
    "signed": false,
    "total_input": {
      "satoshi_amount": 974300,
      "bitcoin_amount": "0.00974300"
    },
    "total_output": {
      "satoshi_amount": 974075,
      "bitcoin_amount": "0.00974075"
    },
    "fee": {
      "satoshi_amount": 225,
      "bitcoin_amount": "0.00000225"
    },
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "change": {
      "satoshi_amount": 499775,
      "bitcoin_amount": "0.00499775"
    },
    "estimated_size_bytes": 436,
    "estimated_fee_rate": {
      "satoshi_per_byte": "0.5161",
      "bitcoin_per_byte": "0.00000001"
    },
    "size_bytes": null,
    "fee_rate": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  }
  tx_signed_expected = {}
  tx_signed_hex_expected = """
""".strip()
  a = Namespace(
    inputs = available_inputs_data,
    design = design
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 225
  assert len(tx_unsigned.inputs) == 2
  assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")




def test_add_input_to_pay_fee_2():
  # Situation:
  # - The first input covers the output.
  # - We add a second input to pay the fee. A change output is created to receive the change.
  # - The third available input is not used.
  # Input data:
  private_keys_hex = [
    'ec30b469f5e9b16d565168fbf4c9a60050feab0349ac03ff7611a3a76f2bcd4a',
    '0f1691d20a6ee40f608b46404b9b42d44ee3599f51ebf48ea7439653044fa3f7',
    '9c75fc45b299cf2796809481228d8601dd895f55ffb15f64b583e05bfda3a368',
  ]
  available_inputs_data = [
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
  design = {
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "fee": 225,
    "max_fee": 250,
    "max_spend_percentage": "100.00",
    "input_selection_approach": ["smallest_first"],
    "outputs": [
      {
        "address": "1Fivx1V444aqjY85SxvzsEG5NjYdM6JWib",
        "bitcoin_amount": "0.00100000",
      },
    ]
  }
  tx_unsigned_expected = {
    "version": "01000000",
    "input_count": "02",
    "inputs": [
      {
        "previous_output_hash": "58d1959be4810e3b7850cdb42226383391b449ea2b7d68262834751cab9ea645",
        "previous_output_index": "00000000",
        "previous_output_index_int": 0,
        "script_length": null,
        "script_length_int": null,
        "script_sig": null,
        "sequence": "ffffffff",
        "public_key_hex": null,
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a914898dff254ca0f389679ce68b33ae0c46b992d9f088ac",
        "address": "1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP",
        "txid": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
        "satoshi_amount": 100000,
        "bitcoin_amount": "0.00100000"
      },
      {
        "previous_output_hash": "58d1959be4810e3b7850cdb42226383391b449ea2b7d68262834751cab9ea645",
        "previous_output_index": "01000000",
        "previous_output_index_int": 1,
        "script_length": null,
        "script_length_int": null,
        "script_sig": null,
        "sequence": "ffffffff",
        "public_key_hex": null,
        "script_pub_key_length": "19",
        "script_pub_key_length_int": 25,
        "script_pub_key": "76a9146f5302de794fa5b6331e7fe95e895ac8bc328ea888ac",
        "address": "1B9dT1kcvJqhmF9FpanKbY2vRvNiV6qR2L",
        "txid": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
        "satoshi_amount": 200000,
        "bitcoin_amount": "0.00200000"
      }
    ],
    "output_count": "02",
    "outputs": [
      {
        "value": "5f0c030000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a91417091ffac2b6bb51d9fd1d979fac6ec6bf3a2f1e88ac",
        "address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
        "bitcoin_amount": "0.00199775",
        "satoshi_amount": 199775
      },
      {
        "value": "a086010000000000",
        "script_length": "19",
        "script_length_int": 25,
        "script_pub_key": "76a914a17fd96a5a6d76be05542f1a93a263bf02e3b9bc88ac",
        "address": "1Fivx1V444aqjY85SxvzsEG5NjYdM6JWib",
        "bitcoin_amount": "0.00100000",
        "satoshi_amount": 100000
      }
    ],
    "block_lock_time": "00000000",
    "hash_type_4_byte": "01000000",
    "hash_type_1_byte": "01",
    "signed": false,
    "total_input": {
      "satoshi_amount": 300000,
      "bitcoin_amount": "0.00300000"
    },
    "total_output": {
      "satoshi_amount": 299775,
      "bitcoin_amount": "0.00299775"
    },
    "fee": {
      "satoshi_amount": 225,
      "bitcoin_amount": "0.00000225"
    },
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "change": {
      "satoshi_amount": 199775,
      "bitcoin_amount": "0.00199775"
    },
    "estimated_size_bytes": 436,
    "estimated_fee_rate": {
      "satoshi_per_byte": "0.5161",
      "bitcoin_per_byte": "0.00000001"
    },
    "size_bytes": null,
    "fee_rate": {
      "satoshi_amount": null,
      "bitcoin_amount": null
    }
  }
  tx_signed_expected = {}
  tx_signed_hex_expected = """
""".strip()
  a = Namespace(
    inputs = available_inputs_data,
    design = design
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 225
  assert len(tx_unsigned.inputs) == 2
  assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex)
  #print(tx_signed.to_json())
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")




def test_fee_rate_argument():
  # Build tx2 using fee_rate.
  # Input data:
  private_keys_hex = [
    '00000000000000000000007468655f6d6f74655f696e5f676f6427735f657965'
  ]
  random_values_hex = [
    '00000000005468652046616365206f6620476f64206468636d726c636874646a'
  ]
  available_inputs_data = [
    {
      "address": "138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam",
      "transaction_id": "e4609e0f1ca854b8b07381f32ba31adbad9713205f5a4f3f56a5a32853d47855",
      "previous_output_index": 8,
      "bitcoin_amount": "0.0024200"
    },
  ]
  design = {
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
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
01000000015578d45328a3a5563f4f5a5f201397addb1aa32bf38173b0b854a81c0f9e60e4080000008a473044022017ece35581a034a4838a577fe438f108cf22764927a1ad197ed379460c0764cd022066723723eff05c10bac9a2f63b3e782e24fde290701c9408f3d1054722adad360141041ad06846fd7cf9998a827485d8dd5aaba9eccc385ba7759a6e9055fbdf90d7513c0d11fe5e5dcfcf8d4946c67f6c45f8e7f7d7a9c254ca8ebde1ffd64ab9dd58ffffffff0171b00300000000001976a9142069a3fae01db74cef12d1d01811afdf6a3e1c2e88ac00000000
""".strip()
  txid_expected = '745e224ccba0a033c55ea80523f207da18b903418ac1f5d293eed62c19e0334d'
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 223
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #return
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_fee_rate_argument_2():
  # Build tx11 using fee_rate.
  # - This also tests the allow_duplicate_output_address option.
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
  ]
  random_values_hex = [
    '9a1f6aec7c093dd63676f18520cab23c989a387a56ce870b1296510d0b11c7a8',
  ]
  available_inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "dcb76b885dd8130a5e926edde743b8cae969449213686313917eb4ccda6bf3cf",
      "previous_output_index": 0,
      "bitcoin_amount": "0.01000000",
    },
  ]
  design = {
    "change_address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
    "fee_rate": 100,
    "max_fee": 30000,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00474300",
      },
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00500000",
      },
    ]
  }
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000001cff36bdaccb47e9113636813924469e9cab843e7dd6e925e0a13d85d886bb7dc000000008a47304402207da19140017b49a6bd5dad326d4fe21edc0337ef4d5d1415e6aba1e3419a703702204c6617b87383efc3bab4d3b082a350a72754ecd85c7ed6287923cb862615b88d0141045141d905ca3f3c688bd1fd9b2d91ffeb7c12082dcfe2674ccf0239d75b0456acdf5a53b153907a14712d1c6743a264488e7705c42229fe4d2365bfcd592ab254ffffffff02bc3c0700000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac20a10700000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac00000000
""".strip()
  txid_expected = '674232a1575e618e4755a17c7b0738f33a81fcb63d5db25d41016a3be18db900'
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
    allow_duplicate_output_address = True,
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 25700
  #assert tx_unsigned.to_dict() == tx_unsigned_expected
  tx_signed = tx_unsigned.sign(private_keys_hex, random_values_hex)
  #print(tx_signed.to_json())
  #return
  #assert tx_signed.to_dict() == tx_signed_expected
  valid_signatures = tx_signed.verify()
  if not valid_signatures:
    raise ValueError("Invalid signature(s)!")
  tx_signed_hex = tx_signed.to_hex_signed_form()
  #print(tx_signed_hex)
  assert tx_signed_hex == tx_signed_hex_expected
  txid = tx_signed.calculate_txid()
  assert txid == txid_expected




def test_fee_rate_argument_3():
  # Build tx3 using fee_rate.
  # Input data:
  private_keys_hex = [
    '7972b641101c0ad67b0e401b800a9b6f3225c97fc6b8115042cf66968c2fb2e5'
  ]
  random_values_hex = [
    '257c2ff4ac1606d5e42fe152c2624cffac2aa58cdfe8578a69b12beefbce68b9'
  ]
  available_inputs_data = [
    {
      "address": "16ASCUS3s7D4UQh6J9oHGuT19agPvD3PFj",
      "transaction_id": "f02eca2852bf73f3c722db2d151e7755d853efd8dd6224249b14f8b51dffbc6e",
      "previous_output_index": 12,
      "bitcoin_amount": "0.00600000"
    }
  ]
  design = {
    "change_address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
    "fee_rate": "3.01167",
    "max_fee": 1000,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "1KHDLNmqBtiBELUsmTCkNASg79jfEVKrig",
        "bitcoin_amount": "0.00300000"
      },
      {
        "address": "1DLg5i1kBjXYXy9f82xZcHokEMC9dtct7P",
        "bitcoin_amount": "0.00299226"
      }
    ]
  }
  tx_signed_hex_expected = """
01000000016ebcff1db5f8149b242462ddd8ef53d855771e152ddb22c7f373bf5228ca2ef00c0000008a47304402202d8617427fc589848ef2e0481d148e0ce5d60aaa26e466fdfe62890d0d67ca6902200df89728ea73816cecfdfd6a734ca8b70da7000e213b87dcfdc9d48400164fac014104108e1c01a42bbd09b77a26b5f732f10d7108b2fe31cba137e9d15e24c7c30d2515904dfe646f3e94a3aa482afbbe0dc178b9b212154529768e0ba74452df1c2affffffff02e0930400000000001976a914c8833727be832b6634d8ddf7bfcf51e379b28f6388acda900400000000001976a914875a093668adff783d0835f4db655c5a47a0ceaa88ac00000000
""".strip()
  txid_expected = 'db2c3d84708cd9d0e40ae1754021f9146a0d6ab555fc0e1d547d7876c0c092f4'
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
    allow_duplicate_output_address = True,
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 774
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




def test_fee_rate_argument_4():
  # Build tx8 using fee_rate.
  # Input data:
  private_keys_hex = [
    'ecfb8057d4e053dda6849f6a361ca2d6797368651bbb2b52ce4691515a7909e1',
    'fc8c7e92b44fe66f8f20d98a648f659da69461661673e22292a67dc20742ef17',
  ]
  random_values_hex = [
    '0a5a9cc087cf3337bfb0fa12f6fa036d17d6b6dc0e93dfa657c8caca47ad8155',
    '2493ac84058e4f4b79f1bd267c45f52bc7545ef01dd66b8bf077cae86460e954',
  ]
  available_inputs_data = [
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
  design = {
    "change_address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
    "fee_rate": "100",
    "max_fee": 50000,
    "max_spend_percentage": "100.00",
    "input_selection_approach": ["smallest_first"],
    "outputs": [
      {
        "address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
        "bitcoin_amount": "0.00430700",
      },
      {
        "address": "12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ",
        "bitcoin_amount": "0.00500000",
      },
    ]
  }
  tx_signed_hex_expected = """
0100000002ea1b9db39c6fd5df377e381a896ddb47da4c3c23faf80fe2da9b13014c055f58000000008b483045022100d75efc99b640bcc09f569b1b53cb33d407720f9931a719d0ae3212182927cbb802205ea59d7e86f3bdcf7ec5b483a181704909e401cdeb3f8c60172d72aa842ec142014104e5f0aa4e9ee32cc982db529c981f18171cd9d1ccf224a94e4b3c09b51fd3752c6ebf66f0861dc435fee962f995ab9c5346d32332a409c598eb575cec74115180ffffffffea1b9db39c6fd5df377e381a896ddb47da4c3c23faf80fe2da9b13014c055f58010000008b483045022100c70dbea33b9a7d51a9f952a63d65f0572194af68774c09e03d347f65cddd38c3022072e8341e85f5cb6c49be050c862837d451f46a6f5d0f51fa80993a45983cf9d6014104cca91b1ad65fc428789b469f0e030fb2de58132c61f3240f416e3a6eb1963009a359770805e71e9b7c7982da51c2a3209ec908efe71cf5ec8b65f5b9eb05115bffffffff026c920600000000001976a91417091ffac2b6bb51d9fd1d979fac6ec6bf3a2f1e88ac20a10700000000001976a9140f3a634504545b37a97b10214b2f640fb16085e588ac00000000
""".strip()
  txid_expected = '2b0cef7b0abfefeb6c7c6b228930e6218e86e9d8c33f5525d10f34f91cc7bad4'
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
    allow_duplicate_output_address = True,
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 43600
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




def test_change_output_index():
  # I constructed a transaction (Transaction 11 / tx11) that sends two outputs to the same address, which is also the change address.
  # This is strange but permitted by the protocol.
  # We test here that, in this event, we can specify the output to which to send any change.
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
  ]
  random_values_hex = [
    '9a1f6aec7c093dd63676f18520cab23c989a387a56ce870b1296510d0b11c7a8',
  ]
  available_inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "dcb76b885dd8130a5e926edde743b8cae969449213686313917eb4ccda6bf3cf",
      "previous_output_index": 0,
      "bitcoin_amount": "0.01000000",
    },
  ]
  design = {
    "change_address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
    "fee_rate": 100,
    "max_fee": 30000,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00174300",
      },
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00500000",
      },
    ]
  }
  tx_unsigned_expected = {}
  tx_signed_expected = {}
  tx_signed_hex_expected = """
0100000001cff36bdaccb47e9113636813924469e9cab843e7dd6e925e0a13d85d886bb7dc000000008a47304402207da19140017b49a6bd5dad326d4fe21edc0337ef4d5d1415e6aba1e3419a703702204c6617b87383efc3bab4d3b082a350a72754ecd85c7ed6287923cb862615b88d0141045141d905ca3f3c688bd1fd9b2d91ffeb7c12082dcfe2674ccf0239d75b0456acdf5a53b153907a14712d1c6743a264488e7705c42229fe4d2365bfcd592ab254ffffffff02bc3c0700000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac20a10700000000001976a9146bc4673483dfe54e2cc83fed2f235cf8102e643d88ac00000000
""".strip()
  txid_expected = '674232a1575e618e4755a17c7b0738f33a81fcb63d5db25d41016a3be18db900'
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
    allow_duplicate_output_address = True,
    change_output_index = 0,
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 25700
  assert tx_unsigned.outputs[0].satoshi_amount == 474300
  assert tx_unsigned.outputs[1].satoshi_amount == 500000
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




def test_duplicate_output_address_error():
  # Confirm that by default an error occurs if multiple outputs send to the same address.
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
  ]
  random_values_hex = [
    '9a1f6aec7c093dd63676f18520cab23c989a387a56ce870b1296510d0b11c7a8',
  ]
  available_inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "dcb76b885dd8130a5e926edde743b8cae969449213686313917eb4ccda6bf3cf",
      "previous_output_index": 0,
      "bitcoin_amount": "0.01000000",
    },
  ]
  design = {
    "change_address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
    "fee_rate": 100,
    "max_fee": 30000,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00174300",
      },
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00500000",
      },
    ]
  }
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
  )
  with pytest.raises(DuplicateOutputAddressError):
    tx_unsigned = code.create_transaction.create_transaction(a)




def test_duplicate_change_output_address_error():
  # Confirm that, even if duplicate output addresses are permitted, an error occurs by default if multiple outputs send to the change address.
  # Input data:
  private_keys_hex = [
    '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad',
  ]
  random_values_hex = [
    '9a1f6aec7c093dd63676f18520cab23c989a387a56ce870b1296510d0b11c7a8',
  ]
  available_inputs_data = [
    {
      "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
      "transaction_id": "dcb76b885dd8130a5e926edde743b8cae969449213686313917eb4ccda6bf3cf",
      "previous_output_index": 0,
      "bitcoin_amount": "0.01000000",
    },
  ]
  design = {
    "change_address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
    "fee_rate": 100,
    "max_fee": 30000,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00174300",
      },
      {
        "address": "1AppardGrpGdddB2HUTLRd2GGWaYAWDByX",
        "bitcoin_amount": "0.00500000",
      },
    ]
  }
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
    allow_duplicate_output_address = True,
  )
  with pytest.raises(ValueError):
    tx_unsigned = code.create_transaction.create_transaction(a)




def test_add_input_selection_approach():
  # We test that within the transaction the inputs are sorted according to the default input_selection_approach: 'largest_first'
  # Input data:
  private_keys_hex = [
    'ec30b469f5e9b16d565168fbf4c9a60050feab0349ac03ff7611a3a76f2bcd4a',
    '0f1691d20a6ee40f608b46404b9b42d44ee3599f51ebf48ea7439653044fa3f7',
    '9c75fc45b299cf2796809481228d8601dd895f55ffb15f64b583e05bfda3a368',
  ]
  available_inputs_data = [
    {
      "address": "1B9dT1kcvJqhmF9FpanKbY2vRvNiV6qR2L",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00200000",
    },
    {
      "address": "1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00100000",
    },
    {
      "address": "1LgQCG1DPBpk7Avdex5bSGqyKnxWv6spH2",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 2,
      "bitcoin_amount": "0.00500225",
    },
  ]
  design = {
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "fee": 225,
    "max_fee": 250,
    "max_spend_percentage": "100.00",
    "outputs": [
      {
        "address": "1Fivx1V444aqjY85SxvzsEG5NjYdM6JWib",
        "bitcoin_amount": "0.00800000",
      },
    ]
  }
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 225
  assert tx_unsigned.inputs[0].bitcoin_amount == "0.00500225"
  assert tx_unsigned.inputs[1].bitcoin_amount == "0.00200000"
  assert tx_unsigned.inputs[2].bitcoin_amount == "0.00100000"




def test_add_input_selection_approach_2():
  # We test that within the transaction the inputs are sorted according to the input_selection_approach: 'smallest_first'
  # Input data:
  private_keys_hex = [
    'ec30b469f5e9b16d565168fbf4c9a60050feab0349ac03ff7611a3a76f2bcd4a',
    '0f1691d20a6ee40f608b46404b9b42d44ee3599f51ebf48ea7439653044fa3f7',
    '9c75fc45b299cf2796809481228d8601dd895f55ffb15f64b583e05bfda3a368',
  ]
  available_inputs_data = [
    {
      "address": "1B9dT1kcvJqhmF9FpanKbY2vRvNiV6qR2L",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 1,
      "bitcoin_amount": "0.00200000",
    },
    {
      "address": "1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 0,
      "bitcoin_amount": "0.00100000",
    },
    {
      "address": "1LgQCG1DPBpk7Avdex5bSGqyKnxWv6spH2",
      "transaction_id": "45a69eab1c75342826687d2bea49b49133382622b4cd50783b0e81e49b95d158",
      "previous_output_index": 2,
      "bitcoin_amount": "0.00500225",
    },
  ]
  design = {
    "change_address": "136oURWq1zjkdQHKcanE7TyA3o36ibARNM",
    "fee": 225,
    "max_fee": 250,
    "max_spend_percentage": "100.00",
    "input_selection_approach": ["smallest_first"],
    "outputs": [
      {
        "address": "1Fivx1V444aqjY85SxvzsEG5NjYdM6JWib",
        "bitcoin_amount": "0.00800000",
      },
    ]
  }
  a = Namespace(
    inputs = available_inputs_data,
    design = design,
  )
  tx_unsigned = code.create_transaction.create_transaction(a)
  #print(tx_unsigned.to_json())
  assert tx_unsigned.fee == 225
  assert tx_unsigned.inputs[0].bitcoin_amount == "0.00100000"
  assert tx_unsigned.inputs[1].bitcoin_amount == "0.00200000"
  assert tx_unsigned.inputs[2].bitcoin_amount == "0.00500225"



