import os
import subprocess
import sys
from abc import ABC, abstractmethod

MAX_ADDRESS_FOR_FULL = 100

EXIT_CODE = 'exit'
WRITE_CODE = 'write'
FULLWRITE_CODE = 'fullwrite'
READ_CODE = 'read'
FULLREAD_CODE = 'fullread'
HELP_CODE = 'help'
ERASE_CODE = 'erase'
ERASE_RANGE_CODE = 'erase_range'

TESTAPP2 = 'testapp2'
TESTAPP1 = 'testapp1'

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')
SSD_PATH = os.path.join(ROOT_DIR, 'SSD/ssd_interface.py')


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


def is_valid_size(size: str):
    for num in size:
        if not ord('0') <= ord(num) <= ord('9'):
            return False
    if int(size) <= 0 or int(size) > 10:
        return False
    return True


class Command(ABC):

    def __init__(self):
        self.params = None

    def execute(self, input_command_elements: list):
        if not self.is_valid_command(input_command_elements):
            print('INVALID COMMAND')
            return False
        self.set_param(input_command_elements)
        return self.run()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def set_param(self, input_command_elements: list):
        pass

    @abstractmethod
    def is_valid_command(self, input_command_elements: list):
        pass


class WriteCommand(Command):
    def __init__(self):
        super().__init__()

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 3:
            return False
        if not is_valid_address(input_command_elements[1]):
            return False
        if not is_valid_data_format(input_command_elements[2]):
            return False
        return True

    def set_param(self, input_command_elements: list):
        self.params = ['W', input_command_elements[1], input_command_elements[2]]

    def run(self):
        result = subprocess.run(['python', SSD_PATH] + self.params, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            return True
        return False


class FullWriteCommand(Command):
    def __init__(self):
        super().__init__()
        self.write_cmd = WriteCommand()
        self.address = None

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 2:
            return False
        if not is_valid_data_format(input_command_elements[1]):
            return False
        return True

    def set_param(self, input_command_elements: list):
        self.params = ['W', input_command_elements[1]]

    def run(self):
        for each_address in range(MAX_ADDRESS_FOR_FULL):
            self.write_cmd.set_param([self.params[1], str(each_address), self.params[1]])
            result = self.write_cmd.run()
            if result == False:
                return False
        return True


class ReadCommand(Command):
    def __init__(self):
        super().__init__()

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 2:
            return False
        if not is_valid_address(input_command_elements[1]):
            return False
        return True

    def set_param(self, input_command_elements: list):
        self.params = ['R', input_command_elements[1]]

    def run(self):
        result = subprocess.run(['python', SSD_PATH] + self.params, capture_output=True, text=True, check=True)
        if result.returncode == 0:
            with open(RESULT_PATH, 'r') as fp:
                written_value = fp.readline().split(',')[0]
                print(written_value)
            return written_value
        return False


class FullReadCommand(Command):
    def __init__(self):
        super().__init__()
        self.read_cmd = ReadCommand()

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 1:
            return False
        return True

    def set_param(self, input_command_elements: list):
        self.params = ['R']

    def run(self):
        result_array = list()
        for each_address in range(MAX_ADDRESS_FOR_FULL):
            self.read_cmd.set_param([self.params[0], str(each_address)])
            result = self.read_cmd.run()
            result_array.append(result)
            if result == False:
                return False
        return result_array


class HelpCommand(Command):
    def __init__(self):
        super().__init__()

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 1:
            return False
        return True

    def set_param(self, input_command_elements: list):
        pass

    def run(self):
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
        self.full_write_cmd = FullWriteCommand()
        self.full_read_cmd = FullReadCommand()

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 1:
            return False
        return True

    def set_param(self, input_command_elements: list):
        pass

    def run(self):
        write_data = '0xABCDFFFF'
        self.full_write_cmd.set_param(['fullwrite', write_data])
        self.full_write_cmd.run()
        self.full_read_cmd.set_param(['fullread'])
        fullread_result = self.full_read_cmd.run()
        for read_value in fullread_result:
            if read_value != write_data:
                return False
        return True


class TestApp2command(Command):
    def __init__(self):
        super().__init__()
        self.write_cmd = WriteCommand()
        self.read_cmd = ReadCommand()

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 1:
            return False
        return True

    def set_param(self, input_command_elements: list):
        pass

    def run(self):
        for i in range(30):
            for addr in range(6):
                self.write_cmd.set_param(['W', str(addr), '0xAAAABBBB'])
                self.write_cmd.run()
        for addr in range(6):
            self.write_cmd.set_param(['W', str(addr), '0x12345678'])
            self.write_cmd.run()
        for addr in range(6):
            self.read_cmd.set_param(['W', str(addr)])
            self.read_cmd.run()
            with open(RESULT_PATH, 'r') as fp:
                written_value = fp.readline().split(',')[0]
                if written_value != '0x12345678':
                    return False
        return True


class EraseCommand(Command):

    def __init__(self):
        super().__init__()

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 3:
            return False
        if not is_valid_address(input_command_elements[1]):
            return False
        if not is_valid_size(input_command_elements[2]):
            return False
        if int(input_command_elements[1]) + int(input_command_elements[2]) >= 100:
            return False
        return True

    def set_param(self, input_command_elements: list):
        self.params = ['E', input_command_elements[1], input_command_elements[2]]

    def run(self):
        result = subprocess.run(['python', SSD_PATH] + self.params, capture_output=True, text=True, check=True)
        if result.returncode == 0:
            return True
        return False


class EraseRangeCommand(Command):

    def __init__(self):
        super().__init__()
        self.erase_cmd = EraseCommand()

    def set_param(self, input_command_elements: list):
        self.params = ['E',
                       input_command_elements[1],
                       str(int(input_command_elements[2]) - int(input_command_elements[1]))]

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) != 3:
            return False
        if not is_valid_address(input_command_elements[1]):
            return False
        if not is_valid_address(input_command_elements[2]):
            return False
        if int(input_command_elements[1]) >= int(input_command_elements[2]):
            return False
        return True

    def run(self):
        if int(self.params[2]) > 10:
            total_size = int(self.params[2])
            div = 10
            while total_size:
                self.params[2] = str(min(div, total_size))
                self.erase_cmd.set_param(self.params)
                result = self.erase_cmd.run()
                if result == False:
                    return False
                total_size = max(0, total_size - div)
                if total_size:
                    self.params[1] = str(int(self.params[1]) + int(self.params[2]))
        else:
            self.erase_cmd.set_param(self.params)
            result = self.erase_cmd.run()
        return result


class ExitCommand(Command):
    def is_valid_command(self, input_command_elements: list):
        pass

    def set_param(self, input_command_elements: list):
        pass

    def run(self):
        exit(0)


class InvalidCommand(Command):
    def is_valid_command(self, input_command_elements: list):
        pass

    def set_param(self, input_command_elements: list):
        pass

    def run(self):
        print("INVALID COMMAND")



class TestShellApplication:
    cmd_table = {
        'write': WriteCommand,
        'read': ReadCommand,
        'fullwrite': FullWriteCommand,
        'fullread': FullReadCommand,
        'erase': EraseCommand,
        'erase_range': EraseRangeCommand,
        'testapp1': TestApp1Command,
        'testapp2': TestApp2command,
        'help': HelpCommand,
        'exit': ExitCommand,
        'invalid': InvalidCommand
    }

    def __init__(self):
        self.terminate = False

    def run(self, input_command: str):
        if len(input_command.split()) > 3 or len(input_command.split()) <= 0:
            print('INVALID COMMAND')
            return False
        self.execution = input_command.split()[0]
        return self.go_execution(input_command)

    def init_command(self, input_command: str):
        self.execution = input_command.split()[0]

    def go_execution(self, input_command=None):
        # if self.execution == EXIT_CODE:
        #     self.terminate = True
        #     return False
        #
        # cmd = None
        # if self.execution == WRITE_CODE:
        # cmd = WriteCommand()
        # elif self.execution == READ_CODE:
        #     cmd = ReadCommand()
        # elif self.execution == FULLWRITE_CODE:
        #     cmd = FullwriteCommand()
        # elif self.execution == FULLREAD_CODE:
        #     cmd = FullreadCommand()
        # elif self.execution == HELP_CODE:
        #     cmd = HelpCommand()
        # elif self.execution == TESTAPP1:
        #     cmd = Testapp1Command()
        # elif self.execution == TESTAPP2:
        #     cmd = Testapp2Command()
        # elif self.execution == ERASE_CODE:
        #     cmd = EraseCommand()
        # elif self.execution == ERASE_RANGE_CODE:
        #     cmd = EraserangeCommand()

        # first way : using getattr
        # command_name = f"{self.execution.capitalize()}Command"
        # cmd = getattr(sys.modules[__name__], command_name)()

        # second way : using dict
        cmd = self.cmd_table.get(self.execution) if self.execution in self.cmd_table else InvalidCommand
        return cmd().execute(input_command.split())

    def is_exit(self):
        return self.terminate


def main():
    shell = TestShellApplication()

    while True:
        shell.run(input('Input command: '))
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()
