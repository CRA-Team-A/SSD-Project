from abc import ABC, abstractmethod


class SSDDriver(ABC):
    def __init__(self, nand_path, result_path):
        self.nand_path = nand_path
        self.result_path = result_path
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, value):
        pass
