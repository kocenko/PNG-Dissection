from typing import Callable, TypeVar


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

    def __init__(self, length: int, name: str, content: bytearray, corrupted: bool):
        self.corrupted: bool = corrupted
        self.length: int = length
        self.name: str = name
        self.data: bytearray = content
        self.processed_data: T = None

    def process(self) -> None:
        ''' Method processing a chunk according to its specification
        '''

        if self.corrupted:
            raise ValueError("Chunk is corrupted. Cannot process")
        
        if self.processed_data != None:
            raise ValueError("Chunk was already processed")
        
        if self.name not in self.processing_logic:    
            raise NotImplementedError(f"Processing for {self.name} was not implemented yet")
        
        method_name = Chunk.processing_logic[self.name]
        method: Callable[[bytearray], T] = getattr(self, method_name)
        self.processsed_data = method()
    
    
    def process_IHDR(self) -> None:
        print("Processing IHDR...")
    
    def process_PLTE(self) -> None:
        print("Processing PLTE...")

    def process_IDAT(self) -> None:
        print("Processing IDAT...")

    def process_IEND(self) -> None:
        print("Processing IEND...")

    def process_cHRM(self) -> None:
        print("Processing cHRM...")

    def process_gAMA(self) -> None:
        print("Processing gAMA...")

    def process_iCCP(self) -> None:
        print("Processing iCCP...")

    def process_sBIT(self) -> None:
        print("Processing sBIT...")

    def process_sRGB(self) -> None:
        print("Processing sRGB...")

    def process_bKGD(self) -> None:
        print("Processing bKGD...")

    def process_hIST(self) -> None:
        print("Processing hIST...")

    def process_tRNS(self) -> None:
        print("Processing tRNS...")

    def process_pHYs(self) -> None:
        print("Processing pHYs...")

    def process_sPLT(self) -> None:
        print("Processing sPLT...")

    def process_tIME(self) -> None:
        print("Processing tIME...")

    def process_iTXt(self) -> None:
        print("Processing iTXt...")

    def process_tEXt(self) -> None:
        print("Processing tEXt...")

    def process_zTXt(self) -> None:
        print("Processing zTXt...")