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


def main():

    shell = TestShellApplication()
    while True:
        shell.run()
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()