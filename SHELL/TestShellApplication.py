import sys


class TestShellApplication:

    def __init__(self):
        self.__terminate = False

    def run(self):
        __inputCommand = input('Input command: ').split()

        if len(__inputCommand) == 3:
            execution, address, data = __inputCommand
        else:
            execution = __inputCommand

        if execution[0] == 'exit':
            self.__terminate = True

    def is_exit(self):
        return self.__terminate

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