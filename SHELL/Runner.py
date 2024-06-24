from TestShellApplication import *
from abc import ABC, abstractmethod

import io
from contextlib import redirect_stdout


class TestScenario(ABC):
    @abstractmethod
    def run_test(self, shell: TestShellApplication):
        pass


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


class Runner:
    def __init__(self, shell: TestShellApplication, run_list: str):
        self.shell = shell
        with open(run_list, 'r') as file:
            lines = file.readlines()
        self.run_list = [line.strip() for line in lines]
        self.scenarios = {
            'FullWriteReadCompare': FullWriteReadCompare(),
            'FullRead10AndCompare': FullRead10AndCompare(),
            'Write10AndCompare': Write10AndCompare(),
            'Loop_WriteAndReadCompare': LoopWriteAndReadCompare()
        }

    def run(self):
        for each_test in self.run_list:
            if self.run_test(each_test) == False:
                break

    def run_test(self, test_type: str):
        self.print_head_text(test_type)
        scenario = self.scenarios.get(test_type)
        if scenario:
            result = scenario.run_test(self.shell)
        else:
            result = False
        self.print_tail_text(result)
        return result

    def print_head_text(self, text: str):
        print(text, '   ---   Run...', end='', flush=True)

    def print_tail_text(self, result: bool):
        if result:
            print("Pass")
        else:
            print("Fail!")
