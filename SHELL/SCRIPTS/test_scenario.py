import os
import sys
from abc import ABC, abstractmethod

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)
from SHELL.TestShellApplication import TestShellApplication


class TestScenario(ABC):
    def __init__(self, shell: TestShellApplication):
        self.shell = shell

    @abstractmethod
    def run_test(self):
        pass
