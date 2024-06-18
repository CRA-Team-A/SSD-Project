from abc import ABC, abstractmethod
import os


class SSDDriver(ABC):
    def __init__(self, nand_path, result_path):
        # if not os.path.isfile(nand_path):
        #     with open(nand_path, 'w') as file:
        #         pass
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
        if not os.path.exists(nand_path):
            with open(nand_path, 'w') as file:
                file.write(','.join([str(0)]*100))
        pass

    def read(self, addr: int):
        self.check_exist_nand()
        values = self.read_nand()
        self.save_result(self.convert_to_hex(values[addr]))

    def read_nand(self):
        with open(self.nand_path, 'r') as nand:
            buffer = nand.readline().strip()
        return [int(lba) for lba in buffer.split(',')]

    def check_exist_nand(self):
        if not os.path.exists(self.nand_path):
            raise FileNotFoundError

    def save_result(self, value):
        with open(self.result_path, 'w') as result:
            result.write(value)

    def save_nand(self, values: list):
        with open(self.nand_path, 'w') as nand:
            nand.write(','.join(values))

    @staticmethod
    def convert_to_hex(decimal: int):
        return '0x{:08x}'.format(decimal)

    @staticmethod
    def convert_to_dec(hexadecimal: str):
        return int(hexadecimal, 16)

    def write(self, addr, value):
        values = self.read_nand()
        values[addr] = self.convert_to_dec(value)
        self.save_nand([str(v) for v in values])




