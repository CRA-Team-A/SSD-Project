import io
import os
import sys
from contextlib import redirect_stdout

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)
from SHELL.SCRIPTS.test_scenario import TestScenario


class FullWriteReadCompare(TestScenario):
    def run_test(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.shell.run("fullwrite 0xAAAABBBB")
            self.shell.run("fullread")
        output = f.getvalue()

        if output == '\n'.join(["0xAAAABBBB"] * 100) + '\n':
            return True
        return False
