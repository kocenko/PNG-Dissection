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