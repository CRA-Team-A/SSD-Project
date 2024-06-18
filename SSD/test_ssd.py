import os
from unittest import TestCase

from SSD.ssd import SSDDriverEnter

TEST_RESULT_FILE_PATH = 'result_tmp.txt'

TEST_NAND_FILE_PATH = 'nand_tmp.txt'

INITIAL_VALUE = "0x00000000"


class TestSSDDriverEnter(TestCase):
    def setUp(self):
        initial_data = ""
        for i in range(20):
            initial_data += "0" + "\n"
        self.nand_path = os.path.dirname(os.getcwd()) + '\\' + TEST_NAND_FILE_PATH
        self.result_path = os.path.dirname(os.getcwd()) + '\\' + TEST_RESULT_FILE_PATH
        with open(self.nand_path, 'w') as nand_file:
            nand_file.write(initial_data)
        self.ssd_driver = SSDDriverEnter(self.nand_path, self.result_path)

    def tearDown(self):
        self.clear_test_files()

    def clear_test_files(self):
        if os.path.exists(self.nand_path):
            os.remove(self.nand_path)
        if os.path.exists(self.result_path):
            os.remove(self.result_path)

    def test_read_initialized_file(self):
        self.ssd_driver.read(0)
        result = ''
        with open(self.result_path, 'r') as result_file:
            result += result_file.read()
        self.assertEqual(INITIAL_VALUE, result)

