import os.path

import numpy as np
from png import chunks
from png import utils
from PIL import Image

import zlib
import matplotlib.pyplot as plt

class PNG:
    list_of_chunks = chunks.critical_chunks + chunks.ancillary_chunks
    signature = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    multiple_chunks_allowed_for = ["IDAT", "sPLT", "iTXt", "tEXt", "zTXt"]

    def __init__(self, file_path: str):
        self.__img_path = file_path
        self.__data = self.__read_file()
        self.chunks = self.__init_chunks()
        
        if not self.__is_png():
            raise ValueError("Given file is not a PNG file or it is corrupted")
        
        self.__read_chunks()

        self.processing_arguments_mapping = {
            'IHDR': {},
            'PLTE': {"IHDR_values": lambda: self.chunks["IHDR"]},
            'IDAT': {"IHDR_values": lambda: self.chunks["IHDR"], "PLTE_values": lambda: self.chunks["PLTE"]}
        }

    def __read_file(self) -> bytearray:
        ''' Reads bytes from file

        Returns:
            Returns a list of bytes read from the file
        '''

        with open(self.__img_path, 'rb') as file:
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
        ''' Checks if requirements about chunk ordering are met
        
        Args:
            str:
                chunk type name
        '''

        match chunk_type:
            case "IHDR":
                if any(self.chunks[chunk] != None for chunk in PNG.list_of_chunks):
                    raise ValueError(f"Chunk {chunk_type} should appear first")
            case "PLTE":
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
                if self.chunks["bKGD"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"bKGD\"")
                if self.chunks["hIST"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"hIST\"")
                if self.chunks["tRNS"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"tRNS\"")
            case "cHRM":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "gAMA":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "iCCP":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["sRGB"] != None:
                    raise ValueError(f"{chunk_type} should not be present when \"sRGB\" is present")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "sBIT":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "sRGB":
                if self.chunks["PLTE"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"PLTE\"")
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["iCCP"] != None:
                    raise ValueError(f"{chunk_type} should not be present when \"iCCP\" is present")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "bKGD":
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "hIST":
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "tRNS":
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "pHYs":
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
            case "sPLT":
                if self.chunks["IDAT"] != None:
                    raise ValueError(f"{chunk_type} should be read before \"IDAT\"")
                if self.chunks["IEND"] != None:
                    raise ValueError(f"Chunk \"IEND\" should appear after the chunk {chunk_type}")
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
                print(f"Decoded chunk {chunk_type} type not in the list of standard chunks")
                return None

            self.__check_ordering(chunk_type)

            if chunk_type in PNG.multiple_chunks_allowed_for:
                if self.chunks[chunk_type] == None:
                    self.chunks[chunk_type] = chunks.Chunk(length, chunk_type, [chunk_data], crc, crc != actual_crc)
                else:
                    self.chunks[chunk_type].data.append(chunk_data)
            else:
                if self.chunks[chunk_type] != None:
                    raise KeyError(f"Chunk {chunk_type} does not allow multiple instances")
                self.chunks[chunk_type] = chunks.Chunk(length, chunk_type, chunk_data, crc, crc != actual_crc)

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
                    processed_arguments = {}
                    for arg_key, arg_val in arguments.items():
                        processed_arguments[arg_key] = arg_val() if callable(arg_val) else arg_val
                    value.process(**processed_arguments)
                else:
                    value.process()

    def display_chunk(self, chunk_type: str) -> None:
        ''' Displays processed chunk

        Args:
            str:
                chunk type name
        '''

        try:
            if chunk_type not in self.chunks.keys():
                raise ValueError(f"Could not display chunk {chunk_type}, not in the list")
            
            if not self.is_chunk_read(chunk_type):
                raise ValueError(f"Could not display chunk {chunk_type}, it was not read")

            self.chunks[chunk_type].display()
        except Exception as e:
            print(e)

    def __clear_ancillaries(self) -> bytearray:
        cleared_image = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'  # PNG magic number

        cleared_image += (self.chunks["IHDR"].length.to_bytes(length=4, byteorder='big') +
                          self.chunks["IHDR"].identifier +
                          self.chunks["IHDR"].data +
                          self.chunks["IHDR"].crc.to_bytes(length=4, byteorder='big'))

        if self.chunks["PLTE"] is not None:
            cleared_image += (self.chunks["PLTE"].length.to_bytes(length=4, byteorder='big') +
                              self.chunks["PLTE"].identifier +
                              self.chunks["PLTE"].data +
                              self.chunks["PLTE"].crc.to_bytes(length=4, byteorder='big'))

        cleared_image += (self.chunks["IDAT"].length.to_bytes(length=4, byteorder='big') +
                          self.chunks["IDAT"].identifier +
                          b''.join(self.chunks["IDAT"].data) +
                          self.chunks["IDAT"].crc.to_bytes(length=4, byteorder='big'))

        cleared_image += b'\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82'  # IEND chunk

        return cleared_image

    def __save_to_file(self, file_name: str, image: bytearray) -> None:
        with open("imgs/processed/" + file_name, "wb") as output_file:
            output_file.write(image)

    def anonymize(self, save_file: bool = True) -> bytearray:
        anonymized = self.__clear_ancillaries()
        if save_file:
            self.__save_to_file("anonymized_" + os.path.basename(self.__img_path), anonymized)
        return anonymized

    def fourier_transform(self):
        image = Image.open(self.__img_path)
        gray = image.convert("L")

        np_image = np.asarray(gray, dtype=np.uint8)
        fft_image = np.fft.fft2(np_image)  # 2 dimensional fft
        fft_shifted = np.fft.fftshift(fft_image)

        magnitude = 20 * np.log10(np.abs(fft_shifted))
        phase = np.angle(fft_shifted)

        fig, (ax1, ax2) = plt.subplots(1, 2)

        ax1.imshow(magnitude, cmap='gray')
        ax1.set_title('Magnitude')
        ax1.axis('off')

        ax2.imshow(phase, cmap='gray')
        ax2.set_title('Phase')
        ax2.axis('off')

        plt.show()

        return fft_shifted

    def inverse_fourier(self, transform):
        inv_shift = np.fft.ifftshift(transform)
        inv_fourier = np.fft.ifftn(inv_shift)
        image = abs(inv_fourier)
        original_img = Image.open(self.__img_path).convert("L")

        fig, (ax1, ax2) = plt.subplots(1, 2)

        ax1.imshow(image, cmap='gray')
        ax1.set_title('Reconstructed image')
        ax1.axis('off')

        ax2.imshow(original_img, cmap='gray')
        ax2.set_title('Original image')
        ax2.axis('off')

        plt.show()
