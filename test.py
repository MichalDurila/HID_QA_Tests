# -*- coding: utf-8 -*-
"""Package contains a test suite with test cases, which test the library hash.dll.
It is written for Windows operating system and requires 32-bit version of Python,
e.g. Python 3.13.0 32-bit (https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe).
All necessary libraries are already preinstalled within Python.
"""

import os
import ctypes

HASH_ERROR_OK = 0
HASH_ERROR_GENERAL = 1
HASH_ERROR_EXCEPTION = 2
HASH_ERROR_MEMORY = 3
HASH_ERROR_LOG_EMPTY = 4
HASH_ERROR_ARGUMENT_INVALID = 5
HASH_ERROR_ARGUMENT_NULL = 6
HASH_ERROR_NOT_INITIALIZED = 7
HASH_ERROR_ALREADY_INITIALIZED = 8

dll = ctypes.CDLL(os.path.join("HID_QA_Homework", "bin", "windows", "hash.dll"))

dll.HashInit.restype = ctypes.c_uint32

dll.HashTerminate.restype = ctypes.c_uint32

# Test the HashInit method
result = dll.HashInit()
assert HASH_ERROR_OK == result, "HashInit initialization"

result2 = dll.HashInit()
assert HASH_ERROR_ALREADY_INITIALIZED == result2, "HashInit second initialization"

dll.HashTerminate()
result3 = dll.HashInit(0)
assert result3 in (HASH_ERROR_EXCEPTION, HASH_ERROR_ARGUMENT_INVALID), "HashInit redundant argument"

# Test the HashTerminate method
result = dll.HashTerminate()
assert HASH_ERROR_OK == result, "HashTerminate termination"

result2 = dll.HashTerminate()
assert HASH_ERROR_NOT_INITIALIZED == result2, "HashTerminate second termination"

dll.HashInit()
result3 = dll.HashTerminate(0)
assert result3 in (HASH_ERROR_EXCEPTION, HASH_ERROR_ARGUMENT_INVALID), "HashTerminate redundant argument"

print("Test run finished")

# TODO: Add 2 test cases for redundant arguments, when improperly de-/initialized
# TODO: Rewrite test cases, so that they can run in a different order = add preconditions, action part, postconditions + wrap into methods
# TODO: Introduce UUID of the test cases
# TODO: Catch FAILED test cases, so that they do not interrupt the test run
# TODO: Introduce a test report (printed out into the console / file saved somewhere)
# TODO: Add a brief description of the test cases
# TODO: Add the test cases for other methods from the dll
