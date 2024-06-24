from importlib.util import spec_from_file_location, module_from_spec

from test_shell_application import *


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
            if scenario is None or not scenario.run_test():
                self.print_fail()
            self.print_pass()

    def import_scenario(self, scenario_name):
        try:
            # 모듈의 파일 경로 지정
            module_path = os.path.join(ROOT_DIR, "SHELL", "SCRIPTS", f"{scenario_name}.py")

            # 모듈 스펙을 생성하고 모듈을 로드
            spec = spec_from_file_location(scenario_name, module_path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

            # 모듈에서 클래스 가져오기
            return getattr(module, scenario_name)(self.shell)

        except FileNotFoundError:
            self.print_fail()

    @staticmethod
    def print_header(scenario_name: str):
        print(f"{scenario_name}   ---   Run...", end='', flush=True)

    @staticmethod
    def print_fail():
        print("Fail!")
        exit(1)

    @staticmethod
    def print_pass():
        print("Pass")
