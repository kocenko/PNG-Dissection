from typing import List
import numpy as np


def bytes_to_int(bytes: bytearray) -> int:
    """ Converts bytearray to int

    Args:
        bytes:
            bytearray to convert
    Returns:
        Converted int
    """
    return int.from_bytes(bytes, 'big', signed=False)

def bytes_to_string(bytes: bytearray) -> str:
    """ Converts bytearray to string

    Args:
        bytes:
            bytearray to convert
    Returns:
        Converted string
    """

    bytes_as_string = "".join(map(chr, bytes))
    return bytes_as_string

def string_to_bytes(string: str) -> bytearray:
    """ Converts string to bytearray

    Args:
        string:
            string to convert
    Returns:
        Converted bytearray
    """
    string_as_bytes = string.encode('utf-8')
    return string_as_bytes

def split_bytes_to_bits(byte: bytes or int, how_many: int) -> np.ndarray:
    if how_many not in [1, 2, 4, 8]:
        raise ValueError(f"Cannot split byte into {how_many} bits")

    outcome = np.empty(how_many, dtype=np.uint8)

    mask = 2**(8 // how_many) - 1 << (8 - (8 // how_many))
    for i in range(how_many):
        shift_offset = i * (8 // how_many)
        new_mask = (mask >> shift_offset)
        outcome[i] = (byte & new_mask) >> (8 - shift_offset - (8 // how_many))
    return outcome
