import os
import sys
from abc import ABC, abstractmethod
from typing import Union

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

sys.path.append(ROOT_DIR)
from LOGGER.logger import Logger
from SSD.ssd import SSDDriver


class Command(ABC):
    def __init__(self, driver: SSDDriver, address: int, value: Union[str, int]):
        self.ssd_driver = driver
        self.logger = Logger()
        self.address = address
        self.value = value

    @abstractmethod
    def execute(self):
        pass


class WriteCommand(Command):
    def execute(self):
        try:
            self.ssd_driver.write(self.address, self.value)
            self.logger.log(f'success!')
        except Exception:
            self.logger.log(f'fail! Error 내용 : {str(Exception)}')


class EraseCommand(Command):
    def execute(self):
        try:
            size = int(self.value)
            while size > 10:
                self.ssd_driver.erase(self.address, 10)
                size -= 10
            self.ssd_driver.erase(self.address, size)
            self.logger.log(f'success!')
        except Exception:
            self.logger.log(f'fail! Error 내용 : {str(Exception)}')
