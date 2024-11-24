# -*- coding: utf-8 -*-
"""Package contains a test suite with test cases, which test the library hash.dll.
It is written for Windows operating system and requires 32-bit version of Python,
e.g. Python 3.13.0 32-bit (https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe).
All necessary libraries are already preinstalled within Python.
"""

import os
import datetime
import ctypes

HASH_ERROR_OK = 0  # Success
HASH_ERROR_GENERAL = 1  # Unknown error
HASH_ERROR_EXCEPTION = 2  # Standard exception encountered
HASH_ERROR_MEMORY = 3  # Memory allocation failed
HASH_ERROR_LOG_EMPTY = 4  # Reading an empty log
HASH_ERROR_ARGUMENT_INVALID = 5  # Invalid argument passed to a function
HASH_ERROR_ARGUMENT_NULL = 6  # Empty argument passed to a function
HASH_ERROR_NOT_INITIALIZED = 7  # Library is not initialized
HASH_ERROR_ALREADY_INITIALIZED = 8  # Library is already initialized

TEST_REPORT_FILE_PATH = "test_report.txt"

dll = ctypes.CDLL(os.path.join("HID_QA_Homework", "bin", "windows", "hash.dll"))

dll.HashInit.restype = ctypes.c_uint32

dll.HashTerminate.restype = ctypes.c_uint32


def _generic_action(measured_result, expected_codes, test_case_name, test_case_id):
    """Generic method for a common evaluation of test cases and reporting into a log.

    :param int measured_result: output response code from a library method call
    :param tuple expected_codes: all allowed (expected) response codes
    :param str test_case_name: name of the test case
    :param int test_case_id: unique identifier of the test case
    """
    if isinstance(expected_codes, int):
        expected_codes = (expected_codes,)
    elif isinstance(expected_codes, list):
        expected_codes = tuple(expected_codes)

    evaluation = "PASS"
    expected = ""

    if measured_result not in expected_codes:
        evaluation = "FAIL"
        expected = f"; Expected = {expected_codes}"

    msg = f"{evaluation} {test_case_id:03d}: {test_case_name}. Measured = {measured_result}{expected}"
    print(msg)

    with open(TEST_REPORT_FILE_PATH, "at", encoding="UTF-8") as report_file:
        report_file.write(msg + "\n")


# Test Cases
def hash_init():
    """Test if HashInit() returns the right response code"""
    measured_result = dll.HashInit()
    _generic_action(measured_result, HASH_ERROR_OK, "HashInit initialization", 0)
    dll.HashTerminate()


def hash_init_twice():
    """Test if HashInit() returns the right error code, when initialized for the second time"""
    dll.HashInit()
    measured_result = dll.HashInit()
    _generic_action(
        measured_result,
        HASH_ERROR_ALREADY_INITIALIZED,
        "HashInit second initialization",
        1,
    )
    dll.HashTerminate()


def hash_init_redundant():
    """Test if HashInit() returns the right error code, when called with an input argument"""
    measured_result = dll.HashInit(0)
    _generic_action(
        measured_result,
        (HASH_ERROR_EXCEPTION, HASH_ERROR_ARGUMENT_INVALID),
        "HashInit redundant argument",
        2,
    )
    dll.HashTerminate()


def hash_init_twice_redundant():
    """Test if HashInit() returns the right error code,
    when initialized for the second time and even with an input argument
    """
    dll.HashInit()
    measured_result = dll.HashInit(0)
    _generic_action(
        measured_result,
        (
            HASH_ERROR_EXCEPTION,
            HASH_ERROR_ARGUMENT_INVALID,
            HASH_ERROR_ALREADY_INITIALIZED,
        ),
        "HashInit redundant argument in the second initialization",
        3,
    )
    dll.HashTerminate()


def hash_terminate():
    """Test if HashTerminate() returns the right response code"""
    dll.HashInit()
    measured_result = dll.HashTerminate()
    _generic_action(measured_result, HASH_ERROR_OK, "HashTerminate termination", 4)


def hash_terminate_twice():
    """Test if HashTerminate() returns the right error code, when terminated for the second time"""
    measured_result = dll.HashTerminate()
    _generic_action(
        measured_result,
        HASH_ERROR_NOT_INITIALIZED,
        "HashTerminate second termination",
        5,
    )


def hash_terminate_redundant():
    """Test if HashTerminate() returns the right error code, when called with an input argument"""
    dll.HashInit()
    measured_result = dll.HashTerminate(0)
    _generic_action(
        measured_result,
        (HASH_ERROR_EXCEPTION, HASH_ERROR_ARGUMENT_INVALID),
        "HashTerminate redundant argument",
        6,
    )


def hash_terminate_twice_redundant():
    """Test if HashTerminate() returns the right error code,
    when terminated for the second time and even with an input argument
    """
    measured_result = dll.HashTerminate(0)
    _generic_action(
        measured_result,
        (HASH_ERROR_EXCEPTION, HASH_ERROR_ARGUMENT_INVALID, HASH_ERROR_NOT_INITIALIZED),
        "HashTerminate redundant argument in the second termination",
        7,
    )


# Test Suite
if __name__ == "__main__":
    # Create an empty test report file
    with open(TEST_REPORT_FILE_PATH, "wt", encoding="UTF-8") as report:
        report.write(
            f"Test report from {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f %z')}\n\n"
        )

    # Test the HashInit method
    hash_init()
    hash_init_twice()
    hash_init_redundant()
    hash_init_twice_redundant()

    # Test the HashTerminate method
    hash_terminate()
    hash_terminate_twice()
    hash_terminate_redundant()
    hash_terminate_twice_redundant()

    print("Test run finished")


# TODO: Add the test cases for other methods from the dll
