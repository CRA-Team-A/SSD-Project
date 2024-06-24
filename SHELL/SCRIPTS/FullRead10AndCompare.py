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


class FullRead10AndCompare(TestScenario):
    def run_test(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.shell.run("fullread")
        output1 = f.getvalue()
        with redirect_stdout(f):
            for i in range(2):
                self.shell.run("fullread")
            output2 = f.getvalue()

        if output1 * 3 == output2:
            return True
        return False
