import os
from unittest import TestCase

from SSD.buffer import SSDBuffer
from SSD.ssd import SSDDriverEnter

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
NAND_PATH = os.path.join(ROOT_DIR, 'nand.txt')
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')


class TestSSDBuffer(TestCase):
    def setUp(self):
        self.buffer = SSDBuffer(SSDDriverEnter(NAND_PATH, RESULT_PATH))

    def test_update(self):
        self.buffer.update("W", 1, 2)
        self.buffer.update("W", 0, 2)
        self.buffer.update("W", 6, 2)

        self.buffer.read(1)
        result = self.get_value(RESULT_PATH)
        self.assertEqual(result, "0x00000002")
        self.buffer.read(38)
        result = self.get_value(RESULT_PATH)
        self.assertEqual(result, "0x00000000")

    def test_invalid_command_type(self):
        self.buffer.update("D", 1, 2)

    def test_save_db(self):
        pass

    def test_load_db(self):
        with open("../buffer.txt", "w") as f:
            f.write("1\nW 1 2")

        self.assertEqual(len(self.buffer.load_db()), 1)
        # self.assertEqual(self.buffer.commands[0], WriteCommand())

    def test_find(self):
        pass

    def test_flush(self):
        self.buffer.update("W", 1, 5)
        self.buffer.update("W", 0, 5)
        self.buffer.update("W", 6, 5)
        self.assertNotEqual(self.read(1), "0x00000005")
        self.buffer.flush()
        self.assertEqual(self.read(1), "0x00000005")

    def read(self, address):
        self.buffer.driver.read(1)
        return self.get_value(RESULT_PATH)

    @staticmethod
    def get_value(path: str) -> str:
        with open(path, 'r') as file:
            data = file.readline().strip()
        return data
