from TestShellApplication import *


class Runner:
    def __init__(self, shell: TestShellApplication, run_list: str):
        self.shell = shell
        with open(run_list, 'r') as file:
            lines = file.readlines()
        self.run_list = [line.strip() for line in lines]

    def run(self):
        for each_test in self.run_list:
            self.run_test(each_test)

    def run_test(self, test_type: str):
        if test_type == 'FullWriteReadCompare':
            self.full_write_read_compare()
        elif test_type == 'FullRead10AndCompare':
            self.full_read_10_and_compare()
        elif test_type == 'Write10AndCompare':
            self.write_10_and_compare()
        elif test_type == 'Loop_WriteAndReadCompare':
            self.loop_write_and_read_compare()

    def full_write_read_compare(self):
        print('FullRead10AndCompare')
        pass

    def full_read_10_and_compare(self):
        print('FullWriteReadCompare')
        pass

    def write_10_and_compare(self):
        print('Write10AndCompare')
        pass

    def loop_write_and_read_compare(self):
        print('Loop_WriteAndReadCompare')
        pass

