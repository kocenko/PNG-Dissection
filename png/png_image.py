from png import chunks
from png import utils
import zlib


class PNG:
    list_of_chunks = chunks.critical_chunks + chunks.ancillary_chunks
    signature = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    multiple_chunks_allowed_for = ["IDAT", "sPLT", "iTXt", "tEXt", "zTXt"]

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__data = self.__read_file()
        self.chunks = self.__init_chunks()
        
        if not self.__is_png():
            raise ValueError("Given file is not a PNG file or it is corrupted")
        
        self.__read_chunks()

        self.processing_arguments_mapping = {
            'IHDR': (),
            'PLTE': (lambda: self.chunks["IHDR"], ),
            'IDAT': (lambda: self.chunks["IHDR"], )
        }

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
                chunks[chunk_name] = None

        return chunks 

    def __is_png(self) -> bool:
        ''' Checks if the file begins with the PNG signature

        Returns:
            Returns True if its begins with the PNG signature, else False
        '''

        return True if self.__data[:8] == self.signature else False

    def __check_ordering(self, chunk_type: str) -> None:
        match chunk_type:
            case "IHDR":
                if any(self.chunks[chunk] != None for chunk in PNG.list_of_chunks):
                    raise ValueError(f"Chunk {chunk_type} should appear first")
            case "PLTE":
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "cHRM":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
            case "gAMA":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
            case "iCCP":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["sRGB"] != None:
                    raise ValueError(f"{chunk_type} should not be present when \"sRGB\" is present")
            case "sBIT":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
            case "sRGB":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["iCCP"] != None:
                    raise ValueError(f"{chunk_type} should not be present when \"iCCP\" is present")
            case _:
                pass

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
            
            self.__check_ordering(chunk_type)

            if chunk_type in PNG.multiple_chunks_allowed_for:
                if self.chunks[chunk_type] == None:
                    self.chunks[chunk_type] = chunks.Chunk(length, chunk_type, [chunk_data], crc != actual_crc)
                else:
                    self.chunks[chunk_type].data.append(chunk_data)
            else:
                if self.chunks[chunk_type] != None:
                    raise KeyError(f"Chunk {chunk_type} does not allow multiple instances")
                self.chunks[chunk_type] = chunks.Chunk(length, chunk_type, chunk_data, crc != actual_crc)

            i = i+8+length+4

    def is_chunk_read(self, chunk_type: str) -> bool:
        ''' Checks if the chunk of the given name was read

        Args:
            str:
                Chunk name

        Returns:
            True if was read, False otherwise
        '''

        if self.chunks[chunk_type] == None:
            return False
        return True

    def process_chunks(self) -> None:
        ''' Processes chunks to get information according to the chunk specification
        '''

        for key, value in self.chunks.items():
            if value != None:
                arguments = self.processing_arguments_mapping.get(key)
                if arguments:
                    processed_arguments = [arg() if callable(arg) else arg for arg in arguments]
                    value.process(*processed_arguments)
                else:
                    value.process()

    def display_chunk(self, chunk_type: str) -> None:
        ''' Displays processed chunk
        '''

        if chunk_type not in self.chunks.keys():
            raise ValueError(f"Could not display chunk {chunk_type}, not in the list")
        
        if not self.is_chunk_read(chunk_type):
            raise ValueError(f"Could not display chunk {chunk_type}, it was not read")

        self.chunks[chunk_type].display()

