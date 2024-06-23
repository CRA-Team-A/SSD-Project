from SHELL.command import *


EXIT_CODE = 'exit'
WRITE_CODE = 'write'
FULLWRITE_CODE = 'fullwrite'
READ_CODE = 'read'
FULLREAD_CODE = 'fullread'
HELP_CODE = 'help'
ERASE_CODE = 'erase'
ERASE_RANGE_CODE = 'erase_range'
INVALID_CODE = 'invalid'

TESTAPP2 = 'testapp2'
TESTAPP1 = 'testapp1'

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')
SSD_PATH = os.path.join(ROOT_DIR, 'SSD/ssd_interface.py')


class TestShellApplication:
    cmd_table = {
        WRITE_CODE: WriteCommand,
        READ_CODE: ReadCommand,
        FULLWRITE_CODE: FullWriteCommand,
        FULLREAD_CODE: FullReadCommand,
        ERASE_CODE: EraseCommand,
        ERASE_RANGE_CODE: EraseRangeCommand,
        TESTAPP1: TestApp1Command,
        TESTAPP2: TestApp2command,
        HELP_CODE: HelpCommand,
        EXIT_CODE: ExitCommand,
        INVALID_CODE: InvalidCommand
    }

    def __init__(self):
        self.terminate = False

    def run(self, input_command: str):
        inputs = input_command.split()
        command = input_command.split()[0] if inputs else ''
        args = tuple(inputs[1:]) if len(inputs) > 1 else ()
        self.go_execution(command, *args)

    def go_execution(self, command, *args):
        # first way : using getattr
        # command_name = f"{self.execution.capitalize()}Command"
        # cmd = getattr(sys.modules[__name__], command_name)()

        # second way : using dict
        cmd = self.cmd_table.get(command) if command in self.cmd_table else InvalidCommand
        return cmd().execute(*args)


def main():
    shell = TestShellApplication()

    while True:
        shell.run(input('Input command: '))


if __name__ == "__main__":
    main()
