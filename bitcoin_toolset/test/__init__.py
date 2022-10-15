# This file is needed so that Pytest will work.
# If it is not present, we will get
# SystemError: Parent module '' not loaded, cannot perform relative import
# caused by relative import lines in test modules e.g.
# from .. import code
# in test_hello.py

