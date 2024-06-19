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


class SSDDriverEnter(SSDDriver):
    def __init__(self, nand_path, result_path):
        super().__init__(nand_path, result_path)
        if not os.path.isfile(nand_path):
            self.write_nand_file([0 for i in range(MAX_DATA_LENGTH)])

    @staticmethod
    def convert_decimal_to_hex(decimal: int):
        return '0x' + '{:08x}'.format(decimal).upper()

    @staticmethod
    def convert_hex_to_decimal(value: str):
        return int(value, 16)

    def write_nand_file(self, raw_data: list):
        result = ""
        for i in range(MAX_DATA_LENGTH):
            result += str(raw_data[i]) + "\n"
        with open(self.nand_path, 'w') as nand_file:
            nand_file.write(result)

    def read_nand_file_data(self):
        with open(self.nand_path, 'r') as nand_file:
            return nand_file.read().split('\n')

    def read(self, addr: int):
        nand_data = ''
        with open(self.nand_path, 'r') as nand_file:
            nand_data = int(self.read_nand_file_data()[:MAX_DATA_LENGTH][addr])
        with open(self.result_path, 'w') as result_file:
            result_file.write(self.convert_decimal_to_hex(nand_data))

    def write(self, addr: int, value: str):
        with open(self.nand_path, 'r') as nand_file:
            nand_raw_data = list(map(int, self.read_nand_file_data()[:MAX_DATA_LENGTH]))
        nand_raw_data[addr] = self.convert_hex_to_decimal(value)
        self.write_nand_file(nand_raw_data)


class SSDDriverComma(SSDDriver):
    def __init__(self, nand_path: str, result_path: str):
        super().__init__(nand_path, result_path)
        if not os.path.exists(nand_path):
            with open(nand_path, 'w') as file:
                file.write(','.join([str(0)] * 100))

    def read(self, addr: int):
        self.check_exist_nand()
        values = self.read_nand()
        self.save(self.result_path, self.convert_to_hex(values[addr]))

    def read_nand(self) -> list:
        with open(self.nand_path, 'r') as nand:
            buffer = nand.readline().strip()
        return [int(lba) for lba in buffer.split(',')]

    def check_exist_nand(self):
        if not os.path.exists(self.nand_path):
            raise FileNotFoundError

    @staticmethod
    def save(path: str, text: str):
        with open(path, 'w') as file:
            file.write(text)

    @staticmethod
    def convert_to_hex(decimal: int) -> str:
        return '0x'+'{:08x}'.format(decimal).upper()

    @staticmethod
    def convert_to_dec(hexadecimal: str) -> int:
        return int(hexadecimal, 16)

    def write(self, addr: int, value: str):
        values = self.read_nand()
        values[addr] = self.convert_to_dec(value)
        self.save(self.nand_path, ','.join([str(v) for v in values]))
