from abc import ABC, abstractmethod
import os

MAX_DATA_LENGTH = 100


class SSDDriver(ABC):
    def __init__(self, nand_path, result_path):
        self.nand_path = nand_path
        self.result_path = result_path

    @abstractmethod
    def read(self, addr):
        pass

    @abstractmethod
    def write(self, addr, value):
        pass


class SSDDriverCommon(SSDDriver):
    def __init__(self, sep, nand_path: str, result_path: str):
        super().__init__(nand_path, result_path)
        self.sep = sep
        if not os.path.exists(nand_path):
            with open(nand_path, 'w') as file:
                file.write(self.convert_to_str([0] * 100))

    def convert_to_str(self, values):
        return self.sep.join([str(v) for v in values])

    def read(self, addr: int):
        self.check_exist_nand()
        values = self.read_nand()
        self.save(self.result_path, self.convert_to_hex(values[addr]))

    def write(self, addr: int, value: str):
        values = self.read_nand()
        values[addr] = self.convert_to_dec(value)
        self.save(self.nand_path, self.convert_to_str(values))

    def erase(self, addr: int, size: int):
        for each_addr in range(addr, addr + size):
            self.write(each_addr, '0x00000000')

    def read_nand(self) -> list:
        with open(self.nand_path, 'r') as nand:
            buffer = nand.readline().strip()
        return [int(lba) for lba in buffer.split(self.sep)]

    def check_exist_nand(self):
        if not os.path.exists(self.nand_path):
            raise FileNotFoundError

    @staticmethod
    def save(path: str, text: str):
        with open(path, 'w') as file:
            file.write(text)

    @staticmethod
    def convert_to_hex(decimal: int) -> str:
        return '0x' + '{:08x}'.format(decimal).upper()

    @staticmethod
    def convert_to_dec(hexadecimal: str) -> int:
        return int(hexadecimal, 16)

