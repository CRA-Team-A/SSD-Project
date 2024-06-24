import os
import sys

from SHELL.Runner import Runner

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

sys.path.append(ROOT_DIR)
from SHELL.TestShellApplication import TestShellApplication


def main():
    shell = TestShellApplication()
    runner = Runner(shell)

    while True:
        shell.run(input('Input command: '))


if __name__ == "__main__":
    main()