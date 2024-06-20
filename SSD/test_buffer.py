import os
from unittest import TestCase

from SSD.buffer import SSDBuffer
from SSD.ssd import SSDDriverEnter

BUFFER_PATH = "../buffer.txt"

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

    def tearDown(self):
        self.clear_test_files()

    def test_update(self):
        self.buffer.update("W", 1, "0x00000002")
        self.buffer.update("W", 0, "0x00000002")
        self.buffer.update("W", 6, "0x00000002")

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
        with open(BUFFER_PATH, "w") as f:
            f.write("1\nW 1 0x00000002")

        self.assertEqual(len(self.buffer.load_db()), 1)
        # self.assertEqual(self.buffer.commands[0], WriteCommand())

    def test_find(self):
        pass

    def test_flush(self):
        self.buffer.update("W", 1, "0x00000005")
        self.buffer.update("W", 0, "0x00000005")
        self.buffer.update("W", 6, "0x00000005")
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

    @staticmethod
    def clear_test_files():
        if os.path.exists(NAND_PATH):
            os.remove(NAND_PATH)
        if os.path.exists(RESULT_PATH):
            os.remove(RESULT_PATH)
        if os.path.exists(BUFFER_PATH):
            os.remove(BUFFER_PATH)
        pass
