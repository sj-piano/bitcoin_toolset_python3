# Imports
import os
import string
import re




# Notes:
# - We treat this module as foundational. It shouldn't import anything other than standard library modules.
# - Functions at the bottom are the most basic.
# -- Functions further up may use functions below them.
# - "validate" means "check that this data is in the expected format".






# ### SECTION
# Components.

# https://stackoverflow.com/a/45598540
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
hex_digits = '0123456789abcdef'






# ### SECTION
# Some more complex validation functions




def validate_list_contains_items(input, items):
  # input is a list. items is a list.
  validate_list(input)
  validate_list(items)
  not_found = []
  for x in items:
    if x not in input:
      not_found.append(x)
  if len(not_found) == 0:
    return True
  msg = "Some items are not in the list."
  msg += "\nList items:"
  for x in input:
    msg += "\n- %s" % str(x)
  msg += "\nItems not found:"
  for x in not_found:
    msg += "\n- %s" % str(x)
  raise ValueError(msg)




def validate_item_in_list(input, list1):
  validate_list(list1)
  if input in list1:
    return True
  msg = "Item not in list. Item: {}".format(input)
  msg += "\nList items:"
  for item in list1:
    msg += "\n- {}".format(item)
  raise ValueError(msg)




def validate_lists_are_identical(list1, list2):
  if sorted(list1) != sorted(list2):
    msg = '''
List are not identical.
- List 1:
{}
- List 2:
{}
'''
    msg = msg.format(list1, list2)
    raise ValueError(msg)




def validate_integer_domain(n, min_value, max_value):
  # n must be within [min_value, max_value].
  validate_integer(n)
  validate_integer(min_value)
  validate_integer(max_value)
  if min_value > max_value:
    msg = '''
Minimum value must be less than maximum value.
- Mininimum value: {}
- Maximum value: {}
'''.format(min_value, max_value)
    raise ValueError(msg)
  if (min_value <= n <= max_value):
    return
  elif n < min_value:
    msg = '''
Input is less than the minimum value.
- Minimum value: {}
- Input: {}
'''.format(min_value, n)
    raise ValueError(msg)
  elif n > max_value:
    msg = '''
Input is greater than the maximum value.
- Maximum value: {}
- Input: {}
'''.format(max_value, n)
    raise ValueError(msg)




def validate_string_is_printable_ascii(x, name=None, location=None, kind='string_is_printable_ascii'):
  # We want to be able to confirm that the data contains only printable ASCII characters.
  # http://edgecase.net/articles/printable_ascii
  data_characters = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
  escaped_characters = "\"" + "\\"
  whitespace_characters = " \t\n"
  permitted_data_characters = data_characters + escaped_characters + whitespace_characters
  validate_string(x)
  line = 0
  index = 0
  for c in x:
    index += 1
    if c not in permitted_data_characters:
      msg = "Line {}, index {}: Character '{}' (ord={}) is not in the list of permitted data characters."
      msg = msg.format(line, index, c, ord(c))
      msg = build_error_msg(msg, x, name, location, kind)
      raise ValueError(msg)
    if c == '\n':
      line += 1
      index = 0




def validate_string_is_whole_number_or_decimal(
    s, dp=None, name=None, location=None, kind='integer',
  ):
  # 's' only needs to pass one check out of the two.
  stored_exceptions = []
  success = 0
  try:
    validate_string_is_whole_number(s, name, location, kind)
    success = 1
  except Exception as e1:
    stored_exceptions.append(e1)
  try:
    validate_string_is_decimal(s, dp, name, location, kind)
    success = 1
  except Exception as e2:
    stored_exceptions.append(e2)
  if not success:
    e = stored_exceptions[0]
    raise e




def validate_string_is_decimal(
    s, dp=None, name=None, location=None, kind='integer',
    ):
  # dp = decimal places
  validate_string(s, name, location, kind)
  if s.count('.') != 1:
    msg = "which has {} decimal points, not 1.".format(s.count('.'))
    msg = build_error_msg(msg, s, name, location=location, kind=None)
    raise TypeError(msg)
  s1, s2 = s.split('.')
  if not s1.isdigit() or not s2.isdigit():
    msg = "which has non-digit characters."
    msg = build_error_msg(msg, s, name, location=location, kind=None)
    raise TypeError(msg)
  # Check if an exact number of decimal places has been specified.
  if isinstance(dp, int):
    regex = r'^\d*.\d{%d}$' % dp
    decimal_pattern = re.compile(regex)
    if not decimal_pattern.match(s):
      msg = 'which is not a valid {}-decimal-place decimal value.'.format(dp)
      msg = build_error_msg(msg, s, name, location, kind)
      raise ValueError(msg)


sd = validate_string_is_decimal










# ### SECTION
# Basic validation functions.




def validate_dict(x, name=None, location=None, kind='dict'):
  if not isinstance(x, dict):
    msg = "which has type '{}', not 'dict'.".format(type(x).__name__)
    msg = build_error_msg(msg, x, name, location, kind)
    raise TypeError(msg)




def validate_list(x, name=None, location=None, kind='list'):
  if not isinstance(x, list):
    msg = "which has type '{}', not 'list'.".format(type(x).__name__)
    msg = build_error_msg(msg, x, name, location, kind)
    raise TypeError(msg)




def validate_bytes(b, name=None, location=None, kind='bytes'):
  if not isinstance(b, bytes):
    msg = "which has type '{}', not 'int'.".format(type(b).__name__)
    msg = build_error_msg(msg, b, name, location, kind)
    raise TypeError(msg)




def validate_whole_number(n, name=None, location=None, kind='whole_number'):
  # 0 is a whole number.
  if n == 0:
    return
  validate_positive_integer(n, name, location, kind)


wn = validate_whole_number




def validate_positive_integer(n, name=None, location=None, kind='positive_integer'):
  validate_integer(n, name, location, kind)
  if n < 1:
    msg = "which is less than 1."
    msg = build_error_msg(msg, n, name, location, kind)
    raise ValueError(msg)


pi = validate_positive_integer




def validate_integer(n, name=None, location=None, kind='integer'):
  if not isinstance(n, int):
    msg = "which has type '{}', not 'int'.".format(type(n).__name__)
    msg = build_error_msg(msg, n, name, location, kind)
    raise TypeError(msg)


i = validate_integer




def validate_boolean(b, name=None, location=None, kind='boolean'):
  if type(b) != bool:
    msg = "which has type '{}', not 'bool'.".format(type(b).__name__)
    msg = build_error_msg(msg, b, name, location, kind)
    raise TypeError(msg)


b = validate_boolean




def validate_hex_length(s, n, name=None, location=None, kind=None):
  if kind is None:
    kind = 'hex_length_{}_bytes'.format(n)
  validate_hex(s, name, location, kind)
  if not isinstance(n, int):
    msg = "which has type '{}', not 'int'.".format(type(n).__name__)
    name2 = 'n (i.e. the hex length)'
    msg = build_error_msg(msg, n, name=name2, location=location, kind=None)
    raise TypeError(msg)
  # 1 byte is 2 hex chars.
  if len(s) != n * 2:
    msg = "whose length is {} chars, not {} chars.".format(len(s), n * 2)
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


def validate_hex(s, name=None, location=None, kind='hex'):
  validate_string(s, name, location, kind)
  # find indices of non-hex characters in the string.
  indices = [i for i in range(len(s)) if s[i] not in hex_digits]
  if len(indices) > 0:
    non_hex_chars = [s[i] for i in indices]
    msg = "where the chars at indices {} (with values {}) are not hex chars.".format(indices, ','.join(non_hex_chars))
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)




def validate_string_is_whole_number(
    s, name=None, location=None, kind='string_is_whole_number',
    ):
  # 0 is a whole number.
  validate_string(s, name, location, kind)
  if s == '0':
    return
  validate_string_is_positive_integer(s, name, location, kind)


swn = validate_string_is_whole_number




def validate_string_is_positive_integer(
    s, name=None, location=None, kind='string_is_positive_integer',
    ):
  validate_string(s, name, location, kind)
  if s == '0':
    raise ValueError('0 is not a positive number.')
  # find indices of non-digit characters in the string.
  indices = [i for i in range(len(s)) if not s[i].isdigit()]
  if len(indices) > 0:
    non_digit_chars = [s[i] for i in indices]
    msg = "where the chars at indices {} (with values {}) are not digits.".format(indices, ','.join(non_digit_chars))
    msg = build_error_msg(msg, s, name, non_digit_chars, kind)
    raise ValueError(msg)


spi = validate_string_is_positive_integer




def validate_string_is_date(s, name=None, location=None, kind='string_is_date'):
  validate_string(s, name, location, kind)
  if not date_pattern.match(s):
    msg = 'which is not a valid YYYY-MM-DD date string.'
    msg = build_error_msg(msg, s, name, location, kind)
    raise ValueError(msg)


sdate = validate_string_is_date




def validate_string(s, name=None, location=None, kind='string'):
  if not isinstance(s, str):
    msg = "which has type '{}', not 'str'.".format(type(s).__name__)
    msg = build_error_msg(msg, s, name, location, kind)
    raise TypeError(msg)


s = validate_string




def build_error_msg(msg, value, name=None, location=None, kind=None):
  # Build out an expanded error message with useful detail.
  m = ''
  if location is not None:
    m += "in location {}, ".format(repr(location))
  if name is not None:
    # This is a complicated way of putting single quotes around _only_ the first word in the name.
    # This means that a description can be added after the name.
    words = name.split(' ')
    name2 = "'{}'".format(words[0])
    if len(words) > 1:
      name2 += ' ' + ' '.join(words[1:])
    m += "for variable {}, ".format(name2)
  if kind is not None:
    m += "expected a {}, but ".format(repr(kind))
  m += "received value {}".format(repr(value))
  if msg != '':
    m += ', ' + msg
  m = m[0].capitalize() + m[1:]
  return m



