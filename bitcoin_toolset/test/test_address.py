# Imports
import pytest




# Relative imports
from .. import code
from .. import util
from .. import submodules




# Shortcuts
ecdsa = submodules.ecdsa_python3
format_private_key_hex = ecdsa.format_private_key_hex
private_key_hex_to_address = code.basic.private_key_hex_to_address



# Notes
# Source for test addresses:
# http://edgecase.net/articles/bitcoin_address_test_set_2




# Setup for this file.
@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):
  # If log_level is supplied to pytest in the commandline args, then use it to set up the logging in the application code.
  log_level = pytestconfig.getoption('log_cli_level')
  if log_level is not None:
    log_level = log_level.lower()
    code.setup(log_level = log_level)
    submodules.setup(log_level = log_level)




def test_a1():
  private_key_bytes = b'hello_world'
  private_key_hex = private_key_bytes.hex()
  private_key_hex_2 = '00000000000000000000000000000000000000000068656c6c6f5f776f726c64'
  assert format_private_key_hex(private_key_hex) == private_key_hex_2
  x = private_key_hex_to_address(private_key_hex)
  assert x == '19VdGCFG8QH3CmYXjMXd3UQCK2HdC3UodP'




def test_a2():
  private_key_bytes = b'the_library_of_babel'
  private_key_hex = private_key_bytes.hex()
  private_key_hex_2 = '0000000000000000000000007468655f6c6962726172795f6f665f626162656c'
  assert format_private_key_hex(private_key_hex) == private_key_hex_2
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1CTumCMjzBfccCJBTkHoPQmAwEqU9Uj2sQ'




def test_a3():
  private_key_bytes = b'the_eye_of_argon'
  private_key_hex = private_key_bytes.hex()
  private_key_hex_2 = '000000000000000000000000000000007468655f6579655f6f665f6172676f6e'
  assert format_private_key_hex(private_key_hex) == private_key_hex_2
  x = private_key_hex_to_address(private_key_hex)
  assert x == '12RbVkKwHcwHbMZmnSVAyR4g88ZChpQD6f'




def test_a4():
  private_key_hex = 'b675ceedba0843d19934d1e0508cde736b4bb7f0a56b9585329ebcbfed559346'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1FJdRWN7tAd8rnivBm7yojppwvDmS7F55X'




def test_a5():
  private_key_bytes = b"the_mote_in_god's_eye"
  private_key_hex = private_key_bytes.hex()
  private_key_hex_2 = '00000000000000000000007468655f6d6f74655f696e5f676f6427735f657965'
  assert format_private_key_hex(private_key_hex) == private_key_hex_2
  x = private_key_hex_to_address(private_key_hex)
  assert x == '138obEZkdWaWEQ4x8ZAYw4MybHSZtX1Nam'




def test_a6():
  private_key_bytes = b"roadside_picnic"
  private_key_hex = private_key_bytes.hex()
  private_key_hex_2 = '0000000000000000000000000000000000726f6164736964655f7069636e6963'
  assert format_private_key_hex(private_key_hex) == private_key_hex_2
  x = private_key_hex_to_address(private_key_hex)
  assert x == '13xPBB175FtPbPQ84iB8KuawaVy3mHrady'




def test_a7():
  private_key_hex = 'a26e15954d2dafcee70eeaaa084eab8a4c1a30b0f71a42be4d8da20123bff121'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1AGygbyEFYduWkkmZbbvirgS9kuBBMLJCP'




def test_a8():
  private_key_hex = 'c592e1dad5e9871fdeffb551b4544b0a1cf0378c6371d7a397ff5faf04c934ca'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1vkb4YyPMFcxyC83Z5m5zuN45xASoHeNK'




def test_a9():
  private_key_hex = '1fbc45dc460d14c07bcac41b8e17649455e92d9bfda29a89ba3addeee0eccaaa'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '17rEGTR4ss7xhVVMwL969Y8xszS7FaFsae'




def test_a10():
  private_key_hex = '7972b641101c0ad67b0e401b800a9b6f3225c97fc6b8115042cf66968c2fb2e5'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '16ASCUS3s7D4UQh6J9oHGuT19agPvD3PFj'




def test_a11():
  private_key_hex = 'd45941cae4e31c824b041407053c9c15624e6234f9649bfd7d5bb5a93c53fe85'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1KHDLNmqBtiBELUsmTCkNASg79jfEVKrig'




def test_a12():
  private_key_hex = '1faf3c86105fe6ee328b29e94197de7e8500ddb8308385a9a8b0cba08d59ce27'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1DLg5i1kBjXYXy9f82xZcHokEMC9dtct7P'




def test_a13():
  private_key_hex = '7a0d11f6015f941ea486922e45310535c5b71c59d8489447648eebdb6a39e2a8'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '17pNyD9ur28aBgPhHtAFi6fAyrvgshp5yn'




def test_a14():
  private_key_hex = 'cbac84458fcfbb39f87fca7ab9a9ef2f76812a6f999a75dfa25dbcbb0ee3eb6f'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1PFw45xp5JUcLZfDQnMpto6yJpcjRLqrJ8'




def test_a15():
  private_key_hex = '7d37c1a74d3b87d3994ac6db65b4f298f64a8ed6144edfdb2cacea70cf3070af'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '19u4WSjpp19yoAK9kdRyY9HJ7ad2S8s1E4'




def test_a16():
  private_key_hex = '419292d169b515be1aec881018157f0a41883ea54da2b2405e10fd8a6abb76ec'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '17PZ6uyL59vPirNqqpMnB1kjEXkU7ske7s'




def test_a17():
  private_key_hex = 'dd23f217012efd9ac3dec71d0c2b42212a58bff75d9e97af900403cf5657bad3'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '15BLTZb6uQr24MrxqXJaPpRGz1tKrzq7iC'




def test_a18():
  private_key_hex = 'f6c8b60b49c35ef5e6e05e9b06aa5b2b28bd28fbfce696dfc2301347d494a22b'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1BB66Gx4833uKx8Lo2k8Mt4TRk42WTr7cZ'




def test_a19():
  private_key_hex = 'ecfb8057d4e053dda6849f6a361ca2d6797368651bbb2b52ce4691515a7909e1'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '12YCFdpsRDvEHNcj5rsmvJ5G2XXkW1icJP'




def test_a20():
  private_key_hex = 'fc8c7e92b44fe66f8f20d98a648f659da69461661673e22292a67dc20742ef17'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1H5SUR7Fv7x252WuJPqBjewwpeHuJ218Ky'




def test_a21():
  private_key_hex = 'f7def6819cf8efb7c4aeaddecb951688bcda37cee73b92f73a29be076e66579c'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '136oURWq1zjkdQHKcanE7TyA3o36ibARNM'




def test_a22():
  private_key_hex = '11717a85a51ba5cd1711905816a694bdd288d0639f27d8bb113ba94df9da1501'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '12PX5jPyQYejyrU79nZUDmKXvB3ttMfDqZ'




def test_a23():
  private_key_hex = 'bdd04ba66229d390b565b3aec61ea7aef4863fac98b493d1c6c3e7c6e0d5e391'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1LVenxwqnmvwjjBdyUByWsD7mXNmJJP2ZF'




def test_a24():
  private_key_hex = '1647a11df9b9785669d630fa90d6c8242a622a8fc077fb50fc4c52f8391c22ad'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1AppardGrpGdddB2HUTLRd2GGWaYAWDByX'




def test_a25():
  private_key_hex = 'ec30b469f5e9b16d565168fbf4c9a60050feab0349ac03ff7611a3a76f2bcd4a'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1DYKgP9cMG3wQhgowRJdrE4gRQvz6yMYEP'




def test_a26():
  private_key_hex = '0f1691d20a6ee40f608b46404b9b42d44ee3599f51ebf48ea7439653044fa3f7'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1B9dT1kcvJqhmF9FpanKbY2vRvNiV6qR2L'




def test_a27():
  private_key_hex = '9c75fc45b299cf2796809481228d8601dd895f55ffb15f64b583e05bfda3a368'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1LgQCG1DPBpk7Avdex5bSGqyKnxWv6spH2'




def test_a28():
  private_key_hex = 'a99c96b4f983d3d0cee414480578f219995a7d8c7dea40a99d83402421a436f3'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1Fivx1V444aqjY85SxvzsEG5NjYdM6JWib'




def test_a29():
  private_key_hex = '2f6356a88c432f0149c877553eed29c1aba597dbf59515724f0e001f1adf1556'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1K1zwZscQNA1vsnNzKPdiDpkCmWo4EtWLD'




def test_a30():
  private_key_hex = '153fa0dd919216f4a557d295fb1a8bc3c321ad1492daee35c9eb82227a2d5252'
  x = private_key_hex_to_address(private_key_hex)
  assert x == '1ELjTCk6ESp8gydm2KgeyRgBamgrwppTTV'



