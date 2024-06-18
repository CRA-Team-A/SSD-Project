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
        if not os.path.exists(self.nand_path):
            raise FileNotFoundError
        with open(self.nand_path, 'r') as nand:
            buffer = nand.readline().strip()

        data = buffer.split(',')
        output = self.convert_to_hex(int(data[addr]))

        with open(self.result_path, 'w') as result:
            result.write(output)

    def convert_to_hex(self, hexadecimal: int):
        return '0x{:08x}'.format(hexadecimal)


    def write(self, addr, value):
        pass

