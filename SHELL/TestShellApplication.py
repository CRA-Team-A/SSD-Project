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

    def help(self):
        pass


def verify_if_input_is_ok(inputs):
    pass


if __name__ == '__main__':
    while True:
        _inputs = input().split()
        verify_if_input_is_ok(_inputs)
        if len(_inputs) == 3:
            execution, address, data = _inputs
        else:
            execution = _inputs

        if execution == 'exit':
            sys.exit(0)

        break  # TODO ; will be deleted
