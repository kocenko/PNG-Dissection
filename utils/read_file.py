def read_file(file_name: str) -> bytearray:
    ''' Reads bytes from file

    Args:
        file_name:
            Input file path
    Returns:
        Returns a list of bytes read from the file
    '''

    with open(file_name, 'rb') as file:
        bytes = file.read()

    return bytes


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