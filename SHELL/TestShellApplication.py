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


def main():

    shell = TestShellApplication(ssd=None)
    while True:
        shell.run(input('Input command: '))
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()