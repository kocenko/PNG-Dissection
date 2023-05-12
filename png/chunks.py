from typing import Callable, TypeVar, List
from png import utils
import itertools
import zlib


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

    def process(self, **kwargs) -> None:
        ''' Method processing a chunk according to its specification
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
            if self.processed_data == None:
                raise ValueError("Chunk has not been processed yet")
            
            if self.name not in self.displaying_logic:    
                raise NotImplementedError(f"Displaying for {self.name} was not implemented yet")
            
            getattr(self, Chunk.displaying_logic[self.name])()


        except Exception as e:
            print(e)




    ### Processing methods

    def process_IHDR(self, arguments: dict) -> dict:
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
        if len(self.data) % 3 != 0:
            raise ValueError(f"PLTE chunk length should be divisible by 3 but is {len(self.data)}")

        bit_depth = arguments["IHDR_values"].processed_data["bit_depth"]
        if len(self.data) // 3 > bit_depth:
            raise ValueError(f"Number of palette entries: {len(self.data) // 3} exceeds bit depth: {bit_depth}")

        decoded_values = []
        for i in range(0, len(self.data), 3):
            single_dict = {}
            single_dict["red"] = utils.bytes_to_int(self.data[i])
            single_dict["green"] = utils.bytes_to_int(self.data[i+1])
            single_dict["blue"] = utils.bytes_to_int(self.data[i+2])
            decoded_values.append(single_dict)
            
        return decoded_values

    def process_IDAT(self, arguments: dict) -> None:
        compression_method = arguments["IHDR_values"].processed_data["compression_method"]
        if compression_method == 0:
            zlib_datastream = bytearray(itertools.chain.from_iterable(self.data))
            decompressed = zlib.decompress(zlib_datastream)
        
        # Finding bytes per pixel
        colour_type = arguments["IHDR_values"].processed_data["colour_type"]
        if colour_type in [0, 3]:
            nb_channels = 1
        elif colour_type in [4]:
            nb_channels = 2
        elif colour_type in [2]:
            nb_channels = 3
        else:
            nb_channels = 4
        bit_depth = arguments["IHDR_values"].processed_data["bit_depth"]
        bytes_per_pixel = (bit_depth * nb_channels) // 8

        image_width = arguments["IHDR_values"].processed_data["width"]
        image_height = arguments["IHDR_values"].processed_data["height"]

        # Single scanline consists of 1 byte depicting which filtering was used
        # The rest of the scanline is data to be treated with inverse filter
        filtering_method = arguments["IHDR_values"].processed_data["filter_method"]
        if filtering_method == 0:
            for i in range(image_height):
                filter_flag_begin = i * (image_width * bytes_per_pixel + 1)
                filter_flag_end = filter_flag_begin + 1
                current_filter_flag = utils.bytes_to_int(decompressed[filter_flag_begin: filter_flag_end])
                

    def process_IEND(self, arguments: dict) -> None:
        pass
        #print("Processing IEND...")

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
        for key in self.processed_data:
            print(f"{key} : {self.processed_data[key]}")
    
    def display_PLTE(self) -> None:
        for colour in self.processed_data:
            print(colour)

    def display_IDAT(self) -> None:
        pass
        #print("Displaying IDAT...")

    def display_IEND(self) -> None:
        pass
        #print("Displaying IEND...")

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