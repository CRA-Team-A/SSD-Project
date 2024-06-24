from SHELL.TestShellApplication import *
from SHELL.SCRIPTS.test_scenario import TestScenario

import io
from contextlib import redirect_stdout


class LoopWriteAndReadCompare(TestScenario):
    def run_test(self, shell: TestShellApplication):
        f = io.StringIO()
        with redirect_stdout(f):
            for i in range(10):
                address = str(i)
                shell.run("write " + address + " 0xBBBBAAAA")
                shell.run("read " + address)
        output = f.getvalue()

        if output == '\n'.join(["0xBBBBAAAA"] * 10) + '\n':
            return True
        return False