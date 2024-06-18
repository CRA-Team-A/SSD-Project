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
        self.setup_nand(TEST_NAND_PATH)

        for i in range(100):
            with self.subTest('subtest_' + str(i)):
                self.ssd_comma.read(i)
                data = self.get_result_value()
                self.assertEquals(self.convert_to_hex(i), data)
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    def test_write_SSDDriverComma(self):
        address = 50
        value = '0xFFFFFFFF'

        self.ssd_comma.write(address, value)
        self.ssd_comma.read(address)
        data = self.get_result_value()

        self.assertEquals(value.lower(), data.lower())
        self.clear_files(TEST_NAND_PATH, TEST_RESULT_PATH)

    @staticmethod
    def clear_files(TEST_NAND_PATH, TEST_RESULT_PATH):
        if os.path.exists(TEST_NAND_PATH):
            os.remove(TEST_NAND_PATH)
        if os.path.exists(TEST_RESULT_PATH):
            os.remove(TEST_RESULT_PATH)

    @staticmethod
    def setup_nand(TEST_NAND_PATH):
        with open(TEST_NAND_PATH, 'w') as file:
            file.write(','.join([str(n) for n in range(100)]))

    @staticmethod
    def get_result_value():
        with open(TEST_RESULT_PATH, 'r') as result:
            data = result.readline().strip()
        return data

    @staticmethod
    def convert_to_hex(hexadecimal: int):
        return '0x{:08x}'.format(hexadecimal)
