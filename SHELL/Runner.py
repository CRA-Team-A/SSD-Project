from importlib.util import spec_from_file_location, module_from_spec

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
    def __init__(self, shell: TestShellApplication, file_path: str):
        self.shell = shell
        self.file = file_path
        self.scenarios = self.get_scenarios(file_path)
        self.run_list = [line.strip() for line in lines]
        self.scenarios = {
            'FullWriteReadCompare': FullWriteReadCompare(),
            'FullRead10AndCompare': FullRead10AndCompare(),
            'Write10AndCompare': Write10AndCompare(),
            'Loop_WriteAndReadCompare': LoopWriteAndReadCompare()
        }

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
        self.print_head_text(test_type)
        scenario = self.scenarios.get(test_type)
        if scenario:
            result = scenario.run_test(self.shell)
        else:
            result = False
        self.print_tail_text(result)
        return result

    @staticmethod
    def print_header(scenario_name: str):
        print(f"{scenario_name}   ---   Run...", end='', flush=True)

    def print_tail_text(self, result: bool):
        if result:
            print("Pass")
        else:
            print("Fail!")
