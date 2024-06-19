import subprocess

EXIT_CODE = 'exit'
WRITE_CODE = 'write'
FULLWRITE_CODE = 'fullwrite'
READ_CODE = 'read'
FULLREAD_CODE = 'fullread'
HELP_CODE = 'help'


class TestShellApplication:
    def __init__(self, ssd):
        self.terminate = False
        self.ssd = ssd

    def run(self, input_command: str):
        is_valid = self.split_and_parse_input_command(input_command)
        if not is_valid:
            return False

        return self.go_execution()

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
        params = [self.execution, self.address, self.data]
        result = subprocess.run(['python', '../SSD/ssd_main.py'] + params, capture_output=True, text=True)
        output = result.stdout.strip()
        if output == 'True':
            output = True
        elif output == 'False':
            output = False
        return output

    def write(self):
        self.execution = 'W'
        return self.run_subprocess()

    def read(self):
        self.execution = 'R'
        return self.run_subprocess()

    def fullwrite(self):
        for each_address in range(100):
            self.address = each_address
            result = self.write()
            if result == False:
                return False
        return True

    def fullread(self):
        for each_address in range(100):
            self.address = each_address
            result = self.read()
            if result == False:
                return False
        return True

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
        return False


def main():
    shell = TestShellApplication(ssd=None)

    while True:
        shell.run(input('Input command: '))
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()
