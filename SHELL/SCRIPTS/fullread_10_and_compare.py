from SHELL.TestShellApplication import *
from SHELL.SCRIPTS.test_scenario import TestScenario

import io
from contextlib import redirect_stdout


class FullRead10AndCompare(TestScenario):
    def run_test(self, shell: TestShellApplication):
        f = io.StringIO()
        with redirect_stdout(f):
            shell.run("fullread")
        output1 = f.getvalue()
        with redirect_stdout(f):
            for i in range(2):
                shell.run("fullread")
            output2 = f.getvalue()

        if output1 * 3 == output2:
            return True
        return False