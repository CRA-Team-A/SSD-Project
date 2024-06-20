from abc import ABC, abstractmethod

from SSD.ssd import SSDDriver


class Command(ABC):
    def __init__(self, driver: SSDDriver):
        self.ssd_driver = driver

    @abstractmethod
    def execute(self, address: int, value: str):
        pass


class WriteCommand(Command):
    def execute(self, address: int, value: str):
        self.ssd_driver.write(address, value)
