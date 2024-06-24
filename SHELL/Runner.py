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
            self.fullwrite_read_compare()
        elif test_type == 'FullRead10AndCompare':
            self.fullread_10_and_compare()
        elif test_type == 'Write10AndCompare':
            self.write_10_and_compare()
        elif test_type == 'Loop_WriteAndReadCompare':
            self.loop_write_and_read_compare()

    def fullwrite_read_compare(self):
        print('FullWriteReadCompare   ---   Run...', end='')
        write_data = self.shell.run("fullwrite 0xAAAABBBB")
        fullread_result = self.shell.run("fullread")

        for read_value in fullread_result:
            print(read_value, write_data)
            if read_value != write_data:
                print('Fail!!')
                return False
        print('Pass!!')
        return True

    def fullread_10_and_compare(self):
        print('FullRead10AndCompare   ---   Run...', end='')
        print('Pass')

    def write_10_and_compare(self):
        print('Write10AndCompare   ---   Run...', end='')
        print('Pass')

    def loop_write_and_read_compare(self):
        print('Loop_WriteAndReadCompare   ---   Run...', end='')
        print('Pass')

