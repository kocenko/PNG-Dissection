from abc import ABC, abstractmethod

critical_chunks = ["IHDR", "PLTE", "IDAT", "IEND"]
ancillary_chunks = ["cHRM", "gAMA", "iCCP", "sBIT", "sRGB", "bKGD", "hIST", "tRNS", "pHYs", "sPLT", "tIME", "iTXt", "tEXt", "zTXt"]

class Chunk():
    def __init__(self, length: int, name: str, content: bytearray, corrupted: bool):
        self.corrupted = corrupted
        self.length = length
        self.name = name
        self.data = content
        self.processed = False
        
        self.processing_logic = {
            "IHDR": self.process_IHDR,
            "PLTE": self.process_PLTE,
            "IDAT": self.process_IDAT,
            "IEND": self.process_IEND,
            "cHRM": self.process_cHRM,
            "gAMA": self.process_gAMA,
            "iCCP": self.process_iCCP,
            "sBIT": self.process_sBIT,
            "sRGB": self.process_sRGB,
            "bKGD": self.process_bKGD,
            "hIST": self.process_hIST,
            "tRNS": self.process_tRNS,
            "pHYs": self.process_pHYs,
            "sPLT": self.process_sPLT,
            "tIME": self.process_tIME,
            "iTXt": self.process_iTXt,
            "tEXt": self.process_tEXt,
            "zTXt": self.process_zTXt,
        }

    def process(self) -> None:
        if self.corrupted:
            raise ValueError("Chunk is corrupted. Cannot process")
        
        if self.processed:
            raise ValueError("Chunk was already processed")
        
        if self.name not in self.processing_logic:    
            raise NotImplementedError(f"Processing for {self.name} was not implemented yet")
        
        self.processing_logic[self.name]()
        self.processsed = True
    

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