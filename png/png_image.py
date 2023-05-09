from png import chunks
import zlib


class PNG:
    list_of_chunks = chunks.chunk_list
    signature = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__data = self.__read_file()
        self.__chunks = self.__init_chunks()
        
        if not self.__is_png():
            raise ValueError("Given file is not a PNG file or it is corrupted")

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
    
    @staticmethod
    def __bytes_to_string(bytes: bytearray) -> str:
        """ Converts bytearray to string

        Args:
            bytes:
                bytearray to convert
        Returns:
            Converted string
        """

        bytes_as_string = "".join(map(chr, bytes))
        return bytes_as_string
    
    @staticmethod
    def __bytes_to_int(bytes: bytearray) -> int:
        """ Converts bytearray to int

        Args:
            bytes:
                bytearray to convert
        Returns:
            Converted int
        """
        return int.from_bytes(bytes, 'big', signed=False)

    def __read_chunks(self) -> None:
        data_rest = self.__data[8:]
        try:
            i = 0
            while i < len(data_rest):
                length = self.__bytes_to_int(data_rest[i:i+4])
                chunk_type = self.__bytes_to_string(data_rest[i+4:i+8])
                chunk_data = data_rest[i+8:i+8+length] if length > 0 else b""
                crc = self.__bytes_to_int(data_rest[i+8+length:i+8+length+4])
                actual_crc = zlib.crc32(data_rest[i+4:i+8+length])

                print(f"Length: {length} Chunk_Type: {chunk_type} Chunk_Data (size): {len(chunk_data)} CRC: {crc} Calc CRC {actual_crc}")
                i = i+8+length+4
        except:
            print("Could not read chunks: possible data corruption")


    def find_chunks(self):
        self.__read_chunks()
    #     for i in range(len(self.__data) - 4):
    #         current_string = self.__bytes_to_string(self.__data[i:i+4])
    #         if current_string in self.list_of_chunks:
    #             print(f'Found {current_string} chunk')

