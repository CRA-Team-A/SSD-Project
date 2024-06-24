from TestShellApplication import *

from SCRIPTS.fullwrite_read_compare import FullWriteReadCompare
from SCRIPTS.fullread_10_and_compare import FullRead10AndCompare
from SCRIPTS.write_10_and_compare import Write10AndCompare
from SCRIPTS.loop_write_and_read_compare import LoopWriteAndReadCompare


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
