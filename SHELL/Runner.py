from TestShellApplication import *


class Runner:
    def __init__(self, shell: TestShellApplication, run_list: str):
        self.shell = shell
        with open(run_list, 'r') as file:
            lines = file.readlines()
        self.run_list = [line.strip() for line in lines]

    def run(self):
        for each_test in self.run_list:
            if self.run_test(each_test) == False:
                break

    def run_test(self, test_type: str):
        self.print_head_text(test_type)
        if test_type == 'FullWriteReadCompare':
            result = self.fullwrite_read_compare()
        elif test_type == 'FullRead10AndCompare':
            result = self.fullread_10_and_compare()
        elif test_type == 'Write10AndCompare':
            result = self.write_10_and_compare()
        elif test_type == 'Loop_WriteAndReadCompare':
            result = self.loop_write_and_read_compare()
        self.print_tail_text(result)
        return result

    def print_head_text(self, text: str):
        print(text, '   ---   Run...', end='', flush=True)

    def print_tail_text(self, result: str):
        if result == True:
            print("Pass")
        else:
            print("Fail!")

    def fullwrite_read_compare(self):
        return False
        write_data = self.shell.run("fullwrite 0xAAAABBBB")
        fullread_result = self.shell.run("fullread")
        for read_value in fullread_result:
            print(read_value, write_data)
            if read_value != write_data:
                return False
        return True

    def fullread_10_and_compare(self):
        read_value_compare = self.shell.run("fullread")
        for i in range(9):
            read_value = self.shell.run("fullread")
            if read_value != read_value_compare:
                return False
        return True

    def write_10_and_compare(self):
        for i in range(10):
            write_data = self.shell.run("write 5 0xAAAABBBB")
            read_value = self.shell.run("read 5")
            if read_value != write_data:
                return False
        return True

    def loop_write_and_read_compare(self):
        for i in range(10):
            address = str(i)
            write_data = self.shell.run("write " + address + " 0xAAAABBBB")
            read_value = self.shell.run("read " + address)
            if read_value != write_data:
                return False
        return True

