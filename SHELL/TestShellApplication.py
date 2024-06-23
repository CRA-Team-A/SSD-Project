import os
import subprocess
import sys
from abc import ABC, abstractmethod

from SHELL.command import *
from SHELL.ssd_handler import SSDHandler

MAX_ADDRESS = 100

EXIT_CODE = 'exit'
WRITE_CODE = 'write'
FULLWRITE_CODE = 'fullwrite'
READ_CODE = 'read'
FULLREAD_CODE = 'fullread'
HELP_CODE = 'help'
ERASE_CODE = 'erase'
ERASE_RANGE_CODE = 'erase_range'

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
        'write': WriteCommand,
        'read': ReadCommand,
        'fullwrite': FullWriteCommand,
        'fullread': FullReadCommand,
        'erase': EraseCommand,
        'erase_range': EraseRangeCommand,
        'testapp1': TestApp1Command,
        'testapp2': TestApp2command,
        'help': HelpCommand,
        'exit': ExitCommand,
        'invalid': InvalidCommand
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

    def is_exit(self):
        return self.terminate


def main():
    shell = TestShellApplication()

    while True:
        shell.run(input('Input command: '))
        if shell.is_exit():
            break


if __name__ == "__main__":
    main()
