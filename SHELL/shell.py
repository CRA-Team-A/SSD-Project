import os
import sys

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

sys.path.append(ROOT_DIR)
from SHELL.TestShellApplication import TestShellApplication
from SHELL.Runner import Runner


def main():
    shell = TestShellApplication()

    while True:
        user_input = input('Input command: ')

        if os.path.exists(user_input):
            runner = Runner(shell, user_input)
            runner.run()
        else:
            shell.run(user_input)


if __name__ == "__main__":
    main()
