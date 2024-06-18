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


class SSDDriverComma(SSDDriver):
    def __init__(self, nand_path, result_path):
        super().__init__(nand_path, result_path)

    def read(self):
        buffer = ''
        with open(self.nand_path, 'r') as nand:
            buffer = nand.readlines()

    def write(self):
        pass

