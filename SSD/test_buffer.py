import os
from unittest import TestCase

from SSD.buffer import SSDBuffer
from SSD.ssd import SSDDriverCommon

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
BUFFER_PATH = os.path.join(ROOT_DIR, "buffer.txt")
NAND_PATH = os.path.join(ROOT_DIR, 'nand.txt')
RESULT_PATH = os.path.join(ROOT_DIR, 'result.txt')


class TestSSDBuffer(TestCase):
    def setUp(self):
        self.buffer = SSDBuffer(SSDDriverCommon('\n', NAND_PATH, RESULT_PATH))

    def tearDown(self):
        self.clear_test_files()

    def test_write_after_read(self):
        self.buffer.update("W", 1, "0x00000002")

        self.buffer.read(1)
        result = self.get_value(RESULT_PATH)
        self.assertEqual(result, "0x00000002")

    def test_read_first(self):
        self.buffer.read(1)
        result = self.get_value(RESULT_PATH)
        self.assertEqual(result, "0x00000000")

    def test_write_after_erase(self):
        self.buffer.update("W", 1, "0x00000002")
        self.buffer.update("E", 1, "2")
        self.buffer.read(1)
        result = self.get_value(RESULT_PATH)
        self.assertEqual(result, "0x00000000")

    def test_invalid_command_type(self):
        self.buffer.update("D", 1, 2)

    def test_save_db(self):
        self.buffer.update("W", 1, "0x00000002")
        self.buffer.update("W", 2, "0x00000003")
        with open(BUFFER_PATH, "r") as f:
            result = f.read()
        self.assertEqual(result, '2' + '\n' + 'W 1 0x00000002' + '\n' + 'W 2 0x00000003' + '\n')

    def test_load_db(self):
        with open(BUFFER_PATH, "w") as f:
            f.write("1\nW 1 0x00000002")

        self.assertEqual(len(self.buffer.load_db()), 1)

    def test_optimize_ignore_write_1(self):
        self.buffer.update("W", 20, "0xABCDABCD")
        self.buffer.update("W", 21, "0x12341234")
        self.buffer.update("W", 20, "0xEEEEFFFF")
        self.assertEqual(len(self.buffer.commands), 2)
        self.assertEqual(self.buffer_read(20), "0xEEEEFFFF")

    def test_optimize_ignore_write_2(self):
        self.buffer.update("W", 20, "0xABCDABCD")
        self.buffer.update("W", 21, "0x12341234")
        self.buffer.update("E", 18, "5")
        self.assertEqual(len(self.buffer.commands), 1)
        self.assertEqual(self.buffer_read(20), "0x00000000")
        self.assertEqual(self.buffer_read(21), "0x00000000")

    def test_optimize_merge_erase_3(self):
        self.buffer.update("W", 20, "0xABCDABCD")
        self.buffer.update("E", 10, "2")
        self.buffer.update("E", 12, "3")

        self.assertEqual(len(self.buffer.commands), 2)
        self.assertEqual(self.buffer_read(20), "0xABCDABCD")

    def test_optimize_narrow_range_of_erase_4_1(self):
        self.buffer.update("E", 10, "4")
        self.buffer.update("E", 40, "5")
        self.buffer.update("W", 12, "0xABCD1234")
        self.buffer.update("W", 13, "0x4BCD5351")

        self.assertEqual(len(self.buffer.commands), 4)
        self.assertEqual(self.buffer_read(12), "0xABCD1234")
        self.assertEqual(self.buffer_read(13), "0x4BCD5351")

    def test_optimize_ignore_erase_4_2(self):
        self.buffer.update("E", 50, "1")
        self.buffer.update("E", 40, "5")
        self.buffer.update("W", 50, "0xABCD1234")

        self.assertEqual(len(self.buffer.commands), 2)
        self.assertEqual(self.buffer_read(50), "0xABCD1234")

    def test_optimize_merge_discrete_erase_5(self):
        self.buffer.update("E", 10, "2")
        self.buffer.update("W", 10, "0xABCDABCD")
        self.buffer.update("E", 12, "3")
        self.assertEqual(len(self.buffer.commands), 2)
        self.assertEqual(self.buffer_read(10), "0xABCDABCD")

    def test_optimize_merge_discrete_erase_6(self):
        self.buffer.update("E", 0, "10")
        self.buffer.update("W", 10, "0xABCDABCD")
        self.buffer.update("W", 11, "0xABCDABC0")
        self.buffer.update("W", 12, "0xABCDABC1")
        self.buffer.update("W", 13, "0xABCDABC2")
        self.buffer.update("W", 14, "0xABCDABC3")
        self.buffer.update("W", 15, "0xABCDABC4")
        self.buffer.update("W", 16, "0xABCDABC5")
        self.buffer.update("E", 13, "3")
        self.buffer.update("E", 16, "7")
        self.assertEqual(len(self.buffer.commands), 5)
        self.assertEqual(self.buffer_read(10), "0xABCDABCD")
        self.assertEqual(self.buffer_read(13), "0x00000000")
        self.assertEqual(self.buffer_read(16), "0x00000000")

    def test_optimize_merge_discrete_erase_7(self):
        self.buffer.update("E", 0, "7")
        self.buffer.update("E", 7, "6")
        self.buffer.update("W", 7, "0xABCDABCD")
        self.buffer.update("E", 14, "6")
        self.buffer.update("W", 13, "0xABCDABC3")
        self.buffer.update("W", 14, "0xABCDABC4")
        self.assertEqual(len(self.buffer.commands), 5)
        self.assertEqual(self.buffer_read(7), "0xABCDABCD")
        self.assertEqual(self.buffer_read(13), "0xABCDABC3")
        self.assertEqual(self.buffer_read(14), "0xABCDABC4")
        self.assertEqual(self.buffer_read(11), "0x00000000")

    def test_flush(self):
        self.buffer.update("W", 1, "0x00000005")
        self.buffer.update("W", 0, "0x00000005")
        self.buffer.update("W", 6, "0x00000005")
        self.assertNotEqual(self.driver_read(1), "0x00000005")
        self.buffer.flush()
        self.assertEqual(self.driver_read(1), "0x00000005")

    def driver_read(self, address):
        self.buffer.driver.read(1)
        return self.get_value(RESULT_PATH)

    def buffer_read(self, address):
        self.buffer.read(address)
        with open(RESULT_PATH, "r") as f:
            result_value = f.read()
        return result_value

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
