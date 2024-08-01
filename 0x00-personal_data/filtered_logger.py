#!/usr/bin/env python3
"""
This module provides a function to obfuscate sensitive fields in log messages.
"""

import re
from typing import List, Tuple


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
        """
        Obfuscates sensitive fields in a log message.

        Args:
            fields (List[str]): A list of field names to be obfuscated.
            redaction (str): The string to use for obfuscation.
            message (str): The log message to be processed.
            separator (str): The character used to separate fields in the log message.

        Returns:
                str: The log message with the sensitive fields obfuscated.
        """

        pattern = r'({})=.*?{}'.format('|'.join(fields), separator)
        return re.sub(pattern, r'\1={}{}'.format(redaction, separator), message)
