import sys


class TestShellApplication:

    def __init__(self):
        self.terminate = False

    def run(self):
        inputCommand = input('Input command: ').split()

        if len(inputCommand) == 3:
            execution, address, data = inputCommand
        else:
            execution = inputCommand

        if execution[0] == 'exit':
            self.terminate = True

    def is_exit(self):
        return self.terminate

    def write(self, address: int, data: str):
        pass

    def read(self, address: int):
        pass

    def fullwrite(self):
        pass

    def fullread(self):
        pass

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


def main():
    shell = TestShellApplication()
    while True:
        shell.run()
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()
