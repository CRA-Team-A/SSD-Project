import sys


class TestShellApplication:
    def __init__(self):
        pass

    def write(self, address: int, data: str):
        pass

    def read(self, address: int):
        pass

    def fullwrite(self):
        pass

    def fullread(self):
        pass


if __name__ == '__main__':
    while True:
        _input = input()
        print(_input)   # TODO ; will be deleted

        if _input == 'exit':
            sys.exit(0)

        break  # TODO ; will be deleted
