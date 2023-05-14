from typing import Callable, TypeVar, List
from png import utils
import itertools
import zlib
import math
import numpy as np
import matplotlib.pyplot as plt


T = TypeVar('T')

critical_chunks = ["IHDR", "PLTE", "IDAT", "IEND"]
ancillary_chunks = ["cHRM", "gAMA", "iCCP", "sBIT", "sRGB", "bKGD", "hIST", "tRNS", "pHYs", "sPLT", "tIME", "iTXt", "tEXt", "zTXt"]

class Chunk():
    processing_logic = {
        "IHDR": "process_IHDR",
        "PLTE": "process_PLTE",
        "IDAT": "process_IDAT",
        "IEND": "process_IEND",
        "cHRM": "process_cHRM",
        "gAMA": "process_gAMA",
        "iCCP": "process_iCCP",
        "sBIT": "process_sBIT",
        "sRGB": "process_sRGB",
        "bKGD": "process_bKGD",
        "hIST": "process_hIST",
        "tRNS": "process_tRNS",
        "pHYs": "process_pHYs",
        "sPLT": "process_sPLT",
        "tIME": "process_tIME",
        "iTXt": "process_iTXt",
        "tEXt": "process_tEXt",
        "zTXt": "process_zTXt",
    }

    displaying_logic = {
        "IHDR": "display_IHDR",
        "PLTE": "display_PLTE",
        "IDAT": "display_IDAT",
        "IEND": "display_IEND",
        "cHRM": "display_cHRM",
        "gAMA": "display_gAMA",
        "iCCP": "display_iCCP",
        "sBIT": "display_sBIT",
        "sRGB": "display_sRGB",
        "bKGD": "display_bKGD",
        "hIST": "display_hIST",
        "tRNS": "display_tRNS",
        "pHYs": "display_pHYs",
        "sPLT": "display_sPLT",
        "tIME": "display_tIME",
        "iTXt": "display_iTXt",
        "tEXt": "display_tEXt",
        "zTXt": "display_zTXt",
    }

    def __init__(self, length: int, name: str, content: bytearray or List[bytearray], corrupted: bool):
        self.corrupted: bool = corrupted
        self.length: int = length
        self.name: str = name
        self.data: bytearray or List[bytearray] = content
        self.processed_data: T = None

    def process(self, **kwargs: dict) -> None:
        ''' Method processing a chunk according to its specification

        Args:
            dict:
                Dictionary of arguments used to pass it to the processing function
        '''

        try:
            if self.corrupted:
                raise ValueError("Chunk is corrupted. Cannot process")
            
            if self.processed_data != None:
                raise ValueError("Chunk was already processed")
            
            if self.name not in self.processing_logic:    
                raise NotImplementedError(f"Processing for {self.name} was not implemented yet")
            
            self.processed_data = getattr(self, Chunk.processing_logic[self.name])(kwargs)
        
        except Exception as e:
            print(e)
    
    def display(self) -> None:
        ''' Method displaying processed chunk
        '''

        try:
            if self.processed_data is None:
                raise ValueError("Chunk has not been processed yet")
            
            if self.name not in self.displaying_logic:    
                raise NotImplementedError(f"Displaying for {self.name} was not implemented yet")
            
            getattr(self, Chunk.displaying_logic[self.name])()


        except Exception as e:
            print(e)




    ### Processing methods

    def process_IHDR(self, arguments: dict) -> dict:
        ''' Method used to process IHDR chunk

        Args:
            dict:
                Dictionary of arguments

        Returns:
            Dictinary with converted values of IHDR chunk's sections
        '''
        
        if len(arguments) == 0:
            pass

        decoded_values = {}
        decoded_values["width"] = utils.bytes_to_int(self.data[: 4])
        decoded_values["height"] = utils.bytes_to_int(self.data[4: 8])
        decoded_values["bit_depth"] = utils.bytes_to_int(self.data[8: 9])
        decoded_values["colour_type"] = utils.bytes_to_int(self.data[9: 10])
        decoded_values["compression_method"] = utils.bytes_to_int(self.data[10: 11])
        decoded_values["filter_method"] = utils.bytes_to_int(self.data[11: 12])
        decoded_values["interlace_method"] = utils.bytes_to_int(self.data[12: ])

        return decoded_values

    def process_PLTE(self, arguments: dict) -> List[dict]:
        ''' Method used to process PLTE chunk

        Args:
            dict:
                Dictionary of arguments

        Returns:
            List of dictinaries with converted colour values {red, green, blue}
        '''

        if len(self.data) % 3 != 0:
            raise ValueError(f"PLTE chunk length should be divisible by 3 but is {len(self.data)}")

        bit_depth = arguments["IHDR_values"].processed_data["bit_depth"]
        if len(self.data) // 3 > 2**bit_depth:
            raise ValueError(f"Number of palette entries: {len(self.data) // 3} exceeds range defined by the bit depth: {2**bit_depth}")

        decoded_values = []
        for i in range(0, len(self.data), 3):
            single_dict = {}
            single_dict["red"] = self.data[i]
            single_dict["green"] = self.data[i+1]
            single_dict["blue"] = self.data[i+2]
            decoded_values.append(single_dict)
            
        return decoded_values

    def __decompress_zlib_datastream(self, arguments: dict) -> bytearray:
        ''' Method used to decompress zlib datastream

        Args:
            dict:
                Dictionary of arguments

        Returns:
            bytearray of decompressed datastream
        '''
        compression_method = arguments["IHDR_values"].processed_data["compression_method"]
        if compression_method != 0:
            raise ValueError(f"Only compression method {compression_method} is defined by the standard")

        zlib_datastream = bytearray(itertools.chain.from_iterable(self.data))
        return zlib.decompress(zlib_datastream)

    def __calculate_bytes_per_pixel(self, arguments: dict, num_channels: int) -> int or float:
        ''' Calculates how many bytes describing a pixel

        Outcome value depends on the bit depth. If bit depth is smaller than 8,
        it is assumed that the bytes per pixel value is equal to 1.

        Args:
            dict:
                Dictionary of arguments
            int:
                Number of image's channels

        Returns:
            number of bytes per pixel
        '''
        
        colour_type = arguments["IHDR_values"].processed_data["colour_type"]
        bit_depth = arguments["IHDR_values"].processed_data["bit_depth"]

        match colour_type:
            case 0:
                return bit_depth / 8
            case 2:
                return num_channels * bit_depth / 8
            case 3:
                return bit_depth / 8
            case 4:
                return num_channels * bit_depth / 8
            case 6:
                return num_channels * bit_depth / 8
            case _:
                raise ValueError(f"Unrecognized colour type: {colour_type}")

    @staticmethod
    def __paeth_predictor(a: int, b: int, c: int) -> int:
        ''' Returns a value of the Paeth's predictor
        
        Args:
            int:
                a: byte to the left of the current one
                b: byte above the current one
                c: upper left byte to the current one

        Returns:
            Paeth's descriptor value
        '''
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)

        if pa <= pb and pa <= pc:
            Pr = a
        elif pb <= pc:
            Pr = b
        else:
            Pr = c
        return Pr

    def __reconstruct_scanline(self, to_reconstruct: bytearray, prior_scanline: bytearray, bytes_per_pixel: int, filter_flag: int) -> np.ndarray:
        ''' Calculates inverse filtering of scanlines to reconstruct

        Args:
            bytearray:
                to_reconstruct: filtered scanline
                prior_scanline: scanline above the current one, already inverse filtered
            int:
                bytes_per_pixel: Number of bytes per pixel
                filter_flag: Number depicting which filter type should be used
        
        Returns:
            numpy array of the reconstructed bytearray
        '''

        reconstructed = np.zeros(len(to_reconstruct))
        modulo_value = 256
        bpp = math.ceil(bytes_per_pixel)

        for i in range(len(to_reconstruct)):
            current_byte = to_reconstruct[i]
            prior_byte = reconstructed[i-bpp] if i >= bpp else 0
            prior_scanline_byte = prior_scanline[i]
            prior_scanline_prior_byte = prior_scanline[i-bpp] if i >= bpp else 0

            match filter_flag:
                case 0:
                    reconstructed_byte = current_byte
                case 1:
                    reconstructed_byte = (current_byte + prior_byte) % modulo_value
                case 2:
                    reconstructed_byte = (current_byte + prior_scanline_byte) % modulo_value
                case 3:
                    reconstructed_byte = (current_byte + (prior_byte + prior_scanline_byte) // 2) % modulo_value
                case 4:
                    reconstructed_byte = (current_byte + self.__paeth_predictor(prior_byte, prior_scanline_byte, prior_scanline_prior_byte)) % modulo_value
                case _:
                    raise ValueError(f"Invalid filter flag: {filter_flag}")
            
            reconstructed[i] = reconstructed_byte


        return reconstructed

    @staticmethod
    def __scanline_to_pixel_row(scanline: np.ndarray, num_channels: int, bit_depth: int, colour_type: int) -> np.ndarray:
        ''' Reshaping scanline to row of pixels

        Args:
            np.ndarray:
                scanline: scanline to convert to pixels
            int:
                num_channels: Number of channels
                bit_depth: Number indicating bit depth
                colour_type: Number indicating colour type

        Returns:
            numpy array of row of pixels
        '''
        output = scanline.copy()
        
        if bit_depth < 8:
            num_bits = 8 // bit_depth
            for i, b in enumerate(scanline):
                output[i: i+num_bits] = utils.split_bytes_to_bits(int(b), num_bits)

        if colour_type != 3:
            output = output.reshape((-1, num_channels))
        else:
            output = output  # Change to the values from the PLTE
        
        return output

    def __reconstruct_pixels(self, arguments: dict, decompressed: bytearray, bytes_per_pixel: int, num_channels: int) -> np.ndarray:
        ''' Converts decompressed bytearray to numpy array of pixels

        Args:
            dict:
                arguments: Arguments passed by the outside function
            bytearray:
                decompressed: bytearray decompressed by zlib
            int:
                bytes_per_pixel: Number of bytes per pixel
                num_channels: Number of channels

        Returns:
            numpy array of pixels
        '''
        
        image_height = arguments["IHDR_values"].processed_data["height"]
        image_width = arguments["IHDR_values"].processed_data["width"]
        bit_depth = arguments["IHDR_values"].processed_data["bit_depth"]
        colour_type = arguments["IHDR_values"].processed_data["colour_type"]

        output = np.empty((image_height, image_width, num_channels), dtype=np.uint8)

        scanlines_width = math.ceil(image_width * bytes_per_pixel + 1)
        scanlines_height = int(len(decompressed) / scanlines_width)

        prior_scanline = bytearray(scanlines_width)
        for i in range(scanlines_height):
            scanline_begin = i * scanlines_width
            scanline_end = scanline_begin + scanlines_width
            filter_flag = decompressed[scanline_begin]
            single_scanline = bytearray(decompressed[scanline_begin+1: scanline_end])
            prior_scanline = self.__reconstruct_scanline(single_scanline, prior_scanline, bytes_per_pixel, filter_flag)
            output[i] = self.__scanline_to_pixel_row(prior_scanline, num_channels, bit_depth)
            
        return output

    def process_IDAT(self, arguments: dict) -> np.ndarray:
        ''' Processes IDAT chunk data
        
        Args:
            dict: 
                arguments: Arguments passed by the outside function
        
        Returns:
            numpy array of pixels
        '''
        num_channels_dict = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}

        filtering_method = arguments["IHDR_values"].processed_data["filter_method"]
        colour_type = arguments["IHDR_values"].processed_data["colour_type"]

        decompressed = self.__decompress_zlib_datastream(arguments)
        bytes_per_pixel = self.__calculate_bytes_per_pixel(arguments, num_channels_dict[colour_type])

        if filtering_method != 0:
            raise ValueError(f"Only filter method 0 is defined by the standard not {filtering_method}")
        
        return self.__reconstruct_pixels(arguments, decompressed, bytes_per_pixel, num_channels_dict[colour_type])            

    def process_IEND(self, arguments: dict) -> bool:
        ''' Processes IEND chunk
        
        Args:
            dict:
                arguments: Dictionary of arguments passed by the outside funtion

        Returns:
            True if the chunk is not corrupted, False otherwise
        '''

        if len(arguments) == 0:
            pass

        return not self.corrupted

    def process_cHRM(self, arguments: dict) -> None:
        pass
        #print("Processing cHRM...")

    def process_gAMA(self, arguments: dict) -> None:
        pass
        #print("Processing gAMA...")

    def process_iCCP(self, arguments: dict) -> None:
        pass
        #print("Processing iCCP...")

    def process_sBIT(self, arguments: dict) -> None:
        pass
        #print("Processing sBIT...")

    def process_sRGB(self, arguments: dict) -> None:
        pass
        #print("Processing sRGB...")

    def process_bKGD(self, arguments: dict) -> None:
        pass
        #print("Processing bKGD...")

    def process_hIST(self, arguments: dict) -> None:
        pass
        #print("Processing hIST...")

    def process_tRNS(self, arguments: dict) -> None:
        pass
        #print("Processing tRNS...")

    def process_pHYs(self, arguments: dict) -> None:
        pass
        #print("Processing pHYs...")

    def process_sPLT(self, arguments: dict) -> None:
        pass
        #print("Processing sPLT...")

    def process_tIME(self, arguments: dict) -> None:
        pass
        #print("Processing tIME...")

    def process_iTXt(self, arguments: dict) -> str:
        if len(arguments) == 0:
            pass
        return "".join(utils.bytes_to_string(a) for a in self.data)

    def process_tEXt(self, arguments: dict) -> None:
        pass
        #print("Processing tEXt...")

    def process_zTXt(self, arguments: dict) -> None:
        pass
        #print("Processing zTXt...")




    ### Displaying methods

    def display_IHDR(self) -> None:
        ''' Method used to display processed IHDR chunk data
        '''
        
        for key in self.processed_data:
            print(f"{key} : {self.processed_data[key]}")
    
    def display_PLTE(self) -> None:
        ''' Method used to display processed PLTE chunk data
        '''

        for colour in self.processed_data:
            print(colour)

    def display_IDAT(self) -> None:
        ''' Method used to display processed IDAT chunk data
        '''

        plt.imshow(self.processed_data)
        plt.show()

    def display_IEND(self) -> None:
        print("Chunk IEND was read correctly")

    def display_cHRM(self) -> None:
        pass
        #print("Displaying cHRM...")

    def display_gAMA(self) -> None:
        pass
        #print("Displaying gAMA...")

    def display_iCCP(self) -> None:
        pass
        #print("Displaying iCCP...")

    def display_sBIT(self) -> None:
        pass
        #print("Displaying sBIT...")

    def display_sRGB(self) -> None:
        pass
        #print("Displaying sRGB...")

    def display_bKGD(self) -> None:
        pass
        #print("Displaying bKGD...")

    def display_hIST(self) -> None:
        pass
        #print("Displaying hIST...")

    def display_tRNS(self) -> None:
        pass
        #print("Displaying tRNS...")

    def display_pHYs(self) -> None:
        pass
        #print("Displaying pHYs...")

    def display_sPLT(self) -> None:
        pass
        #print("Displaying sPLT...")

    def display_tIME(self) -> None:
        pass
        #print("Displaying tIME...")

    def display_iTXt(self) -> None:
        print(f"{self.processed_data}")

    def display_tEXt(self) -> None:
        pass
        #print("Displaying tEXt...")

    def display_zTXt(self) -> None:
        pass
        #print("Displaying zTXt...")