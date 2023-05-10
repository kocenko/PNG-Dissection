from abc import ABC, abstractmethod

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
        self.corrupted = corrupted
        self.length = length
        self.name = name
        self.data = content
        self.processed = False

    def process(self) -> None:
        ''' Method processing a chunk according to its specification
        '''

        if self.corrupted:
            raise ValueError("Chunk is corrupted. Cannot process")
        
        if self.processed:
            raise ValueError("Chunk was already processed")
        
        if self.name not in self.processing_logic:    
            raise NotImplementedError(f"Processing for {self.name} was not implemented yet")
        
        getattr(self, Chunk.processing_logic[self.name])()
        self.processsed = True
    

    @staticmethod    
    def process_IHDR() -> None:
        print("Processing IHDR...")

    @staticmethod   
    def process_PLTE() -> None:
        print("Processing PLTE...")

    @staticmethod
    def process_IDAT() -> None:
        print("Processing IDAT...")

    @staticmethod
    def process_IEND() -> None:
        print("Processing IEND...")

    @staticmethod
    def process_cHRM() -> None:
        print("Processing cHRM...")

    @staticmethod
    def process_gAMA() -> None:
        print("Processing gAMA...")

    @staticmethod
    def process_iCCP() -> None:
        print("Processing iCCP...")

    @staticmethod
    def process_sBIT() -> None:
        print("Processing sBIT...")

    @staticmethod
    def process_sRGB() -> None:
        print("Processing sRGB...")

    @staticmethod
    def process_bKGD() -> None:
        print("Processing bKGD...")

    @staticmethod
    def process_hIST() -> None:
        print("Processing hIST...")

    @staticmethod
    def process_tRNS() -> None:
        print("Processing tRNS...")

    @staticmethod
    def process_pHYs() -> None:
        print("Processing pHYs...")

    @staticmethod
    def process_sPLT() -> None:
        print("Processing sPLT...")

    @staticmethod
    def process_tIME() -> None:
        print("Processing tIME...")

    @staticmethod
    def process_iTXt() -> None:
        print("Processing iTXt...")

    @staticmethod
    def process_tEXt() -> None:
        print("Processing tEXt...")

    @staticmethod
    def process_zTXt() -> None:
        print("Processing zTXt...")