from png import chunks
from png import utils
import zlib


class PNG:
    list_of_chunks = chunks.critical_chunks + chunks.ancillary_chunks
    signature = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__data = self.__read_file()
        self.chunks = self.__init_chunks()
        
        if not self.__is_png():
            raise ValueError("Given file is not a PNG file or it is corrupted")
        
        self.__read_chunks()

    def __read_file(self) -> bytearray:
        ''' Reads bytes from file

        Returns:
            Returns a list of bytes read from the file
        '''

        with open(self.__file_name, 'rb') as file:
            bytes = file.read()

        return bytes

    def __init_chunks(self) -> dict:
        ''' Creates chunks dict and initializes with empty lists

        Returns:
            Dict with chunk names as keys and None as their values
        '''

        chunks = {}
        for chunk_name in self.list_of_chunks:
            chunks[chunk_name] = []

        return chunks 

    def __is_png(self) -> bool:
        ''' Checks if the file begins with the PNG signature

        Returns:
            Returns True if its begins with the PNG signature, else False
        '''

        return True if self.__data[:8] == self.signature else False

    def __read_chunks(self) -> None:
        ''' Reads the bytearray and dissects it into chunks
        '''

        data_rest = self.__data[8:]
        i = 0
        while i < len(data_rest):
            length = utils.bytes_to_int(data_rest[i:i+4])
            chunk_type = utils.bytes_to_string(data_rest[i+4:i+8])
            chunk_data = data_rest[i+8:i+8+length] if length > 0 else b""
            crc = utils.bytes_to_int(data_rest[i+8+length:i+8+length+4])
            actual_crc = zlib.crc32(data_rest[i+4:i+8+length])

            if chunk_type not in self.chunks.keys():
                raise ValueError(f"Decoded chunk {chunk_type} type not in the list of standard chunks")
            
            self.chunks[chunk_type].append(chunks.Chunk(length, chunk_type, chunk_data, crc != actual_crc))
            i = i+8+length+4

    def process_chunks(self):
        ''' Processes chunks to get information according to the chunk specification
        '''
        
        for key in self.chunks:
            for single_chunk in self.chunks[key]:
                single_chunk.process()

