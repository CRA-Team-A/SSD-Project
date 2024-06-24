from importlib.util import spec_from_file_location, module_from_spec

from TestShellApplication import *


class Runner:
    def __init__(self, shell: TestShellApplication, file_path: str):
        self.shell = shell
        self.file = file_path
        self.scenarios = self.get_scenarios(file_path)

    @staticmethod
    def get_scenarios(run_list):
        with open(run_list, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]

    def run(self):
        for scenario_name in self.scenarios:
            self.print_header(scenario_name)
            scenario = self.import_scenario(scenario_name)
            if scenario is None or not self.run_test(scenario):
                self.print_fail()
            self.print_pass()

    @staticmethod
    def import_scenario(scenario_name):
        # 모듈의 파일 경로 지정
        module_path = os.path.join(ROOT_DIR, "SHELL", "SCRIPTS", f"{scenario_name}.py")

        # 모듈 스펙을 생성하고 모듈을 로드
        spec = spec_from_file_location(scenario_name, module_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        # 모듈에서 클래스 가져오기
        return getattr(module, scenario_name)()

    def run_test(self, test_type: str):
        self.print_header(test_type)
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

    @staticmethod
    def print_header(scenario_name: str):
        print(f"{scenario_name}   ---   Run...", end='', flush=True)

    @staticmethod
    def print_fail():
        print("FAIL!")
        exit(1)

    def fullwrite_read_compare(self):
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
