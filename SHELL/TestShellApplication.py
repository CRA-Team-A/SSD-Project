import os
import subprocess

MAX_ADDRESS_FOR_FULL = 100

EXIT_CODE = 'exit'
WRITE_CODE = 'write'
FULLWRITE_CODE = 'fullwrite'
READ_CODE = 'read'
FULLREAD_CODE = 'fullread'
HELP_CODE = 'help'

TESTAPP2 = 'testapp2'
TESTAPP1 = 'testapp1'

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')
SSD_PATH = os.path.join(ROOT_DIR, 'SSD/ssd_interface.py')


class TestShellApplication:
    def __init__(self):
        self.terminate = False
        self.verbose = True

    def run(self, input_command: str):
        self.init_command()
        is_valid = self.split_and_parse_input_command(input_command)
        if not is_valid:
            return False
        return self.go_execution()

    def init_command(self):
        self.execution = None
        self.address = None
        self.data = None

    def go_execution(self):
        if self.execution == WRITE_CODE:
            return self.write()
        elif self.execution == READ_CODE:
            return self.read()
        elif self.execution == FULLWRITE_CODE:
            return self.fullwrite()
        elif self.execution == FULLREAD_CODE:
            return self.fullread()
        elif self.execution == HELP_CODE:
            return self.help()
        elif self.execution == TESTAPP1:
            return self.test_app_1()
        elif self.execution == TESTAPP2:
            return self.test_app_2()

    def test_app_1(self):
        self.verbose = False
        write_data = '0xABCDFFFF'
        self.run("fullwrite " + write_data)
        fullread_result = self.run("fullread")
        self.verbose = True
        for read_value in fullread_result:
            if read_value != write_data:
                return False
        return True

    def split_and_parse_input_command(self, input_command: str):
        command = input_command.split()
        if not self.is_valid_command(command):
            print('INVALID COMMAND')
            return False

        self.execution = command[0]
        if self.execution == EXIT_CODE:
            self.terminate = True
            return False

        if self.execution == WRITE_CODE:
            self.address = command[1]
            self.data = command[2]
        elif self.execution == FULLWRITE_CODE:
            self.data = command[1]
        elif self.execution == READ_CODE:
            self.address = command[1]

        return True

    def is_exit(self):
        return self.terminate

    def run_subprocess(self):
        if self.execution == 'W':
            params = [self.execution, self.address, self.data]
        elif self.execution == 'R':
            params = [self.execution, self.address]
        else:
            raise NotImplementedError
        result = subprocess.run(['python', SSD_PATH] + params, capture_output=True, text=True, check=True)
        if result.returncode == 0:
            return True
        return False

    def write(self):
        self.execution = 'W'
        return self.run_subprocess()

    def read(self):
        self.execution = 'R'
        if self.run_subprocess():
            with open(RESULT_PATH, 'r') as fp:
                written_value = fp.readline().split(',')[0]
                if self.verbose:
                    print(written_value)
            return written_value
        return False

    def fullwrite(self):
        for each_address in range(MAX_ADDRESS_FOR_FULL):
            self.address = str(each_address)
            result = self.write()
            if result == False:
                return False
        return True

    def fullread(self):
        result_array = list()
        for each_address in range(MAX_ADDRESS_FOR_FULL):
            self.address = str(each_address)
            result = self.read()
            result_array.append(result)
            if result == False:
                return False
        return result_array

    def help(self):
        print(
            'HOW TO TEST SSD',
            'To WRITE new data : write {LBA index} {data}',
            'To READ written data : read {LBA index}',
            'To WRITE data on all LBA : fullwrite {data}',
            'To READ every data from 0~99 LBA : fullread',
            'To finish this app : exit',
            'To repeat this information : help',
            sep='\n')

    def is_valid_address(self, address: int):
        for num in address:
            if not ord('0') <= ord(num) <= ord('9'):
                return False
        if int(address) < 0 or 99 < int(address):
            return False
        return True

    def is_valid_data_format(self, input_data: str):
        if len(input_data) != 10:
            return False
        if input_data[0] != '0' or input_data[1] != 'x':
            return False
        for num in input_data[2:]:
            if not (ord('0') <= ord(num) <= ord('9') or ord('A') <= ord(num) <= ord('F')):
                return False
        return True

    def is_valid_command(self, input_command_elements: list):
        if len(input_command_elements) > 3 or len(input_command_elements) <= 0:
            return False

        if input_command_elements[0] == WRITE_CODE:
            if len(input_command_elements) != 3:
                return False
            if not self.is_valid_address(input_command_elements[1]):
                return False
            if not self.is_valid_data_format(input_command_elements[2]):
                return False
            return True
        elif input_command_elements[0] == READ_CODE:
            if len(input_command_elements) != 2:
                return False
            if not self.is_valid_address(input_command_elements[1]):
                return False
            return True
        elif input_command_elements[0] == FULLWRITE_CODE:
            if len(input_command_elements) != 2:
                return False
            if not self.is_valid_data_format(input_command_elements[1]):
                return False
            return True
        elif input_command_elements[0] == FULLREAD_CODE:
            if len(input_command_elements) != 1:
                return False
            return True
        elif input_command_elements[0] == HELP_CODE:
            if len(input_command_elements) != 1:
                return False
            return True
        elif input_command_elements[0] == EXIT_CODE:
            if len(input_command_elements) != 1:
                return False
            return True
        elif input_command_elements[0] == TESTAPP1:
            if len(input_command_elements) != 1:
                return False
            return True
        elif input_command_elements[0] == TESTAPP2:
            if len(input_command_elements) != 1:
                return False
            return True
        return False

    def test_app_2(self):
        self.verbose = False
        for i in range(30):
            for addr in range(6):
                self.run('write %s 0xAAAABBBB' % str(addr))
        for addr in range(6):
            self.run('write %s 0x12345678' % addr)
        for addr in range(6):
            self.run('read %s' % addr)
            with open(RESULT_PATH, 'r') as fp:
                written_value = fp.readline().split(',')[0]
                if written_value != '0x12345678':
                    self.verbose = True
                    return False
        self.verbose = True
        return True


def main():
    shell = TestShellApplication()

    while True:
        shell.run(input('Input command: '))
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()
