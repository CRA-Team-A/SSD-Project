from abc import ABC, abstractmethod
import os


class SSDDriver(ABC):
    def __init__(self, nand_path, result_path):
        if not os.path.isfile(nand_path):
            with open(nand_path, 'w') as file:
                pass
        self.nand_path = nand_path
        self.result_path = result_path

    @abstractmethod
    def read(self, addr):
        pass

    @abstractmethod
    def write(self, addr, value):
        pass


class SSDDriverEnter(SSDDriver):
    def __init__(self, nand_path, result_path):
        super().__init__(nand_path, result_path)

    def read(self, addr: int):
        nand_data = ''
        with open(self.nand_path, 'r') as nand_file:
            nand_data = int(nand_file.read().split('\n')[:20][addr])
        nand_hex_string = '0x{:08x}'.format(nand_data)
        with open(self.result_path, 'w') as result_file:
            result_file.write(nand_hex_string)

    def write(self, addr: int, value: int):
        pass