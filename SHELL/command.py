import os
import subprocess
from abc import ABC, abstractmethod

from SHELL.ssd_handler import SSDHandler

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')
SSD_PATH = os.path.join(ROOT_DIR, 'SSD/ssd_interface.py')
MAX_ADDRESS = 100


def is_valid_address(address: str):
    for num in address:
        if not ord('0') <= ord(num) <= ord('9'):
            return False
    if int(address) < 0 or 99 < int(address):
        return False
    return True


def is_valid_data_format(input_data: str):
    if len(input_data) != 10:
        return False
    if input_data[0] != '0' or input_data[1] != 'x':
        return False
    for num in input_data[2:]:
        if not (ord('0') <= ord(num) <= ord('9') or ord('A') <= ord(num) <= ord('F')):
            return False
    return True


def is_valid_size(start: str, size: str):
    if not size.isdigit():
        return False
    if int(size) <= 0:
        return False
    if int(start) + int(size) > MAX_ADDRESS:
        return False
    return True


class Command(ABC):
    def __init__(self):
        self.ssd = SSDHandler()
        self.params = None

    def execute(self, *args):
        if not self.check_valid(*args):
            print('INVALID COMMAND')
            return
        self.run(*args)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def check_valid(self, *args):
        pass

    @staticmethod
    def print_pass(is_pass: bool):
        if is_pass:
            print("Pass")
        else:
            print("Fail")


class WriteCommand(Command):
    def __init__(self):
        super().__init__()

    def check_valid(self, *args):
        if len(args) != 2:
            return False
        if not is_valid_address(args[0]):
            return False
        if not is_valid_data_format(args[1]):
            return False
        return True

    def run(self, *args):
        self.ssd.write(*args)


class ReadCommand(Command):
    def check_valid(self, *args):
        if len(args) != 1:
            return False
        if not is_valid_address(args[0]):
            return False
        return True

    def run(self, *args):
        ret = self.ssd.read(*args)
        if ret == 0:
            with open(RESULT_PATH, 'r') as fp:
                print(fp.readline().strip())


class FullWriteCommand(Command):
    def check_valid(self, *args):
        if len(args) != 1:
            return False
        if not is_valid_data_format(args[0]):
            return False
        return True

    def run(self, *args):
        for address in range(MAX_ADDRESS):
            self.ssd.write(str(address), args[0])


class FullReadCommand(Command):
    def check_valid(self, *args):
        if len(args) != 0:
            return False
        return True

    def run(self, *args):
        for address in range(MAX_ADDRESS):
            self.ssd.read(str(address))
            with open(RESULT_PATH, 'r') as fp:
                print(fp.readline().strip())


class HelpCommand(Command):
    def check_valid(self, *args):
        if len(args) != 0:
            return False
        return True

    def run(self, *args):
        print(
            'HOW TO TEST SSD',
            'To WRITE new data : write {LBA index} {data}',
            'To READ written data : read {LBA index}',
            'To WRITE data on all LBA : fullwrite {data}',
            'To READ every data from 0~99 LBA : fullread',
            'To finish this app : exit',
            'To repeat this information : help',
            sep='\n')


class TestApp1Command(Command):
    def __init__(self):
        super().__init__()
        self.write_value = '0xABCDFFFF'

    def check_valid(self, *args):
        if len(args) != 0:
            return False
        return True

    def run(self, *args):
        is_pass = True

        # Fullwrite
        for address in range(MAX_ADDRESS):
            self.ssd.write(str(address), self.write_value)

        # Fullread
        for address in range(MAX_ADDRESS):
            self.ssd.read(str(address))
            with open(RESULT_PATH, 'r') as fp:
                read_value = fp.readline().strip()
            print(read_value)
            is_pass &= self.write_value == read_value
        self.print_pass(is_pass)


class TestApp2command(Command):
    def __init__(self):
        super().__init__()
        self.write_1st_value = '0xAAAABBBB'
        self.write_2nd_value = '0x12345678'

    def check_valid(self, *args):
        if len(args) != 0:
            return False
        return True

    def run(self, *args):
        is_pass = True

        # write LBA[0:6] * 30
        for i in range(30):
            for addr in range(6):
                self.ssd.write(str(addr), self.write_1st_value)

        # write LBA[0:6]
        for addr in range(6):
            self.ssd.write(str(addr), self.write_2nd_value)

        # read LBA[0:6]
        for addr in range(6):
            self.ssd.read(str(addr))
            with open(RESULT_PATH, 'r') as fp:
                value = fp.readline().strip()
            print(value)
            is_pass &= self.write_2nd_value == value
        self.print_pass(is_pass)


class EraseCommand(Command):
    def check_valid(self, *args):
        if len(args) != 2:
            return False
        if not is_valid_address(args[0]):
            return False
        if not is_valid_size(*args):
            return False
        return True

    def run(self, *args):
        steps = self.get_steps_with_size(int(args[0]), int(args[1]))
        for n in range(len(steps) - 1):
            size = steps[n + 1] - steps[n]
            self.ssd.erase(steps[n], size)

    @staticmethod
    def get_steps_with_size(start, size):
        end = start + size
        numbers = list(range(start, end, 10))
        if numbers and numbers[-1] != end:
            numbers.append(end)
        elif not numbers:
            numbers.append(end)

        return numbers


class EraseRangeCommand(Command):
    def check_valid(self, *args):
        if len(args) != 2:
            return False
        if not is_valid_address(args[0]):
            return False
        if not is_valid_address(args[1]):
            return False
        if int(args[0]) >= int(args[1]):
            return False
        return True

    def run(self, *args):
        steps = self.get_steps_with_end(int(args[0]), int(args[1]))
        for n in range(len(steps) - 1):
            size = steps[n + 1] - steps[n]
            self.ssd.erase(steps[n], size)

    @staticmethod
    def get_steps_with_end(start, end):
        numbers = list(range(start, end, 10))
        if numbers and numbers[-1] != end:
            numbers.append(end)
        elif not numbers:
            numbers.append(end)

        return numbers


class ExitCommand(Command):
    def check_valid(self, *args):
        return True

    def run(self, *args):
        exit(0)


class InvalidCommand(Command):
    def check_valid(self, *args):
        return True

    def run(self, *args):
        print("INVALID COMMAND")
