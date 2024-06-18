from unittest import TestCase
from ssd import SSDDriverComma
import os

TEST_NAND_PATH = 'nand_temp.txt'
TEST_RESULT_PATH = 'result_temp.txt'


class TestSSDDriver(TestCase):
    def setUp(self):
        self.ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_init_SSDDriverComma(self):
        self.assertTrue(os.path.isfile(TEST_NAND_PATH))
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_read_SSDDriverComma(self):
        self.setup_nand_1_100(TEST_NAND_PATH)
        ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

        for i in range(100):
            with self.subTest('subtest_' + str(i)):
                ssd_comma.read(i)
                data = self.get_result_value(TEST_RESULT_PATH)
                self.assertEquals(self.convert_to_hex(i), data)
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_read_empty_SSDDriverComma(self):
        ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

        ssd_comma.read(0)
        data = self.get_result_value(TEST_RESULT_PATH)
        self.assertEquals(self.convert_to_hex(0), data)
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_write_SSDDriverComma(self):
        address = 50
        value = '0xFFFFFFFF'
        ssd_comma = SSDDriverComma(TEST_NAND_PATH, TEST_RESULT_PATH)

        ssd_comma.write(address, value)
        ssd_comma.read(address)
        data = self.get_result_value(TEST_RESULT_PATH)

        self.assertEquals(value, data)
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    @staticmethod
    def clear_files(nand_path:str, result_path:str):
        if os.path.exists(nand_path):
            os.remove(nand_path)
        if os.path.exists(result_path):
            os.remove(result_path)

    @staticmethod
    def setup_nand_1_100(nand_path:str):
        with open(nand_path, 'w') as file:
            file.write(','.join([str(n) for n in range(100)]))

    @staticmethod
    def get_result_value(result_path:str) -> str:
        with open(result_path, 'r') as result:
            data = result.readline().strip()
        return data

    @staticmethod
    def convert_to_hex(decimal: int) -> str:
        return '0x'+'{:08x}'.format(decimal).upper()
