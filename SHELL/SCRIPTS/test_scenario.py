from SHELL.TestShellApplication import *


class TestScenario(ABC):
    @abstractmethod
    def run_test(self, shell: TestShellApplication):
        pass