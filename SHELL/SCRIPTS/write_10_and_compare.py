from SHELL.TestShellApplication import *
from SHELL.SCRIPTS.test_scenario import TestScenario

import io
from contextlib import redirect_stdout


class Write10AndCompare(TestScenario):
    def run_test(self, shell: TestShellApplication):
        f = io.StringIO()
        with redirect_stdout(f):
            for i in range(10):
                shell.run("write 5 0xAABBAABB")
                shell.run("read 5")
        output = f.getvalue()

        if output == '\n'.join(["0xAABBAABB"] * 10) + '\n':
            return True
        return False