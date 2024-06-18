import sys


EXIT_CODE = 'exit'


class TestShellApplication:

    def __init__(self):
        self.terminate = False

    def run(self, inputCommand: str):
        self.split_and_parse_input_command(inputCommand)

    def split_and_parse_input_command(self, inputCommand: str):
        command = inputCommand.split()

        self.execution = command[0]
        if self.execution == EXIT_CODE:
            self.terminate = True

        if len(command) == 3:
            self.address = command[1]
            self.data = command[2]

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


def main():

    shell = TestShellApplication()
    while True:
        shell.run(input('Input command: '))
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()