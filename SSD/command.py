from abc import ABC, abstractmethod

from LOGGER.logger import Logger
from SSD.ssd import SSDDriver


class Command(ABC):
    def __init__(self, driver: SSDDriver):
        self.ssd_driver = driver
        self.logger = Logger()

    @abstractmethod
    def execute(self, address: int, value: str):
        pass


class WriteCommand(Command):
    def execute(self, address: int, value: str):
        try:
            self.ssd_driver.write(address, value)
            self.logger.log(f'{self.__class__.__name__}.{self.execute.__name__} success!')
        except Exception:
            self.logger.log(f'{self.__class__.__name__}.{self.execute.__name__} fail! Error 내용 : {str(Exception)}')


class EraseCommand(Command):
    def execute(self, address: int, value: str = None):
        try:
            self.ssd_driver.erase(address)
            self.logger.log(f'{self.__class__.__name__} 클래스 {self.execute.__name__} success!')
        except Exception:
            self.logger.log(f'{self.__class__.__name__} 클래스 {self.execute.__name__} fail! Error 내용 : {str(Exception)}')
