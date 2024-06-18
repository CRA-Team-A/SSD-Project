import sys


class TestShellApplication:

    def __init__(self, ssd):
        self.terminate = False
        self.ssd = ssd

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
        self.ssd.write(address, data)

    def read(self, address: int):
        pass

    def fullwrite(self, data):
        for each_address in range(100):
            self.write(each_address, data)

    def fullread(self):
        pass

    def help(self):
        pass


def main():

    shell = TestShellApplication(ssd=None)
    while True:
        shell.run()
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()