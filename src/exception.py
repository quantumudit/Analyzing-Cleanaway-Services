"""
This module provides utility functions for handling errors and a custom
exception class.

The error_details function retrieves information about an error, such as
the file name and line number where the error occurred. It takes an error
object as input and returns a formatted error message.

The CustomException class is a subclass of the built-in Exception class. It
overrides the __init__ and __str__ methods to provide a custom error message
that includes the file name and line number where the exception was raised.
"""

import sys


def error_details(error) -> str:
    """
    Retrieves information about an error, such as the file name and line
    number where the error occurred.

    Args:
        error (object): The error object.

    Returns:
        str: A formatted error message that includes the file name and line
        number where the error occurred.
    """
    _, _, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (
        "Error occurred in Python script "
        f"[{file_name}] at line [{line_number}]: [{str(error)}]"
    )
    return error_message


class CustomException(Exception):
    """
    A custom exception class that provides a custom error message including
    the file name and line number where the exception was raised.

    Args:
        Exception (class): The built-in Exception class.

    Attributes:
        error_message (str): The formatted error message that includes the
        file name and line number where the exception was raised.
    """

    def __init__(self, error_message):
        super().__init__(error_message)
        self.error_message = error_details(error_message)

    def __str__(self):
        return self.error_message
