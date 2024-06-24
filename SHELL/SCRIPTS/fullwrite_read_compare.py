from SHELL.TestShellApplication import *
from SHELL.SCRIPTS.test_scenario import TestScenario

import io
from contextlib import redirect_stdout


class FullWriteReadCompare(TestScenario):
    def run_test(self, shell: TestShellApplication):
        f = io.StringIO()
        with redirect_stdout(f):
            shell.run("fullwrite 0xAAAABBBB")
            shell.run("fullread")
        output = f.getvalue()

        if output == '\n'.join(["0xAAAABBBB"] * 100) + '\n':
            return True
        return False