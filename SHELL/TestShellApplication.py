import sys


EXIT_CODE = 'exit'


class TestShellApplication:

    def __init__(self, ssd):
        self.terminate = False
        self.ssd = ssd

    def run(self, input_command: str):
        self.split_and_parse_input_command(input_command)

    def split_and_parse_input_command(self, input_command: str):
        command = input_command.split()

        self.execution = command[0]
        if self.execution == EXIT_CODE:
            self.terminate = True

        if len(command) == 3:
            self.address = command[1]
            self.data = command[2]

    def is_exit(self):
        return self.terminate

    def write(self, address: int, data: str):
        self.ssd.write(address, data)

    def read(self, address: int):
        self.ssd.read(address)

    def fullwrite(self, data):
        for each_address in range(100):
            self.write(each_address, data)

    def fullread(self):
        for each_address in range(100):
            self.read(each_address)

    def help(self):
        pass

    def is_valid_address(self, address):
        for num in address:
            if not ord('0') <= ord(num) <= ord('9'):
                return False
        if int(address) < 0 or 99 < int(address):
            return False
        return True

    def is_valid_data_format(self, input_data):
        if len(input_data) != 10:
            return False
        if input_data[0] != '0' or input_data[1] != 'x':
            return False
        for num in input_data[2:]:
            if not (ord('0') <= ord(num) <= ord('9') or ord('A') <= ord(num) <= ord('F')):
                return False
        return True

    def is_valid_command(self, input_commands):
        if len(input_commands) > 3:
            return False
        if input_commands[0] == 'write':
            if len(input_commands) != 3:
                return False
            if not self.is_valid_address(input_commands[1]):
                return False
            if not self.is_valid_data_format(input_commands[2]):
                return False
            return True



    shell = TestShellApplication(ssd=None)

    while True:
        shell.run(input('Input command: '))
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()
