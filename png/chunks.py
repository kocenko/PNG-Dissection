from abc import ABC, abstractmethod

critical_chunks = ["IHDR", "PLTE", "IDAT", "IEND"]
ancillary_chunks = ["cHRM", "gAMA", "iCCP", "sBIT", "sRGB", "bKGD", "hIST", "tRNS", "pHYs", "sPLT", "tIME", "iTXt", "tEXt", "zTXt"]

class Chunk(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_content(self):
        pass

    @classmethod
    def create_chunk(cls, name):
        if name == "iTXt":
            return Chunk_iTXt(name)
        else:
            return Chunk(name)
        
class Chunk_iTXt(Chunk):
    def __init__(self, name):
        super().__init__(name)

    def get_content(self):
        print(f"Getting content of {self.name}")

if __name__ == "__main__":
    c = Chunk("iTXt")
    c.get_content()